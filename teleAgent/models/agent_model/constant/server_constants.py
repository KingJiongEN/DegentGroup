import os
from pathlib import Path

# Database settings
DB_PATH = os.getenv('DB_PATH', 'crossplatform_agent.db')

# Server settings
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', '1'))  # seconds
BACKOFF_INTERVAL = int(os.getenv('BACKOFF_INTERVAL', '5'))  # seconds for error backoff

# Task types
class TaskType:
    TELEGRAM_GROUP_MESSAGE = 'telegram_group_message'
    TELEGRAM_DIRECT_MESSAGE = 'telegram_direct_message'
    TWITTER_THREAD = 'twitter_thread'
    TWITTER_COMMENT = 'twitter_comment'

# Task statuses
class TaskStatus:
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Database table names
class DBTable:
    TASKS = 'tasks'
    CONVERSATIONS = 'conversations'

# SQL Queries
class SQLQuery:
    CREATE_TASKS_TABLE = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            agent_uid TEXT NOT NULL,
            status TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    
    CREATE_CONVERSATIONS_TABLE = """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            messages TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """
    
    GET_PENDING_TASKS = """
        SELECT id, type, agent_uid, status, data, created_at, updated_at 
        FROM tasks 
        WHERE agent_uid = ? AND status = ?
        ORDER BY created_at ASC
    """
    
    GET_CONVERSATION_HISTORY = """
        SELECT messages FROM conversations WHERE task_id = ?
    """
    
    UPDATE_TASK_WITH_RESPONSE = """
        UPDATE tasks 
        SET status = ?, data = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    """
    
    UPDATE_TASK_STATUS = """
        UPDATE tasks 
        SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    """

# Agent configuration
DEFAULT_AGENT_CONFIG = {
    "name": "TwitterBot1",
    "uid": "twitter_bot_1",
    "profile": {
        "personality": "Helpful and informative",
        "interests": ["technology", "science", "current events"],
        "communication_style": "Professional and friendly"
    },
    "core_values": [
        "Provide accurate and helpful information",
        "Maintain professional communication",
        "Respect user privacy and boundaries"
    ],
    "role": "assistant"
}

# Chat prompts
class ChatPrompt:
    GROUP_CHAT = "你在和大家聊天。群聊成员有：{members}"
    PRIVATE_CHAT = "你现在和 # {sender} # 私聊中。你们的消息只会被彼此看见。"
    TWITTER_THREAD = "Generate a Twitter thread about: {topic}"
    TWITTER_COMMENT = "Respond to Twitter comment: {comment}" 