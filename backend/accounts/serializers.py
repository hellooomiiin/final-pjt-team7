from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

# 유저 정보 조회
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'profile_image', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150, required=True)
    nickname = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "비밀번호가 일치하지 않습니다."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

# 회원 정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('nickname', 'profile_image', 'new_password', 'password_confirm')
    
    def validate(self, attrs):
        # 새 비밀번호가 있으면 비밀번호 확인도 필요
        new_password = attrs.get('new_password')
        password_confirm = attrs.get('password_confirm')
        
        if new_password:
            if not password_confirm:
                raise serializers.ValidationError({
                    'password_confirm': '비밀번호 확인을 입력해주세요.'
                })
            if new_password != password_confirm:
                raise serializers.ValidationError({
                    'password_confirm': '새 비밀번호가 일치하지 않습니다.'
                })
        elif password_confirm:
            # 비밀번호 확인만 있고 새 비밀번호가 없으면 에러
            raise serializers.ValidationError({
                'new_password': '새 비밀번호를 입력해주세요.'
            })
        
        return attrs
    
    def update(self, instance, validated_data):
        # 비밀번호 변경 처리
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('password_confirm', None)
        
        if new_password:
            instance.set_password(new_password)
        
        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

