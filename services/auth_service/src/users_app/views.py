from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import SignUpSerializer, allUsersSerializer, LoginSerializer, CustomTokenObtainPairSerializers, UserSerializer
from .models import User
from .permissions import IsOwnerOrReadOnly


class RegisterView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AllUsers(ListAPIView):
    model = User
    serializer_class = allUsersSerializer
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializers


class UserDetail(RetrieveUpdateAPIView):
    """
       The Idea is that any user should be able to see another user's profile
       only the profile owner should be able to modify the profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserProfile(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        user = self.get_queryset()[0]
        Serializer = self.serializer_class(user)
        return Response(Serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # user = self.get_queryset()[0]
        user_obj = User.objects.get(id=request.user.id)
        print("user object", user_obj)
        serializer = self.serializer_class(
            data=request.data, instance=user_obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
