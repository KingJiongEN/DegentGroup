import logging
import requests
import json

from arweave.arweave_lib import Transaction

from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger

logger = get_logger("plugin_solana:utils:arweave:transaction")

class EnhancedTransaction(Transaction):
    def __init__(self, wallet, **kwargs):
        # Call the parent class constructor
        super().__init__(wallet, **kwargs)
        
        # Additional initialization for EnhancedTransaction if needed
        self.error_log = []

    def send(self):
        url = "{}/tx".format(self.api_url)
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        json_data = self.json_data
        
        try:
            response = requests.post(url, data=json_data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending transaction: {e}")
            raise Exception(f"Error sending transaction: {e}")

        # Handle non-200 status codes
        if response.status_code != 200:
            error_message = f"Transaction failed with status code {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)

        logger.debug("{}\n\n{}".format(response.text, self.json_data))

        if response.status_code == 200:
            logger.debug("RESPONSE 200: {}".format(response.text))

        return self.last_tx
