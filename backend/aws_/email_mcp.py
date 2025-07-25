
import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from mcp.server import FastMCP

mcp = FastMCP("Email server", port=8001)


load_dotenv()
AWS_SES_REGION = os.getenv("AWS_SES_REGION")
AWS_SES_SECRET_ACCESS_KEY = os.getenv("AWS_SES_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_SES_ACCESS_KEY_ID")

print(AWS_ACCESS_KEY_ID)
print(AWS_SES_REGION)
print(AWS_SES_SECRET_ACCESS_KEY)


@mcp.tool(description="Send email with html and text body, to recipient from sender with subject. Returns message id")
def send_email(message_html: str, message_text: str, recipient: str = "", sender: str = "", subject: str = "") -> str:
    # ---- Configuration ----
    SENDER = "michael@quantoflow.com"
    RECIPIENT = "michael@quantoflow.com"
    SUBJECT = subject
    HTML_BODY = message_html
    TEXT_BODY = message_text

    # ---- Build Email ----
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    # Alternative part (text + HTML)
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(MIMEText(TEXT_BODY, 'plain'))
    msg_body.attach(MIMEText(HTML_BODY, 'html'))

    # Attach the body to the main message
    msg.attach(msg_body)

    # ---- Attachment ----
    """ 
  ATTACHMENT_PATH = "CRM.xlsx"  # Change this to your file path

     with open(ATTACHMENT_PATH, 'rb') as f:
      part = MIMEApplication(f.read())
      part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ATTACHMENT_PATH))
      msg.attach(part) """

    # ---- Send via SES ----
    client = boto3.client('ses', region_name=AWS_SES_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SES_SECRET_ACCESS_KEY,
                          )

    response = client.send_raw_email(
        Source=SENDER,
        Destinations=[RECIPIENT],
        RawMessage={
            'Data': msg.as_string()
        }
    )

    message_id = response["MessageId"]

    print("Email sent! Message ID:", message_id)
    return message_id


mcp.run(transport="streamable-http")
