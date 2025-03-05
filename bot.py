import os
import asyncio
import requests
from bs4 import BeautifulSoup
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import cv2
import pytesseract

# Flask Server
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "✅ Advanced Image Tool Bot is Running!"

# Bot Credentials
API_ID = 26649585
API_HASH = "588a3ea6fd01ae88bd2e10fed7d55b2c"
BOT_TOKEN = "7023324101:AAEIe2IUtkiz9JXMylB-ndJ0HH1twsdFkk8"
LOG_CHANNEL = "-1002312610528"  # লগ চ্যানেল

app = Client("image_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔹 লগ পাঠানোর ফাংশন
async def log_to_channel(message):
    await app.send_message(LOG_CHANNEL, f"📢 {message}")

# 🔹 নতুন ইউজার এলে লগ পাঠাবে
@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user
    log_text = f"👤 New User Joined:\n\n🆔 ID: `{user.id}`\n📛 Name: {user.first_name}"
    await log_to_channel(log_text)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Enhance Image", callback_data="enhance"),
         InlineKeyboardButton("🖼️ Remove BG", callback_data="remove_bg")],
        [InlineKeyboardButton("📂 Convert Format", callback_data="convert"),
         InlineKeyboardButton("🎭 Apply Filters", callback_data="filters")],
        [InlineKeyboardButton("📝 Extract Text (OCR)", callback_data="ocr"),
         InlineKeyboardButton("📜 Metadata", callback_data="metadata")],
        [InlineKeyboardButton("😂 Meme Generator", callback_data="meme"),
         InlineKeyboardButton("🎨 Sticker Maker", callback_data="sticker")],
        [InlineKeyboardButton("🔎 Reverse Image Search", callback_data="reverse_search")],
        [InlineKeyboardButton("🌐 Extract Images from Web", callback_data="web_extract")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    
    await message.reply_text(
        "**🔹 Welcome to Advanced Image Tool Bot!**\n\n"
        "📌 Send an image and choose an option from the buttons below.",
        reply_markup=buttons
    )

# 🎨 **Image Enhancement**
@app.on_callback_query(filters.regex("enhance"))
async def enhance_image(client, callback_query):
    await callback_query.message.reply_text("📸 **Send an image to enhance.**")

@app.on_message(filters.photo)
async def process_image(client, message):
    file_path = await message.download()
    
    img = Image.open(file_path)
    enhancer = ImageEnhance.Sharpness(img)
    enhanced_img = enhancer.enhance(2.5)  
    
    enhanced_path = file_path.replace(".jpg", "_enhanced.jpg")
    enhanced_img.save(enhanced_path)
    
    await message.reply_photo(enhanced_path, caption="✅ **Image Enhanced Successfully!**")

# 🎭 **Background Removal**
@app.on_callback_query(filters.regex("remove_bg"))
async def remove_bg(client, callback_query):
    await callback_query.message.reply_text("🎨 **Send an image to remove background.**")

@app.on_message(filters.photo)
async def remove_background(client, message):
    file_path = await message.download()
    
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    result = cv2.bitwise_and(img, img, mask=thresh)
    no_bg_path = file_path.replace(".jpg", "_no_bg.png")
    cv2.imwrite(no_bg_path, result)
    
    await message.reply_photo(no_bg_path, caption="✅ **Background Removed!**")

# 📝 **OCR (Text Extraction)**
@app.on_callback_query(filters.regex("ocr"))
async def ocr_text(client, callback_query):
    await callback_query.message.reply_text("📜 **Send an image to extract text.**")

@app.on_message(filters.photo)
async def extract_text(client, message):
    file_path = await message.download()
    img = Image.open(file_path)
    
    text = pytesseract.image_to_string(img)
    await message.reply_text(f"📝 **Extracted Text:**\n\n{text}")

# 😂 **Meme Generator**
@app.on_callback_query(filters.regex("meme"))
async def meme_generator(client, callback_query):
    await callback_query.message.reply_text("😂 **Send an image & meme text (top/bottom).**")

@app.on_message(filters.photo)
async def create_meme(client, message):
    file_path = await message.download()
    img = Image.open(file_path)
    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 40)
    
    text = "MEME TEXT HERE"
    draw.text((10, 10), text, font=font, fill="white")
    
    meme_path = file_path.replace(".jpg", "_meme.jpg")
    img.save(meme_path)
    
    await message.reply_photo(meme_path, caption="✅ **Meme Created!**")

# 🔎 **Reverse Image Search**
@app.on_callback_query(filters.regex("reverse_search"))
async def reverse_search(client, callback_query):
    await callback_query.message.reply_text("🔎 **Send an image to reverse search.**")

# 🌐 **Extract Images from Web**
@app.on_callback_query(filters.regex("web_extract"))
async def web_extract_request(client, callback_query):
    await callback_query.message.reply_text("🌐 **Send a website URL to extract images.**")

@app.on_message(filters.text)
async def extract_images_from_web(client, message):
    url = message.text.strip()
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")

        image_urls = [img["src"] for img in images if "src" in img.attrs]

        if image_urls:
            await message.reply_text("✅ **Extracted Images:**\n\n" + "\n".join(image_urls[:10]))
        else:
            await message.reply_text("❌ **No images found on this webpage.**")

    except Exception as e:
        await message.reply_text(f"⚠️ **Error:** {str(e)}")

# ℹ️ **About Bot**
@app.on_callback_query(filters.regex("about"))
async def about_bot(client, callback_query):
    await callback_query.message.reply_text(
        "**ℹ️ About Advanced Image Bot**\n\n"
        "📌 Developed by **Rahat**\n"
        "📢 Powered by **RM Movie Flix**\n"
        "📌 Supports AI Image Enhancements, Background Removal, OCR, and More!\n"
        "🚀 **Stay tuned for updates!**"
    )

# ✅ **Run the Bot & Server**
async def run():
    await app.start()
    await log_to_channel("✅ **Bot started successfully!**")
    print("✅ Bot is running!")
    app_web.run(host="0.0.0.0", port=5000)

asyncio.run(run())
