import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()

CONTACT_RECIPIENT = os.getenv("CONTACT_RECIPIENT")

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://vionario.com",
        "https://www.vionario.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    company: str | None = None
    phone: str | None = None
    service: str
    message: str


@app.get("/")
def home():
    return {"message": "Vionario backend is running"}

def send_contact_email(form):
    email = EmailMessage()

    email["Subject"] = f"New Vionario Inquiry — {form.name}"
    email["From"] = SMTP_EMAIL
    email["To"] = CONTACT_RECIPIENT
    email["Reply-To"] = form.email

    email.set_content(
        f"""
        New inquiry received from the Vionario website.

        Name: {form.name}
        Email: {form.email}
        Company: {form.company or "Not provided"}
        Phone: {form.phone or "Not provided"}
        Service: {form.service}

        Message:
        {form.message}
        """
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
        smtp.send_message(email)

@app.post("/contact")
def receive_contact(form: ContactForm):
    try:
        send_contact_email(form)

    except Exception as error:
        print("Email sending failed:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to send inquiry"
        )

    return {
        "success": True,
        "message": "Inquiry received"
    }