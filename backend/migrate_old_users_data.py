"""
기존 users 테이블의 데이터를 accounts_user 테이블로 마이그레이션하는 스크립트

사용법:
    python migrate_old_users_data.py
"""
import os
import sys
import django
import sqlite3

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password


def migrate_users_data(default_password='defaultpassword123!'):
    """기존 users 테이블의 데이터를 accounts_user 테이블로 마이그레이션"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. users 테이블이 존재하는지 확인
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    
    if not cursor.fetchone():
        print('[WARNING] users table does not exist.')
        return
    
    # 2. users 테이블의 데이터 조회
    cursor.execute("SELECT user_id, email, nickname FROM users")
    users_data = cursor.fetchall()
    
    if not users_data:
        print('[WARNING] users table has no data.')
        return
    
    print(f'[SUCCESS] Found {len(users_data)} records in users table.\n')
    
    # 3. accounts_user 테이블이 존재하는지 확인
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='accounts_user'
    """)
    
    if not cursor.fetchone():
        print('[ERROR] accounts_user table does not exist.')
        print('[WARNING] Please run Django migration first.')
        print('   Command: python manage.py migrate --fake-initial')
        return
    
    # 4. 기존 accounts_user 테이블의 이메일 목록 조회 (중복 방지)
    existing_emails = set(
        User.objects.values_list('email', flat=True)
    )
    
    # 5. 데이터 마이그레이션
    migrated_count = 0
    skipped_count = 0
    
    print('Starting data migration...\n')
    
    for user_id, email, nickname in users_data:
        # 이메일이 이미 존재하면 건너뛰기
        if email in existing_emails:
            print(f'[SKIP] Email {email} already exists.')
            skipped_count += 1
            continue
        
        try:
            # username은 email의 @ 앞 부분 사용 또는 nickname 사용
            if email and '@' in email:
                username = email.split('@')[0]
            elif nickname:
                username = nickname
            else:
                username = f'user_{user_id}'
            
            # username 중복 방지 (이미 존재하면 숫자 추가)
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # User 객체 생성
            user = User.objects.create(
                username=username,
                email=email,
                nickname=nickname or username,
                password=make_password(default_password),
                is_active=True,
            )
            
            migrated_count += 1
            print(f'[OK] Migrated: {email} (username: {username}, nickname: {nickname})')
            
        except Exception as e:
            print(f'[FAIL] Migration failed for {email}: {str(e)}')
    
    conn.close()
    
    # 6. 결과 요약
    print('')
    print('=' * 60)
    print(f'[RESULT] Migration completed: {migrated_count} succeeded, {skipped_count} skipped')
    print('=' * 60)
    print('')
    print(f'[NOTE] All users have default password: "{default_password}"')
    print('[NOTE] Users need to change their password to login.')


if __name__ == '__main__':
    migrate_users_data()

