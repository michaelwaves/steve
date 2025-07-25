import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from temporalio import activity
from sqlalchemy import create_engine, MetaData, select, func, or_
from sqlalchemy.orm import Session

load_dotenv()

@activity.defn
async def say_hello(name: str) -> str:
    return f'Hello, {name}!'

@activity.defn
async def send_email(message_html: str, message_text: str, recipient: str = "", sender: str = "", subject: str = "") -> str:
    """Send email with html and text body, to recipient from sender with subject. Returns message id"""
    
    AWS_SES_REGION = os.getenv("AWS_SES_REGION")
    AWS_SES_SECRET_ACCESS_KEY = os.getenv("AWS_SES_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_SES_ACCESS_KEY_ID")
    
    # ---- Configuration ----
    SENDER = sender if sender else "michael@quantoflow.com"
    RECIPIENT = recipient if recipient else "michael@quantoflow.com"
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
    return message_id

def fuzzy_search_sanctions(
    db: Session,
    first_name: str,
    last_name: str,
    max_distance: int = 2,
    limit: int = 10
):
    """
    Fuzzy search sanctions table by first and last name using Levenshtein distance.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        raise ValueError("Must set env variable DATABASE_URL for postgres")
    
    engine = create_engine(DATABASE_URL, echo=True)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    sanctions = metadata.tables["sanctions"]
    
    query = (
        select(sanctions)
        .where(
            or_(
                func.levenshtein(sanctions.c.firstName,
                                 first_name) <= max_distance,
                func.levenshtein(sanctions.c.lastName,
                                 last_name) <= max_distance
            )
        )
        .limit(limit)
    )
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

@activity.defn
async def search_sanctions(first_name: str, last_name: str):
    """Get top 10 sanctions results based on first_name last_name"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        raise ValueError("Must set env variable DATABASE_URL for postgres")
    
    engine = create_engine(DATABASE_URL, echo=True)
    
    with Session(engine) as session:
        results = fuzzy_search_sanctions(
            session, first_name=first_name, last_name=last_name)
    return results
