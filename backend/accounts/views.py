from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserUpdateSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    사용자 회원가입 뷰
    새로운 사용자를 등록하고 JWT 토큰을 발급합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # 인증 없이 접근 가능

    def create(self, request, *args, **kwargs):
        """
        회원가입 처리
        - 요청 데이터 검증
        - 사용자 생성
        - JWT 토큰 발급 (access, refresh)
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.save()
        
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # 인증 없이 접근 가능
def login_view(request):
    """
    사용자 로그인 뷰
    이메일과 비밀번호로 로그인하고 JWT 토큰을 발급합니다.
    
    요청:
        - email: 사용자 이메일
        - password: 사용자 비밀번호
    
    응답:
        - user: 사용자 정보
        - tokens: JWT 토큰 (access, refresh)
    
    에러:
        - 이메일/비밀번호 구분된 에러 메시지 반환
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    # 입력값 검증
    if not email or not password:
        return Response(
            {'error': '이메일과 비밀번호를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # email로 사용자 찾기
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': '이메일이 올바르지 않습니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # 비밀번호 검증
    if user.check_password(password):
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': '비밀번호가 올바르지 않습니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    사용자 프로필 조회/수정 뷰
    현재 로그인한 사용자의 프로필 정보를 조회하거나 수정합니다.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증 필요

    def get_object(self):
        """
        현재 요청한 사용자 객체 반환
        """
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    사용자 정보 수정 뷰
    현재 로그인한 사용자의 정보를 수정합니다.
    (닉네임, 프로필 이미지, 비밀번호)
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증 필요

    def get_object(self):
        """
        현재 요청한 사용자 객체 반환
        """
        return self.request.user

