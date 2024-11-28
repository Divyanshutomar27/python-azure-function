import logging
import os
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function triggered to retrieve secret.")

    # Key Vault URL
    key_vault_name = os.getenv("test-az-function")  # Set this in your application settings
    kv_url = f"https://test-az-function.vault.azure.net/"

    try:
        # Use the Managed Identity to authenticate
        credential = ManagedIdentityCredential()

        # Connect to the Key Vault
        secret_client = SecretClient(vault_url=kv_url, credential=credential)

        # Retrieve the secret
        secret_name = "key1"  # Replace with your secret name
        secret = secret_client.get_secret(secret_name)

        logging.info(f"Successfully retrieved secret: {secret.name}")
        return func.HttpResponse(f"Secret Value: {secret.value}", status_code=200)

    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        return func.HttpResponse("Failed to retrieve secret.", status_code=500)
