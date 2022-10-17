from rest_framework.routers import DefaultRouter as DR

from mainapp.views import (UserViewSet, CompanyViewSet, VacancyViewSet, VacancyDescriptionViewSet, EventViewSet,
                           VideoViewSet, )

router = DR()

router.register('users', UserViewSet, basename='users')
router.register('companies', CompanyViewSet, basename='companies')
router.register('vacancies', VacancyViewSet, basename='vacancies')
router.register('vacancy_descs', VacancyDescriptionViewSet, basename='vacancy_descs')
router.register('events', EventViewSet, basename='events')
router.register('videos', VideoViewSet, basename='videos')


urlpatterns = []

urlpatterns += router.urls
