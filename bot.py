from telethon import TelegramClient, events
import http.server
import threading
import os

# --- TELEGRAM SIZNING MA'LUMOTLARINGIZ ---
api_id = 36243984        
api_hash = '5949e0514972286d56099e0bc5fdd045'  
BOT_TOKEN = '8864441897:AAFDg35dji_WoQi_qSmAOIoLiE_-qKDgzG4' # <- Bot tokeningizni yozing!

# --- RENDER PORT XATOSINI YO'QOTISH UCHUN SERVER ---
def run_dummy_server():
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot is active!")

    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


# --- BOTNING JAVOBI ---
AUTO_REPLY_TEXT = """👋 Salom! Men Shuxratning shaxsiy botiman. 

👨‍💻 Hozir Shuxrat biroz Of-line yoki bandroq. Xabaringizni yozib qoldiring! 🚀"""

# Har bir odamga faqat 1 marta javob berish uchun
replied_users = set()

# BOT_TOKEN orqali ulanish (Bu IP xatosini umuman bermaydi!)
client = TelegramClient('shuxrat_bot_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot:
            user_id = sender.id
            if user_id not in replied_users:
                replied_users.add(user_id)
                await event.reply(AUTO_REPLY_TEXT)
                print(f"[{sender.first_name}] ga avto-javob yuborildi.")

print("Bot ishga tushmoqda...")
# Bot token bilan start qilish
client.start(bot_token=8864441897:AAFDg35dji_WoQi_qSmAOIoLiE_-qKDgzG4)
client.run_until_disconnected()
