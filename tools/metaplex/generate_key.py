from cryptography.fernet import Fernet
import base64
import click


def generate_decryption_key() -> str:
    """
    Generate a new Fernet key for Metaplex API encryption/decryption.
    Returns the key in base64 format.
    """
    return Fernet.generate_key().decode('ascii')


def validate_key(key: str) -> bool:
    """
    Validate if a given key is a valid Fernet key.
    
    Args:
        key: The key to validate in base64 format
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Try to decode the key
        key_bytes = key.encode('ascii')
        base64.b64decode(key_bytes)
        
        # Try to initialize Fernet with the key
        Fernet(key_bytes)
        return True
    except Exception:
        return False


@click.command()
@click.option('--validate', '-v', is_flag=True, help='Validate an existing key')
@click.option('--key', '-k', help='Key to validate (required if --validate is used)')
def main(validate: bool, key: str = None):
    """CLI tool to generate or validate Metaplex decryption keys."""
    if validate:
        if not key:
            click.echo("Error: --key is required when using --validate")
            return
        
        is_valid = validate_key(key)
        if is_valid:
            click.echo("✅ Key is valid")
        else:
            click.echo("❌ Key is invalid")
    else:
        new_key = generate_decryption_key()
        click.echo("\n🔑 Generated new decryption key:")
        click.echo(f"\n{new_key}\n")


if __name__ == "__main__":
    main()