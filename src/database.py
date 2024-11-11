import redis
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from src.settings import settings


class Database:
    def __init__(self, url: str):
        self.engine: Engine = create_engine(url=url)
        self.session_factory: sessionmaker = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_session(self) -> Session:
        with self.session_factory() as session:
            yield session


database = Database(url=settings.db_url.unicode_string())
redis_db = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    username=settings.redis_username,
    password=settings.redis_password,
    decode_responses=True
)
Base = declarative_base()

