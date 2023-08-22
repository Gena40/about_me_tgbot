"""Tests for bot main module."""
import os
# from unittest.mock import patch
import pytest
# from http import HTTPStatus
# import requests
# import telegram
# import utils
import main

# pylint: disable=missing-function-docstring


def test_check_token(monkeypatch):
    assert main.check_token() is True, 'Missing TELEGRAM_TOKEN env'

    with monkeypatch.delenv("TELEGRAM_TOKEN") as m:
        assert main.check_token() is False, os.getenv('TELEGRAM_TOKEN')
