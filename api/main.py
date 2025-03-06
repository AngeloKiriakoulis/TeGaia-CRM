import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
# Fix import for utils (add to sys.path if needed)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.agent import EmailAgent

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not EMAIL_USER or not EMAIL_PASS:
    raise ValueError("Missing SMTP credentials! Check your .env file.")

# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tegaia-crm.vercel.app"],  # Change this if deployed
    # allow_origins=["*"],  # Change this if deployed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Define request schema
class ContactForm(BaseModel):
    name: str
    number: str
    email: EmailStr
    company: str
    message: str

# Email sending function
def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Send email via SMTP
        with smtplib.SMTP("mail.tegaia.gr", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return True
    except Exception as e:
        print("Email sending error:", e)
        return False

# API route to handle form submissions
@app.post("/api/contact")
async def contact_form(data: ContactForm):
    try:
        # Send the AI-generated email
        email_sent = send_email(
            to_email=data.email,
            subject="Collaboration with TeGaia!",
            body = EmailAgent(data.company, data.message).run()
        )

        if email_sent:
            return {"success": "Email successfully sent!"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred on the server.")