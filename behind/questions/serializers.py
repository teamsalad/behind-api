from rest_framework import serializers

from companies.models import Job, Company
from companies.serializers import JobSerializer, CompanySerializer
from users.serializers import UserDetailsSerializer
from questions.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    answerer = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'content', 'answerer', 'created_at',)
        read_only_fields = ('id', 'answerer', 'created_at',)


class QuestionSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'company',
                  'answers', 'created_at',)
        read_only_fields = ('id', 'job', 'company',
                            'answers', 'created_at',)


class CreateAnswerSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        required=True,
        allow_blank=False
    )
    question_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Question.objects.all(),
        write_only=True
    )
    answerer = UserDetailsSerializer(read_only=True)

    def create(self, validated_data):
        validated_data['answerer'] = self.context['current_user']
        validated_data['question_id'] = validated_data['question_id'].id
        return Answer.objects.create(**validated_data)

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
    answers = AnswerSerializer(read_only=True, many=True)

    def create(self, validated_data):
        validated_data['job_id'] = validated_data['job_id'].id
        validated_data['company_id'] = validated_data['company_id'].id
        validated_data['questioner'] = self.context['current_user']
        return Question.objects.create(**validated_data)

    class Meta:
        model = Question
        fields = ('id', 'content', 'job', 'job_id',
                  'company_id', 'company', 'answers',
                  'created_at',)
        read_only_fields = ('id', 'job', 'company', 'answers', 'created_at',)
