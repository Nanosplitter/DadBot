import pytest
import yaml

def test_config_file_exists():
    try:
        with open("config.yaml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        pytest.fail("config.yaml file not found")

def test_config_file_format():
    with open("config.yaml") as file:
        try:
            config = yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            pytest.fail(f"Error in config.yaml file format: {exc}")

def test_config_file_content():
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        required_keys = ["bot_prefix", "token", "application_id", "dbhost", "dbuser", "dbpassword", "databasename", "owners", "blacklist", "main_color", "error", "success", "warning", "info", "maps_api_key", "imgflip_pass", "pipeline_token", "openapi_token"]
        for key in required_keys:
            assert key in config, f"Missing required key: {key}"
