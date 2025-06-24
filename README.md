จุดประสงค์ของ AI Agent นี้คือการอัปเดตข่าวสาร BBC Thai โดยแท็ก <Item> จะถูกค้นหาจากการดึงข้อมูลโดยใช้ RSS (XML) ที่แปลงด้วย BeautifulSoup จากนั้นจะดึงหัวข้อ <title> และคำอธิบาย <description> 
เมื่อได้ข้อมูลมาแล้วต่อไป AI ของ Cohere จะทำการสรุปข่าวสาร และใช้ SMTP Gmail เพื่อส่งข้อมูลที่สรุปแล้วไปยังอีเมล

The purpose of this AI agent is to update BBC Thai news. The <Item> tag will be found by pulling data using RSS (XML) transformed with BeautifulSoup. The topic <title> and description <description> 
will then be pulled. Following that, it will use AI Cohere to summarize the news and use SMTP Gmail to send the condensed data to an email.


pip install requests beautifulsoup4 cohere lxml
