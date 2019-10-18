from rest_framework import serializers

from objects.models import Object, TYPE, STATE
from objects.utils import unique_filename


class CreateObjectSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE)
    object = serializers.FileField()

    def create(self, validated_data):
        validated_data['name'] = unique_filename(validated_data['object'].name)
        validated_data['link_alias'] = validated_data['name']
        return Object.objects.create(**validated_data)

    class Meta:
        model = Object
        fields = (
            'id', 'link_alias', 'name', 'object',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'link_alias', 'name',
            'state', 'created_at',
        )


class AliasObjectSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Unalias object when alias exists
        unaliasing_object = Object.objects.filter(
            link_alias=validated_data['link_alias'],
            state=STATE[1][0]).first()
        if unaliasing_object is not None:
            unaliasing_object.state = STATE[2][0]
            unaliasing_object.save()
        instance.link_alias = validated_data['link_alias']
        instance.state = STATE[1][0]
        instance.save()
        return instance

    class Meta:
        model = Object
        fields = (
            'id', 'link_alias', 'name', 'object',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'type', 'name', 'object',
            'state', 'created_at',
        )
