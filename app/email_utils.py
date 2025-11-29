import os
password = os.getenv("EMAIL_PASSWORD")
username = os.getenv("EMAIL_USERNAME")
    
import imaplib
import email
from email.header import decode_header
import time
import sys
from email.utils import parsedate_to_datetime
from app.db_utils import insert_record, IncidentRecord
from app.api_utils import email_structure,get_email_attributes

# 2. Function to convert email date string to Database-friendly format (ISO 8601)
def parse_email_date(date_str):
    try:
        # parsedate_to_datetime handles formats like "Sat, 29 Nov 2025 11:27:00 +0530"
        dt_obj = parsedate_to_datetime(date_str)
        
        # Format the datetime object to a string
        # %Y = Year, %m = Month, %d = Day, %H = Hour (24h), %M = Minute, %S = Second
        formatted_date = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        
        return formatted_date
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None

def extract_email_name(from_str):
    import re

    match = re.match(r'(.*)<(.+)>', from_str)
    if match:
        name = match.group(1).strip()
        email = match.group(2).strip()

    return(name, email)


# --- CONFIGURATION ---
USERNAME = username
PASSWORD = password  # Use the 16-char App Password, NOT your real password
IMAP_URL = "imap.gmail.com"
CHECK_INTERVAL = 10 # Seconds between checks

# --- YOUR CUSTOM FUNCTION ---
def extract_info(email_data):
    """
    This function is triggered whenever a new email is received.
    email_data is a dictionary containing: 'subject', 'from', 'body'
    """
    print("\n>>> TRIGGERING EXTRACT_INFO FUNCTION <<<")
    
    # Example logic: Extract specific data or print it
    content = email_structure.format(subject=email_data['subject'],
                           body=email_data['body'])
    attributes = get_email_attributes(content)
    return attributes
    
    



# --- HELPER FUNCTIONS ---
def clean_header(text):
    """Decodes headers like Subject/From that might be encoded."""
    if not text: return ""
    return "".join(
        (c.decode(enc or "utf-8") if isinstance(c, bytes) else c)
        for c, enc in decode_header(text)
    )

def get_email_body(msg):
    """Extracts plain text body from the email object."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # Skip attachments
            if "attachment" in cdispo:
                continue
            
            # Prefer plain text, but you can also handle 'text/html'
            if ctype == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode()
                    break # Stop if we found the plain text part
                except:
                    pass
    else:
        # Not multipart
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            pass
    return body

# --- MAIN LISTENER ---
def start_listening():
    print(f"Connecting to {IMAP_URL} as {USERNAME}...")
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_URL)
        mail.login(USERNAME, PASSWORD)
        print("Login successful. Listening for new emails...")
        
        try:
            mail.select("INBOX")
            
            # Search for UNSEEN (Unread) emails
            status, messages = mail.search(None, "UNSEEN")
            
            if status == "OK":
                email_ids = messages[0].split()
                
                if email_ids:
                    print(f"New email(s) detected: {len(email_ids)}")
                    
                    for e_id in email_ids:
                        # Fetch the email
                        _, msg_data = mail.fetch(e_id, "(RFC822)")
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                name,email_address = extract_email_name(msg["From"])
                                # Prepare data for your function
                                email_content = {
                                    "subject": clean_header(msg["Subject"]),
                                    "from": email_address,
                                    "body": get_email_body(msg)}
                                
                                # --- EXECUTE Extract function ---
                                attributes =  extract_info(email_content)
                                print(attributes)
                                # -----------------------------
                                # --- Write to db---
                                inc = IncidentRecord(subject=email_content["subject"],
                                                     body=email_content["body"],
                                                     email=email_content["from"],
                                                     **attributes)
                                print("--->Writing to DB")
                                insert_record(inc)

                                # -----------------------------
                    
                else:
                    # Optional: print a dot to show it's alive
                    print("No new emails", end="", flush=True)

        except imaplib.IMAP4.error as e:
            print(f"IMAP Error: {e}. Reconnecting...")
                
    except KeyboardInterrupt:
        print("\nStopping script...")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        try:
            mail.close()
            mail.logout()
        except:
            pass
