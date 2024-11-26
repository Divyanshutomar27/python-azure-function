import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Replace with your Key Vault URL
        key_vault_url = "https://test-az-function.vault.azure.net/"
        secret_name = "key1"
        
        # Authenticate using Managed Identity
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Fetch the secret
        secret = client.get_secret(secret_name).value
        print(f"Fetched secret: {secret}")  # For debugging (remove in production)

        # Set it as an environment variable
        os.environ["MY_SECRET"] = secret

        # Use the secret in your application logic
        secret_value = os.getenv("MY_SECRET")
        return func.HttpResponse(f"Secret value: {secret_value}", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
