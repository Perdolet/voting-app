from typing import Dict
from collections import defaultdict
from django.db import transaction


def get_prepared_answers(answers: list) -> Dict[str, int]:
    prepared_answers = defaultdict(int)
    for answer in answers:
        prepared_answers[answer]    # pylint: disable=pointless-statement
    return prepared_answers


@transaction.atomic
def create_survey(view, serializer, user, model):
    view.perform_create(serializer)
    model.objects.create(user=user,
                         survey=serializer.instance,
                         is_owner=True)


@transaction.atomic
def perform_survey_vote(survey_obj, junction_model, user):
    survey_obj.save(update_fields=['answers'])
    junction_model.objects.update_or_create(
        user=user,
        survey=survey_obj,
        defaults={'is_voted': True}
    )
