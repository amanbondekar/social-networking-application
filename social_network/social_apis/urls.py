from django.urls import path
from .views import UserSearchAPI,SendFriendRequestAPI,PendingFriendRequestsAPI,ListFriendsAPI

urlpatterns = [
    path('search/', UserSearchAPI.as_view(), name='user_search'),
    path('friend-request/send/', SendFriendRequestAPI.as_view(), name='send-friend-request'),
    path('friends/', ListFriendsAPI.as_view(), name='list_friends'),
    path('friend-requests/pending/', PendingFriendRequestsAPI.as_view(), name='pending_friend_requests'),


]