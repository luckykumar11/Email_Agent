import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.models.email_config import EmailConfiguration

logger = logging.getLogger(__name__)

# Import exception classes directly so they remain real even when smtplib is mocked in tests
SMTPAuthenticationError = smtplib.SMTPAuthenticationError
SMTPConnectError = smtplib.SMTPConnectError
SMTPServerDisconnected = smtplib.SMTPServerDisconnected
SMTPException = smtplib.SMTPException


def _get_password(config: EmailConfiguration) -> str:
    from app.core.security import decrypt_password
    return decrypt_password(config.encrypted_password)


def _send_via_smtp(
    security_type: str,
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    email_address: str,
    all_recipients: list[str],
    msg: MIMEMultipart,
) -> dict:
    refused: dict = {}
    if security_type == "SSL_TLS":
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=30) as server:
            server.login(username, password)
            refused = server.sendmail(email_address, all_recipients, msg.as_string())
    elif security_type == "STARTTLS":
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(username, password)
            refused = server.sendmail(email_address, all_recipients, msg.as_string())
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.login(username, password)
            refused = server.sendmail(email_address, all_recipients, msg.as_string())
    return refused


def send_smtp_email(
    config: EmailConfiguration,
    sender_name: str | None,
    reply_to: str | None,
    recipient: str,
    subject: str,
    body: str,
    format: str = "html",
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
) -> tuple[bool, str]:
    try:
        password = _get_password(config)
    except Exception as e:
        logger.error("Failed to decrypt SMTP password: %s", e)
        return False, f"Failed to decrypt SMTP password: {type(e).__name__}"

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{config.email_address}>" if sender_name else config.email_address
    msg["To"] = recipient
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    if cc:
        msg["Cc"] = ", ".join(cc)

    content_type = "html" if format.lower() == "html" else "plain"
    if content_type == "html":
        body = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        body = body.replace("\n\n", "</p><p>")
        body = body.replace("\n", "<br>")
        body = f"<p>{body}</p>"
    msg.attach(MIMEText(body, content_type))

    all_recipients = [recipient]
    if cc:
        all_recipients.extend(cc)
    if bcc:
        all_recipients.extend(bcc)

    try:
        refused = _send_via_smtp(
            security_type=config.security_type,
            smtp_host=config.smtp_host,
            smtp_port=config.smtp_port,
            username=config.username,
            password=password,
            email_address=config.email_address,
            all_recipients=all_recipients,
            msg=msg,
        )
        if refused:
            error_details = "; ".join(
                f"{addr}: {info}" for addr, info in refused.items()
            )
            logger.error("SMTP recipients refused: %s", error_details)
            return False, f"Recipients refused: {error_details}"
        return True, "Email sent successfully"
    except SMTPAuthenticationError:
        logger.error("SMTP auth failed for %s@%s", config.username, config.smtp_host)
        return False, "SMTP authentication failed - check username and password"
    except SMTPConnectError:
        logger.error("SMTP connect failed for %s:%s", config.smtp_host, config.smtp_port)
        return False, "Could not connect to SMTP server"
    except SMTPServerDisconnected:
        logger.error("SMTP disconnected for %s", config.smtp_host)
        return False, "SMTP server disconnected unexpectedly"
    except TimeoutError:
        logger.error("SMTP timeout for %s:%s", config.smtp_host, config.smtp_port)
        return False, "SMTP connection timed out"
    except OSError as e:
        logger.error("Network error connecting to %s:%s - %s", config.smtp_host, config.smtp_port, e)
        return False, f"Network error: {str(e)}"
    except SMTPException as e:
        logger.error("SMTP error: %s", e)
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        logger.error("Unexpected error sending email: %s: %s", type(e).__name__, e)
        return False, f"Unexpected error sending email: {type(e).__name__}: {str(e)}"


def verify_smtp_connection(
    config: EmailConfiguration,
    recipient: str,
) -> tuple[bool, str]:
    password = _get_password(config)

    try:
        if config.security_type == "SSL_TLS":
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, context=context, timeout=15) as server:
                server.login(config.username, password)
                test_msg = MIMEMultipart()
                test_msg["From"] = config.email_address
                test_msg["To"] = recipient
                test_msg["Subject"] = "SMTP Configuration Test"
                test_msg.attach(MIMEText("This is a test email to verify your SMTP configuration.", "plain"))
                server.sendmail(config.email_address, [recipient], test_msg.as_string())
        elif config.security_type == "STARTTLS":
            with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=15) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(config.username, password)
                test_msg = MIMEMultipart()
                test_msg["From"] = config.email_address
                test_msg["To"] = recipient
                test_msg["Subject"] = "SMTP Configuration Test"
                test_msg.attach(MIMEText("This is a test email to verify your SMTP configuration.", "plain"))
                server.sendmail(config.email_address, [recipient], test_msg.as_string())
        else:
            with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=15) as server:
                server.ehlo()
                server.login(config.username, password)
                test_msg = MIMEMultipart()
                test_msg["From"] = config.email_address
                test_msg["To"] = recipient
                test_msg["Subject"] = "SMTP Configuration Test"
                test_msg.attach(MIMEText("This is a test email to verify your SMTP configuration.", "plain"))
                server.sendmail(config.email_address, [recipient], test_msg.as_string())
        return True, "SMTP test successful - connection verified and test email sent"
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed - check username and password"
    except smtplib.SMTPConnectError:
        return False, "Could not connect to SMTP server - check host and port"
    except TimeoutError:
        return False, "SMTP connection timed out - check host and port settings"
    except OSError as e:
        return False, f"Network error: {str(e)}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error during SMTP test: {str(e)}"
