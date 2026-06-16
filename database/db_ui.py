import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from utils.config import Config
from utils.logger import logger
from database.db_handler import IncidentDatabase

class DatabaseUI:
    """کلاس برای نماش داده‌های دیتابیس در Streamlit"""
    
    def __init__(self):
        self.db = IncidentDatabase()
    
    def show_incidents_table(self, limit: int = 100):
        """نماش جدول incidents"""
        incidents = self.db.get_incidents(limit=limit)
        
        if not incidents:
            st.info("✅ هیچ رویدادی ثبت نشده است")
            return
        
        df = pd.DataFrame(incidents)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['threat_level'] = df['threat_level'].apply(lambda x: f"🔴 {x}" if x == 'high' else f"🟠 {x}" if x == 'medium' else f"🟡 {x}")
        df['in_hand'] = df['in_hand'].apply(lambda x: "✅ بله" if x else "❌ خیر")
        
        st.dataframe(
            df.drop('id', axis=1),
            use_container_width=True,
            hide_index=True
        )
    
    def show_alerts_table(self, limit: int = 50):
        """نماش جدول alerts"""
        alerts = self.db.get_alerts(limit=limit)
        
        if not alerts:
            st.info("✅ هیچ هشداری ثبت نشده است")
            return
        
        df = pd.DataFrame(alerts)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['severity'] = df['severity'].apply(
            lambda x: f"🔴 {x}" if x == 'critical' else f"🟠 {x}" if x == 'warning' else f"ℹ️ {x}"
        )
        
        st.dataframe(
            df.drop('id', axis=1),
            use_container_width=True,
            hide_index=True
        )
    
    def show_statistics(self):
        """نماش آمار سیستم"""
        stats = self.db.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 کل رویدادها",
                value=stats.get('total_incidents', 0)
            )
        
        with col2:
            st.metric(
                label="🔴 تهدیدات شدید",
                value=stats.get('high_threats', 0)
            )
        
        with col3:
            st.metric(
                label="🤚 در دست انسان",
                value=stats.get('in_hand_count', 0)
            )
        
        with col4:
            st.metric(
                label="📋 رویدادهای امروز",
                value="0"  # می‌تونی این رو بهتر کنی
            )
        
        # نمودار اشیاء برتر
        top_objects = stats.get('top_objects', [])
        if top_objects:
            st.subheader("🏆 اشیاء خطرناک برتر")
            df_top = pd.DataFrame(top_objects)
            st.bar_chart(
                df_top.set_index('name'),
                use_container_width=True
            )
