import pytest
import os

def test_dockerfile_exists():
    assert os.path.isfile("Dockerfile"), "Dockerfile does not exist"

def test_dockerfile_content():
    with open("Dockerfile", "r") as file:
        content = file.read()
        assert "FROM python:3.11-slim" in content, "Base image is not correct"
        assert "WORKDIR /app" in content, "WORKDIR is not set to /app"
        assert "COPY . /app" in content, "COPY command is not correct"
        assert "RUN pip install --no-cache-dir -r requirements.txt" in content, "RUN command to install requirements is not correct"
        assert "EXPOSE 80" in content, "EXPOSE command is not correct"
        assert 'ENV NAME DadBot' in content, "ENV command is not correct"
        assert 'CMD ["python", "bot.py"]' in content, "CMD command is not correct"
