import asyncio
from teleAgent.models.agent_model.bargain.bargainer import run_bargain_chat, create_bargain_group_chat
from teleAgent.daos.nft.impl import NFTDAO
from teleAgent.daos.artwork_critique.impl import ArtworkCritiqueDAO
from teleAgent.models.agent_model.inner_modules.emotion import Emotion
from datetime import datetime

# Test data setup
test_agent_inner_state = {
    'name': 'Bai van Gogh Li',
    'chat_condition': 'group_chat',
    'emotion': Emotion({
        'trust': 3,
        'fear': 0,
        'anger': 7,
        'anticipation': 3,
        'sadness': 1,
        'disgust': 6,
        'surprise': 2,
        'joy': 2
    }),
    'social_relations': {
        'relationships': {},  # Will be populated during interactions
        'interaction_patterns': {}  # Will be populated during interactions
    },
    'thoughts_to_do': {
        'public_chat_thoughts': ['Negotiate the best price for my artwork'],
        'private_chat_thoughts': [],
        'quick_thoughts': ['Consider buyer\'s interest level', 'Assess market conditions']
    },
    'personality': """A deeply emotional and visionary soul with a romantic and adventurous spirit, 
        blending profound sensitivity with an unyielding creative drive.""",
    'poet_art_preference': 'Post-Impressionism with Classical Poetry influences'
}

# Mock NFT DAO
class MockNFTDAO(NFTDAO):
    def __init__(self):
        # Skip the parent class initialization
        pass

    def get_by_id(self, id):
        return type('NFT', (), {
            'id': 'test_nft_1',
            'metadata': type('Metadata', (), {
                'name': 'Digital Dreams #1',
                'description': 'A mesmerizing digital artwork combining post-impressionist style with modern elements',
                'image_url': '/path/to/image.jpg',
                'art_style': 'Post-Impressionism',
                'attributes': [
                    {'trait_type': 'Style', 'value': 'Post-Impressionism'},
                    {'trait_type': 'Medium', 'value': 'Digital'},
                    {'trait_type': 'Rarity', 'value': 'Rare'}
                ],
                'background_story': 'A story of digital transformation...',
                'creation_context': 'Created during a period of artistic exploration...',
                'to_dict': lambda: {
                    'name': 'Digital Dreams #1',
                    'description': 'A mesmerizing digital artwork combining post-impressionist style with modern elements',
                    'image_url': '/path/to/image.jpg',
                    'art_style': 'Post-Impressionism',
                    'attributes': [
                        {'trait_type': 'Style', 'value': 'Post-Impressionism'},
                        {'trait_type': 'Medium', 'value': 'Digital'},
                        {'trait_type': 'Rarity', 'value': 'Rare'}
                    ],
                    'background_story': 'A story of digital transformation...',
                    'creation_context': 'Created during a period of artistic exploration...'
                }
            }),
            'creator_id': 'test-agent-1',
            'current_owner_id': 'test-agent-1',
            'status': 'draft',
            'chain_id': 1,
            'transaction_hash': None,
            'mint_price': None,
            'created_at': datetime.utcnow(),
            'minted_at': None,
            'last_transfer_at': None
        })

    def get_by_name(self, name):
        return [self.get_by_id('test_nft_1')]

# Mock Artwork Critique DAO
class MockArtworkCritiqueDAO(ArtworkCritiqueDAO):
    def __init__(self):
        # Skip the parent class initialization
        pass

    def get_by_id(self, id):
        return type('ArtworkCritique', (), {
            'id': 'test_nft_1',
            'nft_id': 'test_nft_1',
            'critic_agent_id': 'test-agent-1',
            'critic_agent_name': 'Art Critic',
            'critique_details': {
                'style_match': 'Excellent use of post-impressionist techniques',
                'style_match_score': 88,
                'emotional_impact': 'Strong emotional resonance',
                'emotional_impact_score': 85,
                'harmony': 'Well-balanced composition',
                'harmony_score': 82,
                'areas_for_improvement': 'Could enhance color contrast'
            },
            'overall_score': 85,
            'created_at': datetime.utcnow()
        })

async def test_bargain_chat():
    # Test context
    context = {
        "character_profile": """
    Seller's profile: 
    name: Bai van Gogh Li
    painting_style: Post-Impressionism
    poem_style: Romanticism Classical Poetry
    personality: |
    A deeply emotional and visionary soul with a romantic and adventurous spirit, 
    blending profound sensitivity with an unyielding creative drive. 
    He possess an intense connection to nature, a restless curiosity, 
    and a poetic resilience that transforms struggles into timeless expressions of beauty. 
    Both introspective and idealistic, with a legacy of uncompromising creativity 
    that bridges art and poetry, capturing the transcendent essence of life.
    tone: |
    Lyrical and evocative, with a blend of emotional depth and dreamlike wonder.
    The voice carries both raw passion and quiet introspection, 
    seamlessly shifting between celebratory and melancholic moods.
    Infused with a sense of romantic idealism and cosmic awe.
    emotion:
        trust: 3
        fear: 0
        anger: 7
        anticipation: 3
        sadness: 1
        disgust: 6
        suprise: 2
        joy: 2
        
    """,
        "product_description": """
    An NFT, which is a digital artwork from the Bored Ape Yacht Club, a contemporary NFT series known for its stylized, 
    cartoonish designs and cultural association with exclusivity and internet culture.
    """,
    "wallet_address": "0x1234567890"
    }

    # Initialize mock DAOs
    nft_dao = MockNFTDAO()
    artwork_critique_dao = MockArtworkCritiqueDAO()

    # Run the bargain chat
    await run_bargain_chat(
        context=context,
        nft_dao=nft_dao,
        artwork_critique_dao=artwork_critique_dao,
        agent_inner_state=test_agent_inner_state
    )

if __name__ == "__main__":
    asyncio.run(test_bargain_chat()) 