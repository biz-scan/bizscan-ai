# MySQL 연결
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST") # localhost
port = os.getenv("DB_PORT") # 3306
db_name = os.getenv("DB_NAME")

# DB 접속 정보
# 형식: mysql+pymysql://아이디:비밀번호@주소:포트/DB이름
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# 세션 공장 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Entity들이 상속받을 기본 클래스
Base = declarative_base()

# 의존성 주입용 함수 (매 요청마다 DB 세션을 열고 닫음)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()