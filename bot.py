from telethon import TelegramClient, events
import http.server
import threading

api_id = 36243984        
api_hash = '5949e0514972286d56099e0bc5fdd045'  

# --- RENDER XATOLIGINI OLISH UCHUN SOXTA PORT OCHISH ---
def run_dummy_server():
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot is running successfully!")

    server = http.server.HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


# --- TELEGRAM BOT ASOSIY QISMI ---
AUTO_REPLY_TEXT = """👋 Salom! Men Shuxratning shaxsiy botiman. 

👨‍💻 Hozir Shuxrat biroz Of-line yoki bandroq. Xabaringizni yozib qoldiring! 🚀"""

replied_users = set()

client = TelegramClient('shuxrat_session', api_id, api_hash)

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

print("Aqlli bot ishga tushdi...")
client.start()
client.run_until_disconnected()
