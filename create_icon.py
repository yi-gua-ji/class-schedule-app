# -*- coding: utf-8 -*-
try:
    from PIL import Image, ImageDraw
    
    img = Image.new('RGB', (512, 512), color=(70, 130, 180))
    d = ImageDraw.Draw(img)
    
    d.rectangle([100, 100, 412, 412], fill=(255, 255, 255))
    d.rectangle([120, 120, 392, 392], fill=(70, 130, 180))
    
    try:
        d.text((256, 256), '课', fill=(255, 255, 255), anchor='mm')
    except:
        d.text((256, 256), '课', fill=(255, 255, 255))
    
    img.save('icon.png')
    print('图标已创建：icon.png')
except ImportError:
    print('PIL 未安装，跳过图标创建')
