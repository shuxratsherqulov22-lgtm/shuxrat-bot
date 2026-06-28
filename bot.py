from telethon import TelegramClient, events
import http.server
import threading
import os

# --- TELEGRAM API MA'LUMOTLARI ---
api_id = 36243984        
api_hash = '5949e0514972286d56099e0bc5fdd045'  

# --- RENDER PORT XATOSINI YO'QOTISH UCHUN SERVER ---
def run_dummy_server():
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Userbot is active!")

    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


# --- SHAXSIY LICHKA UCHUN AVTO-JAVOB MATNI ---
AUTO_REPLY_TEXT = """👋 Salom! Hozir Shuxrat hozir biroz bandroq yoki oflayn.

Xabaringizni yoki stikeringizni qoldiring, telegramga kirishi bilan srazu javob beradi! 🚀"""

# Har bir odamga faqat 1 marta javob qaytarish uchun
replied_users = set()

# MUTLAQO YANGI SESSIYA NOMI (Sizning shaxsiy profilingiz ulanadi)
client = TelegramClient('shuxrat_lichka_session_v9', api_id, api_hash)

# --- FAQAT SHAXSIY LICHKADAGI KIRUVCHI XABARLAR UCHUN (Matn, Stiker va h.k.) ---
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    # Faqat shaxsiy xabarlarga (lichkaga) javob beradi, guruh va kanallarga emas
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot: # Agar yozgan odam bot bo'lmasa
            user_id = sender.id
            if user_id not in replied_users:
                replied_users.add(user_id)
                # respond() o'rniga reply() ishlatildi - bu xabarga javob qilib yuboradi
                await event.reply(AUTO_REPLY_TEXT)
                print(f"[{sender.first_name}] ga shaxsiy lichkada avto-javob ketdi.")

print("Shaxsiy yordamchi ishga tushmoqda...")
client.start()
client.run_until_disconnected()
