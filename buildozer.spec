[app]

title = 任宝琦课表
package.name = classschedule
package.domain = com.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xls,json

version = 1.0.0

requirements = python3,kivy==2.3.0,pandas,xlrd,python-dateutil

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.archs = arm64-v8a

android.allow_backup = True

android.fullscreen = True
