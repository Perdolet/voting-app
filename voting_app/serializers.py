from rest_framework import serializers
from .models import SurveyModel
from .validators import answers_unique_validator


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyModel
        fields = (
            'id',
            'survey_question',
            'answers',
            'finishing_date',
            'is_finished',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'survey_question': {'read_only': True},
            'answers': {'read_only': True},
            'finishing_date': {'required': False},
            'is_finished': {'required': False},
        }


class SurveyCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ('survey_question', 'answers', 'finishing_date', 'url')
        extra_kwargs = {
            'url': {'view_name': 'surveys-detail', 'required': False},
            'id': {'required': False}
        }


class SurveyCreateRequestSerializer(serializers.Serializer):
    survey_question = serializers.CharField(max_length=50)
    answers = serializers.ListSerializer(
        child=serializers.CharField(max_length=80),
        validators=(answers_unique_validator,),
        allow_empty=False
    )
    finishing_date = serializers.DateTimeField()


class SurveyListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ('id', 'survey_question', 'url')
        extra_kwargs = {
            'url': {'view_name': 'surveys-detail'},
        }


class SurveyVotingSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices_from_db', [])
        self.fields['voted_answer'] = serializers.ChoiceField(choices=choices)
        super().__init__(*args, **kwargs)
