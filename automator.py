#========================================================================
#project: News Email Automator
#purpose: Fetch banking news and send it via email daily
#relevance: learning Automation and API integration
#========================================================================

#---SECTION 1: IMPORTING LIBRARIES---
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import requests
#---SECTION 2: LOAD SECRET KEYS FROM .env---
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
#---SEFETY CHECK: ENSURE KEYS ARE LOADED---
if not NEWS_API_KEY or not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("Error: Missing environment variables. Please check your .env file.")
else:
    print("Environment variables loaded successfully!")
#---SECTION 3: FUNCTION TO FETCH BANKING NEWS---
def fetch_banking_news():
    url = "https://newsapi.org/v2/everything"
    parameters = {
        "q": "ING bank OR fintech OR banking technology",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    if data.get("status") == "ok":
        return data.get("articles", [])
    else:
        print("Error fetching news:", data.get("message"))
        return []
#---SECTION 4: FORMAT EMAIL CONTENT---
def format_email_content(articles):
    email_body = """
    <html>
    <body>
    <h2 style="color: #FF6200;">">🏦 Daily Banking & Fintech News</h2>
    <p>Here are today's top stories relevant to ING and the wider financial technology sector:</p>
    <hr>
    """
    for article in articles:
        email_body += f"""
         <h3><a href="{article['url']}">{article['title']}</a></h3>
        <p><strong>Source:</strong> {article['source']['name']}</p>
        <p>{article['description']}</p>
        <hr>
        """
    email_body += """
   </body>
    </html>
    """

    return email_body
#---SECTION 5: FUNCTION TO SEND EMAIL---
def send_email(email_body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🏦 Your Daily Banking & Fintech News"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    
    part = MIMEText(email_body, 'html')
    msg.attach(part)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        print("✅ Email sent successfully!")
#---SECTION 6: MAIN FUNCTION TO RUN THE AUTOMATOR---
print("🚀 Fetching latest banking and fintech news...")

articles = fetch_banking_news()

if articles:
    print(f"✅ Found {len(articles)} articles!")
    email_body = format_email_content(articles)
    send_email(email_body)
else:
    print("❌ No articles found. Check your API key.")
