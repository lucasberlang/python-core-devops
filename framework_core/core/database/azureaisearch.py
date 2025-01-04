try:
    from typing import Any, Dict, List, Optional
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient, SearchItemPaged
    from azure.search.documents.models import QueryType
    from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger
except ImportError:
    raise ImportError("Need to install core['azure']")

logger = AzureOpenTelemetryLogger().logger


class AzureSearchConnector:
    """
    A class to manage Azure AI Search operations.
    Supports endpoint and key authentication.
    """

    def __init__(self, service_endpoint: str, index_name: str, credential: str):
        """Initializes an instance of the class with the specified Azure Search service endpoint, index name, and credentials.

        Args:
            service_endpoint (str): The endpoint URL of the Azure Search service.
            index_name (str): The name of the Azure Search index to connect to.
            credential (str): The credential used to authenticate with the Azure Search service.

        Raises:
            Exception: If the connection to the Azure Search client fails.
        """
        self.service_endpoint = service_endpoint
        self.index_name = index_name
        self.credential = AzureKeyCredential(credential)

        try:
            self.client = SearchClient(
                endpoint=self.service_endpoint,
                index_name=self.index_name,
                credential=self.credential,
            )
            logger.info(f"Successfully connected to Azure Search index: {index_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure Search client: {str(e)}")
            raise

    def simple_search(self, search_text: str, top: int = 10) -> SearchItemPaged[Dict]:
        """Perform a simple search using the provided search text.

        This method interacts with the search client to retrieve a list of search results based on the specified search text. It allows for pagination by specifying the number of top results to return.

        Args:
            search_text (str): The text to search for.
            top (int, optional): The maximum number of results to return. Defaults to 10.

        Returns:
            SearchItemPaged[Dict]: A paginated list of search results.

        Raises:
            Exception: If an error occurs during the search process, an exception is logged and re-raised.
        """
        try:
            results = self.client.search(
                search_text=search_text, top=top, include_total_count=True
            )
            return list(results)
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise

    def advanced_search(
        self,
        search_text: str,
        filter_condition: Optional[str] = None,
        order_by: Optional[List[str]] = None,
        select: Optional[List[str]] = None,
        facets: Optional[List[str]] = None,
    ) -> SearchItemPaged[Dict]:
        """Performs an advanced search with optional filtering, ordering, and selection of fields.

        Args:
            search_text (str): The text to search for.
            filter_condition (Optional[str]): An optional filter condition to apply to the search results.
            order_by (Optional[List[str]]): A list of fields to order the results by.
            select (Optional[List[str]]): A list of fields to select in the results.
            facets (Optional[List[str]]): A list of facets to include in the search.

        Returns:
            SearchItemPaged[Dict]: A dictionary containing the search results, facets, and total count of results.

        Raises:
            Exception: If an error occurs during the search process.
        """
        try:
            results = self.client.search(
                search_text=search_text,
                filter=filter_condition,
                facets=facets,
                order_by=order_by,
                select=select,
                query_type=QueryType.FULL,
                include_total_count=True,
            )

            results_list = list(results)
            facet_results = results.get_facets()

            return {
                "results": results_list,
                "facets": facet_results,
                "count": results.get_count(),
            }
        except Exception as e:
            logger.error(f"Advanced search error: {str(e)}")
            raise

    def semantic_search(
        self,
        search_text: str,
        semantic_configuration_name: Optional[str] = None,
        top: int = 10,
        query_caption: str = "extractive",
    ) -> SearchItemPaged[Dict]:
        """Performs a semantic search using the specified search text and configuration.

        Args:
            search_text (str): The text to search for semantically.
            semantic_configuration_name (Optional[str]): The name of the semantic configuration to use. Defaults to None.
            top (int): The number of top results to return. Defaults to 10.
            query_caption (str): The caption type for the query. Defaults to "extractive".

        Returns:
            SearchItemPaged[Dict]: A paginated list of search results.

        Raises:
            Exception: If an error occurs during the search process.
        """
        try:
            results = self.client.search(
                search_text=search_text,
                top=top,
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name=semantic_configuration_name,
                query_caption=query_caption,
                include_total_count=True,
            )
            return list(results)
        except Exception as e:
            logger.error(f"Semantic search error: {str(e)}")
            raise

    def suggest(
        self, search_text: str, suggester_name: str, top: int = 5
    ) -> List[Dict[str, Any]]:
        """Suggests a list of items based on the provided search text and suggester name.

        Args:
            search_text (str): The text to search for suggestions.
            suggester_name (str): The name of the suggester to use for generating suggestions.
            top (int, optional): The maximum number of suggestions to return. Defaults to 5.

        Returns:
            List[Dict[str, Any]]: A list of suggested items, where each item is represented as a dictionary.

        Raises:
            Exception: If an error occurs while fetching suggestions, an exception is logged and re-raised.
        """
        try:
            suggestions = self.client.suggest(
                search_text=search_text, suggester_name=suggester_name, top=top
            )
            return list(suggestions)
        except Exception as e:
            logger.error(f"Suggestion error: {str(e)}")
            raise

    def lookup_document(self, key: str) -> Dict[str, Any]:
        """Lookup a document by its key.

        This method retrieves a document from the client using the provided key.
        It ensures that the result is a dictionary and raises an error if it is not.
        In case of any exceptions during the lookup, an error is logged.

        Args:
            key (str): The key of the document to be looked up.

        Returns:
            Dict[str, Any]: The document retrieved from the client, represented as a dictionary.

        Raises:
            ValueError: If the retrieved document is not a dictionary.
            Exception: If there is an error during the document lookup process.
        """
        try:
            result = self.client.get_document(key=key)
            if not isinstance(result, dict):
                raise ValueError("Document is not a dictionary")
            return result
        except Exception as e:
            logger.error(f"Document lookup error: {str(e)}")
            raise
