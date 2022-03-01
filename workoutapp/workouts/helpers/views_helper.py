from rest_framework_api_key.models import APIKey
from ..models import User

def get_user_data(request):
    user = None
    # Check if key in headers
    if "HTTP_AUTHORIZATION" in request.META:
        # Get key value and then name of owner
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        user_name = APIKey.objects.get_from_key(key)
        user = User.objects.filter(username=user_name)
    else:
        # Else jsut pull the user from the db
        user = User.objects.filter(id=request.user.id)

    return user
