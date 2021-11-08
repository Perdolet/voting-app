from rest_framework import routers
from .views import SurveyApiViewSet

router = routers.SimpleRouter()
router.register(r'surveys', SurveyApiViewSet, 'surveys')


urlpatterns = router.urls
