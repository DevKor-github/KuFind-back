from rest_framework import (
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Person, Comment
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


# def new_comment(request, pk):
#     if request.user.is_authenticated:
#         post = get_object_or_404(Person, pk=pk)
#
#         if request.method == 'POST':
#             comment_form = CommentForm(request.POST)
#             if comment_form.is_valid():
#                 comment = comment_form.save(commit=False)
#                 comment.post = post
#                 comment.user = request.user
#                 comment.save()
#                 return redirect(comment.get_absolute_url())
#         else:
#             return redirect(post.get_absolute_url())
#     else:
#         raise PermissionDenied
#
# class CommentUpdate(LoginRequiredMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and request.user == self.get_object().user:
#             return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#
#
#
# def delete_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     person = comment.person
#     if request.user.is_authenticated and request.user == comment.user:
#         comment.delete()
#         return redirect(person.get_absolute_url())
#     else:
#         raise PermissionDenied


