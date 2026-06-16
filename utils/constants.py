# ثابت‌های سیستم

# اشیاء خطرناک قابل تشخیص
DANGEROUS_OBJECTS = {
    "knife": "چاقو 🔪",
    "gun": "اسلحه 🔫",
    "pistol": "تفنگ 🔫",
    "rifle": "تفنگ شکاری 🔫",
    "sword": "شمشیر ⚔️",
    "axe": "تبر 🪓",
    "bomb": "بمب 💣",
    "phone": "گوشی 📱",
}

# سطح‌های تهدید
THREAT_LEVELS = {
    "low": {"color": "#FFA500", "label": "کم ⚠️"},
    "medium": {"color": "#FF6B6B", "label": "متوسط ⚠️⚠️"},
    "high": {"color": "#DC143C", "label": "بالا 🚨"},
}

# حداقل اعتماد
MIN_CONFIDENCE = 0.5

# تعداد تشخیصات برای ثبت incident
REPEAT_THRESHOLD = 3

# زمان پنجره (ثانیه)
TIME_WINDOW = 10

# YOLO Model
YOLO_MODEL = "yolov8m.pt"

# Pose Detection
POSE_CONFIDENCE_THRESHOLD = 0.5

# رنگ‌ها
COLORS = {
    "danger": "#FF6B6B",
    "warning": "#FFA500",
    "success": "#51CF66",
    "info": "#4ECDC4",
    "primary": "#667EEA",
}

# پیام‌های فارسی
MESSAGES = {
    "detecting": "🔍 در حال تشخیص...",
    "alert": "⚠️ تهدید تشخیص داده شد!",
    "incident_logged": "📝 رویداد ثبت شد",
    "no_threat": "✅ هیچ تهدیدی تشخیص نشد",
}
