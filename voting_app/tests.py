from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import SurveyModel, UserSurveyJunctionModel

User = get_user_model()


class SurveyTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user',
            password='123456qwerty',
            email='test_email@test.com'
        )
        self.token = str(Token.objects.create(user=self.user))
        self.data = {
            'survey_question': 'Test survey',
            'answers': {'1': 0, '2': 0},
            'finishing_date': '3021-11-05T18:25:43.511Z'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.valid_survey = SurveyModel.objects.create(**self.data)
        UserSurveyJunctionModel.objects.create(survey=self.valid_survey, user=self.user, is_owner=True)
        self.valid_survey_id = self.valid_survey.pk

    def test_survey_creation_success(self):
        url = '/api/surveys/'
        survey_count_before_request = len(SurveyModel.objects.all())
        data = {
            'survey_question': 'Test survey',
            'answers': ['1', '2'],
            'finishing_date': '3021-11-05T18:25:43.511Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        survey_count_after_request = len(SurveyModel.objects.all())
        self.assertEqual(survey_count_before_request + 1, survey_count_after_request)

    def test_survey_create_without_token(self):
        url = '/api/surveys/'
        self.client.credentials()
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_create_wrong_data(self):
        url = '/api/surveys/'
        data = {
            'survey_question': 'Test survey',
            'answers': ['1', '1'],
            'finishing_date': '3021-11-05T18:25:43.511Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_surveys_list(self):
        url = '/api/surveys/'
        for _ in range(5):
            self.client.post(url, self.data, format='json')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_count = len(SurveyModel.objects.all())
        self.assertEqual(len(response.data), current_count)

    def test_survey_detail(self):
        url = f'/api/surveys/{self.valid_survey_id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.valid_survey_id)
        valid_response_data = {
            'survey_question': 'Test survey',
            'answers': {'1': 0, '2': 0},
            'finishing_date': '3021-11-05T18:25:43.511000Z',
        }
        self.assertEqual(
            valid_response_data['survey_question'],
            response.data.get('survey_question')
        )
        self.assertEqual(
            valid_response_data['answers'],
            response.data.get('answers')
        )
        self.assertEqual(
            valid_response_data['finishing_date'],
            response.data.get('finishing_date')
        )

    def test_survey_voting(self):
        url = f'/api/surveys/{self.valid_survey_id}/vote/'
        voted_answer = {'voted_answer': '1'}
        self.assertEqual(self.valid_survey.answers.get('1'), 0)
        response = self.client.patch(
            url,
            data=voted_answer,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.valid_survey.refresh_from_db()
        self.assertEqual(self.valid_survey.answers.get('1'), 1)

    def test_survey_update(self):
        url = f'/api/surveys/{self.valid_survey_id}/edit-survey/'
        new_data = {'is_finished': True}
        response = self.client.patch(
            url,
            new_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.valid_survey_id)
        self.assertEqual(response.data.get('is_finished'), True)

    def test_survey_update_not_owner(self):
        user = User.objects.create_user(
            username='test_user2',
            password='123456qwerty',
            email='test_email2@test.com'
        )
        token = str(Token.objects.create(user=user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = f'/api/surveys/{self.valid_survey_id}/edit-survey/'
        new_data = {'is_finished': True}
        response = self.client.patch(
            url,
            new_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_vote_finished_survey(self):
        finished_survey_id = SurveyModel.objects.create(is_finished=True, **self.data).pk
        url = f'/api/surveys/{finished_survey_id}/vote/'
        voted_answer = {'voted_answer': '1'}
        response = self.client.patch(
            url,
            data=voted_answer,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vote_expired_survey(self):
        data = {
            'survey_question': 'Is Lenin Rip?',
            'answers': {'DA': 0, 'GYLAG': 0},
            'finishing_date': '1943-11-05T18:25:43.511Z'
        }
        expired_survey_id = SurveyModel.objects.create(**data).pk
        url = f'/api/surveys/{expired_survey_id}/vote/'
        voted_answer = {'voted_answer': '1'}
        response = self.client.patch(
            url,
            data=voted_answer,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_survey_delete(self):
        survey = SurveyModel.objects.create(**self.data)
        UserSurveyJunctionModel.objects.create(survey=survey, user=self.user, is_owner=True)
        url = f'/api/surveys/{survey.pk}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        test_response = self.client.get(url, format='json')
        self.assertEqual(test_response.status_code, status.HTTP_404_NOT_FOUND)
