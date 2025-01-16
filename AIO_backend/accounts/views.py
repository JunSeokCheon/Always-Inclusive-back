from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, logout
from rest_framework.authtoken.models import Token

from .serializers import UserSignupSerializer, UserProfileSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]  # 회원가입은 인증 안 된 상태에서도 가능

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # (선택) 가입과 동시에 토큰 발급
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # 로그인은 인증 없이 접근 가능

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"success": False, "message": "이메일과 비밀번호를 모두 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "해당 계정이 존재하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 확인
        if not user.check_password(password):
            return Response(
                {"success": False, "message": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 여기까지 통과하면 로그인 성공
        # (옵션) TokenAuthentication을 쓴다면 토큰 발급/조회
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": True,
                "message": "로그인 성공",
                "token": token.key
            },
            status=status.HTTP_200_OK
        )

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Token 삭제
        Token.objects.filter(user=request.user).delete()
        # Django session logout (세션 사용 시)
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "User has been deleted."}, status=status.HTTP_200_OK)