from rest_framework.permissions import BasePermission
from .models import UserSurveyJunctionModel
from . import constants


class HasNotVoted(BasePermission):
    message = 'You already voted!'

    def has_permission(self, request, view):
        if view.action != constants.VOTE:
            return True
        relation = UserSurveyJunctionModel.objects.filter(
            user=request.user,
            survey=view.kwargs.get(view.lookup_field)).first()
        return not relation or relation.is_voted is False


class IsOwner(BasePermission):
    message = 'You are not owner!'

    def has_permission(self, request, view):
        if view.action not in [constants.EDIT_SURVEY, constants.DESTROY]:
            return True
        return UserSurveyJunctionModel.objects.filter(
            user=request.user,
            survey=view.kwargs.get(view.lookup_field),
            is_owner=True).exists()
