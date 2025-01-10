# Artwork Creation Guide

This tutorial will guide you through implementing AI-powered artwork creation using TeleAgent's artwork generation system.

## Overview

We'll create a system that:
1. Generates AI artwork using DALL-E
2. Implements artwork critique and refinement
3. Manages artwork storage and retrieval
4. Handles style customization
5. Provides quality control

## Prerequisites

- Completed [Basic Bot Setup](basic-bot.md)
- OpenAI API key for DALL-E
- IPFS or similar storage solution
- Basic understanding of image generation

## Project Structure

```
artwork_system/
├── generators/
│   ├── artist.py
│   ├── critic.py
│   └── dalle_client.py
├── storage/
│   ├── ipfs_storage.py
│   └── metadata.py
├── styles/
│   ├── style_manager.py
│   └── templates.py
└── main.py
```

## Step 1: Creative Artist Setup

```python
# generators/artist.py
from teleAgent.models.agent_model.artwork_creation import CreativeArtistAgent
from teleAgent.models.agent_model.artwork_creation.dalle_draw import DalleDrawer

class ArtworkCreator:
    def __init__(self, config: dict):
        self.artist = CreativeArtistAgent(
            character_profile=config["profile"],
            dalle_config=config["dalle"],
            llm_config=config["llm"]
        )
        self.drawer = DalleDrawer(config["dalle"])
        
    async def create_artwork(self, prompt: str, style: dict = None) -> dict:
        """Generate artwork from prompt with optional style"""
        try:
            # Enhance prompt with artistic elements
            enhanced_prompt = await self.artist.enhance_prompt(
                prompt,
                style=style
            )
            
            # Generate initial image
            artwork = await self.drawer.generate_image(enhanced_prompt)
            
            # Get artwork critique
            critique = await self.artist.critique_artwork(artwork)
            
            # Refine if needed
            if critique["score"] < 0.8:
                artwork = await self._refine_artwork(
                    artwork,
                    critique["suggestions"]
                )
            
            return {
                "image_url": artwork["url"],
                "prompt": enhanced_prompt,
                "metadata": artwork["metadata"],
                "critique": critique
            }
        except Exception as e:
            logger.error(f"Artwork creation failed: {e}")
            raise
```

## Step 2: Artwork Critic Implementation

```python
# generators/critic.py
class ArtworkCritic:
    def __init__(self, config: dict):
        self.llm_config = config["llm"]
        self.quality_threshold = config["quality_threshold"]
        
    async def evaluate_artwork(self, artwork: dict) -> dict:
        """Evaluate artwork quality and provide feedback"""
        try:
            # Analyze composition
            composition_score = await self._analyze_composition(artwork)
            
            # Analyze style consistency
            style_score = await self._analyze_style(artwork)
            
            # Analyze technical quality
            technical_score = await self._analyze_technical_quality(artwork)
            
            # Calculate overall score
            overall_score = (
                composition_score * 0.4 +
                style_score * 0.3 +
                technical_score * 0.3
            )
            
            # Generate improvement suggestions
            suggestions = await self._generate_suggestions(
                artwork,
                {
                    "composition": composition_score,
                    "style": style_score,
                    "technical": technical_score
                }
            )
            
            return {
                "score": overall_score,
                "composition_score": composition_score,
                "style_score": style_score,
                "technical_score": technical_score,
                "suggestions": suggestions
            }
        except Exception as e:
            logger.error(f"Artwork evaluation failed: {e}")
            raise
```

## Step 3: Style Management

```python
# styles/style_manager.py
class StyleManager:
    def __init__(self):
        self.available_styles = {
            "impressionist": {
                "brush_strokes": "visible, loose",
                "color_palette": "vibrant",
                "lighting": "natural, outdoor"
            },
            "minimalist": {
                "composition": "simple, clean",
                "color_palette": "limited",
                "details": "essential only"
            },
            "fantasy": {
                "elements": "magical, surreal",
                "color_palette": "ethereal",
                "atmosphere": "mystical"
            }
        }
        
    async def apply_style(self, prompt: str, style_name: str) -> str:
        """Apply selected style to prompt"""
        if style_name not in self.available_styles:
            raise ValueError(f"Unknown style: {style_name}")
            
        style = self.available_styles[style_name]
        
        # Enhance prompt with style elements
        enhanced_prompt = f"{prompt}, in {style_name} style, "
        enhanced_prompt += f"with {style['brush_strokes']} brush strokes, "
        enhanced_prompt += f"using a {style['color_palette']} color palette"
        
        return enhanced_prompt
```

## Step 4: Storage Implementation

```python
# storage/ipfs_storage.py
from ipfs_client import IPFSClient

class ArtworkStorage:
    def __init__(self, config: dict):
        self.ipfs = IPFSClient(config["ipfs_endpoint"])
        self.metadata_store = {}
        
    async def store_artwork(self, artwork: dict) -> str:
        """Store artwork and metadata in IPFS"""
        try:
            # Store image
            image_cid = await self.ipfs.add_file(artwork["image"])
            
            # Prepare metadata
            metadata = {
                "title": artwork.get("title", "Untitled"),
                "description": artwork["prompt"],
                "image": f"ipfs://{image_cid}",
                "attributes": {
                    "style": artwork.get("style", "default"),
                    "creation_date": datetime.now().isoformat(),
                    "critique_score": artwork["critique"]["score"]
                }
            }
            
            # Store metadata
            metadata_cid = await self.ipfs.add_json(metadata)
            
            # Update local store
            self.metadata_store[metadata_cid] = metadata
            
            return {
                "image_cid": image_cid,
                "metadata_cid": metadata_cid
            }
        except Exception as e:
            logger.error(f"Storage failed: {e}")
            raise
```

## Step 5: Command Implementation

```python
# main.py
class ArtworkCommands:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.creator = ArtworkCreator(config)
        self.storage = ArtworkStorage(config)
        self.style_manager = StyleManager()
        
    async def setup_handlers(self):
        @self.client.on_command("create_artwork")
        async def handle_create_artwork(message):
            try:
                # Parse command
                args = message.text.split(maxsplit=2)
                if len(args) < 2:
                    raise ValueError(
                        "Usage: /create_artwork [style] <prompt>"
                    )
                
                style = args[1] if len(args) == 3 else "default"
                prompt = args[-1]
                
                # Send processing message
                status_message = await self.client.send_message(
                    chat_id=message.chat.id,
                    text="🎨 Creating your artwork..."
                )
                
                # Generate artwork
                artwork = await self.creator.create_artwork(
                    prompt,
                    style=style
                )
                
                # Store artwork
                storage_info = await self.storage.store_artwork(artwork)
                
                # Send result
                await self.client.send_photo(
                    chat_id=message.chat.id,
                    photo=artwork["image_url"],
                    caption=(
                        f"✨ Artwork created!\n"
                        f"Style: {style}\n"
                        f"Quality score: {artwork['critique']['score']:.2f}\n"
                        f"IPFS: ipfs://{storage_info['image_cid']}"
                    )
                )
                
            except Exception as e:
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Failed to create artwork: {str(e)}"
                )
```

## Best Practices

1. **Quality Control**
   ```python
   async def ensure_quality(artwork: dict) -> bool:
       """Verify artwork meets quality standards"""
       # Check resolution
       if not meets_resolution_requirements(artwork["image"]):
           return False
           
       # Check style consistency
       if not verify_style_consistency(artwork):
           return False
           
       # Check content safety
       if not verify_content_safety(artwork):
           return False
           
       return True
   ```

2. **Resource Management**
   ```python
   class ResourceManager:
       def __init__(self):
           self.api_calls = 0
           self.last_reset = time.time()
           
       async def check_resources(self):
           """Check and manage API usage"""
           # Reset counter if needed
           if time.time() - self.last_reset >= 3600:
               self.api_calls = 0
               self.last_reset = time.time()
               
           # Check limits
           if self.api_calls >= MAX_API_CALLS:
               raise ResourceLimitError("API call limit reached")
               
           self.api_calls += 1
   ```

3. **Error Recovery**
   ```python
   async def handle_generation_error(error: Exception, context: dict):
       """Handle artwork generation errors"""
       if isinstance(error, APIError):
           # Retry with different parameters
           return await retry_with_fallback(context)
       elif isinstance(error, QualityError):
           # Try regenerating with enhanced prompt
           return await regenerate_with_improvements(context)
       else:
           raise
   ```

## Testing

```python
# test_artwork.py
@pytest.mark.asyncio
async def test_artwork_creation():
    # Setup
    creator = ArtworkCreator(test_config)
    
    # Test basic creation
    artwork = await creator.create_artwork(
        "A serene mountain landscape"
    )
    assert artwork["critique"]["score"] >= 0.8
    
    # Test style application
    styled_artwork = await creator.create_artwork(
        "A serene mountain landscape",
        style="impressionist"
    )
    assert "impressionist" in styled_artwork["prompt"].lower()
```

## Troubleshooting

1. **Generation Issues**
   - Check API key validity
   - Verify prompt formatting
   - Monitor rate limits

2. **Quality Issues**
   - Review critique scores
   - Check style consistency
   - Verify image resolution

3. **Storage Issues**
   - Check IPFS connection
   - Verify metadata format
   - Monitor storage space

## Next Steps

1. Implement advanced features:
   - Style transfer
   - Image editing
   - Animation support

2. Add enhancement options:
   - Resolution upscaling
   - Color correction
   - Detail enhancement

3. Explore integrations:
   - Social media sharing
   - NFT creation
   - Print-on-demand services 