from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics
from base.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from base.api import *

class Register(APIView):
    
    '''
        User registration
    '''

    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request):

        ''''
            Takes in username and pass
            returns access token for upcoming requests
        '''

        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            user = serializer_data.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'access_token': token.key},status=200)
        else:
            return Response(serializer_data.errors, status=400)

class MoviesList(APIView):
    '''
        Movie Listings    
    '''
    def get(self, request):
        
        '''
            Takes in page number as get request parameter
            returns movie list fatched from 3rd party api
        '''

        page = request.GET.get('page', None)
        return Response(get_movieslist(page), status=200)


class CollectionsView(APIView):

    def post(self, request):

        '''
            Takes in movie list of a user
            returns unique id of the collection
        '''

        serializer_data = CollectionSerializer(data=request.data)
        if serializer_data.is_valid():
            collection = serializer_data.save(user=request.user)
            return Response({"uuid": collection.uuid},status=200)
        else:
            return Response(serializer_data.errors, status=400)

    def get(self, request):
        
        '''
            Returns plain list of collecions with success parameter
        '''

        return Response({"is_success":True, "data": CollectionListSerializer(request.user).data}, status=200)

class CollectionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.all()

class RequestView(APIView):
    def get(self, request):
        '''
        To return number of requests from last reset
        '''
        return Response({"requests": General.objects.get(pk=0).request_count})

class RequestResetView(APIView):
    def post(self, request):
        '''
            To reset the count of request stored in database to 0
        '''
        General.objects.filter(pk=0).update(request_count=0)
        return Response({"message": "request count reset successfully"}, status=200)

