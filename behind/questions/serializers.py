from django.db import transaction
from fcm_django.models import FCMDevice
from rest_framework import serializers

from companies.models import Job, Company, UserJobHistory
from companies.serializers import JobSerializer, CompanySerializer
from users.models import User
from users.serializers import UserDetailsSerializer
from questions.models import Question, Answer


class AnswerListQuestionSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'company', 'questioner', 'created_at',)
        read_only_fields = ('id', 'job', 'company', 'questioner', 'created_at',)


class AnswerListSerializer(serializers.ModelSerializer):
    answerer = UserDetailsSerializer(read_only=True)
    question = AnswerListQuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'content', 'answerer', 'question', 'chat_room', 'created_at',)
        read_only_fields = ('id', 'answerer', 'question', 'chat_room', 'created_at',)


class QuestionListAnswerSerializer(serializers.ModelSerializer):
    answerer = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'content', 'answerer', 'chat_room', 'created_at',)
        read_only_fields = ('id', 'answerer', 'chat_room', 'created_at',)


class QuestionListSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    answers = QuestionListAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'company', 'questioner',
                  'answers', 'created_at',)
        read_only_fields = ('id', 'job', 'company', 'questioner',
                            'answers', 'created_at',)


class CreateAnswerSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=20
    )
    question_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Question.objects.all(),
        write_only=True
    )
    answerer = UserDetailsSerializer(read_only=True)

    @transaction.atomic
    def create(self, validated_data):
        question = validated_data.pop('question_id')
        validated_data['answerer'] = self.context['request'].user
        validated_data['question_id'] = question.id
        new_answer = Answer.objects.create(**validated_data)
        questioner = question.questioner
        if questioner.can_send_push_notification('asked'):
            questioner.active_device().send_message(
                body=f'{questioner.username}님, 재직자님의 답변이 도착했어요! 지금 바로 확인해보세요.',
                sound='default',
                data={'question_id': question.id}
            )
        return new_answer

    class Meta:
        model = Answer
        fields = ('id', 'content', 'answerer', 'question_id', 'created_at',)
        read_only_fields = ('id', 'answerer', 'created_at',)


class CreateQuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        required=True,
        allow_blank=False
    )
    job_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Job.objects.all(),
        write_only=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Company.objects.all(),
        write_only=True
    )
    job = JobSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    answers = QuestionListAnswerSerializer(read_only=True, many=True)

    @transaction.atomic
    def create(self, validated_data):
        # user_id__in=user_ids
        company = validated_data['company_id']
        job = validated_data['job_id']
        validated_data['job_id'] = company.id
        validated_data['company_id'] = job.id
        validated_data['questioner'] = self.context['request'].user
        new_question = Question.objects.create(**validated_data)
        # Send push notifications to employees who can answer
        employee_ids = UserJobHistory.objects \
            .filter(company=company, job=job) \
            .values_list('user_id', flat=True).distinct()
        notifiable_employee_ids = User.objects \
            .select_related('push_notification_setting') \
            .filter(id__in=employee_ids, push_notification_setting__asked=True) \
            .values_list('id', flat=True)
        devices = FCMDevice.objects.filter(
            user_id__in=notifiable_employee_ids,
            active=True
        ).all()
        devices.send_message(
            body=f'구직자님이 {company.name} 관련 상담을 요청하셨어요! 지금 바로 상담하고 따뜻한 커피 한잔 할까요?',
            sound='default',
            data={'question_id': new_question.id}
        )
        return new_question

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'job_id',
                  'company_id', 'company', 'answers',
                  'created_at',)
        read_only_fields = ('id', 'job', 'company', 'answers', 'created_at',)
