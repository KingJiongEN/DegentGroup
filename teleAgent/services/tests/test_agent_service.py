import pytest
from unittest.mock import AsyncMock, Mock, patch
from PIL import Image
import io

from teleAgent.services.agent_service import AgentService
from teleAgent.models.agent_model.proact_groupagent import ProactGroupAgent
from teleAgent.constants import InteractionScene
from teleAgent.integrations.telegram import TelegramResponse

@pytest.fixture
def agent_service():
    return AgentService()

@pytest.fixture
def mock_proact_agent():
    agent = AsyncMock(spec=ProactGroupAgent)
    agent.id = "test-agent-1"
    agent.name = "TestAgent"
    agent.PROFILE_MESSAGE = "Test profile {self}"
    agent.groupchat = Mock()
    agent.groupchat.messages = [{"content": "test message"}]
    # Mock the store_TGgroup_message method
    agent.update_groupchat = AsyncMock()
    return agent

@pytest.mark.asyncio
async def test_process_message_telegram_private(agent_service, mock_proact_agent):
    """Test processing private Telegram messages"""
    # Setup
    agent_service._agents = {"test-agent-1": mock_proact_agent}
    mock_recipient = AsyncMock()
    mock_recipient.groupchat.messages = [{"content": "test response"}]
    
    # Mock the user proxy agent
    mock_user_proxy = AsyncMock()
    mock_user_proxy.a_initiate_chat = AsyncMock(return_value=Mock(summary="test response"))
    
    with patch('teleAgent.services.agent_service.create_bargain_group_chat', return_value=(None, mock_recipient)), \
         patch('teleAgent.services.agent_service.UserProxyAgent', return_value=mock_user_proxy):
        # Execute
        response = await agent_service.process_message(
            agent_id="test-agent-1",
            user_id="user1",
            is_bot=False,
            content="Hello",
            scene=InteractionScene.TELEGRAM_PRIVATE
        )
        
        # Assert
        assert isinstance(response, TelegramResponse)
        assert response.text == "test response"
        assert not response.image

@pytest.mark.asyncio
async def test_process_message_telegram_group_chat(agent_service, mock_proact_agent):
    """Test processing group Telegram messages with normal chat response"""
    # Setup
    agent_service._agents = {"test-agent-1": mock_proact_agent}
    expected_response = "group chat response"
    mock_proact_agent.a_generate_group_chat_response = AsyncMock(return_value=expected_response)
    
    # Force non-periodic action by patching random
    with patch('random.random', return_value=0.9):
        # Execute
        response = await agent_service.process_message(
            agent_id="test-agent-1",
            user_id="group1",
            is_bot=False,
            content="Hello group",
            scene=InteractionScene.TELEGRAM_GROUP
        )
    
    # Assert
    assert isinstance(response, TelegramResponse)
    assert response.text == expected_response
    # Verify the message was stored
    mock_proact_agent.update_groupchat.assert_awaited_once_with(expected_response)

@pytest.mark.asyncio
async def test_process_message_telegram_group_periodic_art(agent_service, mock_proact_agent):
    """Test processing group Telegram messages with periodic art creation"""
    # Setup
    agent_service._agents = {"test-agent-1": mock_proact_agent}
    
    # Create a mock PIL Image
    mock_image = Image.new('RGB', (60, 30), color='red')
    mock_art_response = {
        "drawing": mock_image,
        "poem": "test poem"
    }
    
    # Mock the artwork agent and its creation
    mock_art_agent = AsyncMock()
    mock_art_agent.create_complete_artwork = AsyncMock(return_value=mock_art_response)
    
    # Mock the act_periodically method
    expected_response = TelegramResponse.media_with_text(
        text=f'Hi everyone, I just write a poem and create a painting based on that. Feel free to share your thoughts.\n Poem: {mock_art_response["poem"]}',
        image=mock_image
    )
    agent_service.act_periodically = AsyncMock(return_value=expected_response)
    
    with patch('random.random', return_value=0.05):  # Force periodic action
        # Execute
        response = await agent_service.process_message(
            agent_id="test-agent-1",
            user_id="group1",
            is_bot=False,
            content="Hello group",
            scene=InteractionScene.TELEGRAM_GROUP
        )
    
    # Assert
    assert isinstance(response, TelegramResponse)
    assert isinstance(response.image, Image.Image)
    assert "test poem" in response.text
    # Verify act_periodically was called
    agent_service.act_periodically.assert_awaited_once_with(mock_proact_agent)
    # Verify the message was stored
    mock_proact_agent.update_groupchat.assert_awaited_once_with(response.text)

@pytest.mark.asyncio
async def test_process_message_memory_storage(agent_service, mock_proact_agent):
    """Test that messages are properly stored in memory"""
    # Setup
    agent_service._agents = {"test-agent-1": mock_proact_agent}
    mock_recipient = AsyncMock()
    mock_recipient.groupchat.messages = [{"content": "test response"}]
    
    # Mock the user proxy agent
    mock_user_proxy = AsyncMock()
    mock_user_proxy.a_initiate_chat = AsyncMock(return_value=Mock(summary="test response"))
    
    with patch('teleAgent.services.agent_service.create_bargain_group_chat', return_value=(None, mock_recipient)), \
         patch('teleAgent.services.agent_service.UserProxyAgent', return_value=mock_user_proxy):
        # Execute
        await agent_service.process_message(
            agent_id="test-agent-1",
            user_id="user1",
            is_bot=False,
            content="Hello",
            scene=InteractionScene.TELEGRAM_PRIVATE
        )
        
        # Assert
        stored_messages = agent_service._memories["test-agent-1"]["user1"]
        assert len(stored_messages) == 2  # User message and agent response
        assert stored_messages[0]["content"] == "Hello"
        assert stored_messages[0]["role"] == "user"
        assert stored_messages[1]["role"] == "assistant"
        assert stored_messages[1]["content"] == "test response"

@pytest.mark.asyncio
async def test_process_message_agent_not_found(agent_service):
    """Test processing message with non-existent agent"""
    with pytest.raises(ValueError) as exc_info:
        await agent_service.process_message(
            agent_id="non-existent",
            user_id="user1",
            is_bot=False,
            content="Hello",
            scene=InteractionScene.TELEGRAM_PRIVATE
        )
    assert "Agent not found" in str(exc_info.value)

@pytest.mark.asyncio
async def test_process_message_unsupported_scene(agent_service, mock_proact_agent):
    """Test processing message with unsupported scene"""
    # Setup
    agent_service._agents = {"test-agent-1": mock_proact_agent}
    
    with pytest.raises(ValueError) as exc_info:
        await agent_service.process_message(
            agent_id="test-agent-1",
            user_id="user1",
            is_bot=False,
            content="Hello",
            scene="unsupported_scene"
        )
    assert "Unsupported interaction scene" in str(exc_info.value)
  