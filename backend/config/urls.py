"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 관리자 페이지
    path('api/v1/accounts/', include('accounts.urls')),  # 계정 관련 API (회원가입, 로그인, 프로필 등)
    # path('api/v1/movies/', include('movies.urls')),  # 영화 관련 API (인기 영화 목록 등)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

