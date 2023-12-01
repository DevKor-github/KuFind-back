from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    #Serializers for person.

    class Meta:
        model = Person
        fields = ['id', 'title',]
        read_only_fields = ['id']

class PersonDetailSerializer(PersonSerializer):
    #Serializer for person detail view.

    class Meta(PersonSerializer.Meta):
        fields = PersonSerializer.Meta.fields + ['description']

class PersonImageSerializer(serializers.ModelSerializer):
    #Serializer for uploading images to person.

    class Meta:
        model = Person
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}