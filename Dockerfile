# ✅ Python 3.9 বেস ইমেজ
FROM python:3.9

# 🏠 ওয়ার্কডিরেক্টরি সেট করা
WORKDIR /app

# 🔹 প্রয়োজনীয় লাইব্রেরি ইন্সটল
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 🔹 কোড কপি করা
COPY . /app

# 🔹 ডিপেন্ডেন্সি ইন্সটল করা
RUN pip install --no-cache-dir -r requirements.txt

# 🚀 বট চালানো
CMD ["python", "bot.py"]
