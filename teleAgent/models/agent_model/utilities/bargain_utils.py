import logging
import os
from typing import Dict
from teleAgent.constants import CRITIQUE_PRICE_FACTOR, NEG_EMO_PRICE_FACTOR, POS_EMO_PRICE_FACTOR
from teleAgent.models.agent_model.inner_modules.emotion import Emotion
from teleAgent.plugins.plugin_solana.tools.transfer_nft import transfer_nft
from teleAgent.daos.nft.impl import NFTDAO

async def transfer_nft_both_web3and_db(nft_dao: NFTDAO, nft_id: str, to_address: str, amount: float, new_owner_id: str):
    if not os.environ.get("DEBUG"):
        logging.info(f"Transferring NFT {nft_id} to {to_address} with amount {amount}")
        result = await transfer_nft(nft_id, to_address, amount)
        if not result.success:
            raise Exception(f"Failed to transfer NFT: {result.error}")
    transfer_nft_db(nft_dao, nft_id, new_owner_id)

def transfer_nft_db(nft_dao: NFTDAO, nft_id: str, new_owner_id: str):
    nft = nft_dao.get_by_token_id(nft_id)
    if nft:
        nft.current_owner_id = new_owner_id
        nft_dao.update(nft)
    else:
        raise Exception(f"NFT not found: {nft_id}")

def get_artwork_price(critique_score: float, agent_inner_state: Dict) -> int:
    agent_emotion: Emotion = agent_inner_state.get("emotion", {})
    assert agent_emotion, f"Agent emotion not found for agent {agent_inner_state} "
    
    factor = POS_EMO_PRICE_FACTOR if agent_emotion.extreme_emotion_name in Emotion.positive_emotions\
            else NEG_EMO_PRICE_FACTOR
    return critique_score * CRITIQUE_PRICE_FACTOR + agent_emotion.extreme_emotion_value * factor