from telethon import TelegramClient, events
import asyncio

# my.telegram.org saytidan olingan ma'lumotlar kiritildi:
api_id = 36243984        
api_hash = '5949e0514972286d56099e0bc5fdd045'  

# Avto-javob matni (buni o'zingiz xohlagancha o'zgartirishingiz mumkin)
AUTO_REPLY_TEXT = """👋 Salom! Men Shuxratning shaxsiy botiman xush kelibsiz! ✨

👨‍💻 Hozir Shuxrat biroz band yoki oflayn. Xabaringizni yozib qoldiring, telegramga kirishi bilan sizga aloqaga chiqadi! 🚀"""

# Bot kimga javob berganini eslab qoladigan ro'yxat (xotira)
replied_users = set()

client = TelegramClient('shuxrat_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    # Faqat shaxsiy chatlar va faqat odamlar uchun (botlar va guruhlar hisobga olinmaydi)
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.bot:
            user_id = sender.id
            
            # Agar bu odamga hali bugun javob berilmagan bo'lsa
            if user_id not in replied_users:
                # Uni ro'yxatga qo'shamiz
                replied_users.add(user_id)
                
                await asyncio.sleep(2) # 2 soniya kutadi (haqiqiy odamdek ko'rinish uchun)
                await event.reply(AUTO_REPLY_TEXT)
                print(f"[{sender.first_name}] birinchi marta yozdi. Avto-javob yuborildi.")
            else:
                # Agar oldin yozgan bo'lsa, bot indamaydi
                print(f"[{sender.first_name}] yana yozdi, bot qayta javob bermadi.")

print("Aqlli bot ishga tushdi... Birinchi marta yozadiganlarni kutmoqda.")
client.start()
client.run_until_disconnected()