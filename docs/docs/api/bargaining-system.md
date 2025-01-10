# Bargaining System API Reference

Comprehensive documentation for the TeleAgent Bargaining System, which handles automated price negotiations and deal-making.

## BargainingAgent

The main class for managing price negotiations and deal-making processes.

### Constructor

```python
def __init__(
    self,
    config: dict,
    price_oracle: PriceOracle = None,
    deal_manager: DealManager = None
):
    """
    Initialize BargainingAgent.
    
    Args:
        config (dict): Configuration containing:
            - min_price (float): Minimum acceptable price
            - max_price (float): Maximum acceptable price
            - negotiation_steps (int): Maximum negotiation rounds
            - strategy (str): Negotiation strategy type
        price_oracle (PriceOracle, optional): Custom price oracle
        deal_manager (DealManager, optional): Custom deal manager
            
    Raises:
        ValueError: If configuration is invalid
        InitializationError: If services initialization fails
    """
```

### Core Methods

#### Negotiation Management

```python
async def start_negotiation(
    self,
    item_id: str,
    initial_price: float,
    counterparty_id: str,
    context: dict = None
) -> dict:
    """
    Start a new price negotiation.
    
    Args:
        item_id: Identifier of item being negotiated
        initial_price: Starting price point
        counterparty_id: Identifier of negotiating party
        context: Optional negotiation context:
            - urgency (str): Negotiation urgency level
            - market_data (dict): Current market information
            - preferences (dict): Negotiation preferences
            
    Returns:
        dict: Negotiation session information:
            - session_id (str): Unique negotiation ID
            - initial_offer (float): Starting offer
            - status (str): Current negotiation status
            
    Raises:
        NegotiationError: If negotiation cannot be started
    """

async def make_offer(
    self,
    session_id: str,
    offer_amount: float,
    justification: str = None
) -> dict:
    """
    Make a price offer in negotiation.
    
    Args:
        session_id: Active negotiation session ID
        offer_amount: Proposed price amount
        justification: Optional reasoning for offer
            
    Returns:
        dict: Offer result containing:
            - offer_id (str): Unique offer identifier
            - status (str): Offer status
            - counter_offer (float): Optional counter-offer
            
    Raises:
        OfferError: If offer is invalid
    """
```

#### Price Analysis

```python
class PriceAnalyzer:
    def __init__(self, market_data: dict = None):
        """
        Initialize price analyzer.
        
        Args:
            market_data: Optional market data:
                - historical_prices (list): Price history
                - market_trends (dict): Trend indicators
                - volatility (float): Price volatility
        """
        
    async def analyze_offer(
        self,
        offer_amount: float,
        context: dict
    ) -> dict:
        """
        Analyze price offer fairness.
        
        Args:
            offer_amount: Proposed price
            context: Market context
            
        Returns:
            dict: Analysis results:
                - fairness_score (float): Offer fairness
                - market_alignment (float): Market fit
                - recommendations (list): Action suggestions
        """
        
    async def suggest_counter_offer(
        self,
        current_offer: float,
        negotiation_history: List[dict]
    ) -> float:
        """
        Suggest counter-offer amount.
        
        Args:
            current_offer: Current offer amount
            negotiation_history: Previous offers
            
        Returns:
            float: Suggested counter-offer amount
        """
```

### Deal Management

```python
class DealManager:
    def __init__(self, config: dict):
        """
        Initialize deal manager.
        
        Args:
            config: Deal management configuration:
                - approval_threshold (float): Auto-approval limit
                - confirmation_required (bool): Need confirmation
                - timeout (int): Deal timeout seconds
        """
        
    async def create_deal(
        self,
        negotiation_id: str,
        final_price: float,
        terms: dict
    ) -> dict:
        """
        Create a new deal from negotiation.
        
        Args:
            negotiation_id: Completed negotiation ID
            final_price: Agreed price amount
            terms: Deal terms and conditions
            
        Returns:
            dict: Created deal information:
                - deal_id (str): Unique deal identifier
                - status (str): Deal status
                - execution_plan (dict): Deal execution steps
                
        Raises:
            DealCreationError: If deal creation fails
        """
        
    async def execute_deal(
        self,
        deal_id: str
    ) -> dict:
        """
        Execute finalized deal.
        
        Args:
            deal_id: Deal to execute
            
        Returns:
            dict: Execution results:
                - transaction_id (str): Transaction identifier
                - status (str): Execution status
                - completion_time (str): Completion timestamp
                
        Raises:
            DealExecutionError: If execution fails
        """
```

### Strategy Management

```python
class NegotiationStrategy:
    def __init__(self, strategy_type: str):
        """
        Initialize negotiation strategy.
        
        Args:
            strategy_type: Strategy type:
                - "aggressive": Quick deal focus
                - "balanced": Balanced approach
                - "conservative": Risk-averse approach
        """
        
    async def evaluate_position(
        self,
        current_price: float,
        negotiation_state: dict
    ) -> dict:
        """
        Evaluate negotiation position.
        
        Args:
            current_price: Current offer price
            negotiation_state: Current state
            
        Returns:
            dict: Position evaluation:
                - strength (float): Position strength
                - next_action (str): Suggested action
                - price_range (tuple): Target range
        """
```

### Usage Examples

#### Basic Negotiation

```python
from teleAgent.bargaining.agent import BargainingAgent

# Initialize agent
agent = BargainingAgent({
    "min_price": 100.0,
    "max_price": 1000.0,
    "negotiation_steps": 5,
    "strategy": "balanced"
})

# Start negotiation
negotiation = await agent.start_negotiation(
    item_id="nft_123",
    initial_price=500.0,
    counterparty_id="user_456",
    context={
        "urgency": "medium",
        "market_data": {"current_floor": 450.0}
    }
)

# Make offer
offer_result = await agent.make_offer(
    session_id=negotiation["session_id"],
    offer_amount=450.0,
    justification="Market alignment adjustment"
)
```

#### Deal Execution

```python
# Create and execute deal
deal = await agent.deal_manager.create_deal(
    negotiation_id=negotiation["session_id"],
    final_price=450.0,
    terms={
        "payment_method": "crypto",
        "delivery_time": "immediate"
    }
)

result = await agent.deal_manager.execute_deal(
    deal_id=deal["deal_id"]
)
```

### Error Handling

```python
class BargainingError(Exception):
    """Base exception for bargaining-related errors"""
    pass

class NegotiationError(BargainingError):
    """Exception for negotiation failures"""
    pass

class OfferError(BargainingError):
    """Exception for offer-related errors"""
    pass

class DealError(BargainingError):
    """Exception for deal-related errors"""
    pass

try:
    negotiation = await agent.start_negotiation(item_id, price, counterparty)
except NegotiationError as e:
    logger.error(f"Negotiation failed: {e}")
    # Handle negotiation failure
except OfferError as e:
    logger.error(f"Offer error: {e}")
    # Handle offer failure
except BargainingError as e:
    logger.error(f"Bargaining operation failed: {e}")
    # Handle other errors
```

### Best Practices

1. **Price Validation**
   ```python
   def validate_price(price: float, context: dict) -> bool:
       """Validate price against market conditions"""
       if price < context["market_floor"]:
           return False
       if price > context["market_ceiling"]:
           return False
       return True
   ```

2. **Negotiation Timeout**
   ```python
   async def negotiate_with_timeout(
       agent: BargainingAgent,
       timeout: int = 300
   ):
       """Handle negotiation with timeout"""
       async with timeout_scope(timeout):
           try:
               result = await agent.start_negotiation(...)
               return result
           except TimeoutError:
               await agent.cancel_negotiation(...)
               raise NegotiationTimeout("Negotiation timed out")
   ```

3. **Deal Safety**
   ```python
   async def safe_deal_execution(
       deal_manager: DealManager,
       deal_id: str
   ) -> dict:
       """Execute deal with safety checks"""
       # Verify deal status
       if not await deal_manager.verify_deal(deal_id):
           raise DealError("Invalid deal")
           
       # Check counterparty
       if not await deal_manager.verify_counterparty(deal_id):
           raise DealError("Counterparty verification failed")
           
       # Execute with retry
       return await retry_with_backoff(
           deal_manager.execute_deal,
           deal_id
       )
   ``` 