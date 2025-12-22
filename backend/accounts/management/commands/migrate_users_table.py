"""
기존 users 테이블의 데이터를 accounts_user 테이블로 마이그레이션하는 커맨드

사용법:
    python manage.py migrate_users_table
"""
from django.core.management.base import BaseCommand
from django.db import connection
from accounts.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '기존 users 테이블의 데이터를 accounts_user 테이블로 마이그레이션합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--default-password',
            type=str,
            default='defaultpassword123!',
            help='기존 사용자들에게 적용할 기본 비밀번호 (기본값: defaultpassword123!)',
        )

    def handle(self, *args, **options):
        default_password = options['default_password']
        
        # SQLite 연결
        cursor = connection.cursor()
        
        # 1. users 테이블이 존재하는지 확인
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if not cursor.fetchone():
            self.stdout.write(
                self.style.WARNING('users 테이블이 존재하지 않습니다.')
            )
            return
        
        # 2. users 테이블의 데이터 조회
        cursor.execute("SELECT user_id, email, nickname FROM users")
        users_data = cursor.fetchall()
        
        if not users_data:
            self.stdout.write(
                self.style.WARNING('users 테이블에 데이터가 없습니다.')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'기존 users 테이블에서 {len(users_data)}개의 레코드를 발견했습니다.')
        )
        
        # 3. accounts_user 테이블이 존재하는지 확인
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='accounts_user'
        """)
        
        if not cursor.fetchone():
            self.stdout.write(
                self.style.ERROR('accounts_user 테이블이 존재하지 않습니다.')
            )
            self.stdout.write(
                self.style.WARNING('먼저 "python manage.py migrate"를 실행하여 테이블을 생성해주세요.')
            )
            return
        
        # 4. 기존 accounts_user 테이블의 이메일 목록 조회 (중복 방지)
        existing_emails = set(
            User.objects.values_list('email', flat=True)
        )
        
        # 5. 데이터 마이그레이션
        migrated_count = 0
        skipped_count = 0
        
        for user_id, email, nickname in users_data:
            # 이메일이 이미 존재하면 건너뛰기
            if email in existing_emails:
                self.stdout.write(
                    self.style.WARNING(f'이메일 {email}가 이미 존재하여 건너뜁니다.')
                )
                skipped_count += 1
                continue
            
            try:
                # username은 email의 @ 앞 부분 사용 또는 nickname 사용
                username = email.split('@')[0] if '@' in email else nickname
                
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
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ 마이그레이션 완료: {email} (username: {username}, nickname: {nickname})'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ 마이그레이션 실패: {email} - {str(e)}')
                )
        
        # 6. 결과 요약
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(
            self.style.SUCCESS(f'마이그레이션 완료: {migrated_count}개 성공, {skipped_count}개 건너뜀')
        )
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write(
            self.style.WARNING(
                f'참고: 모든 사용자의 기본 비밀번호는 "{default_password}"로 설정되었습니다.'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '사용자가 로그인하려면 비밀번호를 변경해야 합니다.'
            )
        )

