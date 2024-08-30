# User Roles
USER_ROLE_ADMIN = 'admin'
USER_ROLE_USER = 'user'

# Friend Request Statuses
FRIEND_REQUEST_PENDING = 'pending'
FRIEND_REQUEST_ACCEPTED = 'accepted'
FRIEND_REQUEST_REJECTED = 'rejected'
FROM_USER = 'from_user'
TO_USER = 'to_user'

# Views.py constants
EMAIL = 'email'
PASSWORD = 'password'

STATUS_CHOICES = [
        (FRIEND_REQUEST_PENDING, 'Pending'),
        (FRIEND_REQUEST_ACCEPTED, 'Accepted'),
        (FRIEND_REQUEST_REJECTED, 'Rejected'),
    ]

# Other Constants
MAX_FRIEND_REQUESTS_PER_MINUTE = 3


