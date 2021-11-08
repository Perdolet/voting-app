from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class SurveyModel(models.Model):
    survey_question = models.CharField(max_length=50)
    answers = models.JSONField()
    finishing_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.survey_question}'

    def can_vote(self):
        return not self.is_finished and self.finishing_date > timezone.now()

    def finish_survey(self):
        self.is_finished = True
        self.save(update_fields=['is_finished'])


class UserSurveyJunctionModel(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='users',
                             related_query_name='user')
    survey = models.ForeignKey(SurveyModel,
                               on_delete=models.CASCADE,
                               related_name='surveys',
                               related_query_name='survey')
    is_owner = models.BooleanField(default=False)
    is_voted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'survey')

    def __str__(self):
        return f'User: {self.user}, Survey: {self.survey}'
