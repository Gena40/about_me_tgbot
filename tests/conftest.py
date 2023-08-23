"""Conftest for tests."""
import sys
from os.path import abspath, dirname

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

# pytest_plugins = [
#     'tests.fixtures.fixture_data'
# ]
# import os
# import pytest
# from unittest import mock


# @pytest.fixture
# def mock_env(monkeypatch):
#     from main import check_token
#     def mock_env(*args, **kwargs):
#         pass
#     monkeypatch.setattr('')
