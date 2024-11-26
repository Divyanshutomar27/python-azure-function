import os
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Key Vault URL and Secret Name
        key_vault_url = os.getenv("KEY_VAULT_URL")  # Set in Function App Application Settings
        secret_name = os.getenv("SECRET_NAME")     # Set in Function App Application Settings
        
        if not key_vault_url or not secret_name:
            return func.HttpResponse(
                "KEY_VAULT_URL or SECRET_NAME environment variables are not set.",
                status_code=400
            )

        # Authenticate using Managed Identity
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Fetch the secret from Azure Key Vault
        secret_value = client.get_secret(secret_name).value
        logging.info(f"Fetched secret for '{secret_name}' successfully.")

        # Temporarily store the secret in an environment variable
        os.environ["MY_SECRET"] = secret_value
        logging.info("Stored secret in environment variable 'MY_SECRET'.")

        # Use the secret (for demonstration)
        used_secret = os.getenv("MY_SECRET")
        logging.info(f"Using secret: {used_secret}")

        # Respond with success
        return func.HttpResponse(f"Secret fetched and used: {used_secret}", status_code=200)

    except Exception as e:
        logging.error(f"Error fetching secret: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
