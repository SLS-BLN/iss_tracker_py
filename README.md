# ISS Overhead Notifier

A Python script that checks if the International Space Station (ISS) is currently passing over a specified location during hours of darkness and sends an email notification when it does.

---

## Features

- Fetches real-time ISS position from a public API  
- Retrieves local sunrise and sunset times to determine darkness  
- Checks if the ISS is within a configurable geographic range  
- Sends email alerts via Gmail SMTP when conditions are met  
- Configurable via environment variables  

---

## Prerequisites

- Python 3.9 or higher  
- A Gmail account with an app-specific password  
- Internet connectivity  

---

## Installation

1. Clone the repository:  
    git clone https://github.com/yourusername/iss-overhead-notifier.git  
    cd iss-overhead-notifier  
2. Create and activate a virtual environment:  
    python3 -m venv venv  
    source venv/bin/activate  
3. Install dependencies:  
    pip install -r requirements.txt  

---

## Configuration

Create a file named `.env` in the project root with these variables:

    EMAIL=your_email@gmail.com  
    APP_PASSWORD=your_gmail_app_password  
    SEND_TO=recipient_email@example.com  

- `EMAIL` – your Gmail address  
- `APP_PASSWORD` – the app-specific password you generated  
- `SEND_TO` – the email address to receive notifications  

---

## Usage

Run the script directly:

    python main.py

To automate every minute via cron (Unix-like):

    * * * * * cd /path/to/iss-overhead-notifier && /path/to/venv/bin/python main.py

---

## Project Structure

- `main.py`  
- `requirements.txt`  
- `.env`  
- `README.md`  

---

## Dependencies

| Package       | Purpose                                |
|---------------|----------------------------------------|
| requests      | HTTP requests to public APIs           |
| python-dotenv | Load environment variables from `.env` |
| smtplib       | Send email via SMTP (stdlib)           |

---

## License

This project is released under the MIT License.
