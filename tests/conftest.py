import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)
    return TestClient(app_module.app)
