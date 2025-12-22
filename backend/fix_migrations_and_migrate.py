"""
마이그레이션 의존성 문제를 해결하고 데이터를 마이그레이션하는 통합 스크립트
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
from django.db import connection


def fix_migrations():
    """마이그레이션 의존성 문제 해결"""
    
    cursor = connection.cursor()
    
    # django_migrations 테이블에 accounts.0001_initial 추가 (fake)
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='django_migrations'
    """)
    
    if not cursor.fetchone():
        print('[ERROR] django_migrations table does not exist.')
        return False
    
    # 이미 적용되었는지 확인
    cursor.execute("""
        SELECT * FROM django_migrations 
        WHERE app='accounts' AND name='0001_initial'
    """)
    
    if cursor.fetchone():
        print('[INFO] accounts.0001_initial migration already recorded.')
    else:
        # fake 마이그레이션 추가
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('accounts', '0001_initial', datetime('now'))
        """)
        connection.commit()
        print('[SUCCESS] Added accounts.0001_initial as fake migration.')
    
    return True


def create_accounts_user_table():
    """accounts_user 테이블이 없으면 생성"""
    
    cursor = connection.cursor()
    
    # accounts_user 테이블이 이미 존재하는지 확인
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='accounts_user'
    """)
    
    if cursor.fetchone():
        print('[INFO] accounts_user table already exists.')
        return True
    
    # 테이블 생성 (AbstractUser 기반)
    print('[INFO] Creating accounts_user table...')
    
    cursor.execute("""
        CREATE TABLE accounts_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password VARCHAR(128) NOT NULL,
            last_login DATETIME NULL,
            is_superuser BOOLEAN NOT NULL DEFAULT 0,
            username VARCHAR(150) NOT NULL UNIQUE,
            first_name VARCHAR(150) NOT NULL DEFAULT '',
            last_name VARCHAR(150) NOT NULL DEFAULT '',
            email VARCHAR(254) NOT NULL UNIQUE,
            is_staff BOOLEAN NOT NULL DEFAULT 0,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            date_joined DATETIME NOT NULL,
            nickname VARCHAR(100) NULL,
            profile_image VARCHAR(100) NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
    """)
    
    # 인덱스 생성
    cursor.execute("CREATE INDEX accounts_user_username_6821ab7c ON accounts_user(username)")
    cursor.execute("CREATE INDEX accounts_user_email_6821ab7c ON accounts_user(email)")
    
    connection.commit()
    print('[SUCCESS] accounts_user table created.')
    return True


def migrate_users_data(default_password='defaultpassword123!'):
    """기존 users 테이블의 데이터를 accounts_user 테이블로 마이그레이션"""
    
    cursor = connection.cursor()
    
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
    
    # 3. 기존 accounts_user 테이블의 이메일 목록 조회 (중복 방지)
    existing_emails = set(
        User.objects.values_list('email', flat=True)
    )
    
    # 4. 데이터 마이그레이션
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
    
    # 5. 결과 요약
    print('')
    print('=' * 60)
    print(f'[RESULT] Migration completed: {migrated_count} succeeded, {skipped_count} skipped')
    print('=' * 60)
    print('')
    print(f'[NOTE] All users have default password: "{default_password}"')
    print('[NOTE] Users need to change their password to login.')


if __name__ == '__main__':
    print('=' * 60)
    print('Starting migration process...')
    print('=' * 60)
    print('')
    
    # 1. 마이그레이션 의존성 문제 해결
    if not fix_migrations():
        print('[FAILED] Could not fix migrations.')
        sys.exit(1)
    
    print('')
    
    # 2. accounts_user 테이블 생성
    if not create_accounts_user_table():
        print('[FAILED] Could not create accounts_user table.')
        sys.exit(1)
    
    print('')
    
    # 3. 데이터 마이그레이션
    migrate_users_data()
    
    print('')
    print('=' * 60)
    print('[SUCCESS] All migration processes completed!')
    print('=' * 60)

