from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    사용자 모델
    Django의 AbstractUser를 상속받아 커스텀 사용자 모델을 구현합니다.
    """
    # 이메일 (고유값, 로그인 시 사용)
    email = models.EmailField(unique=True)
    
    # 닉네임 (선택사항)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    
    # 프로필 이미지 (선택사항, profiles/ 디렉토리에 저장)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # 계정 생성일시 (자동 생성)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 계정 수정일시 (자동 업데이트)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        사용자 객체의 문자열 표현
        닉네임이 있으면 닉네임을, 없으면 username을 반환합니다.
        """
        return self.nickname or self.username

