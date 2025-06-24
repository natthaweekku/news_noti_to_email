#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
สคริปต์ทดสอบ BBC Thai News Bot
รันด้วยคำสั่ง: python test.py
"""

import os

def setup_environment():
    """ตั้งค่า environment variables สำหรับทดสอบ"""
    print("🔧 กำลังตั้งค่า environment variables...")

    # *** แก้ไขข้อมูลเหล่านี้ให้เป็นของจริง ***
    test_config = {
         "COHERE_API_KEY": "1sWtnnpdI9U6uE9Kl59QoLbB43jMI8jCvK58NFoc",        # ✅ ใส่ Cohere API Key ที่นี่
        "EMAIL_SENDER": "pes.sofree01@gmail.com",             # Gmail ของคุณ
        "EMAIL_RECEIVER": "pee.tep2545@gmail.com",            # อีเมลผู้รับ
        "EMAIL_PASSWORD": "molcxbsosjtjpzhu"                  # Gmail App Password
    }

    # ตรวจสอบว่าแก้ไขแล้วหรือยัง
    if any("your-" in value or "example" in value for value in test_config.values()):
        print("❌ กรุณาแก้ไขข้อมูลในไฟล์ test.py ก่อน!")
        print("📝 แก้ไขบรรทัดใน test_config ให้เป็นข้อมูลจริงของคุณ")
        print("\n📚 วิธีการขอ API Key และรหัสผ่าน:")
        print("🔑 Cohere API Key: https://dashboard.cohere.com/api-keys")
        print("📧 Gmail App Password: https://myaccount.google.com/security (เปิด 2FA ก่อน)")
        return False

    # ตั้งค่า environment variables
    for key, value in test_config.items():
        os.environ[key] = value

    print("✅ ตั้งค่า environment variables เรียบร้อย")
    return True

def test_imports():
    """ทดสอบการ import modules"""
    print("\n📦 ทดสอบการ import modules...")

    try:
        import requests
        import bs4
        import cohere
        print("✅ Import modules สำเร็จ")
        return True
    except ImportError as e:
        print(f"❌ Import ไม่สำเร็จ: {e}")
        print("💡 รันคำสั่ง: pip install requests beautifulsoup4 cohere lxml")
        return False

def run_test():
    """รันการทดสอบหลัก"""
    print("\n🧪 เริ่มการทดสอบ BBC Thai News Bot...")

    try:
        from news_noti import main  

        print("🚀 รันโปรแกรมหลัก...")
        main()

        print("\n🎉 การทดสอบสำเร็จ!")
        print("📧 ตรวจสอบอีเมลของคุณเพื่อดูรายงาน")

    except Exception as e:
        print(f"\n❌ การทดสอบไม่สำเร็จ: {str(e)}")
        print("\n🔍 วิธีแก้ไขปัญหาทั่วไป:")
        print("1. ตรวจสอบ Cohere API Key ว่าถูกต้อง")
        print("2. ตรวจสอบ Gmail App Password")
        print("3. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
        return False

    return True

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 BBC Thai News Bot - การทดสอบ")
    print("=" * 60)

    steps = [
        ("ตั้งค่า Environment", setup_environment),
        ("ทดสอบ Import Modules", test_imports),
        ("รันการทดสอบหลัก", run_test)
    ]

    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"\n💥 หยุดการทดสอบที่ขั้นตอน: {step_name}")
            return

    print("\n" + "=" * 60)
    print("🎊 การทดสอบทั้งหมดเสร็จสิ้น!")
    print("📱 หากต้องการรันทุกวันอัตโนมัติ ให้อัปโหลดไปยัง GitHub หรือใช้ cron")

if __name__ == "__main__":
    main()