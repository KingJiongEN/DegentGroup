import pytest
from unittest.mock import Mock, AsyncMock, patch
from PIL import Image
from io import BytesIO
from teleAgent.services.agent_service import AgentService
from teleAgent.integrations.telegram import TelegramResponse
from teleAgent.models.agent_model.proact_groupagent import ProactGroupAgent
from teleAgent.models.nft import NFT, NFTMetadata
from datetime import datetime

@pytest.fixture
def session_factory():
    return Mock()

@pytest.fixture
def agent_service(session_factory):
    service = AgentService(session_factory)
    # Mock the internal agents dictionary
    service._agents = {
        'agent1': Mock(spec=ProactGroupAgent, id='agent1', name='Agent1'),
        'agent2': Mock(spec=ProactGroupAgent, id='agent2', name='Agent2')
    }
    return service

@pytest.mark.asyncio
async def test_act_periodically_artwork_creation_success(agent_service):
    # Mock the agent
    mock_agent = Mock(spec=ProactGroupAgent)
    mock_agent.id = 'test_agent'
    mock_agent.name = 'Test Agent'
    
    # Mock artwork creation result
    mock_artwork = {
        'name': 'Test Artwork',
        'description': 'Test Description',
        'poem': 'Test Poem',
        'drawing': Image.new('RGB', (100, 100)),  # Create dummy image
        'local_image_path': 'test/path.png',
        'art_style': 'Test Style',
        'attributes': {'test': 'attribute'}
    }
    
    # Mock critics result
    mock_critics = [
        {
            'agent_id': 'critic1',
            'agent_name': 'Critic 1',
            'critique_details': 'Test critique',
            'overall_score': 8.5,
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    # Mock NFT
    mock_nft = NFT(
        id='test_nft',
        token_id='token1',
        contract_address='address1',
        metadata=NFTMetadata(
            name='Test NFT',
            description='Test Description',
            image_url='test/path.png',
            art_style='pop_art',
            attributes='attributes'
        ),
        creator_id='test_agent',
        owner_id='test_agent'
    )
    
    # Setup mocks
    with patch('teleAgent.models.agent_model.artwork_creation.artwork_creater.create_artwork_agent') as mock_create_artwork_agent:
        mock_artwork_agent = AsyncMock()
        mock_artwork_agent.create_complete_artwork.return_value = mock_artwork
        mock_create_artwork_agent.return_value = mock_artwork_agent
        
        with patch.object(agent_service, 'critic_artwork', return_value=mock_critics):
            with patch.object(agent_service, 'store_artwork', return_value=mock_nft):
                # Execute test
                result = await agent_service.act_periodically_artwork_creation(mock_agent)
                
                # Assertions
                assert isinstance(result, TelegramResponse)
                assert 'Test Artwork' in result.text
                assert result.image is not None
                assert isinstance(result.image, BytesIO)

@pytest.mark.asyncio
async def test_act_periodically_artwork_creation_error(agent_service):
    mock_agent = Mock(spec=ProactGroupAgent)
    
    with patch('teleAgent.models.agent_model.artwork_creation.artwork_creater.create_artwork_agent') as mock_create_artwork_agent:
        mock_artwork_agent = AsyncMock()
        mock_artwork_agent.create_complete_artwork.side_effect = Exception("Artwork creation failed")
        mock_create_artwork_agent.return_value = mock_artwork_agent
        
        result = await agent_service.act_periodically_artwork_creation(mock_agent)
        
        assert isinstance(result, TelegramResponse)
        assert "Sorry, I encountered an error" in result.text

@pytest.mark.asyncio
async def test_act_periodically_market_adjust_success(agent_service):
    # Mock the artificial market
    mock_deal = {
        'nft_id': 'test_nft',
        'buyer_id': 'agent2',
        'seller_id': 'agent1',
        'transaction_amount': 100
    }
    agent_service.artificial_market.agent_sell = AsyncMock(return_value=mock_deal)
    
    # Mock NFT DAO
    mock_nft = Mock()
    mock_nft.metadata.image_url = 'test/path.png'
    mock_nft.metadata.name = 'Test NFT'
    agent_service.nft_dao.get_by_id = Mock(return_value=mock_nft)
    
    # Mock image handling
    with patch('PIL.Image.open') as mock_image_open:
        mock_image = Mock()
        mock_image.tobytes.return_value = b'test_image_bytes'
        mock_image_open.return_value = mock_image
        
        result = await agent_service.act_periodically_market_adjust(Mock(spec=ProactGroupAgent))
        
        assert isinstance(result, TelegramResponse)
        assert "NEW DEAL MADE!" in result.text
        assert result.image is not None
        assert result.caption == "Test NFT"

@pytest.mark.asyncio
async def test_act_periodically_market_adjust_no_deal(agent_service):
    # Mock the artificial market to return no deal
    agent_service.artificial_market.agent_sell = AsyncMock(return_value=None)
    
    result = await agent_service.act_periodically_market_adjust(Mock(spec=ProactGroupAgent))
    
    assert result is None
