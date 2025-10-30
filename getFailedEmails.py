import imaplib
import email
import re
from email.header import decode_header

# --- USER CONFIGURATION ---
# Enter your Gmail address and the 16-digit App Password you generated.
# IMPORTANT: Do NOT use your regular Gmail password.
EMAIL = "madhur.ahlawat17@gmail.com"
APP_PASSWORD = "ghat dpaz iyps nztm"
# --- END OF CONFIGURATION ---

# Gmail IMAP server
IMAP_SERVER = "imap.gmail.com"

def get_failed_emails():
    """
    Connects to Gmail, searches for bounced emails, extracts the failed
    email addresses, and returns them as a list.
    """
    failed_emails = set() # Using a set to automatically handle duplicates

    # Regex to find email addresses. It's flexible and works in most cases.
    email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    imap = None # Initialize imap to None
    try:
        # Connect to the server over SSL
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)

        # Login using your email and the App Password
        imap.login(EMAIL, APP_PASSWORD)

        # Select the mailbox you want to check (e.g., "INBOX")
        imap.select("INBOX")

        # Search for emails from mailer-daemon that indicate a hard bounce
        # This query is more robust and checks the body for common failure text.
        search_query = '(FROM "mailer-daemon@googlemail.com" BODY "Address not found")'
        status, messages = imap.search(None, search_query)

        if status != "OK":
            print("No messages found!")
            return []

        # Get a list of email IDs
        email_ids = messages[0].split()

        print(f"Found {len(email_ids)} bounced emails. Processing...")

        # Loop through each email
        for email_id in email_ids:
            # Fetch the email by ID
            status, msg_data = imap.fetch(email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the email content
                    msg = email.message_from_bytes(response_part[1])

                    # Look for the plain text body
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode()
                                    # Find the first email address in the body
                                    match = email_regex.search(body)
                                    if match:
                                        failed_emails.add(match.group(0))
                                        break # Move to the next email once found
                                except:
                                    continue
                    else:
                        # Not a multipart email, just get the payload
                        try:
                            body = msg.get_payload(decode=True).decode()
                            match = email_regex.search(body)
                            if match:
                                failed_emails.add(match.group(0))
                        except:
                            continue

        return list(failed_emails)

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        # Gracefully close the connection
        if imap:
            imap.close()
            imap.logout()
            print("Connection closed.")