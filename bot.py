# Ultimate TXT → Video Uploader Bot with Full Admin Authorization
import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WATERMARK_TEXT = "👑 Bot by King"

app = Client("txt-video-bot", bot_token=BOT_TOKEN)
scheduler = AsyncIOScheduler()
scheduler.start()

BATCH_MODE = {}  # user_id: {channels, thumb, count, active}

def is_admin(user_id):
    return user_id == ADMIN_ID

def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Upload TXT", callback_data="upload"),
         InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("🛑 Stop Batch", callback_data="stop"),
         InlineKeyboardButton("⏰ Schedule Batch", callback_data="schedule")],
        [InlineKeyboardButton("🖼 Set Thumbnail", callback_data="thumbnail"),
         InlineKeyboardButton("📢 Set Channel", callback_data="channel")]
    ])

@app.on_message(filters.private)
async def all_messages(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("❌ Access Denied
You are not authorized to use this bot.")
        return
    await message.reply("✅ You are authorized. Use buttons below.", reply_markup=main_buttons())

@app.on_callback_query()
async def callbacks(client, callback):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access Denied", show_alert=True)
        return
    data = callback.data
    if data == "upload":
        await callback.message.edit("📤 Send TXT file now...")
    elif data == "help":
        await callback.message.edit("ℹ️ Help Menu: Only admin can use bot.
👑 Bot by King")
    elif data == "stop":
        await callback.message.edit("🛑 Stop batch command received.")
    elif data == "schedule":
        await callback.message.edit("⏰ Send schedule time (YYYY-MM-DD HH:MM) or 'now'.")
    elif data == "thumbnail":
        await callback.message.edit("🖼 Send new thumbnail or type 'no' to skip.")
    elif data == "channel":
        await callback.message.edit("📢 Send channel IDs / usernames (comma separated).")

print("🤖 Ultimate TXT → Video Bot (Admin Version) Started | 👑 Bot by King")
app.run()
