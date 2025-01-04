import pytest
import os
import tempfile
import yaml
import json
from typing import Iterator
from core.config.configmanager import ConfigManager


@pytest.fixture  # type: ignore[misc]
def temp_config_dir() -> Iterator[str]:
    """Fixture to create a temporary directory for config files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture  # type: ignore[misc]
def config_manager(temp_config_dir: str) -> ConfigManager:
    """Fixture to create a ConfigManager instance with temporary directory."""
    return ConfigManager(temp_config_dir)


@pytest.fixture  # type: ignore[misc]
def sample_yaml_config(temp_config_dir: str) -> str:
    """Fixture to create a sample YAML config file."""
    config_data = {
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "api": {"timeout": 30, "retry_attempts": 3},
    }

    filepath = os.path.join(temp_config_dir, "config.yaml")
    with open(filepath, "w") as f:
        yaml.dump(config_data, f)
    return filepath


@pytest.fixture  # type: ignore[misc]
def sample_json_config(temp_config_dir: str) -> str:
    """Fixture to create a sample JSON config file."""
    config_data = {
        "api_key": "test-key-123",
        "secret_key": "secret-456",
        "endpoints": {"auth": "/api/auth", "users": "/api/users"},
    }

    filepath = os.path.join(temp_config_dir, "config.json")
    with open(filepath, "w") as f:
        json.dump(config_data, f)
    return filepath


@pytest.fixture  # type: ignore[misc]
def sample_ini_config(temp_config_dir: str) -> str:
    """Fixture to create a sample INI config file."""
    config_content = """
[server]
host = 127.0.0.1
port = 8000

"""

    filepath = os.path.join(temp_config_dir, "config.ini")
    with open(filepath, "w") as f:
        f.write(config_content)
    return filepath


class TestConfigManager:
    def test_load_yaml_config(
        self, config_manager: ConfigManager, sample_yaml_config: str
    ) -> None:
        """Test loading YAML configuration.

        Args:
            config_manager (ConfigManager): An instance of ConfigManager used to load the YAML configuration.
            sample_yaml_config (str): A string representing the path to the sample YAML configuration file.

        Returns:
            None

        Assertions:
            Asserts that the database host is 'localhost'.
            Asserts that the database port is 5432.
            Asserts that the API timeout is 30.
        """
        config = config_manager.load_yaml("config.yaml")

        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == 5432
        assert config["api"]["timeout"] == 30

    def test_load_json_config(
        self, config_manager: ConfigManager, sample_json_config: str
    ) -> None:
        """Test loading JSON configuration.

        Args:
            config_manager (ConfigManager): The configuration manager instance used to load the JSON config.
            sample_json_config (str): A string representing the sample JSON configuration file.

        Returns:
            None

        Assertions:
            Asserts that the loaded configuration contains the expected API key and endpoint.
        """
        config = config_manager.load_json("config.json")

        assert config["api_key"] == "test-key-123"
        assert config["endpoints"]["auth"] == "/api/auth"

    def test_load_ini_config(
        self, config_manager: ConfigManager, sample_ini_config: str
    ) -> None:
        """Test the loading of an INI configuration file.

        This function tests the `load_ini` method of the `ConfigManager` class to ensure
        that the configuration values for the server host and port are correctly loaded
        from the specified INI file.

        Args:
            config_manager (ConfigManager): An instance of the ConfigManager used to load the INI file.
            sample_ini_config (str): A string representing the path to the sample INI configuration file.

        Raises:
            AssertionError: If the loaded configuration values do not match the expected values.
        """
        config = config_manager.load_ini("config.ini")

        assert config["server"]["host"] == "127.0.0.1"
        assert config["server"]["port"] == "8000"

    def test_load_environment_variables(
        self, config_manager: ConfigManager, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test loading environment variables using the provided config manager.

        This test function uses the `monkeypatch` fixture to set specific environment
        variables for the application. It verifies that the `load_environment_variables`
        method of the `ConfigManager` correctly loads the expected variables while
        ignoring any that do not match the specified prefix.

        Args:
            config_manager (ConfigManager): An instance of the ConfigManager used to
                load environment variables.
            monkeypatch (pytest.MonkeyPatch): The pytest fixture used to modify the
                environment variables during the test.

        Returns:
            None: This function does not return a value; it asserts conditions to
            validate the behavior of the config manager.
        """
        monkeypatch.setenv("APP_API_KEY", "test-key")
        monkeypatch.setenv("APP_DEBUG", "true")
        monkeypatch.setenv("ANOTHER_VAR", "ignore-this")

        config = config_manager.load_environment_variables("APP_")

        assert config["APP_API_KEY"] == "test-key"
        assert config["APP_DEBUG"] == "true"
        assert "ANOTHER_VAR" not in config

    def test_load_multiple_configs(
        self,
        config_manager: ConfigManager,
        sample_yaml_config: str,
        sample_json_config: str,
        sample_ini_config: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test loading multiple configuration files.

        This function tests the ability of the `ConfigManager` to load configurations from
        YAML, JSON, and INI files while ensuring that the values are correctly retrieved
        from the different sources. It uses the `monkeypatch` fixture to set the environment
        variable for the application environment to "testing".

        Args:
            config_manager (ConfigManager): The configuration manager instance to test.
            sample_yaml_config (str): Path to the sample YAML configuration file.
            sample_json_config (str): Path to the sample JSON configuration file.
            sample_ini_config (str): Path to the sample INI configuration file.
            monkeypatch (pytest.MonkeyPatch): The pytest monkeypatch fixture for modifying
                environment variables.

        Returns:
            None: This function does not return a value. It asserts the expected values
            from the loaded configurations.
        """
        monkeypatch.setenv("APP_ENV", "testing")

        config_manager.load_config(
            yaml_file="config.yaml",
            json_file="config.json",
            ini_file="config.ini",
            env_prefix="APP_",
        )

        assert config_manager.get("database")["host"] == "localhost"
        assert config_manager.get("api_key") == "test-key-123"
        assert config_manager.get("server")["port"] == "8000"
        assert config_manager.get("APP_ENV") == "testing"

    def test_get_with_default(self, config_manager: ConfigManager) -> None:
        """Test the behavior of the `get` method in `ConfigManager` when a non-existent key is requested.

        Args:
            config_manager (ConfigManager): An instance of the ConfigManager to be tested.

        Returns:
            None

        Asserts:
            The method should return the default value when the specified key does not exist in the configuration.
        """
        assert config_manager.get("non_existent_key", "default") == "default"

    def test_set_config_value(self, config_manager: ConfigManager) -> None:
        """Test the configuration manager's ability to set and retrieve a configuration value.

        Args:
            config_manager (ConfigManager): The configuration manager instance to test.

        Returns:
            None

        Raises:
            AssertionError: If the value retrieved from the configuration manager does not match the expected value.
        """
        config_manager.set("new_key", "new_value")
        assert config_manager.get("new_key") == "new_value"

    def test_save_config_yaml(
        self, config_manager: ConfigManager, temp_config_dir: str
    ) -> None:
        """Test the saving of configuration to a YAML file.

        This test verifies that the configuration manager correctly saves a given
        configuration dictionary to a YAML file and that the saved file matches
        the original configuration.

        Args:
            config_manager (ConfigManager): The configuration manager instance
                used to save the configuration.
            temp_config_dir (str): The temporary directory where the output YAML
                file will be saved.

        Returns:
            None

        Raises:
            AssertionError: If the saved configuration does not match the original
            configuration.
        """
        test_config = {"test": "value", "nested": {"key": "value"}}
        config_manager.config = test_config

        config_manager.save_config("output.yaml", format="yaml")

        with open(os.path.join(temp_config_dir, "output.yaml"), "r") as f:
            saved_config = yaml.safe_load(f)

        assert saved_config == test_config

    def test_save_config_json(
        self, config_manager: ConfigManager, temp_config_dir: str
    ) -> None:
        """Test the saving of configuration to a JSON file.

        This function tests the `save_config` method of the `ConfigManager` class by
        saving a sample configuration to a JSON file and verifying that the contents
        of the saved file match the original configuration.

        Args:
            config_manager (ConfigManager): An instance of the ConfigManager used to
                manage configuration settings.
            temp_config_dir (str): The temporary directory where the output JSON file
                will be saved.

        Returns:
            None
        """
        test_config = {"test": "value", "nested": {"key": "value"}}
        config_manager.config = test_config

        config_manager.save_config("output.json", format="json")

        with open(os.path.join(temp_config_dir, "output.json"), "r") as f:
            saved_config = json.load(f)

        assert saved_config == test_config

    def test_invalid_yaml_file(
        self, config_manager: ConfigManager, temp_config_dir: str
    ) -> None:
        """Test case for handling an invalid YAML file.

        This function creates a temporary invalid YAML file and verifies that
        loading it with the ConfigManager raises an exception.

        Args:
            config_manager (ConfigManager): The configuration manager instance
                used to load the YAML file.
            temp_config_dir (str): The directory path where the temporary
                configuration file is stored.

        Raises:
            Exception: An exception is expected to be raised when attempting
            to load the invalid YAML file.
        """
        invalid_yaml = """
        key: value
        - invalid
            yaml: content
        """

        filepath = os.path.join(temp_config_dir, "invalid.yaml")
        with open(filepath, "w") as f:
            f.write(invalid_yaml)

        with pytest.raises(Exception):
            config_manager.load_yaml("invalid.yaml")

    def test_invalid_config_format(self, config_manager: ConfigManager) -> None:
        """Test that saving a configuration with an invalid format raises a ValueError.

        Args:
            config_manager (ConfigManager): The configuration manager instance used to save the configuration.

        Raises:
            ValueError: If the format provided to save_config is invalid.
        """
        with pytest.raises(ValueError):
            config_manager.save_config("config.txt", format="txt")

    def test_missing_config_file(self, config_manager: ConfigManager) -> None:
        """Test that loading a non-existent YAML configuration file raises an exception.

        Args:
            config_manager (ConfigManager): The configuration manager instance used to load the YAML file.

        Raises:
            Exception: If the specified YAML file does not exist, an exception is expected to be raised.
        """
        with pytest.raises(Exception):
            config_manager.load_yaml("non_existent.yaml")
