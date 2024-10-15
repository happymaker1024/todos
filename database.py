from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite3 엔진을 정의, DB파일 todo.sqlite3
DB_URL = 'sqlite:///todo.sqlite3'

# 엔진객체 생성
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

# DB 연결(세션) 객체 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()