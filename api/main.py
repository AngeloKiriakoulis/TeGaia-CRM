import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
# from transformers import pipeline

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
# HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL")
# HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tegaia-crm.vercel.app"],  # Change this if deployed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load Hugging Face model for text generation
# generator = pipeline("text-generation", model=HUGGINGFACE_MODEL,token=HUGGINGFACE_TOKEN)

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
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
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
#         messages = [
#     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
#     {"role": "user", "content": "Who are you?"},
# ]
#         ai_response = generator(messages)

        # Send the AI-generated email
        email_sent = send_email(
            to_email=data.email,
            subject="Collaboration with TeGaia!",
            body="HI!"
        )
        print(email_sent)

    #     if email_sent:
    #         return {"success": "Email successfully sent!"}
    #     else:
    #         raise HTTPException(status_code=500, detail="Failed to send email")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # Simulate the email sending or any other backend operation
        print(f"Received contact form data: {data}")
        # Return a success message
        return {"success": "Form submitted successfully!"}
    except Exception as e:
        print(f"Error: {e}")
        return {"detail": "An error occurred on the server."}
