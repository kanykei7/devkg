from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions
from mainapp.serializers import User, UserSerializer, Company, CompanySerializer, Vacancy, VacancySerializer, \
    VacancyDescription, VacancyDescriptionSerializer, Event, EventSerializer, Video, VideoSerializer, \
    CompanyRetrieveSerializer, VacancyRetrieveSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from mainapp.paginations import StandardResultsSetPagination


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', ]
    pagination_class = StandardResultsSetPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return CompanyRetrieveSerializer
        elif self.action == 'create_vacancies':
            return VacancySerializer
        else:
            return CompanySerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['post', ], detail=True, serializer_class=VacancySerializer)
    def create_vacancies(self, request, *args, **kwargs):
        company = self.get_object()
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            vacancy = Vacancy.objects.create(
                company=company,
                type_work=data.get('type_work'),
                type=data.get('type'),
                salary=data.get('salary'),
                currency=data.get('currency')
            )

            return Response(VacancySerializer(instance=vacancy).data)


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['type_work', ]
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return VacancyRetrieveSerializer
        elif self.action == 'create_vacancies_desc':
            return VacancyDescriptionSerializer
        else:
            return VacancySerializer

    @action(methods=['post', ], detail=True, serializer_class=VacancyDescriptionSerializer)
    def create_vacancies_desc(self, request, *args, **kwargs):
        vacancy = self.get_object()
        serializer = VacancyDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            vacancy_desc = VacancyDescription.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                vacancy=vacancy
            )
            return Response(VacancyDescriptionSerializer(instance=vacancy_desc).data)


class VacancyDescriptionViewSet(ReadOnlyModelViewSet):
    queryset = VacancyDescription.objects.all()
    serializer_class = VacancyDescriptionSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', ]
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', ], detail=False, permission_classes=(permissions.IsAuthenticated,))
    def profile(self, request, *args, **kwargs):
        user = request.user
        data = self.serializer_class(instance=user, many=False)
        return Response(data.data)
