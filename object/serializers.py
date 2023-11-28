from rest_framework import serializers

from core.models import Object, ObjectComment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectComment
        fields = ('pk', 'post', 'text')
    
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectComment
        fields = ('post', 'text')

class ObjectSerializer(serializers.ModelSerializer):
    #Serializers for object.

    class Meta:
        model = Object
        fields = ['id', 'title',]
        read_only_fields = ['id']

class ObjectDetailSerializer(ObjectSerializer):
    #Serializer for object detail view.
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(ObjectSerializer.Meta):
        fields = ObjectSerializer.Meta.fields + ['description', 'comments']

class ObjectImageSerializer(serializers.ModelSerializer):
    #Serializer for uploading images to object.

    class Meta:
        model = Object
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}