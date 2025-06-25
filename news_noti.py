import os
import requests
import smtplib
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cohere import Client

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ตั้งค่า Cohere API
client = Client(os.getenv("COHERE_API_KEY"))

def fetch_bbc_thai_rss():
    """ดึงข่าวจาก BBC Thai RSS"""
    url = "https://feeds.bbci.co.uk/thai/rss.xml"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")

        headlines = []
        for item in items[:3]:  
            title = item.title.get_text(strip=True)
            description = item.description.get_text(strip=True)
            headlines.append(f"{title} - {description}")
        return headlines
    except Exception as e:
        logger.error(f"Error fetching from BBC RSS: {str(e)}")
        return []

def summarize_news(headlines_list):
    if not headlines_list:
        return "ไม่มีข่าวที่จะสรุปในวันนี้"

    news_text = "\n".join(headlines_list)

    try:
        response = client.chat(
            model="command-r-plus",
            message=f"""ข่าววันนี้:
{news_text}

กรุณาสรุปประเด็นข่าวเหล่านี้ในรูปแบบรายงานรายวัน เป็นภาษาไทย:
1. หัวข้อของข่าว
2. สรุปประเด็นสำคัญ (3ข้อ)
3. ผลกระทบต่อตลาด/สังคม
4. อิงเว็บไซต์ที่มา

ภาษากระชับ ชัดเจน และเป็นกันเอง"""
        )

        return response.text.strip()

    except Exception as e:
        logger.error(f"Error in Cohere Chat API: {str(e)}")
        return f"❌ ไม่สามารถสรุปข่าวได้: {str(e)}\n\nข่าวดิบ:\n{news_text}"


def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = os.getenv("EMAIL_SENDER")
        msg["To"] = os.getenv("EMAIL_RECEIVER")

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">📰 สรุปข่าวรายวันจาก BBC Thai</h2>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{body}</pre>
                </div>
                <hr>
                <p style="color: #6c757d; font-size: 12px;">
                     สร้างเมื่อ: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} (เวลาไทย)<br>
                    AI Agent News Summarizer By Natthawee
                </p>
                
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(
                os.getenv("EMAIL_SENDER"),
                [os.getenv("EMAIL_RECEIVER")],
                msg.as_string()
            )

        logger.info("ส่งอีเมลสำเร็จ")

    except Exception as e:
        logger.error(f"ไม่สามารถส่งอีเมลได้: {str(e)}")
        raise

def main():
    try:
        logger.info("🚀 เริ่มต้นการทำงาน BBC Thai News Bot")

        required_env = ["COHERE_API_KEY", "EMAIL_SENDER", "EMAIL_RECEIVER", "EMAIL_PASSWORD"]
        missing_env = [env for env in required_env if not os.getenv(env)]

        if missing_env:
            raise ValueError(f"ขาด environment variables: {', '.join(missing_env)}")

        logger.info("📰 กำลังดึงข่าวจาก BBC Thai...")
        headlines = fetch_bbc_thai_rss()

        if not headlines:
            logger.warning("ไม่พบข่าวจาก BBC RSS")
            headlines = ["ไม่สามารถดึงข่าวได้ในวันนี้"]

        logger.info(f"📊 พบข่าว {len(headlines)} ข่าว")
        logger.info("🤖 กำลังสรุปข่าวด้วย AI...")
        summary = summarize_news(headlines)

        subject = f"📰 สรุปข่าว BBC Thai - {datetime.now().strftime('%d/%m/%Y')}"
        logger.info("📧 กำลังส่งอีเมล...")
        send_email(subject, summary)
        logger.info("✅ ส่งรายงานสำเร็จ")

    except Exception as e:
        error_msg = f"❌ เกิดข้อผิดพลาด: {str(e)}"
        logger.error(error_msg)
        try:
            send_email("🚨 BBC Thai Bot - Error Report", error_msg)
        except:
            pass

if __name__ == "__main__":
    main()