from injector import Module, provider, singleton

from sqlalchemy.orm import sessionmaker

from teleAgent.daos.agent.interface import IAgentDAO
from teleAgent.daos.nft.interface import INFTDAO
from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.daos.artwork_critique.interface import IArtworkCritiqueDAO

from .agent_service import AgentService
from .interfaces import IAgentService, INFTService, IWalletService, ITwitterAuthService
from .nft_service_fake import NFTServiceFake
from .wallet_service_fake import WalletServiceFake
from .twitter_auth_service import TwitterAuthService

class ServicesModule(Module):
    @singleton
    @provider
    def provide_wallet_service(self) -> IWalletService:
        return WalletServiceFake()

    @singleton
    @provider
    def provide_nft_service(self) -> INFTService:
        return NFTServiceFake()

    @singleton
    @provider
    def provide_twitter_auth_service(self, dao: ITwitterAuthDAO) -> ITwitterAuthService:
        return TwitterAuthService(dao)

    @singleton
    @provider
    def provide_agent_service(
        self, 
        session_factory: sessionmaker,
        nft_dao: INFTDAO,
        artwork_critique_dao: IArtworkCritiqueDAO,
        agent_dao: IAgentDAO
    ) -> IAgentService:
        return AgentService(session_factory, nft_dao, artwork_critique_dao, agent_dao)
