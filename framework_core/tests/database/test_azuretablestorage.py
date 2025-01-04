import pytest
from unittest.mock import Mock, patch
from typing import Generator
from core.database.azuretablestorage import AzureTableStorage


@pytest.fixture  # type: ignore[misc]
def mock_table_service() -> Generator[Mock, None, None]:
    with patch("core.database.azuretablestorage.TableServiceClient") as mock:
        mock_instance = Mock()
        mock.from_connection_string.return_value = mock_instance
        yield mock


@pytest.fixture  # type: ignore[misc]
def mock_credential() -> Generator[Mock, None, None]:
    with patch("azure.core.credentials.AzureNamedKeyCredential") as mock:
        yield mock


connection_string = "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key"


class TestAzureTableStorage:
    def test_init_with_connection_string(self) -> None:
        """Test initialization with connection string."""
        storage = AzureTableStorage(connection_string=connection_string)

        assert storage.connection_string == connection_string

    def test_init_with_access_key(self) -> None:
        with patch(
            "core.database.azuretablestorage.TableServiceClient"
        ) as mock_service:
            with patch(
                "core.database.azuretablestorage.AzureNamedKeyCredential"
            ) as mock_cred:
                endpoint = "https://test.table.core.windows.net"
                account_name = "testaccount"
                access_key = "testkey"

                AzureTableStorage(
                    endpoint=endpoint, account_name=account_name, access_key=access_key
                )

                mock_cred.assert_called_once_with(account_name, access_key)
                mock_service.assert_called_once_with(
                    endpoint=endpoint, credential=mock_cred.return_value
                )
