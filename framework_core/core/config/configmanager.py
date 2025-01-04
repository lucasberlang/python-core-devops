import os
import yaml
import json
import configparser
from typing import Any, Dict, Optional
from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger

logger = AzureOpenTelemetryLogger().logger


class ConfigManager:
    """
    A class to manage Config in python project.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initializes the class with a configuration path.

        Args:
            config_path (str, optional): The path to the configuration file.
                                          If not provided, it defaults to the
                                          value of the 'CONFIG_PATH' environment
                                          variable or 'config' if that is also not set.

        Attributes:
            config (Dict[str, Any]): A dictionary to hold the configuration data.
        """
        self.config_path = config_path or os.getenv("CONFIG_PATH", "config")
        self.config: Dict[str, Any] = {}

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file.

        This method attempts to load a YAML file from the specified configuration path.
        If successful, it returns the contents of the file as a dictionary. In case of
        an error during the loading process, it logs the error and raises an exception.

        Args:
            filename (str): The name of the YAML file to load.

        Returns:
            Dict[str, Any]: The contents of the YAML file as a dictionary.

        Raises:
            Exception: If there is an error loading the YAML file.
        """
        if self.config_path is None:
            raise ValueError("Configuration path is not set.")

        try:
            filepath = os.path.join(self.config_path, filename)
            with open(filepath, "r") as file:
                data = yaml.safe_load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    f"The content of {filename} is not a valid dictionary."
                )

            return data
        except Exception as e:
            logger.error(f"Error loading YAML config from {filename}: {str(e)}")
            raise

    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load a JSON configuration file.

        This method attempts to load a JSON file from the specified configuration path.
        If successful, it returns the contents of the file as a dictionary.
        In case of an error during the loading process, it logs the error and raises an exception.

        Args:
            filename (str): The name of the JSON file to load.

        Returns:
            Dict[str, Any]: The contents of the JSON file as a dictionary.

        Raises:
            Exception: If there is an error loading the JSON file.
        """
        if self.config_path is None:
            raise ValueError("Configuration path is not set.")

        try:
            filepath = os.path.join(self.config_path, filename)
            with open(filepath, "r") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    f"The content of {filename} is not a valid dictionary."
                )

            return data
        except Exception as e:
            logger.error(f"Error loading JSON config from {filename}: {str(e)}")
            raise

    def load_ini(self, filename: str) -> Dict[str, Any]:
        """Load an INI configuration file and return its contents as a dictionary.

        This method reads an INI file located at the specified filename within the
        configured path and returns a dictionary where each section of the INI file
        is a key, and its corresponding value is another dictionary containing the
        key-value pairs defined in that section.

        Args:
            filename (str): The name of the INI file to load.

        Returns:
            Dict[str, Any]: A dictionary representation of the INI file's sections
            and their respective key-value pairs.

        Raises:
            Exception: If there is an error loading the INI file, an error is logged
            and the exception is raised.
        """
        if self.config_path is None:
            raise ValueError("Configuration path is not set.")

        try:
            filepath = os.path.join(self.config_path, filename)
            config = configparser.ConfigParser()
            config.read(filepath)

            ini_data = {section: dict(config[section]) for section in config.sections()}

            if not isinstance(ini_data, dict):
                raise ValueError(
                    f"The content of {filename} is not a valid dictionary format."
                )

            return ini_data
        except Exception as e:
            logger.error(f"Error loading INI config from {filename}: {str(e)}")
            raise

    def load_environment_variables(self, prefix: str = "") -> Dict[str, str]:
        """Load environment variables that start with a specified prefix.

        Args:
            prefix (str): The prefix to filter environment variable keys. Defaults to an empty string.

        Returns:
            Dict[str, str]: A dictionary containing environment variables that start with the specified prefix.

        Raises:
            Exception: If an error occurs while loading environment variables, an error is logged and the exception is raised.
        """
        try:
            return {
                key: value
                for key, value in os.environ.items()
                if key.startswith(prefix)
            }
        except Exception as e:
            logger.error(f"Error loading environment variables: {str(e)}")
            raise

    def load_config(
        self,
        yaml_file: Optional[str] = None,
        json_file: Optional[str] = None,
        ini_file: Optional[str] = None,
        env_prefix: Optional[str] = None,
    ) -> None:
        """Load configuration from specified files and environment variables.

        This method attempts to load configuration settings from YAML, JSON, and INI files, as well as from environment variables prefixed with a specified string. The loaded configurations are merged into the existing configuration.

        Args:
            yaml_file (Optional[str]): The path to the YAML configuration file.
            json_file (Optional[str]): The path to the JSON configuration file.
            ini_file (Optional[str]): The path to the INI configuration file.
            env_prefix (Optional[str]): The prefix for environment variables to load.

        Raises:
            Exception: If an error occurs while loading the configuration.

        Returns:
            None
        """
        try:
            if yaml_file:
                self.config.update(self.load_yaml(yaml_file))

            if json_file:
                self.config.update(self.load_json(json_file))

            if ini_file:
                self.config.update(self.load_ini(ini_file))

            if env_prefix is not None:
                self.config.update(self.load_environment_variables(env_prefix))

            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves the value associated with the specified key from the configuration.

        Args:
            key (str): The key for which to retrieve the value.
            default (Any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value associated with the key, or the default value if the key is not found.
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value for the specified key.

        Args:
            key (str): The key for the configuration setting.
            value (Any): The value to be associated with the key.

        Returns:
            None: This function does not return a value.

        Logs:
            Debug message indicating that the configuration has been updated.
        """
        self.config[key] = value
        logger.debug(f"Configuration updated: {key}")

    def save_config(self, filename: str, format: str = "yaml") -> None:
        """Saves the configuration to a specified file in the given format.

        This method creates the necessary directory structure if it does not exist and writes the configuration data to a file in either YAML or JSON format. If an unsupported format is provided, a ValueError is raised.

        Args:
            filename (str): The name of the file to save the configuration to.
            format (str, optional): The format to save the configuration in. Defaults to 'yaml'. Supported formats are 'yaml' and 'json'.

        Raises:
            ValueError: If the specified format is not supported.
            Exception: If there is an error during the file writing process.

        Returns:
            None
        """
        if self.config_path is None:
            raise ValueError("Configuration path is not set.")
        try:
            filepath = os.path.join(self.config_path, filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "w") as file:
                if format.lower() == "yaml":
                    yaml.dump(self.config, file, default_flow_style=False)
                elif format.lower() == "json":
                    json.dump(self.config, file, indent=4)
                else:
                    raise ValueError(f"Unsupported format: {format}")

            logger.info(f"Configuration saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise
