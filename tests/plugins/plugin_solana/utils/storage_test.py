import pytest
import json
from io import BytesIO
from pathlib import Path

from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.utils.storage import upload_to_arweave

TEST_IMAGE_PATH = Path(__file__).parent / "fixtures" / "test_image.png"

def load_test_image():
    """Helper to load test image"""
    with open(TEST_IMAGE_PATH, "rb") as f:
        return f.read()

@pytest.mark.integration
class TestArweaveStorage:
    
    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_upload_json_data(self):
        """Test uploading JSON metadata"""
        test_data = {
            "name": "Test NFT",
            "description": "Test Description",
            "attributes": [{"trait_type": "test", "value": "test"}]
        }
        
        url = await upload_to_arweave(test_data)
        print(f"\ntest_upload_json_data url: {url}")
        
        assert url.startswith("https://arweave.net/")
        assert len(url.split("/")[-1]) == 43  # Arweave transaction ID length

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_upload_binary_data(self):
        """Test uploading binary data"""
        image_data = load_test_image()
        
        url = await upload_to_arweave(image_data)
        print(f"\ntest_upload_binary_data url: {url}")

        assert url.startswith("https://arweave.net/")
        assert len(url.split("/")[-1]) == 43
