"""Tests for bot main module."""
# pylint: disable=missing-function-docstring, import-outside-toplevel


def test_check_token_false():
    import main
    main.TELEGRAM_TOKEN = None

    assert main.check_token() is False


def test_check_token_true():
    import main
    main.TELEGRAM_TOKEN = '1234:abcdefg'

    assert main.check_token() is True
