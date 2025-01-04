import logging
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from typing import Optional


class AzureOpenTelemetryLogger:
    """
    A class to manage logging operations.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        log_level: str = "INFO",
        logger_name: str = __name__,
    ):
        """Initializes the class with a logger and Azure Monitor connection.

        Args:
            connection_string (Optional[str]): The connection string for Azure Monitor.
                If None, the default connection settings will be used. Defaults to None.
            log_level (str): The logging level to be used by the logger.
                Defaults to "INFO".
            logger_name (str): The name of the logger. Defaults to the name of the module.
        """
        self.logger = self._setup_logger(logger_name, log_level)
        self._initialize_azure_monitor(connection_string)

    def _setup_logger(self, logger_name: str, log_level: str) -> logging.Logger:
        """Sets up a logger with the specified name and log level.

        Args:
            logger_name (str): The name of the logger to be created or retrieved.
            log_level (str): The logging level to be set for the logger (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

        Returns:
            logging.Logger: The configured logger instance.

        Notes:
            If the logger already has handlers, no new handler will be added.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_azure_monitor(self, connection_string: Optional[str]) -> None:
        """Initializes Azure Monitor with the provided connection string.

        This function checks if a connection string is provided. If not, it attempts to retrieve it from the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING`. If no connection string is available, it logs an informational message indicating that only console logging will be used. If a valid connection string is found, it configures Azure Monitor accordingly.

        Args:
            connection_string (Optional[str]): The connection string for Azure Monitor. If None, the function will look for the environment variable.

        Returns:
            None
        """

        conn_string = connection_string or os.getenv(
            "APPLICATIONINSIGHTS_CONNECTION_STRING"
        )

        if not conn_string:
            self.logger.info(
                "No Azure Monitor connection string provided. Using console logging only."
            )
            return

        configure_azure_monitor(
            connection_string=conn_string,
        )
