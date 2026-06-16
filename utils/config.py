import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات سیستم
class Config:
    # پوشه‌ها
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    
    # دیتابیس
    DATABASE_PATH = os.path.join(DATABASE_DIR, "incidents.db")
    
    # تنظیمات YOLO
    YOLO_CONFIDENCE = float(os.getenv("YOLO_CONFIDENCE", 0.5))
    YOLO_IOU = float(os.getenv("YOLO_IOU", 0.45))
    
    # تنظیمات Pose Detection
    POSE_CONFIDENCE = float(os.getenv("POSE_CONFIDENCE", 0.5))
    
    # تنظیمات Streamlit
    STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "dark")
    STREAMLIT_LAYOUT = "wide"
    
    # تنظیمات سیستم
    DEBUG = os.getenv("DEBUG", False) == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # حداکثر فریم‌ها
    MAX_FRAMES_BUFFER = 100
    
    # تنظیمات camera
    CAMERA_RESOLUTION = (640, 480)
    CAMERA_FPS = 30
    
    @staticmethod
    def init_directories():
        """ایجاد پوشه‌های ضروری"""
        for directory in [Config.DATABASE_DIR, Config.MODELS_DIR, Config.LOGS_DIR]:
            os.makedirs(directory, exist_ok=True)
