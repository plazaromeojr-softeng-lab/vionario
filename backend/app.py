import os

import resend
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()

CONTACT_RECIPIENT = os.getenv("CONTACT_RECIPIENT")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY


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


def send_contact_email(form: ContactForm):
    params: resend.Emails.SendParams = {
        "from": "Vionario Website <forms@vionario.com>",
        "to": [CONTACT_RECIPIENT],
        "subject": f"New Vionario Inquiry — {form.name}",
        "reply_to": form.email,
        "text": f"""
New inquiry received from the Vionario website.

Name: {form.name}
Email: {form.email}
Company: {form.company or "Not provided"}
Phone: {form.phone or "Not provided"}
Service: {form.service}

Message:
{form.message}
""",
    }

    resend.Emails.send(params)


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