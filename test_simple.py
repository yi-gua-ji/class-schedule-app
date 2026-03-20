# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, '.')

print("Starting test...")

# Test imports
from data_parser import ScheduleParser
print("data_parser imported OK")

from main import ScheduleApp, WeekScreen, CourseCard
print("main modules imported OK")

# Test data loading
excel_path = 'd:/BME/temp/任宝琦课表.xls'
parser = ScheduleParser(excel_path)
data = parser.parse()
print(f"Loaded {len(data)} schedule entries")

# Create app and build
print("Creating app...")
app = ScheduleApp()

print("Loading schedule...")
app.load_schedule()
print(f"Schedule has {len(app.schedule_data)} entries, week={app.current_week}")

print("Creating screens...")
app.screen_manager = app.create_week_screens() if hasattr(app, 'create_week_screens') else None

print("All tests passed!")
