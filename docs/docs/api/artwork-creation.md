# Artwork Creation API Reference

Comprehensive documentation for the TeleAgent Artwork Creation system, which handles AI-powered artwork generation and management.

## ArtworkGenerator

The main class for generating and managing AI-powered artwork.

### Constructor

```python
def __init__(
    self,
    config: dict,
    dalle_client: DalleClient = None,
    storage_manager: StorageManager = None
):
    """
    Initialize ArtworkGenerator.
    
    Args:
        config (dict): Configuration containing:
            - model_version (str): DALL-E model version
            - image_size (str): Default image size (e.g., "1024x1024")
            - quality (str): Image quality setting
        dalle_client (DalleClient, optional): Custom DALL-E client
        storage_manager (StorageManager, optional): Custom storage manager
            
    Raises:
        ValueError: If required configuration is missing
        InitializationError: If services initialization fails
    """
```

### Core Methods

#### Artwork Generation

```python
async def generate_artwork(
    self,
    prompt: str,
    style_config: dict = None,
    generation_options: dict = None
) -> dict:
    """
    Generate artwork using AI.
    
    Args:
        prompt: Text description for the artwork
        style_config: Optional style configuration:
            - artistic_style (str): Desired art style
            - color_scheme (str): Preferred colors
            - composition (str): Layout preferences
        generation_options: Optional generation parameters:
            - num_variations (int): Number of variations
            - image_size (str): Custom size for this generation
            - quality (str): Quality setting override
            
    Returns:
        dict: Generated artwork information:
            - image_url (str): URL of generated image
            - prompt_id (str): Unique prompt identifier
            - generation_params (dict): Parameters used
            - variations (list): URLs of variations if requested
            
    Raises:
        GenerationError: If artwork generation fails
    """

async def enhance_prompt(
    self,
    base_prompt: str,
    enhancement_type: str = "detailed"
) -> str:
    """
    Enhance artwork prompt for better results.
    
    Args:
        base_prompt: Original user prompt
        enhancement_type: Type of enhancement:
            - "detailed": Add technical details
            - "artistic": Add artistic elements
            - "style": Add style-specific terms
            
    Returns:
        str: Enhanced prompt
    """
```

#### Style Management

```python
class StyleManager:
    def __init__(self):
        self.available_styles = {}
        
    async def apply_style(
        self,
        prompt: str,
        style_name: str
    ) -> str:
        """
        Apply predefined style to prompt.
        
        Args:
            prompt: Original artwork prompt
            style_name: Name of style to apply
            
        Returns:
            str: Modified prompt with style elements
            
        Raises:
            StyleError: If style is not found
        """
        
    async def register_style(
        self,
        style_name: str,
        style_elements: dict
    ) -> None:
        """
        Register new artwork style.
        
        Args:
            style_name: Name for the style
            style_elements: Style configuration:
                - keywords (list): Style-specific keywords
                - modifiers (list): Prompt modifiers
                - composition (dict): Composition rules
        """
```

### Storage Management

```python
class ArtworkStorage:
    def __init__(self, storage_config: dict):
        """
        Initialize artwork storage.
        
        Args:
            storage_config: Storage configuration:
                - provider (str): Storage provider
                - bucket (str): Storage bucket name
                - path_prefix (str): Storage path prefix
        """
        
    async def store_artwork(
        self,
        image_data: bytes,
        metadata: dict
    ) -> str:
        """
        Store generated artwork.
        
        Args:
            image_data: Raw image data
            metadata: Image metadata:
                - prompt (str): Generation prompt
                - params (dict): Generation parameters
                - timestamp (str): Creation time
                
        Returns:
            str: Storage URL for the artwork
            
        Raises:
            StorageError: If storage operation fails
        """
        
    async def retrieve_artwork(
        self,
        artwork_id: str
    ) -> Tuple[bytes, dict]:
        """
        Retrieve stored artwork.
        
        Args:
            artwork_id: Unique artwork identifier
            
        Returns:
            Tuple containing:
                - bytes: Image data
                - dict: Artwork metadata
                
        Raises:
            NotFoundError: If artwork is not found
        """
```

### Quality Control

```python
class QualityChecker:
    def __init__(self, criteria: dict = None):
        self.criteria = criteria or DEFAULT_CRITERIA
        
    async def check_quality(
        self,
        image_data: bytes,
        prompt: str
    ) -> dict:
        """
        Check artwork quality against criteria.
        
        Args:
            image_data: Generated image data
            prompt: Original generation prompt
            
        Returns:
            dict: Quality check results:
                - score (float): Overall quality score
                - aspects (dict): Individual aspect scores
                - recommendations (list): Improvement suggestions
        """
```

### Usage Examples

#### Basic Artwork Generation

```python
from teleAgent.artwork.generator import ArtworkGenerator

# Initialize generator
generator = ArtworkGenerator({
    "model_version": "dall-e-3",
    "image_size": "1024x1024",
    "quality": "standard"
})

# Generate artwork
artwork = await generator.generate_artwork(
    prompt="A serene landscape with mountains at sunset",
    style_config={
        "artistic_style": "impressionist",
        "color_scheme": "warm",
        "composition": "rule_of_thirds"
    }
)
```

#### Style Application

```python
# Register custom style
await generator.style_manager.register_style(
    style_name="cyberpunk",
    style_elements={
        "keywords": ["neon", "futuristic", "urban"],
        "modifiers": ["high contrast", "vibrant colors"],
        "composition": {
            "lighting": "dramatic",
            "perspective": "dynamic"
        }
    }
)

# Generate with custom style
artwork = await generator.generate_artwork(
    prompt="A city street at night",
    style_config={"artistic_style": "cyberpunk"}
)
```

### Error Handling

```python
class ArtworkError(Exception):
    """Base exception for artwork-related errors"""
    pass

class GenerationError(ArtworkError):
    """Exception for generation failures"""
    pass

class StyleError(ArtworkError):
    """Exception for style-related errors"""
    pass

class StorageError(ArtworkError):
    """Exception for storage operations"""
    pass

try:
    artwork = await generator.generate_artwork(prompt, style_config)
except GenerationError as e:
    logger.error(f"Generation failed: {e}")
    # Handle generation failure
except StyleError as e:
    logger.error(f"Style error: {e}")
    # Handle style-related failure
except ArtworkError as e:
    logger.error(f"Artwork operation failed: {e}")
    # Handle other errors
```

### Best Practices

1. **Prompt Engineering**
   ```python
   def optimize_prompt(prompt: str) -> str:
       """Optimize prompt for better results"""
       # Add detail markers
       prompt = f"Detailed view: {prompt}"
       
       # Add quality markers
       prompt = f"{prompt}, high quality, professional"
       
       # Add composition guidance
       prompt = f"{prompt}, well composed, balanced"
       
       return prompt
   ```

2. **Resource Management**
   ```python
   from contextlib import asynccontextmanager

   @asynccontextmanager
   async def artwork_session():
       """Manage artwork generation resources"""
       generator = ArtworkGenerator(config)
       try:
           yield generator
       finally:
           await generator.cleanup()
   ```

3. **Batch Processing**
   ```python
   async def batch_generate(
       prompts: List[str],
       batch_size: int = 5
   ) -> List[dict]:
       """Process multiple artwork generations"""
       results = []
       for batch in chunks(prompts, batch_size):
           batch_results = await asyncio.gather(
               *(generator.generate_artwork(prompt) for prompt in batch)
           )
           results.extend(batch_results)
       return results
   ``` 