"""
accounts_user 테이블을 생성하고 마이그레이션을 설정하는 스크립트
"""
import os
import sys
import django
import sqlite3

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection


def setup_accounts_table():
    """accounts_user 테이블 생성 및 마이그레이션 설정"""
    
    cursor = connection.cursor()
    
    # accounts_user 테이블이 이미 존재하는지 확인
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='accounts_user'
    """)
    
    if cursor.fetchone():
        print('[INFO] accounts_user table already exists.')
    else:
        print('[INFO] Creating accounts_user table...')
        # Django 마이그레이션 SQL 실행
        # 실제로는 migrate 명령을 사용해야 하지만, 
        # 의존성 문제를 피하기 위해 여기서는 수동으로 처리하지 않음
        print('[WARNING] Please run: python manage.py migrate')
        return False
    
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


if __name__ == '__main__':
    if setup_accounts_table():
        print('[SUCCESS] Setup completed. You can now run migrate_old_users_data.py')
    else:
        print('[FAILED] Setup failed. Please check the error messages above.')

