from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from typing import List, Optional, Dict
from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger

logger = AzureOpenTelemetryLogger().logger


class AzureKeyVaultManager:
    """
    A class to manage Azure Key Vault operations including retrieving secrets.
    Supports both managed identity and service principal authentication.
    """

    def __init__(
        self,
        vault_url: str,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """Initializes a Key Vault client with the specified parameters.

        This constructor sets up the connection to an Azure Key Vault using either service principal authentication or managed identity authentication based on the provided credentials.

        Args:
            vault_url (str): The URL of the Azure Key Vault.
            tenant_id (Optional[str]): The tenant ID for service principal authentication. Defaults to None.
            client_id (Optional[str]): The client ID for service principal authentication. Defaults to None.
            client_secret (Optional[str]): The client secret for service principal authentication. Defaults to None.

        Raises:
            Exception: If the initialization of the Key Vault client fails.
        """
        self.vault_url = vault_url
        try:
            if all([tenant_id, client_id, client_secret]):
                credentials = ClientSecretCredential(
                    tenant_id=tenant_id,
                    client_id=client_id,
                    client_secret=client_secret,
                )
                logger.info("Using service principal authentication")
            else:
                credentials = DefaultAzureCredential()
                logger.info("Using managed identity authentication")

            self.secret_client = SecretClient(
                vault_url=vault_url, credential=credentials
            )

        except Exception as e:
            logger.error(f"Failed to initialize Key Vault client: {str(e)}")
            raise

    def get_secret(
        self, secret_name: str, version: Optional[str] = None
    ) -> Optional[str]:
        """Retrieves a secret value from the secret client.

        Args:
            secret_name (str): The name of the secret to retrieve.
            version (Optional[str], optional): The version of the secret to retrieve. Defaults to None.

        Returns:
            Optional[str]: The value of the secret if retrieval is successful, otherwise None.

        Raises:
            Exception: Logs an error if the secret retrieval fails.
        """
        try:
            secret = self.secret_client.get_secret(name=secret_name, version=version)
            return str(secret.value)
        except Exception as e:
            logger.error(f"Failed to retrieve secret '{secret_name}': {str(e)}")
            return None

    def get_multiple_secrets(self, secret_names: List[str]) -> Dict[str, Optional[str]]:
        """Retrieves multiple secrets based on the provided list of secret names.

        Args:
            secret_names (List[str]): A list of secret names to retrieve.

        Returns:
            Dict[str, Optional[str]]: A dictionary where the keys are the secret names and the values are the corresponding secret values. If a secret cannot be found, its value will be None.
        """
        secrets = {}
        for secret_name in secret_names:
            secrets[secret_name] = self.get_secret(secret_name)
        return secrets

    def list_secrets(self) -> List[str]:
        """Lists the names of all secrets managed by the secret client.

        This method retrieves the properties of all secrets and returns a list of their names.
        In case of an error during the retrieval process, it logs the error and returns an empty list.

        Returns:
            list: A list of secret names. If an error occurs, an empty list is returned.
        """
        try:
            return [
                secret.name
                for secret in self.secret_client.list_properties_of_secrets()
            ]
        except Exception as e:
            logger.error(f"Failed to list secrets: {str(e)}")
            return []
