from contextlib import contextmanager
from typing import Generator

from injector import Injector, Module, multiprovider, singleton
from sqlalchemy.orm import Session, sessionmaker

from teleAgent.database.di import DatabaseModule
from teleAgent.daos.di import DAOModule
from teleAgent.services.di import ServicesModule
from teleAgent.integrations.di import IntegrationsModule
from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService
from teleAgent.core.config import settings
from teleAgent.integrations.telegram import TelegramBot

def setup_injector() -> Injector:
    """Initialize dependency injection container"""
    injector = Injector(
        [
            DatabaseModule(),
            DAOModule(),
            ServicesModule(),
            IntegrationsModule(),
        ]
    )
    return injector

def get_injector() -> Injector:
    """Get global injector instance"""
    if not hasattr(get_injector, "_injector"):
        get_injector._injector = setup_injector()
    return get_injector._injector

@contextmanager
def get_db_session(injector: Injector = None) -> Generator[Session, None, None]:
    """Get database session from injector"""
    if injector is None:
        injector = get_injector()
    
    session_factory = injector.get(sessionmaker)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
      
