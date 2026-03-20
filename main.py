# -*- coding: utf-8 -*-
import os
import json
import datetime
import copy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.properties import NumericProperty, DictProperty
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.clock import Clock

from data_parser import ScheduleParser, PERIODS, Course


def setup_chinese_fonts():
    font_paths = [
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/msyhbd.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/simkai.ttf',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                print(f'成功加载中文字体：{font_path}')
                return 'ChineseFont'
            except Exception as e:
                print(f'加载字体失败 {font_path}: {e}')
                continue
    print('警告：无法找到合适的中文字体')
    return None


CHINESE_FONT = setup_chinese_fonts()


COURSE_COLORS = [
    (0.85, 0.92, 1.0, 1),
    (0.85, 1.0, 0.92, 1),
    (1.0, 0.92, 0.85, 1),
    (1.0, 0.85, 0.92, 1),
    (0.92, 1.0, 0.85, 1),
    (0.92, 0.85, 1.0, 1),
]

TEXT_COLORS = [
    (0.1, 0.3, 0.6, 1),
    (0.1, 0.5, 0.3, 1),
    (0.6, 0.3, 0.1, 1),
    (0.6, 0.1, 0.3, 1),
    (0.3, 0.5, 0.1, 1),
    (0.4, 0.1, 0.6, 1),
]


class CourseCard(BoxLayout):
    def __init__(self, course=None, color_idx=0, day=None, period=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(4), dp(2)]
        self.spacing = dp(2)
        self.size_hint_y = None
        self.height = dp(85)
        self.course = course
        self.day = day
        self.period = period
        
        base_color = COURSE_COLORS[color_idx % len(COURSE_COLORS)]
        text_color = TEXT_COLORS[color_idx % len(TEXT_COLORS)]
        
        with self.canvas.before:
            Color(*base_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(4)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        if course:
            name_label = Label(
                text=course.name if course.name else '',
                font_size=dp(10),
                bold=True,
                color=text_color,
                halign='center',
                valign='middle',
                size_hint_y=0.65,
                text_size=(self.width - dp(6), None)
            )
            if CHINESE_FONT:
                name_label.font_name = CHINESE_FONT
            
            loc_label = Label(
                text=course.location if course.location else '',
                font_size=dp(9),
                color=(*text_color[:3], 0.8),
                halign='center',
                valign='middle',
                size_hint_y=0.35,
                text_size=(self.width - dp(6), None)
            )
            if CHINESE_FONT:
                loc_label.font_name = CHINESE_FONT
            
            self.name_label = name_label
            self.loc_label = loc_label
            self.add_widget(name_label)
            self.add_widget(loc_label)
            self.bind(size=self.update_text_sizes)
    
    def update_text_sizes(self, instance, value):
        if hasattr(self, 'name_label'):
            self.name_label.text_size = (self.width - dp(6), None)
        if hasattr(self, 'loc_label'):
            self.loc_label.text_size = (self.width - dp(6), None)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class EmptyCell(BoxLayout):
    def __init__(self, is_weekend=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(85)
        
        bg_color = (0.96, 0.94, 0.96, 1) if is_weekend else (0.98, 0.98, 0.99, 1)
        
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(3)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TimeCell(BoxLayout):
    def __init__(self, period, time_str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(85)
        self.padding = [dp(4), dp(4)]
        self.spacing = dp(2)
        
        with self.canvas.before:
            Color(0.90, 0.92, 0.95, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(3)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        period_lbl = Label(
            text=period,
            font_size=dp(10),
            bold=True,
            color=(0.2, 0.2, 0.25, 1),
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        if CHINESE_FONT:
            period_lbl.font_name = CHINESE_FONT
        
        time_lbl = Label(
            text=time_str,
            font_size=dp(9),
            color=(0.4, 0.4, 0.45, 1),
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        if CHINESE_FONT:
            time_lbl.font_name = CHINESE_FONT
        
        self.add_widget(period_lbl)
        self.add_widget(time_lbl)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class DayHeader(Label):
    def __init__(self, text, date_str='', is_time=False, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        if date_str and not is_time:
            self.text = f'{text}\n{date_str}'
        self.font_size = dp(10) if is_time else dp(11)
        self.bold = True
        self.color = (0.15, 0.15, 0.2, 1)
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(45) if date_str and not is_time else dp(35)
        if CHINESE_FONT:
            self.font_name = CHINESE_FONT


class CourseEditPopup(Popup):
    def __init__(self, app, course=None, day=None, period=None, on_save=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.course = course
        self.day = day
        self.period = period
        self.on_save = on_save
        self.title = '编辑课程' if course else '添加课程'
        self.title_size = dp(18)
        if CHINESE_FONT:
            self.title_font = CHINESE_FONT
        self.size_hint = (0.9, 0.8)
        
        self.build_ui()
    
    def build_ui(self):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        fields = [
            ('课程名称', 'name', self.course.name if self.course else ''),
            ('教师', 'teacher', self.course.teacher if self.course else ''),
            ('地点', 'location', self.course.location if self.course else ''),
        ]
        
        self.inputs = {}
        for label_text, field_name, default_value in fields:
            box = BoxLayout(size_hint_y=None, height=dp(50))
            lbl = Label(
                text=label_text + ':',
                size_hint_x=0.3,
                font_size=dp(14),
                color=(0.2, 0.2, 0.3, 1)
            )
            if CHINESE_FONT:
                lbl.font_name = CHINESE_FONT
            
            inp = TextInput(
                text=default_value if default_value else '',
                font_size=dp(14),
                size_hint_x=0.7
            )
            if CHINESE_FONT:
                inp.font_name = CHINESE_FONT
            
            self.inputs[field_name] = inp
            box.add_widget(lbl)
            box.add_widget(inp)
            content.add_widget(box)
        
        weeks_box = BoxLayout(size_hint_y=None, height=dp(50))
        weeks_lbl = Label(
            text='上课周数:',
            size_hint_x=0.3,
            font_size=dp(14),
            color=(0.2, 0.2, 0.3, 1)
        )
        if CHINESE_FONT:
            weeks_lbl.font_name = CHINESE_FONT
        
        default_weeks = ''
        if self.course and self.course.weeks:
            weeks_str = ','.join(map(str, self.course.weeks))
            default_weeks = weeks_str
        
        self.weeks_input = TextInput(
            text=default_weeks,
            font_size=dp(14),
            hint_text='如：1,2,3,4 或 1-16'
        )
        if CHINESE_FONT:
            self.weeks_input.font_name = CHINESE_FONT
        
        weeks_box.add_widget(weeks_lbl)
        weeks_box.add_widget(self.weeks_input)
        content.add_widget(weeks_box)
        
        btn_box = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(15))
        
        save_btn = Button(
            text='保存',
            background_color=(0.18, 0.45, 0.75, 1),
            background_normal='',
            background_down='',
            font_size=dp(16),
            bold=True
        )
        if CHINESE_FONT:
            save_btn.font_name = CHINESE_FONT
        save_btn.bind(on_press=self.save_course)
        
        cancel_btn = Button(
            text='取消',
            background_color=(0.6, 0.6, 0.6, 1),
            background_normal='',
            background_down='',
            font_size=dp(16),
            bold=True
        )
        if CHINESE_FONT:
            cancel_btn.font_name = CHINESE_FONT
        cancel_btn.bind(on_press=lambda x: self.dismiss())
        
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        
        content.add_widget(Label(size_hint_y=1))
        content.add_widget(btn_box)
        
        self.content = content
    
    def parse_weeks(self, weeks_str):
        weeks = []
        if not weeks_str.strip():
            return list(range(1, 21))
        
        parts = weeks_str.replace(' ', '').split(',')
        for part in parts:
            if '-' in part:
                try:
                    start, end = part.split('-')
                    weeks.extend(range(int(start), int(end) + 1))
                except:
                    pass
            else:
                try:
                    weeks.append(int(part))
                except:
                    pass
        return weeks
    
    def save_course(self, instance):
        name = self.inputs['name'].text.strip()
        teacher = self.inputs['teacher'].text.strip()
        location = self.inputs['location'].text.strip()
        weeks_str = self.weeks_input.text.strip()
        
        if not name:
            print('课程名称不能为空')
            return
        
        weeks = self.parse_weeks(weeks_str)
        
        course = Course(
            name=name,
            teacher=teacher,
            location=location,
            weeks=weeks
        )
        
        if self.on_save:
            self.on_save(course, self.day, self.period)
        
        self.app.save_schedule_data()
        self.app.refresh_week_screens()
        self.dismiss()


class SettingsScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(
            text='设置',
            font_size=dp(24),
            bold=True,
            color=(0.15, 0.25, 0.45, 1),
            size_hint_y=None,
            height=dp(60)
        )
        if CHINESE_FONT:
            title.font_name = CHINESE_FONT
        content.add_widget(title)
        
        date_label = Label(
            text='新学期第一天',
            font_size=dp(16),
            bold=True,
            color=(0.2, 0.2, 0.3, 1),
            size_hint_y=None,
            height=dp(40)
        )
        if CHINESE_FONT:
            date_label.font_name = CHINESE_FONT
        content.add_widget(date_label)
        
        date_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.year_input = TextInput(
            text=str(self.app.start_date.year),
            font_size=dp(14),
            input_filter='int',
            size_hint_x=0.3
        )
        
        year_label = Label(
            text='年',
            font_size=dp(14),
            size_hint_x=0.1
        )
        if CHINESE_FONT:
            year_label.font_name = CHINESE_FONT
        
        self.month_input = TextInput(
            text=str(self.app.start_date.month),
            font_size=dp(14),
            input_filter='int',
            size_hint_x=0.2
        )
        
        month_label = Label(
            text='月',
            font_size=dp(14),
            size_hint_x=0.1
        )
        if CHINESE_FONT:
            month_label.font_name = CHINESE_FONT
        
        self.day_input = TextInput(
            text=str(self.app.start_date.day),
            font_size=dp(14),
            input_filter='int',
            size_hint_x=0.2
        )
        
        day_label = Label(
            text='日',
            font_size=dp(14),
            size_hint_x=0.1
        )
        if CHINESE_FONT:
            day_label.font_name = CHINESE_FONT
        
        date_box.add_widget(self.year_input)
        date_box.add_widget(year_label)
        date_box.add_widget(self.month_input)
        date_box.add_widget(month_label)
        date_box.add_widget(self.day_input)
        date_box.add_widget(day_label)
        content.add_widget(date_box)
        
        save_btn = Button(
            text='保存设置',
            background_color=(0.18, 0.45, 0.75, 1),
            background_normal='',
            background_down='',
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        if CHINESE_FONT:
            save_btn.font_name = CHINESE_FONT
        save_btn.bind(on_press=self.save_settings)
        content.add_widget(save_btn)
        
        back_btn = Button(
            text='返回',
            background_color=(0.6, 0.6, 0.6, 1),
            background_normal='',
            background_down='',
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        if CHINESE_FONT:
            back_btn.font_name = CHINESE_FONT
        back_btn.bind(on_press=lambda x: self.go_back())
        content.add_widget(back_btn)
        
        content.add_widget(Label(size_hint_y=1))
        
        self.add_widget(content)
    
    def save_settings(self, instance):
        try:
            year = int(self.year_input.text)
            month = int(self.month_input.text)
            day = int(self.day_input.text)
            new_date = datetime.date(year, month, day)
            self.app.save_start_date(new_date)
            self.app.current_week = self.app.calc_week()
            self.app.refresh_week_screens()
            self.go_back()
        except Exception as e:
            print(f'日期错误：{e}')
    
    def go_back(self):
        self.manager.current = 'main'


class WeekScreen(Screen):
    def __init__(self, week: int, schedule_data: dict, course_colors: dict, start_date=None, **kwargs):
        super().__init__(**kwargs)
        self.week_number = week
        self.schedule_data = schedule_data
        self.course_colors = course_colors
        self.start_date = start_date
        self.last_touch_time = 0
        self.last_touch_pos = None
        self.double_tap_delay = 0.4
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        with root.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            Rectangle(pos=root.pos, size=root.size)
        
        header = self.create_header()
        root.add_widget(header)
        
        content = self.create_content()
        root.add_widget(content)
        
        self.add_widget(root)

    def get_week_dates(self):
        if not self.start_date:
            return ['', '', '', '', '', '', '']
        
        start_of_week = self.start_date + datetime.timedelta(days=(self.week_number - 1) * 7)
        dates = []
        for i in range(7):
            day = start_of_week + datetime.timedelta(days=i)
            dates.append(f'{day.month}/{day.day}')
        return dates

    def create_header(self):
        header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=[dp(10), dp(10)]
        )
        
        with header_box.canvas.before:
            Color(0.92, 0.94, 0.98, 1)
            Rectangle(pos=header_box.pos, size=header_box.size)
        
        settings_btn = Button(
            text='设置',
            size_hint_x=None,
            width=dp(60),
            background_color=(0.6, 0.6, 0.7, 1),
            background_normal='',
            background_down='',
            font_size=dp(14)
        )
        if CHINESE_FONT:
            settings_btn.font_name = CHINESE_FONT
        settings_btn.bind(on_press=lambda x: self.show_settings())
        
        week_label = Label(
            text=f'第 {self.week_number} 周',
            font_size=dp(20),
            bold=True,
            color=(0.15, 0.25, 0.45, 1),
            halign='center',
            valign='middle',
            size_hint_x=1
        )
        if CHINESE_FONT:
            week_label.font_name = CHINESE_FONT
        
        header_box.add_widget(settings_btn)
        header_box.add_widget(week_label)
        return header_box
    
    def show_settings(self):
        app = App.get_running_app()
        if app.main_screen_manager:
            app.main_screen_manager.current = 'settings'

    def create_content(self):
        root = BoxLayout(orientation='vertical', padding=[dp(5), dp(5)], spacing=dp(3))
        
        dates = self.get_week_dates()
        day_bar = GridLayout(cols=8, size_hint_y=None, height=dp(45), spacing=dp(2))
        day_names = ['', '一', '二', '三', '四', '五', '六', '日']
        for i, name in enumerate(day_names):
            if i == 0:
                day_bar.add_widget(DayHeader('时间', is_time=True))
            else:
                day_bar.add_widget(DayHeader(name, date_str=dates[i-1]))
        root.add_widget(day_bar)
        
        scroll = ScrollView(size_hint_y=1, do_scroll_x=False)
        grid = GridLayout(cols=8, spacing=dp(2), padding=[dp(2), dp(2)], size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        times = ['08:00', '10:10', '14:00', '16:10', '19:00', '21:10']
        periods = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        
        for idx, period in enumerate(PERIODS):
            grid.add_widget(TimeCell(periods[idx], times[idx]))
            
            for day in range(7):
                key = (day, period)
                courses = self.schedule_data.get(key, [])
                
                is_weekend = day >= 5
                
                if courses:
                    week_courses = []
                    for c in courses:
                        if not c.weeks or self.week_number in c.weeks:
                            week_courses.append(c)
                    
                    if week_courses:
                        cname = week_courses[0].name if week_courses[0].name else 'Unknown'
                        color_idx = self.course_colors.get(cname, 0)
                        card = CourseCard(week_courses[0], color_idx, day=day, period=period)
                        card.bind(on_touch_down=self.on_course_touch)
                        grid.add_widget(card)
                    else:
                        empty = EmptyCell(is_weekend=is_weekend)
                        empty.bind(on_touch_down=self.on_empty_touch)
                        empty.day = day
                        empty.period = period
                        grid.add_widget(empty)
                else:
                    empty = EmptyCell(is_weekend=is_weekend)
                    empty.bind(on_touch_down=self.on_empty_touch)
                    empty.day = day
                    empty.period = period
                    grid.add_widget(empty)
        
        scroll.add_widget(grid)
        root.add_widget(scroll)
        return root
    
    def is_double_tap(self, touch):
        import time
        current_time = time.time()
        if self.last_touch_pos and self.last_touch_time > 0:
            time_diff = current_time - self.last_touch_time
            if time_diff < self.double_tap_delay:
                if self.last_touch_pos:
                    pos_diff = abs(touch.x - self.last_touch_pos[0]) + abs(touch.y - self.last_touch_pos[1])
                    if pos_diff < dp(20):
                        self.last_touch_time = 0
                        self.last_touch_pos = None
                        return True
        self.last_touch_time = current_time
        self.last_touch_pos = (touch.x, touch.y)
        return False

    def on_course_touch(self, instance, touch):
        if touch.is_double_tap or self.is_double_tap(touch):
            app = App.get_running_app()
            card = instance
            self.edit_course_name = card.course.name if card.course else ''
            popup = CourseEditPopup(
                app,
                course=card.course,
                day=card.day,
                period=card.period,
                on_save=self.update_course
            )
            popup.open()
            return True
        return False

    def on_empty_touch(self, instance, touch):
        if touch.is_double_tap or self.is_double_tap(touch):
            app = App.get_running_app()
            popup = CourseEditPopup(
                app,
                course=None,
                day=instance.day,
                period=instance.period,
                on_save=self.add_course
            )
            popup.open()
            return True
        return False
    
    def update_course(self, new_course, day, period):
        key = (day, period)
        if key in self.app.schedule_data:
            for i, course in enumerate(self.app.schedule_data[key]):
                if hasattr(self, 'edit_course_name') and course.name == self.edit_course_name:
                    self.app.schedule_data[key][i] = new_course
                    break
        else:
            self.app.schedule_data[key] = [new_course]
        delattr(self, 'edit_course_name')
    
    def add_course(self, new_course, day, period):
        key = (day, period)
        if key not in self.app.schedule_data:
            self.app.schedule_data[key] = []
        self.app.schedule_data[key].append(new_course)


class ScheduleApp(App):
    current_week = NumericProperty(1)
    total_weeks = 20
    schedule_data = {}
    course_colors = DictProperty({})
    main_screen_manager = None
    start_date = None
    touch_start_x = 0

    def build(self):
        Window.clearcolor = (0.95, 0.96, 0.98, 1)
        Window.size = (360, 700)

        self.load_start_date()
        self.load_schedule()
        self.load_schedule_data()

        self.main_screen_manager = ScreenManager()
        
        main_screen = Screen(name='main')
        main_content = self.create_main_content()
        main_screen.add_widget(main_content)
        self.main_screen_manager.add_widget(main_screen)
        
        settings_screen = SettingsScreen(self, name='settings')
        self.main_screen_manager.add_widget(settings_screen)

        return self.main_screen_manager

    def create_main_content(self):
        root = BoxLayout(orientation='vertical')
        root.bind(on_touch_down=self.on_touch_down)
        root.bind(on_touch_up=self.on_touch_up)

        self.week_screen_manager = ScreenManager(transition=SlideTransition(duration=0.2))
        self.create_week_screens()

        week_screen = self.get_screen(self.current_week)
        if week_screen:
            self.week_screen_manager.current = week_screen.name
        
        root.add_widget(self.week_screen_manager)

        return root
    
    def on_touch_down(self, instance, touch):
        if self.week_screen_manager.collide_point(*touch.pos):
            self.touch_start_x = touch.x
            return True
        return False
    
    def on_touch_up(self, instance, touch):
        if hasattr(self, 'touch_start_x'):
            delta_x = touch.x - self.touch_start_x
            if abs(delta_x) > dp(60):
                if delta_x > 0:
                    self.change_week(-1)
                else:
                    self.change_week(1)
        return False

    def load_schedule(self, path=None):
        if path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(script_dir, '..', '..', '任宝琦课表.xls')
            path = os.path.normpath(path)
            if not os.path.exists(path):
                path = 'd:/BME/temp/任宝琦课表.xls'

        if os.path.exists(path):
            parser = ScheduleParser(path)
            self.schedule_data = parser.parse()
            self.assign_colors()
            self.current_week = self.calc_week()

    def assign_colors(self):
        courses = set()
        for cs in self.schedule_data.values():
            for c in cs:
                if c.name:
                    courses.add(c.name)

        course_list = sorted(courses)
        color_map = {}
        for i, name in enumerate(course_list):
            color_map[name] = i % len(COURSE_COLORS)
        self.course_colors = color_map

        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_colors.json')
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({'colors': {k: v for k, v in color_map.items()}}, f, ensure_ascii=False)
        except:
            pass

    def load_start_date(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    date_str = data.get('start_date', '2026-02-24')
                    year, month, day = map(int, date_str.split('-'))
                    self.start_date = datetime.date(year, month, day)
            else:
                self.start_date = datetime.date(2026, 2, 24)
        except:
            self.start_date = datetime.date(2026, 2, 24)
    
    def get_start_date_str(self):
        if self.start_date:
            return self.start_date.strftime('%Y-%m-%d')
        return '2026-02-24'
    
    def save_start_date(self, date):
        self.start_date = date
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({'start_date': date.strftime('%Y-%m-%d')}, f, ensure_ascii=False)
            self.refresh_week_screens()
        except Exception as e:
            print(f"保存设置失败：{e}")
    
    def save_schedule_data(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schedule_data.json')
        try:
            data = {}
            for (day, period), courses in self.schedule_data.items():
                key = f'{day}_{period}'
                data[key] = []
                for course in courses:
                    data[key].append({
                        'name': course.name,
                        'teacher': course.teacher,
                        'weeks': course.weeks,
                        'location': course.location
                    })
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception as e:
            print(f'保存课程数据失败：{e}')
    
    def load_schedule_data(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schedule_data.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.schedule_data = {}
                for key, courses_data in data.items():
                    day_str, period = key.split('_', 1)
                    day = int(day_str)
                    courses = []
                    for cd in courses_data:
                        courses.append(Course(
                            name=cd['name'],
                            teacher=cd['teacher'],
                            weeks=cd['weeks'],
                            location=cd['location']
                        ))
                    self.schedule_data[(day, period)] = courses
        except Exception as e:
            print(f'加载课程数据失败：{e}')
    
    def refresh_week_screens(self):
        if self.week_screen_manager:
            self.assign_colors()
            self.week_screen_manager.clear_widgets()
            self.create_week_screens()
            week_screen = self.get_screen(self.current_week)
            if week_screen:
                self.week_screen_manager.current = week_screen.name

    def calc_week(self):
        if not self.start_date:
            return 1
        today = datetime.date.today()
        if today < self.start_date:
            return 1
        w = (today - self.start_date).days // 7 + 1
        return min(max(w, 1), self.total_weeks)

    def create_week_screens(self):
        for w in range(1, self.total_weeks + 1):
            screen = WeekScreen(
                week=w,
                schedule_data=self.schedule_data,
                course_colors=self.course_colors,
                start_date=self.start_date,
                name=f'week_{w}'
            )
            self.week_screen_manager.add_widget(screen)

    def get_screen(self, week):
        week = max(1, min(week, self.total_weeks))
        name = f'week_{week}'
        if self.week_screen_manager.has_screen(name):
            return self.week_screen_manager.get_screen(name)
        if self.week_screen_manager.has_screen('week_1'):
            return self.week_screen_manager.get_screen('week_1')
        return None

    def change_week(self, direction):
        new = self.current_week + direction
        if 1 <= new <= self.total_weeks:
            self.current_week = new
            if direction > 0:
                self.week_screen_manager.transition = SlideTransition(direction='left')
            else:
                self.week_screen_manager.transition = SlideTransition(direction='right')
            self.week_screen_manager.current = f'week_{new}'


if __name__ == '__main__':
    ScheduleApp().run()
