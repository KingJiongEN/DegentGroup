import pytest
from sqlalchemy.orm import Session
from injector import Injector

from teleAgent.core.di import get_injector, get_db_session
from teleAgent.daos.agent.interface import IAgentDAO
from teleAgent.daos.dialog.interface import IDialogDAO
from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService, ITwitterAuthService

@pytest.mark.integration
class TestDependencyInjection:
    def test_get_injector_returns_singleton(self):
        """Test that get_injector returns the same instance"""
        injector1 = get_injector()
        injector2 = get_injector()
        
        assert isinstance(injector1, Injector)
        assert injector1 is injector2  # Should be the same instance

    def test_injector_provides_core_dependencies(self):
        """Test that injector provides all required core dependencies"""
        injector = get_injector()
        
        # Test database session
        with get_db_session(injector) as session:
            assert isinstance(session, Session)
        
        # Test DAOs
        agent_dao = injector.get(IAgentDAO)
        dialog_dao = injector.get(IDialogDAO)
        twitter_auth_dao = injector.get(ITwitterAuthDAO)
        assert agent_dao is not None
        assert dialog_dao is not None
        assert twitter_auth_dao is not None
        
        # Test Services
        agent_service = injector.get(IAgentService)
        nft_service = injector.get(INFTService)
        wallet_service = injector.get(IWalletService)
        twitter_auth_service = injector.get(ITwitterAuthService)
        
        assert agent_service is not None
        assert nft_service is not None
        assert wallet_service is not None
        assert twitter_auth_service is not None

    def test_different_sessions_are_independent(self):
        """Test that different database sessions are independent"""
        injector = get_injector()
        
        with get_db_session(injector) as session1:
            with get_db_session(injector) as session2:
                assert session1 is not session2