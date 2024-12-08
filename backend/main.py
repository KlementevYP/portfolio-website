from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
from babel.dates import format_date

app = FastAPI()
templates = Jinja2Templates(directory='../templates/')
app.mount('/static', StaticFiles(directory='../assets'), name='static')

def format_date_ru(value: date, format: str = "long"):
    """Форматирует дату на русском"""
    return format_date(value, format=format, locale='ru_RU')

templates.env.filters['date'] = format_date_ru  # Регистрация фильтра


@app.get('/')
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.post("/contact")
async def handle_contact_form(
    fullname: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Настройки SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "klementev712@gmail.com"
    smtp_password = "noxj kwcw jeby lxnc"

    # Создание сообщения
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = "klementev712@gmail.com"  # Ваш email
    msg["Subject"] = "Новое сообщение с сайта-портфолио"

    body = f"Имя: {fullname}\nEmail: {email}\nСообщение:\n{message}"
    msg.attach(MIMEText(body, "plain"))

    # Отправка письма
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/", status_code=303)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)