from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from authenticate_user.models import CustomUser
from authenticate_user.serializer import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import FriendRequest
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from .serializer import FriendRequestSerializer


class UserSearchAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_keyword = request.query_params.get('q')
        if not search_keyword:
            return Response({'error': 'Search keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Search by email
        if '@' in search_keyword:
            users = CustomUser.objects.filter(email=search_keyword)
            if user:
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)

        # Search by name
        else:
            users = CustomUser.objects.filter(first_name__icontains=search_keyword) | CustomUser.objects.filter(last_name__icontains=search_keyword)
            paginator = Paginator(users, 10)
            page_number = request.query_params.get('page', 1)
            page_obj = paginator.get_page(page_number)
            serializer = CustomUserSerializer(page_obj, many=True)
            return Response(serializer.data)


class SendFriendRequestAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        sender = request.user
        receiver_email = request.data.get('receiver_email')
        receiver = CustomUser.objects.filter(email=receiver_email).first()
        
        if not receiver:
            return Response({'error': 'Receiver does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if sender == receiver:
            return Response({'error': 'You cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').exists():
            return Response({'error': 'Friend request already sent to this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has already sent 3 friend requests within the last minute
        recent_requests = FriendRequest.objects.filter(sender=sender, created_at__gte=timezone.now() - timezone.timedelta(minutes=1)).count()
        if recent_requests >= 3:
            return Response({'error': 'You have exceeded the limit of 3 friend requests per minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)



class ListFriendsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve pending friend requests for the authenticated user
        accepted_requests = FriendRequest.objects.filter(receiver=request.user, status='accepted')
        
        # Serialize the friend requests data
        serializer = FriendRequestSerializer(accepted_requests, many=True)
        
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)



class PendingFriendRequestsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve accepted friend requests for the authenticated user
        pending_requests = FriendRequest.objects.filter(sender=request.user, status='pending')
        
        # Get the list of friends who have accepted friend requests
        requests = [request.user.id]  # Add the authenticated user to the list of friends
        for request in pending_requests:
            requests.append(request.receiver.id)
        
        # Return the list of friends as a JSON response
        return Response(requests, status=status.HTTP_200_OK)



