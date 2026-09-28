import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.models.email_config import EmailConfiguration
from app.services.email_config_service import _password_matches


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
    password_override: str | None = None,
) -> tuple[bool, str]:
    password = password_override or ""
    if not password_override:
        return False, "Password must be provided for SMTP sending"

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{config.email_address}>" if sender_name else config.email_address
    msg["To"] = recipient
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    if cc:
        msg["Cc"] = ", ".join(cc)

    content_type = "html" if format.lower() == "html" else "plain"
    msg.attach(MIMEText(body, content_type))

    all_recipients = [recipient]
    if cc:
        all_recipients.extend(cc)
    if bcc:
        all_recipients.extend(bcc)

    try:
        if config.security_type == "SSL_TLS":
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, context=context, timeout=30) as server:
                server.login(config.username, password)
                server.sendmail(config.email_address, all_recipients, msg.as_string())
        elif config.security_type == "STARTTLS":
            with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(config.username, password)
                server.sendmail(config.email_address, all_recipients, msg.as_string())
        else:
            with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as server:
                server.ehlo()
                server.login(config.username, password)
                server.sendmail(config.email_address, all_recipients, msg.as_string())
        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed - check username and password"
    except smtplib.SMTPConnectError:
        return False, "Could not connect to SMTP server"
    except smtplib.SMTPServerDisconnected:
        return False, "SMTP server disconnected unexpectedly"
    except TimeoutError:
        return False, "SMTP connection timed out"
    except OSError as e:
        return False, f"Network error: {str(e)}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"


def verify_smtp_connection(
    config: EmailConfiguration,
    recipient: str,
    password_override: str | None = None,
) -> tuple[bool, str]:
    password = password_override or ""
    if not password_override:
        return False, "Password must be provided for SMTP test"

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
