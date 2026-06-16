import logging
import os
from datetime import datetime
from utils.config import Config

# ایجاد پوشه لاگ
Config.init_directories()

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.logger = logging.getLogger("AdvancedSecurity")
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # فرمت لاگ
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File Handler
        log_file = os.path.join(
            Config.LOGS_DIR,
            f"security_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self._initialized = True
    
    def info(self, message):
        """ثبت پیام معلوماتی"""
        self.logger.info(message)
    
    def warning(self, message):
        """ثبت هشدار"""
        self.logger.warning(message)
    
    def error(self, message):
        """ثبت خطا"""
        self.logger.error(message)
    
    def critical(self, message):
        """ثبت خطای بحرانی"""
        self.logger.critical(message)
    
    def debug(self, message):
        """ثبت پیام debug"""
        self.logger.debug(message)

# نمونه گلوبال
logger = Logger()
