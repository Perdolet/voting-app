from django.contrib import admin
from django.forms import BaseInlineFormSet
from .models import SurveyModel, UserSurveyJunctionModel


class OwnersFormset(BaseInlineFormSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_owner=True)


class VotedUsersFormset(BaseInlineFormSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_voted=True)


class UserSurveyOwnerInline(admin.TabularInline):
    model = UserSurveyJunctionModel
    formset = OwnersFormset
    extra = 0
    verbose_name_plural = 'Owners'


class UserSurveyVotedInline(admin.TabularInline):
    model = UserSurveyJunctionModel
    formset = VotedUsersFormset
    extra = 0
    verbose_name_plural = 'Voted Users'


class SurveyAdmin(admin.ModelAdmin):
    fields = ('survey_question', 'answers', 'finishing_date', 'is_finished',)
    inlines = [
        UserSurveyOwnerInline,
        UserSurveyVotedInline,
    ]


admin.site.register(SurveyModel, SurveyAdmin)
admin.site.register(UserSurveyJunctionModel)
