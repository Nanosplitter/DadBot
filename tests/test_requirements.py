import pytest

def test_requirements_file_exists():
    try:
        with open("requirements.txt") as file:
            requirements = file.readlines()
    except FileNotFoundError:
        pytest.fail("requirements.txt file not found")

def test_requirements_file_format():
    with open("requirements.txt") as file:
        requirements = file.readlines()
        for requirement in requirements:
            assert "==" in requirement, f"Invalid format in requirements.txt: {requirement}"

def test_requirements_file_content():
    with open("requirements.txt") as file:
        requirements = file.readlines()
        required_packages = ["aiohttp", "asyncio", "nextcord", "pyyaml", "pandas", "mysql-connector", "dateparser", "pytz", "requests", "aiofiles", "inspiro", "trafilatura", "scikit-learn", "nltk", "schedule", "apscheduler", "uwuify", "autocorrect", "cmudict", "contractions", "language-tool-python", "colour", "geopy", "Nominatim", "haversine", "syllapy", "openai", "akinator.py", "pyshorteners", "moviepy", "aiomysql", "peewee", "matplotlib", "pdfminer.six"]
        for package in required_packages:
            assert any(package in requirement for requirement in requirements), f"Missing required package: {package}"
