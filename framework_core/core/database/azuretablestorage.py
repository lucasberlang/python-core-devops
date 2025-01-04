try:
    from azure.data.tables import TableServiceClient, TableClient
    from azure.core.exceptions import ResourceExistsError
    from azure.core.credentials import AzureNamedKeyCredential
    from typing import Dict, List, Optional, Any
    from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger
except ImportError:
    raise ImportError("Need to install core['azure']")

logger = AzureOpenTelemetryLogger().logger


class AzureTableStorage:
    """
    A class to manage Azure Table Storage operations.
    Supports both connection string and access key authentication.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        endpoint: Optional[str] = None,
        account_name: Optional[str] = None,
        access_key: Optional[str] = None,
    ):
        """Initializes a Table Storage client using either a connection string or access key authentication.

        Args:
            connection_string (Optional[str]): The connection string for the Azure Table Storage account.
                If provided, it will be used to authenticate the client.
            endpoint (Optional[str]): The endpoint URL for the Azure Table Storage account.
                Required if using access key authentication.
            account_name (Optional[str]): The name of the Azure Storage account.
                Required if using access key authentication.
            access_key (Optional[str]): The access key for the Azure Storage account.
                Required if using access key authentication.

        Raises:
            Exception: If the initialization of the Table Storage client fails.
        """

        self.connection_string = connection_string
        self.table_service = TableServiceClient.from_connection_string(
            connection_string
        )
        try:
            if all([endpoint, account_name, access_key]):
                credential = AzureNamedKeyCredential(account_name, access_key)
                self.table_service = TableServiceClient(
                    endpoint=endpoint, credential=credential
                )
                logger.info("Using access key authentication")
            else:
                self.connection_string = connection_string
                self.table_service = TableServiceClient.from_connection_string(
                    connection_string
                )
                logger.info("Using connection string authentication")

        except Exception as e:
            logger.error(f"Failed to initialize Table Storage client: {str(e)}")
            raise

    def create_table(self, table_name: str) -> None:
        """Creates a table with the specified name.

        Args:
            table_name (str): The name of the table to be created.

        Raises:
            ResourceExistsError: If a table with the specified name already exists, this exception is caught and ignored.
        """
        try:
            self.table_service.create_table(table_name)
        except ResourceExistsError:
            pass

    def get_table_client(self, table_name: str) -> TableClient:
        """Get a TableClient for the specified table.

        Args:
            table_name (str): The name of the table for which to get the TableClient.

        Returns:
            TableClient: An instance of TableClient for the specified table.
        """
        return self.table_service.get_table_client(table_name)

    def insert_entity(self, table_name: str, entity: Dict[str, Any]) -> None:
        """Inserts an entity into the specified table.

        Args:
            table_name (str): The name of the table where the entity will be inserted.
            entity (Dict): A dictionary representing the entity to be inserted.

        Returns:
            None: This function does not return a value.

        Raises:
            Exception: If there is an error while inserting the entity into the table.
        """
        table_client = self.get_table_client(table_name)
        table_client.create_entity(entity=entity)

    def update_entity(self, table_name: str, entity: Dict[str, Any]) -> None:
        """Update an entity in the specified table.

        Args:
            table_name (str): The name of the table where the entity is located.
            entity (Dict): A dictionary representing the entity to be updated.

        Returns:
            None: This function does not return a value.

        Raises:
            Exception: Raises an exception if the update operation fails.
        """
        table_client = self.get_table_client(table_name)
        table_client.update_entity(entity=entity)

    def delete_entity(self, table_name: str, partition_key: str, row_key: str) -> None:
        """Deletes an entity from the specified table.

        Args:
            table_name (str): The name of the table from which the entity will be deleted.
            partition_key (str): The partition key of the entity to be deleted.
            row_key (str): The row key of the entity to be deleted.

        Returns:
            None
        """
        table_client = self.get_table_client(table_name)
        table_client.delete_entity(partition_key, row_key)

    def query_entities(
        self, table_name: str, query_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query entities from a specified table.

        Args:
            table_name (str): The name of the table to query.
            query_filter (str, optional): An optional filter to apply to the query. Defaults to None.

        Returns:
            List[Dict]: A list of entities retrieved from the table, each represented as a dictionary.
        """
        table_client = self.get_table_client(table_name)
        entities = table_client.query_entities(query_filter)
        return [dict(entity) for entity in entities]

    def get_entity(
        self, table_name: str, partition_key: str, row_key: str
    ) -> Dict[str, Any]:
        """Retrieve an entity from a specified table.

        Args:
            table_name (str): The name of the table from which to retrieve the entity.
            partition_key (str): The partition key of the entity to retrieve.
            row_key (str): The row key of the entity to retrieve.

        Returns:
            Dict: A dictionary representation of the entity retrieved from the table.
        """
        table_client = self.get_table_client(table_name)
        return dict(table_client.get_entity(partition_key, row_key))
