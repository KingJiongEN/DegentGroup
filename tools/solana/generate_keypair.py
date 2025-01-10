from solders.keypair import Keypair
import base58

def generate_keypair():
    """
    Generate a new Solana keypair and print the configuration.
    Just run this script directly to generate a new keypair.
    """
    # Generate new keypair
    keypair = Keypair()
    # Get the 64-byte secret key by converting the Keypair object to bytes
    private_key_bytes = bytes(keypair)
    # Encode the 64-byte secret key to base58
    private_key_base58 = base58.b58encode(private_key_bytes).decode('ascii')
    # Get public key string
    public_key = str(keypair.pubkey())
    
    # Print results in a formatted way
    print("\n🔑 Generated new Solana keypair:\n")
    print(f"📫 Wallet Address (public key):\n{public_key}\n")
    print(f"🔐 Private Key (64-byte base58 encoded):\n{private_key_base58}\n")

if __name__ == "__main__":
    generate_keypair()
