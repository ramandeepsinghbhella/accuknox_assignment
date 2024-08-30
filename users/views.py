from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, LoginSerializer, UserSearchSerializer
from users.constants import *
from django.utils import timezone
from datetime import timedelta

class SignupView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        # print(search)
        if '@' in search:  # Email search
            user = User.objects.filter(email__iexact=search)
            if user.exists():
                return user
            else:
                # If no user found, return an empty queryset
                return User.objects.none()
        return User.objects.filter(name__icontains=search)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'User not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FriendRequestView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get(TO_USER)
        to_user = User.objects.get(id=to_user_id)

        # Rate limiting
        recent_requests = FriendRequest.objects.filter(
            from_user=from_user,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).count()
        if recent_requests >= MAX_FRIEND_REQUESTS_PER_MINUTE:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        request = FriendRequest(from_user=from_user, to_user=to_user)
        request.save()
        return Response({'status': 'Request sent'}, status=status.HTTP_201_CREATED)

class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def patch(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        if friend_request.to_user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        requested_status = request.data.get('status')
        if requested_status not in [FRIEND_REQUEST_ACCEPTED, FRIEND_REQUEST_REJECTED]:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.status = requested_status
        friend_request.save()
        return Response({'status': 'Request updated'}, status=status.HTTP_200_OK)

class ListFriendsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(from_user=user, status=FRIEND_REQUEST_ACCEPTED).values_list(TO_USER, flat=True)
        return User.objects.filter(id__in=friends)

class PendingFriendRequestsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status=FRIEND_REQUEST_PENDING)
