"""
Unit tests for Task 1.1 (Password Validation).
"""

from security_utils import validate_password


def test_validate_password_positive() -> None:
    """
    Test positive scenario where password meets all requirements.

    Args: None
    Returns: None
    Raises: None
    """
    assert validate_password("Super_User_2026") is True


def test_validate_password_too_short() -> None:
    """
    Test password that is too short (less than 8 characters).

    Args: None
    Returns: None
    Raises: None
    """
    assert validate_password("Short1") is False


def test_validate_password_no_digits() -> None:
    """
    Test password that contains only letters (no digits).

    Args: None
    Returns: None
    Raises: None
    """
    assert validate_password("PasswordWithoutDigits") is False


def test_validate_password_forbidden_word() -> None:
    """
    Test passwords containing the forbidden word 'admin' in various cases.

    Args: None
    Returns: None
    Raises: None
    """
    assert validate_password("Admin12345") is False
    assert validate_password("root_admin_pass") is False
