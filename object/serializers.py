from rest_framework import serializers

from .models import Object


class ObjectSerializer(serializers.ModelSerializer):
    #Serializers for object.

    class Meta:
        model = Object
        fields = ['id', 'title',]
        read_only_fields = ['id']

class ObjectDetailSerializer(ObjectSerializer):
    #Serializer for object detail view.

    class Meta(ObjectSerializer.Meta):
        fields = ObjectSerializer.Meta.fields + ['description']

class ObjectImageSerializer(serializers.ModelSerializer):
    #Serializer for uploading images to object.

    class Meta:
        model = Object
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}