import pytest
from unittest.mock import Mock, AsyncMock, patch
from telegram import Update, Chat, Message, User
from teleAgent.integrations.telegram import TelegramBot
from teleAgent.constants import InteractionScene
from teleAgent.services.interfaces import IAgentService, INFTService, IWalletService

@pytest.fixture
def mock_services():
    """Fixture to create mock services"""
    return {
        'agent_service': AsyncMock(spec=IAgentService),
        'wallet_service': AsyncMock(spec=IWalletService),
        'nft_service': AsyncMock(spec=INFTService)
    }

@pytest.fixture
def mock_bot_config():
    """Fixture for bot configuration"""
    return {
        'id': 'test_bot',
        'telegram_token': 'test_token'
    }

@pytest.fixture
def telegram_bot(mock_services, mock_bot_config):
    """Fixture to create TelegramBot instance with mocked services"""
    return TelegramBot(
        agent_service=mock_services['agent_service'],
        wallet_service=mock_services['wallet_service'],
        nft_service=mock_services['nft_service'],
        bot_config=mock_bot_config
    )

@pytest.fixture
def mock_group_update():
    """Fixture to create a mock group chat update"""
    mock_user = Mock(spec=User)
    mock_user.id = 12345
    mock_user.first_name = "Test User"

    mock_chat = Mock(spec=Chat)
    mock_chat.id = 67890
    mock_chat.type = 'group'

    mock_message = Mock(spec=Message)
    mock_message.text = "Hello group!"
    mock_message.chat = mock_chat
    
    mock_update = Mock(spec=Update)
    mock_update.effective_user = mock_user
    mock_update.effective_chat = mock_chat
    mock_update.message = mock_message

    return mock_update

@pytest.mark.asyncio
async def test_handle_group_message(telegram_bot, mock_group_update, mock_services):
    """Test handling of a message in a group chat"""
    # Setup mock response
    mock_services['agent_service'].get_response.return_value = "Hello from agent!"
    
    # Call handle_message
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify agent_service was called with correct scene type
    mock_services['agent_service'].get_response.assert_called_once_with(
        bot_id=mock_group_update.effective_chat.id,
        update=mock_group_update,
        message=mock_group_update.message.text,
    )

@pytest.mark.asyncio
async def test_group_chat_commands(telegram_bot, mock_group_update, mock_services):
    """Test handling of commands in group chat"""
    # Test /start command in group
    mock_group_update.message.text = "/start"
    await telegram_bot.start(mock_group_update, Mock())
    assert mock_group_update.message.reply_text.called
    
    # Test /help command in group
    mock_group_update.message.text = "/help"
    await telegram_bot.help(mock_group_update, Mock())
    assert mock_group_update.message.reply_text.called

@pytest.mark.asyncio
async def test_group_chat_mentions(telegram_bot, mock_group_update, mock_services):
    """Test handling of bot mentions in group chat"""
    # Setup mention message
    mock_group_update.message.text = "@test_bot Hello!"
    
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify agent_service was called
    mock_services['agent_service'].get_response.assert_called_once()

@pytest.mark.asyncio
async def test_group_chat_reply(telegram_bot, mock_group_update, mock_services):
    """Test bot's reply to a message in group chat"""
    # Setup mock response
    mock_response = "This is a group chat response"
    mock_services['agent_service'].get_response.return_value = mock_response
    
    # Handle message
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify the reply was sent
    mock_group_update.message.reply_text.assert_called_once_with(mock_response)

@pytest.mark.asyncio
async def test_group_chat_error_handling(telegram_bot, mock_group_update, mock_services):
    """Test error handling in group chat"""
    # Simulate an error in agent service
    mock_services['agent_service'].get_response.side_effect = Exception("Test error")
    
    # Handle message
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify error handling
    mock_group_update.message.reply_text.assert_called_once()
    error_message = mock_group_update.message.reply_text.call_args[0][0]
    assert "Sorry" in error_message

@pytest.mark.asyncio
async def test_group_chat_state_management(telegram_bot, mock_group_update, mock_services):
    """Test group chat state management"""
    # First message
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Second message
    mock_group_update.message.text = "Second message"
    await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify state management
    assert mock_services['agent_service'].get_response.call_count == 2

@pytest.mark.asyncio
async def test_group_chat_rate_limiting(telegram_bot, mock_group_update, mock_services):
    """Test rate limiting in group chat"""
    # Simulate multiple rapid messages
    for _ in range(5):
        await telegram_bot.handle_message(mock_group_update, Mock())
    
    # Verify rate limiting behavior
    assert mock_services['agent_service'].get_response.call_count <= 5 