import asyncio
from telegram import Bot
from telegram.error import TelegramError
from telethon import TelegramClient, events
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# تنظیمات
TOKEN = "YOUR_BOT_TOKEN"  # از @BotFather
API_ID = "YOUR_API_ID"    # از my.telegram.org
API_HASH = "YOUR_API_HASH"
CHANNEL_ID = "@YOUR_CHANNEL"  # مثال: "@English_Learning_Channel"

# کلاینت‌ها
telegram_bot = Bot(token=TOKEN)
telethon_client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=TOKEN)

# تابع ارسال پست به کانال (با python-telegram-bot)
async def send_post_to_channel(text):
    try:
        await telegram_bot.send_message(chat_id=CHANNEL_ID, text=text)
        print(f"✅ پست ارسال شد: {text[:30]}...")
    except TelegramError as e:
        print(f"❌ خطا در ارسال پست: {e}")

# تابع دعوت کاربر به کانال (با telethon)
async def invite_user_to_channel(user_id):
    try:
        await telethon_client.edit_admin(
            entity=CHANNEL_ID,
            user=user_id,
            invite_users=True  # دسترسی دعوت کاربران
        )
        print(f"✅ کاربر {user_id} دعوت شد.")
    except Exception as e:
        print(f"❌ خطا در دعوت کاربر: {e}")

# تابع زمان‌بندی شده برای ارسال خودکار درس‌ها
async def scheduled_english_lesson():
    lessons = [
        "📚 درس امروز: زمان حال ساده (Present Simple)",
        "📚 درس امروز: افعال بی‌قاعده (Irregular Verbs)",
        "📚 درس امروز: اصطلاحات روزمره (Daily Phrases)"
    ]
    for lesson in lessons:
        await send_post_to_channel(lesson)
        await asyncio.sleep(86400)  # هر ۲۴ ساعت یک درس جدید

# هندلر برای دستور /start (اختیاری)
@telethon_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply("🤖 به ربات آموزش انگلیسی خوش آمدید!")

# راه‌اندازی ربات
async def main():
    # زمان‌بندی ارسال خودکار درس‌ها
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_english_lesson, 'interval', days=1)
    scheduler.start()

    # شروع تلثون کلاینت
    await telethon_client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())