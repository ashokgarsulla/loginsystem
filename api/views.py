from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.generics import CreateAPIView

class StudentCreate(CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserRegistrationSerializer