from rest_framework import serializers

from objects.models import Object, TYPE


class CreateObjectSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE)
    object = serializers.FileField()

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
