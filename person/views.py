from rest_framework import (
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from core.models import Person
from person import serializers


class PersonViewSet(viewsets.ModelViewSet):
    #View for manage person APIs.
    serializer_class = serializers.PersonDetailSerializer
    queryset = Person.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        #Retrieve person for authenticated user.
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        #Return the serializer class for request.
        if self.action == 'list':
            return serializers.PersonSerializer
        elif self.action == 'upload_image':
            return serializers.PersonImageSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        #Create a new person.
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        #Upload an image to person.
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

