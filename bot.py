from telethon import TelegramClient, events
import http.server
import threading
import os

# --- TELEGRAM API MA'LUMOTLARI ---
api_id = 36243984        
api_hash = '5949e0514972286d56099e0bc5fdd045'  

# --- RENDER UCHUN SOXTA SERVER (PORT XATOSI BO'LMASLIGI UCHUN) ---
def run_dummy_server():
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot is active!")

    # Render beradigan portni avtomatik oladi
    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# Serverni alohida oqimda orqa fonda yoqamiz
threading.Thread(target=run_dummy_server, daemon=True).start()


# --- AVTO-JAVOB MATNI ---
AUTO_REPLY_TEXT = """👋 Salom! Men Shuxratning shaxsiy botiman. 

👨‍💻 Hozir Shuxrat biroz Of-line yoki bandroq. Xabaringizni yozib qoldiring! 🚀"""

# Har bitta odamga faqat 1 marta javob qaytarishi uchun ro'yxat
replied_users = set()

# YANGI UNIKAL SESSIYA NOMI (Blokirovkadan qutulish uchun)
client = TelegramClient('shuxrat_session', api_id, api_hash)

# --- XABARLARNI USHLASH (Matn, Stiker, Rasm, Ovozli xabar va h.k.) ---
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot:
            user_id = sender.id
            
            # Agar bu foydalanuvchiga hali javob berilmagan bo'lsa
            if user_id not in replied_users:
                replied_users.add(user_id)
                await event.reply(AUTO_REPLY_TEXT)
                print(f"[{sender.first_name}] ga avto-javob daxshat qilib yuborildi.")

print("Bot muvaffaqiyatli ishga tushdi...")
client.start()
client.run_until_disconnected()
