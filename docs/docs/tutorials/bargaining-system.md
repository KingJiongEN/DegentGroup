# Bargaining System Tutorial

This tutorial will guide you through implementing the TeleAgent Bargaining System for automated NFT price negotiations.

## Overview

We'll create a system that:
1. Implements automated price negotiations
2. Handles multi-party bargaining
3. Integrates with NFT pricing data
4. Manages deal completion
5. Provides transaction security

## Prerequisites

- Completed [Basic Bot Setup](basic-bot.md)
- Understanding of [NFT Creation](nft-creation.md)
- Basic knowledge of price negotiation concepts

## Project Structure

```
bargaining_system/
├── agents/
│   ├── bargainer.py
│   ├── deal_maker.py
│   └── price_advisor.py
├── models/
│   ├── negotiation.py
│   └── deal.py
├── services/
│   ├── price_oracle.py
│   └── escrow.py
└── main.py
```

## Step 1: Bargaining Agent Setup

```python
# agents/bargainer.py
from teleAgent.models.agent_model.bargain.bargainer import BargainerAgent
from teleAgent.models.agent_model.utilities.bargain_utils import PriceRange

class NFTBargainer:
    def __init__(self, config: dict):
        self.agent = BargainerAgent(
            agent_id=config["agent_id"],
            nft_dao=config["nft_dao"],
            llm_config=config["llm"]
        )
        self.price_range = PriceRange(
            min_price=config["min_price"],
            max_price=config["max_price"]
        )
        
    async def start_negotiation(self, context: dict) -> dict:
        """Start a new negotiation session"""
        try:
            # Initialize negotiation
            session = await self.agent.create_session(
                context=context,
                price_range=self.price_range
            )
            
            # Set initial offer
            initial_offer = await self._calculate_initial_offer(context)
            await session.set_initial_offer(initial_offer)
            
            return {
                "session_id": session.id,
                "initial_offer": initial_offer,
                "status": "started"
            }
        except Exception as e:
            logger.error(f"Failed to start negotiation: {e}")
            raise
```

## Step 2: Deal Maker Implementation

```python
# agents/deal_maker.py
class DealMaker:
    def __init__(self, config: dict):
        self.min_profit = config["min_profit"]
        self.max_rounds = config["max_rounds"]
        
    async def evaluate_offer(self, offer: dict, context: dict) -> bool:
        """Evaluate if an offer should be accepted"""
        # Check market conditions
        market_price = await self._get_market_price(offer["nft_id"])
        
        # Calculate potential profit
        potential_profit = self._calculate_profit(
            offer["price"],
            market_price
        )
        
        # Check if offer meets criteria
        if potential_profit >= self.min_profit:
            return True
            
        # Consider negotiation history
        if context["round"] >= self.max_rounds:
            return potential_profit > 0
            
        return False
        
    async def finalize_deal(self, session_id: str) -> dict:
        """Finalize a successful negotiation"""
        try:
            # Get session details
            session = await self._get_session(session_id)
            
            # Create deal
            deal = await self._create_deal(session)
            
            # Initialize escrow
            await self._setup_escrow(deal)
            
            return {
                "deal_id": deal.id,
                "status": "finalized",
                "terms": deal.terms
            }
        except Exception as e:
            logger.error(f"Failed to finalize deal: {e}")
            raise
```

## Step 3: Price Oracle Integration

```python
# services/price_oracle.py
class NFTPriceOracle:
    def __init__(self, config: dict):
        self.data_sources = config["data_sources"]
        self.cache_duration = config["cache_duration"]
        self._price_cache = {}
        
    async def get_price_estimate(self, nft_id: str) -> float:
        """Get estimated price for NFT"""
        # Check cache
        if self._is_cache_valid(nft_id):
            return self._price_cache[nft_id]["price"]
            
        # Fetch prices from multiple sources
        prices = await self._fetch_prices(nft_id)
        
        # Calculate weighted average
        estimated_price = self._calculate_weighted_price(prices)
        
        # Update cache
        self._update_cache(nft_id, estimated_price)
        
        return estimated_price
        
    async def _fetch_prices(self, nft_id: str) -> list:
        """Fetch prices from configured data sources"""
        prices = []
        for source in self.data_sources:
            try:
                price = await source.get_price(nft_id)
                prices.append({
                    "price": price,
                    "weight": source.reliability
                })
            except Exception as e:
                logger.warning(f"Failed to fetch price from {source}: {e}")
        return prices
```

## Step 4: Negotiation Flow Implementation

```python
# models/negotiation.py
class NegotiationSession:
    def __init__(self, config: dict):
        self.id = str(uuid.uuid4())
        self.buyer = config["buyer"]
        self.seller = config["seller"]
        self.nft_id = config["nft_id"]
        self.status = "active"
        self.rounds = []
        self.current_offer = None
        
    async def make_offer(self, offer: float, party: str) -> dict:
        """Record a new offer in the negotiation"""
        self.rounds.append({
            "round": len(self.rounds) + 1,
            "party": party,
            "offer": offer,
            "timestamp": datetime.now()
        })
        
        self.current_offer = offer
        return {
            "status": "offer_made",
            "round": len(self.rounds),
            "offer": offer
        }
        
    async def accept_offer(self) -> dict:
        """Accept the current offer"""
        self.status = "accepted"
        return {
            "status": "accepted",
            "final_price": self.current_offer,
            "rounds": len(self.rounds)
        }
        
    async def reject_offer(self, reason: str = None) -> dict:
        """Reject the current offer"""
        self.status = "rejected"
        return {
            "status": "rejected",
            "reason": reason,
            "rounds": len(self.rounds)
        }
```

## Step 5: Command Implementation

```python
# main.py
class BargainingCommands:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.bargainer = NFTBargainer(config)
        self.deal_maker = DealMaker(config)
        
    async def setup_handlers(self):
        @self.client.on_command("start_bargain")
        async def handle_start_bargain(message):
            try:
                # Parse NFT ID and initial price
                nft_id = message.text.split()[1]
                
                # Start negotiation
                result = await self.bargainer.start_negotiation({
                    "nft_id": nft_id,
                    "user_id": message.from_user.id
                })
                
                # Send confirmation
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=f"🤝 Negotiation started!\n"
                         f"Initial offer: {result['initial_offer']} SOL\n"
                         f"Use /make_offer <amount> to negotiate"
                )
                
            except Exception as e:
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Failed to start bargaining: {str(e)}"
                )
                
        @self.client.on_command("make_offer")
        async def handle_make_offer(message):
            try:
                # Parse offer amount
                amount = float(message.text.split()[1])
                
                # Process offer
                result = await self.bargainer.process_offer(
                    session_id=get_active_session(message.from_user.id),
                    amount=amount
                )
                
                # Check if deal can be made
                if await self.deal_maker.evaluate_offer(result, {
                    "round": result["round"]
                }):
                    # Finalize deal
                    deal = await self.deal_maker.finalize_deal(
                        result["session_id"]
                    )
                    
                    await self.client.send_message(
                        chat_id=message.chat.id,
                        text=f"🎉 Deal reached!\n"
                             f"Final price: {deal['terms']['price']} SOL"
                    )
                else:
                    # Continue negotiation
                    counter_offer = await self.bargainer.generate_counter_offer(
                        result
                    )
                    
                    await self.client.send_message(
                        chat_id=message.chat.id,
                        text=f"Counter offer: {counter_offer} SOL"
                    )
                    
            except Exception as e:
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Failed to process offer: {str(e)}"
                )
```

## Best Practices

1. **Price Validation**
   ```python
   def validate_price(price: float, context: dict) -> bool:
       """Validate if price is within acceptable range"""
       return (
           price >= context["min_price"] and
           price <= context["max_price"] and
           price > 0
       )
   ```

2. **Transaction Security**
   ```python
   async def secure_transaction(deal: dict):
       """Implement secure transaction handling"""
       # Create escrow
       escrow = await create_escrow_account(deal)
       
       # Lock funds
       await escrow.lock_funds(deal["price"])
       
       # Verify NFT ownership
       await verify_nft_ownership(deal["nft_id"], deal["seller"])
       
       # Execute transfer
       return await execute_secure_transfer(escrow, deal)
   ```

3. **State Management**
   ```python
   class NegotiationState:
       """Manage negotiation state"""
       def __init__(self):
           self.active_sessions = {}
           self.completed_deals = {}
           
       async def save_state(self):
           """Persist negotiation state"""
           await database.save_sessions(self.active_sessions)
           await database.save_deals(self.completed_deals)
   ```

## Testing

```python
# test_bargaining.py
@pytest.mark.asyncio
async def test_negotiation_flow():
    # Setup
    bargainer = NFTBargainer(test_config)
    deal_maker = DealMaker(test_config)
    
    # Start negotiation
    session = await bargainer.start_negotiation({
        "nft_id": "test_nft",
        "initial_price": 100
    })
    
    # Make offer
    result = await bargainer.process_offer(
        session["session_id"],
        90
    )
    
    # Verify result
    assert result["status"] == "counter_offer"
    assert 80 <= result["counter_offer"] <= 100
```

## Troubleshooting

1. **Price Discrepancies**
   - Check price oracle data
   - Verify calculation logic
   - Monitor market conditions

2. **Failed Negotiations**
   - Review negotiation logs
   - Check price thresholds
   - Verify user permissions

3. **Transaction Issues**
   - Verify wallet balances
   - Check network status
   - Monitor gas prices

## Next Steps

1. Implement advanced features:
   - Multi-party negotiations
   - Auction integration
   - Price prediction

2. Add security features:
   - Fraud detection
   - Dispute resolution
   - Insurance integration

3. Explore other tutorials:
   - [Artwork Creation](artwork-creation.md) 