# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, '.')

print("Testing imports...")
from data_parser import ScheduleParser

print("Testing Excel path resolution...")
script_dir = os.path.dirname(os.path.abspath('main.py'))
print(f"Script dir: {script_dir}")

excel_path = os.path.join(script_dir, '..', '..', '任宝琦课表.xls')
print(f"Excel path: {excel_path}")
print(f"Exists: {os.path.exists(excel_path)}")

excel_path = os.path.normpath(excel_path)
print(f"Normalized path: {excel_path}")
print(f"Exists after normpath: {os.path.exists(excel_path)}")

print("Testing parser...")
parser = ScheduleParser(excel_path)
data = parser.parse()
print(f"Parsed {len(data)} schedule entries")

print("Testing app init...")
from main import ScheduleApp
print("Creating app...")
app = ScheduleApp()
print("Build started...")
try:
    root = app.build()
    print("Build completed successfully!")
except Exception as e:
    print(f"Build failed: {e}")
    import traceback
    traceback.print_exc()
