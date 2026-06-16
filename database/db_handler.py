import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from utils.config import Config
from utils.logger import logger

class IncidentDatabase:
    """کلاس برای مدیریت دیتابیس incidents"""
    
    def __init__(self):
        """اولین سازی دیتابیس"""
        Config.init_directories()
        self.db_path = Config.DATABASE_PATH
        self._init_db()
    
    def _init_db(self):
        """ایجاد جداول دیتابیس"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # جدول incidents
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    object_name TEXT NOT NULL,
                    threat_level TEXT NOT NULL,
                    in_hand BOOLEAN DEFAULT 0,
                    confidence REAL,
                    location TEXT,
                    description TEXT
                )
            ''')
            
            # جدول alerts
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    incident_id INTEGER,
                    FOREIGN KEY (incident_id) REFERENCES incidents(id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ دیتابیس شروع شد")
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد جداول: {str(e)}")
    
    def log_incident(self, incident_data: Dict) -> int:
        """ثبت رویداد خطرناک
        
        Args:
            incident_data: اطلاعات رویداد
            
        Returns:
            ID رویداد
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO incidents
                (object_name, threat_level, in_hand, confidence, location, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                incident_data.get('object_name'),
                incident_data.get('threat_level', 'unknown'),
                incident_data.get('in_hand', False),
                incident_data.get('confidence', 0.0),
                incident_data.get('location', 'unknown'),
                incident_data.get('description', '')
            ))
            
            conn.commit()
            incident_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ روید��د ثبت شد: ID={incident_id}")
            return incident_id
        except Exception as e:
            logger.error(f"❌ خطا در ثبت رویداد: {str(e)}")
            return -1
    
    def log_alert(self, alert_data: Dict) -> int:
        """ثبت هشدار
        
        Args:
            alert_data: اطلاعات هشدار
            
        Returns:
            ID هشدار
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts
                (severity, message, incident_id)
                VALUES (?, ?, ?)
            ''', (
                alert_data.get('severity', 'info'),
                alert_data.get('message', ''),
                alert_data.get('incident_id')
            ))
            
            conn.commit()
            alert_id = cursor.lastrowid
            conn.close()
            
            return alert_id
        except Exception as e:
            logger.error(f"❌ خطا در ثبت هشدار: {str(e)}")
            return -1
    
    def get_incidents(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """دريافت رویدادها
        
        Args:
            limit: تعداد نتایج
            offset: ابتدال
            
        Returns:
            لیست رویدادها
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM incidents
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ خطا در دريافت incidents: {str(e)}")
            return []
    
    def get_incident_by_id(self, incident_id: int) -> Optional[Dict]:
        """دريافت رویداد به راه ID
        
        Args:
            incident_id: ID رویداد
            
        Returns:
            اطلاعات رویداد
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM incidents WHERE id = ?', (incident_id,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"❌ خطا در دريافت incident: {str(e)}")
            return None
    
    def get_alerts(self, limit: int = 100) -> List[Dict]:
        """دريافت هشدارها
        
        Args:
            limit: تعداد نتایج
            
        Returns:
            لیست هشدارها
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM alerts
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ خطا در دريافت alerts: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """دريافت آمار سیستم
        
        Returns:
            آمار کلی
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # تعداد کل incidents
            cursor.execute('SELECT COUNT(*) FROM incidents')
            total_incidents = cursor.fetchone()[0]
            
            # تعداد high-level threats
            cursor.execute('SELECT COUNT(*) FROM incidents WHERE threat_level = "high"')
            high_threats = cursor.fetchone()[0]
            
            # اشیاء خطرناک تر در دست
            cursor.execute('SELECT COUNT(*) FROM incidents WHERE in_hand = 1')
            in_hand_count = cursor.fetchone()[0]
            
            # رائج ترین اشیاء
            cursor.execute('''
                SELECT object_name, COUNT(*) as count
                FROM incidents
                GROUP BY object_name
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_objects = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_incidents': total_incidents,
                'high_threats': high_threats,
                'in_hand_count': in_hand_count,
                'top_objects': [{'name': obj[0], 'count': obj[1]} for obj in top_objects]
            }
        except Exception as e:
            logger.error(f"❌ خطا در دريافت آمار: {str(e)}")
            return {}
