from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .utils import get_prepared_answers, create_survey, perform_survey_vote
from .models import SurveyModel, UserSurveyJunctionModel
from .permissions import HasNotVoted, IsOwner
from .serializers import (
    SurveyRetrieveSerializer, SurveyCreateSerializer,
    SurveyListSerializer, SurveyCreateRequestSerializer,
    SurveyVotingSerializer,
)
from . import constants


class SurveyApiViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = SurveyModel.objects.all()
    serializer_classes = {constants.LIST: SurveyListSerializer,
                          constants.RETRIEVE: SurveyRetrieveSerializer,
                          constants.CREATE: SurveyCreateSerializer,
                          constants.EDIT_SURVEY: SurveyRetrieveSerializer,
                          constants.VOTE: SurveyVotingSerializer,
                          constants.DESTROY: SurveyRetrieveSerializer}
    permission_classes = [IsAuthenticatedOrReadOnly, HasNotVoted, IsOwner]

    def get_serializer_class(self):
        view_action = self.action
        self.serializer_class = self.serializer_classes.get(view_action)
        return self.serializer_class

    @swagger_auto_schema(
        request_body=SurveyCreateRequestSerializer,
        responses={status.HTTP_201_CREATED: SurveyCreateSerializer}
    )
    def create(self, request, *args, **kwargs):
        request_serializer = SurveyCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        answers = get_prepared_answers(
            request_serializer.validated_data['answers']
        )
        request.data['answers'] = answers
        response_serializer = self.get_serializer(data=request.data)
        response_serializer.is_valid(raise_exception=True)
        create_survey(
            view=self,
            user=request.user,
            model=UserSurveyJunctionModel,
            serializer=response_serializer
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['patch'], detail=True, url_path='edit-survey')
    def edit_survey(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def vote(self, request, *args, **kwargs):
        survey_obj = self.get_object()
        if not survey_obj.can_vote():
            raise PermissionDenied('Survey already finished!')
        answers = survey_obj.answers
        request_serializer = self.get_serializer(
            data=request.data,
            choices_from_db=answers.keys(),
        )
        request_serializer.is_valid(raise_exception=True)
        voted_answer = request_serializer.validated_data['voted_answer']
        answers[voted_answer] += 1
        survey_obj.answers = answers
        perform_survey_vote(
            survey_obj=survey_obj,
            junction_model=UserSurveyJunctionModel,
            user=request.user,
        )
        return Response({}, status=status.HTTP_204_NO_CONTENT, )
