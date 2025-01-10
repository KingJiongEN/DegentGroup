from injector import Module, provider, singleton
from sqlalchemy.orm import sessionmaker

from teleAgent.daos.agent.impl import AgentDAO
from teleAgent.daos.agent.interface import IAgentDAO
from teleAgent.daos.dialog.impl import DialogDAO
from teleAgent.daos.dialog.interface import IDialogDAO
from teleAgent.daos.twitter_auth.impl import TwitterAuthDAO
from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.daos.nft.impl import NFTDAO
from teleAgent.daos.nft.interface import INFTDAO
from teleAgent.daos.artwork_critique.impl import ArtworkCritiqueDAO
from teleAgent.daos.artwork_critique.interface import IArtworkCritiqueDAO

class DAOModule(Module):
    @singleton
    @provider
    def provide_agent_dao(self, session_factory: sessionmaker) -> IAgentDAO:
        return AgentDAO(session_factory)

    @singleton
    @provider
    def provide_dialog_dao(self, session_factory: sessionmaker) -> IDialogDAO:
        return DialogDAO(session_factory)

    @singleton
    @provider
    def provide_twitter_auth_dao(self, session_factory: sessionmaker) -> ITwitterAuthDAO:
        return TwitterAuthDAO(session_factory)
        
    @singleton
    @provider
    def provide_nft_dao(self, session_factory: sessionmaker) -> INFTDAO:
        return NFTDAO(session_factory)
        
    @singleton
    @provider
    def provide_artwork_critique_dao(self, session_factory: sessionmaker) -> IArtworkCritiqueDAO:
        return ArtworkCritiqueDAO(session_factory)