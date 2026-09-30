import pytest
from unittest.mock import patch, MagicMock
from app.services.smtp_service import send_smtp_email, verify_smtp_connection
from app.models.email_config import EmailConfiguration
from app.core.security import encrypt_password
from datetime import datetime, timezone


def make_config(password: str = "testpass") -> EmailConfiguration:
    return EmailConfiguration(
        id=1,
        company_id=1,
        email_address="sender@example.com",
        smtp_host="smtp.example.com",
        smtp_port=587,
        username="sender@example.com",
        encrypted_password=encrypt_password(password),
        security_type="STARTTLS",
        sender_name="Test",
        reply_to=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@patch("app.services.smtp_service.smtplib")
def test_send_email_success(mock_smtplib):
    config = make_config("password123")
    mock_server = MagicMock()
    mock_server.sendmail.return_value = {}
    mock_smtplib.SMTP.return_value.__enter__ = lambda s: mock_server
    mock_smtplib.SMTP.return_value.__exit__ = MagicMock(return_value=False)

    success, msg = send_smtp_email(
        config=config,
        sender_name="Test",
        reply_to=None,
        recipient="to@example.com",
        subject="Test",
        body="Hello",
    )
    assert success is True


@patch("app.services.smtp_service.smtplib")
def test_send_email_auth_failure(mock_smtplib):
    config = make_config("wrongpass")
    mock_smtplib.SMTPAuthenticationError = Exception
    mock_server = MagicMock()
    mock_server.login.side_effect = Exception("auth failed")
    mock_smtplib.SMTP.return_value.__enter__ = lambda s: mock_server
    mock_smtplib.SMTP.return_value.__exit__ = MagicMock(return_value=False)

    success, msg = send_smtp_email(
        config=config,
        sender_name="Test",
        reply_to=None,
        recipient="to@example.com",
        subject="Test",
        body="Hello",
    )


def test_send_email_decrypts_password():
    config = make_config("mypassword")
    with patch("app.services.smtp_service.smtplib") as mock_smtplib:
        mock_server = MagicMock()
        mock_server.sendmail.return_value = {}
        mock_smtplib.SMTP.return_value.__enter__ = lambda s: mock_server
        mock_smtplib.SMTP.return_value.__exit__ = MagicMock(return_value=False)

        success, msg = send_smtp_email(
            config=config,
            sender_name="Test",
            reply_to=None,
            recipient="to@example.com",
            subject="Test",
            body="Hello",
        )
        mock_server.login.assert_called_once_with("sender@example.com", "mypassword")


def test_verify_smtp_decrypts_password():
    config = make_config("securepass")
    with patch("app.services.smtp_service.smtplib") as mock_smtplib:
        mock_server = MagicMock()
        mock_smtplib.SMTP.return_value.__enter__ = lambda s: mock_server
        mock_smtplib.SMTP.return_value.__exit__ = MagicMock(return_value=False)

        success, msg = verify_smtp_connection(config, "test@example.com")
        mock_server.login.assert_called_once_with("sender@example.com", "securepass")


@patch("app.services.smtp_service.smtplib")
def test_verify_smtp_connection_success(mock_smtplib):
    config = make_config("pass")
    mock_server = MagicMock()
    mock_server.sendmail.return_value = {}
    mock_smtplib.SMTP.return_value.__enter__ = lambda s: mock_server
    mock_smtplib.SMTP.return_value.__exit__ = MagicMock(return_value=False)

    success, msg = verify_smtp_connection(config, "test@example.com")
    assert success is True
