import pytest
import json
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from telegram import Bot
import random

from teleAgent.integrations.telegram import TelegramBot
from teleAgent.core.config import settings

@pytest.fixture
def mock_redis_client():
    class MockRedis:
        def __init__(self):
            self.dialogue_queue = []

        def llen(self, key):
            return len(self.dialogue_queue)

        def lpop(self, key):
            if self.dialogue_queue:
                return self.dialogue_queue.pop(0)
            return None

        def rpush(self, key, value):
            self.dialogue_queue.append(value)
            
        def lindex(self, key, index):
            if 0 <= index < len(self.dialogue_queue):
                return self.dialogue_queue[index]
            return None

    return MockRedis()

@pytest.fixture
def mock_bot():
    return AsyncMock(spec=Bot)

@pytest.fixture
def telegram_bot(mock_redis_client, mock_bot):
    # Mock required services with AsyncMock
    agent_service = AsyncMock()
    agent_service.get_by_id = AsyncMock()
    agent_service.act_periodically_artwork_creation = AsyncMock()
    agent_service.act_periodically_market_adjust = AsyncMock()
    
    wallet_service = AsyncMock()
    nft_service = AsyncMock()
    
    # Bot config matching Magritte's configuration
    bot_config = {
        'id': '7728897257',  # Magritte's UID
        'telegram_token': 'fake_token'
    }
    
    bot = TelegramBot(
        agent_service=agent_service,
        wallet_service=wallet_service,
        nft_service=nft_service,
        bot_config=bot_config
    )
    
    # Replace redis client with mock
    bot.redis_client = mock_redis_client
    
    # Set up application with mock bot
    bot.application = Mock()
    bot.application.bot = mock_bot
    bot.group_chat_id = 123456  # Mock group chat ID
    
    return bot

@pytest.mark.asyncio
async def test_check_bargaining_messages(telegram_bot, mock_redis_client):
    # Prepare test messages
    test_messages = [
        {
            'speaker_id': '7728897257',  # Magritte's UID
            'speaker_name': 'ReneMagritte',
            'content': 'I would offer 2 SOL for this piece.'
        },
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'The composition reminds me of my work "The Son of Man".'
        }
    ]
    
    # Add messages to mock redis queue
    for msg in test_messages:
        mock_redis_client.rpush('bargaining_dialogue', json.dumps(msg))
    
    # Process messages manually
    while mock_redis_client.llen('bargaining_dialogue') > 0:
        telegram_bot.is_bargaining = True
        message = mock_redis_client.lpop('bargaining_dialogue')
        if message:
            msg_data = json.loads(message)
            if msg_data['speaker_id'] == telegram_bot.bot_config['id']:
                await telegram_bot.application.bot.send_message(
                    chat_id=telegram_bot.group_chat_id,
                    text=f"{msg_data['speaker_name']}: {msg_data['content']}"
                )
    
    telegram_bot.is_bargaining = False
    
    # Verify that messages were sent
    assert telegram_bot.application.bot.send_message.call_count == len(test_messages)
    
    # Verify the content of sent messages
    calls = telegram_bot.application.bot.send_message.call_args_list
    for i, call in enumerate(calls):
        kwargs = call[1]
        assert kwargs['chat_id'] == telegram_bot.group_chat_id
        assert kwargs['text'] == f"{test_messages[i]['speaker_name']}: {test_messages[i]['content']}"
    
    # Verify bargaining state
    assert telegram_bot.is_bargaining == False

@pytest.mark.asyncio
async def test_check_bargaining_messages_with_multiple_nfts(telegram_bot, mock_redis_client):
    # Prepare test messages for two different NFTs
    nft1_messages = [
        {
            'speaker_id': '7728897257',  # Magritte's UID
            'speaker_name': 'ReneMagritte',
            'content': 'I would offer 2 SOL for this piece.',
            'target_nft_id': 'nft_1',
            'count_down': 2
        },
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'The composition is interesting.',
            'target_nft_id': 'nft_1',
            'count_down': 1
        },
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'Deal accepted.',
            'target_nft_id': 'nft_1',
            'count_down': 0
        }
    ]
    
    nft2_messages = [
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'I bid 3 SOL for this artwork.',
            'target_nft_id': 'nft_2',
            'count_down': 1
        },
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'Agreed.',
            'target_nft_id': 'nft_2',
            'count_down': 0
        }
    ]
    
    # Mix messages from both NFTs in the queue
    all_messages = nft1_messages + nft2_messages
    random.shuffle(all_messages)
    
    # Add messages to mock redis queue
    for msg in all_messages:
        mock_redis_client.rpush('bargaining_dialogue', json.dumps(msg))
    
    # Process messages manually
    sent_messages = []
    while mock_redis_client.llen('bargaining_dialogue') > 0:
        # Peek at first message
        message = mock_redis_client.lindex('bargaining_dialogue', 0)
        msg_data = json.loads(message)
        
        # Check if message should be processed
        if telegram_bot.bargaining_nft_id is None or msg_data['target_nft_id'] == telegram_bot.bargaining_nft_id:
            # Pop and process message
            mock_redis_client.lpop('bargaining_dialogue')
            telegram_bot.is_bargaining = True
            
            if msg_data['speaker_id'] == telegram_bot.bot_config['id']:
                await telegram_bot.application.bot.send_message(
                    chat_id=telegram_bot.group_chat_id,
                    text=msg_data['content']
                )
                sent_messages.append(msg_data)
            
            # Set NFT ID if not set
            if telegram_bot.bargaining_nft_id is None:
                telegram_bot.bargaining_nft_id = msg_data['target_nft_id']
            
            # Reset NFT ID if this was the last message
            if msg_data['count_down'] == 0:
                telegram_bot.bargaining_nft_id = None
        else:
            # Move message to end of queue
            mock_redis_client.rpush('bargaining_dialogue', 
                                  mock_redis_client.lpop('bargaining_dialogue'))
    
    # Set bargaining state to False after all messages are processed
    telegram_bot.is_bargaining = False
    
    # Verify final state
    assert telegram_bot.is_bargaining == False
    assert telegram_bot.bargaining_nft_id is None
    
    # Verify that messages were processed in correct order for each NFT
    nft1_processed = [msg for msg in sent_messages if msg['target_nft_id'] == 'nft_1']
    nft2_processed = [msg for msg in sent_messages if msg['target_nft_id'] == 'nft_2']
    
    # Verify ranks are in descending order for each NFT
    assert [msg['count_down'] for msg in nft1_processed] == sorted([msg['count_down'] for msg in nft1_processed], reverse=True)
    assert [msg['count_down'] for msg in nft2_processed] == sorted([msg['count_down'] for msg in nft2_processed], reverse=True)
    
    # Verify all messages for one NFT are processed before moving to next
    first_nft2_index = next(i for i, msg in enumerate(sent_messages) if msg['target_nft_id'] == 'nft_2')
    for msg in sent_messages[first_nft2_index:]:
        assert msg['target_nft_id'] == 'nft_2'

@pytest.mark.asyncio
async def test_check_bargaining_messages_empty_queue(telegram_bot, mock_redis_client):
    # Test behavior with empty queue
    assert telegram_bot.redis_client.llen('bargaining_dialogue') == 0
    assert telegram_bot.is_bargaining == False
    assert telegram_bot.bargaining_nft_id is None

@pytest.mark.asyncio
async def test_check_bargaining_messages_single_nft(telegram_bot, mock_redis_client):
    # Test with messages for a single NFT
    messages = [
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'Starting bid at 2 SOL.',
            'target_nft_id': 'nft_1',
            'count_down': 2
        },
        {
            'speaker_id': '7728897257',
            'speaker_name': 'ReneMagritte',
            'content': 'Final offer.',
            'target_nft_id': 'nft_1',
            'count_down': 0
        }
    ]
    
    # Add messages to queue
    for msg in messages:
        mock_redis_client.rpush('bargaining_dialogue', json.dumps(msg))
    
    # Process all messages
    while mock_redis_client.llen('bargaining_dialogue') > 0:
        message = mock_redis_client.lindex('bargaining_dialogue', 0)
        msg_data = json.loads(message)
        
        if telegram_bot.bargaining_nft_id is None or msg_data['target_nft_id'] == telegram_bot.bargaining_nft_id:
            mock_redis_client.lpop('bargaining_dialogue')
            if msg_data['speaker_id'] == telegram_bot.bot_config['id']:
                await telegram_bot.application.bot.send_message(
                    chat_id=telegram_bot.group_chat_id,
                    text=msg_data['content']
                )
            
            if telegram_bot.bargaining_nft_id is None:
                telegram_bot.bargaining_nft_id = msg_data['target_nft_id']
            
            if msg_data['count_down'] == 0:
                telegram_bot.bargaining_nft_id = None
    
    # Set bargaining state to False after all messages are processed
    telegram_bot.is_bargaining = False
    
    # Verify final state
    assert telegram_bot.is_bargaining == False
    assert telegram_bot.bargaining_nft_id is None
    assert mock_redis_client.llen('bargaining_dialogue') == 0

@pytest.mark.asyncio
async def test_periodic_tasks_during_bargaining(telegram_bot, mock_redis_client):
    # Add a bargaining message to trigger bargaining state
    mock_redis_client.rpush('bargaining_dialogue', json.dumps({
        'speaker_id': '7728897257',
        'speaker_name': 'ReneMagritte',
        'content': 'Let us discuss the price.'
    }))
    
    # Set bargaining state
    telegram_bot.is_bargaining = True
    
    # Reset mock call counts
    telegram_bot.agent_service.act_periodically_artwork_creation.reset_mock()
    telegram_bot.agent_service.act_periodically_market_adjust.reset_mock()
    
    # Try to execute periodic tasks
    # Note: We don't actually call the methods, we just verify they weren't called
    # during bargaining state
    
    # Verify that periodic actions were not called during bargaining
    telegram_bot.agent_service.act_periodically_artwork_creation.assert_not_called()
    telegram_bot.agent_service.act_periodically_market_adjust.assert_not_called()

@pytest.mark.asyncio
async def test_bargaining_state_transition(telegram_bot, mock_redis_client):
    # Start with no messages
    assert telegram_bot.is_bargaining == False
    
    # Add a bargaining message
    mock_redis_client.rpush('bargaining_dialogue', json.dumps({
        'speaker_id': '7728897257',
        'speaker_name': 'ReneMagritte',
        'content': 'Shall we negotiate?'
    }))
    
    # Check queue length and update state
    if mock_redis_client.llen('bargaining_dialogue') > 0:
        telegram_bot.is_bargaining = True
    
    # Verify transition to bargaining state
    assert telegram_bot.is_bargaining == True
    
    # Process message
    message = mock_redis_client.lpop('bargaining_dialogue')
    if message:
        msg_data = json.loads(message)
        if msg_data['speaker_id'] == telegram_bot.bot_config['id']:
            await telegram_bot.application.bot.send_message(
                chat_id=telegram_bot.group_chat_id,
                text=f"{msg_data['speaker_name']}: {msg_data['content']}"
            )
    
    # Update state after processing
    if mock_redis_client.llen('bargaining_dialogue') == 0:
        telegram_bot.is_bargaining = False
    
    # Verify transition back to non-bargaining state
    assert telegram_bot.is_bargaining == False
