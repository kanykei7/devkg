from rest_framework import serializers
from mainapp.models import User, Company, Vacancy, VacancyDescription, Event, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'company', 'title', 'create_at', 'description', 'preview', 'video', 'is_active',
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'company', 'title', 'description', 'start_at', 'end_at', 'location', 'image', 'price', 'registration',
            'is_active',
        )


class VacancyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyDescription
        fields = (
            'title', 'description', 'vacancy',
        )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id', 'name', 'logo', 'vacancy_amount',
            'event_amount', 'video_amount',
        )
        read_only_fields = ('user',)


class CompanyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id', 'description', 'logo', 'name', 'web_site', 'email', 'phone', 'location',
        )


class UserSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'companies',
        )


class VacancySerializer(serializers.ModelSerializer):
    company_logo = serializers.ReadOnlyField(source='company.logo.path')
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Vacancy
        fields = (
            'id', 'company', 'type_work', 'type', 'salary', 'currency', 'company_logo', 'company_name', 'is_active',
        )
        read_only_fields = ('company',)


class VacancyRetrieveSerializer(serializers.ModelSerializer):
    description = VacancyDescriptionSerializer(read_only=True, many=True)
    company_logo = serializers.ReadOnlyField(source='company.logo.path')
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Vacancy
        fields = (
            'company', 'type_work', 'type', 'salary', 'currency', 'description', 'company_logo', 'company_name',
            'is_active',
        )
