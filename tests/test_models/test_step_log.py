import pytest
from models.step_log import StepLog
import datetime

@pytest.fixture
def step_log():
    return StepLog(
        server_id="123456789",
        user_id="987654321",
        steps=10000,
        submit_time=datetime.datetime(2022, 1, 1, 0, 0)
    )

def test_step_log_str(step_log):
    assert str(step_log) == "Server: 123456789, User: 987654321, Steps: 10000, Time: 2022-01-01 00:00:00"

def test_step_log_repr(step_log):
    assert repr(step_log) == "Server: 123456789, User: 987654321, Steps: 10000, Time: 2022-01-01 00:00:00"
