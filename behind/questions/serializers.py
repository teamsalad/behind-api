from django.db import transaction
from rest_framework import serializers

from companies.models import Job, Company
from companies.serializers import JobSerializer, CompanySerializer
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
        device = question.questioner.active_device()
        if device is not None:
            device.send_message(
                body=f'{question.questioner.nickename}님, 재직자님의 답변이 도착했어요! 지금 바로 확인해보세요.',
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
        validated_data['job_id'] = validated_data['job_id'].id
        validated_data['company_id'] = validated_data['company_id'].id
        validated_data['questioner'] = self.context['request'].user
        return Question.objects.create(**validated_data)

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'job_id',
                  'company_id', 'company', 'answers',
                  'created_at',)
        read_only_fields = ('id', 'job', 'company', 'answers', 'created_at',)
