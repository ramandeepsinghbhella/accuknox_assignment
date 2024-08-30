from django.urls import path
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, AcceptRejectFriendRequestView, ListFriendsView, PendingFriendRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/search/', UserSearchView.as_view(), name='user_search'),
    path('friends/requests/', FriendRequestView.as_view(), name='send_friend_request'),
    path('friends/requests/<int:pk>/', AcceptRejectFriendRequestView.as_view(), name='accept_reject_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friends/requests/pending/', PendingFriendRequestsView.as_view(), name='pending_friend_requests'),
]
