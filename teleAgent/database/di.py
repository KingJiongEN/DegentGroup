from typing import Generator

from injector import Module, provider, singleton
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import URL

from teleAgent.core.config import settings
from teleAgent.database.base import Base

class DatabaseModule(Module):
    @singleton
    @provider
    def provide_engine(self) -> Engine:
        engine_kwargs = {
            "pool_pre_ping": True,
        }
        
        if not settings.DATABASE_URL.startswith("sqlite"):
            engine_kwargs.update({
                "pool_size": 20,
                "max_overflow": 10,
            })
            
        engine = create_engine(
            settings.DATABASE_URL,
            **engine_kwargs
        )
        Base.metadata.create_all(bind=engine)
        return engine

    @singleton
    @provider
    def provide_session_factory(self, engine: Engine) -> sessionmaker:
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )

    @provider
    def provide_db_session(self, session_factory: sessionmaker) -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()