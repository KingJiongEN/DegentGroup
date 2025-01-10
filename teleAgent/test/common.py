import os
import pytest

# Custom decorator for skipping tests in GitHub Actions
skip_in_github_actions = pytest.mark.skipif(
    os.getenv('GITHUB_ACTIONS') == 'true',
    reason="Skip Arweave upload tests in GitHub Actions"
)