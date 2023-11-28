from rest_framework import serializers

from core.models import Person, PersonComment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonComment
        fields = ('pk', 'post', 'text')
    
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonComment
        fields = ('post', 'text')

class PersonSerializer(serializers.ModelSerializer):
    #Serializers for person.

    class Meta:
        model = Person
        fields = ['id', 'title']
        read_only_fields = ['id']

class PersonDetailSerializer(PersonSerializer):
    #Serializer for person detail view.
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PersonSerializer.Meta):
        fields = PersonSerializer.Meta.fields + ['description', 'comments']

class PersonImageSerializer(serializers.ModelSerializer):
    #Serializer for uploading images to person.

    class Meta:
        model = Person
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


