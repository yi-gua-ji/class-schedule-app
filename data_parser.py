# -*- coding: utf-8 -*-
"""
Schedule Data Parser Module
"""
import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    teacher: str
    weeks: List[int]
    location: str


class ScheduleParser:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.schedule = {}

    def parse(self):
        import pandas as pd
        df = pd.read_excel(self.excel_path, header=None)

        day_map = {2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}

        for row_idx in range(2, 8):
            period = ''
            if not pd.isna(df.iloc[row_idx, 1]):
                period = str(df.iloc[row_idx, 1]).strip()

            for col_idx in range(2, 9):
                cell_value = df.iloc[row_idx, col_idx]
                if pd.isna(cell_value) or str(cell_value).strip() == '':
                    continue

                day = day_map.get(col_idx)
                if day is None:
                    continue

                courses = self._parse_cell(str(cell_value))

                key = (day, period)
                if key not in self.schedule:
                    self.schedule[key] = []
                self.schedule[key].extend(courses)

        return self.schedule

    def _parse_cell(self, text: str) -> List[Course]:
        courses = []
        text = text.replace('\r\n', '\n').replace('\r', '\n').strip()

        blocks = text.split('\n')

        i = 0
        while i < len(blocks):
            block = blocks[i].strip()
            if not block:
                i += 1
                continue

            teacher = ''
            weeks = []
            location = ''

            j = i + 1
            info_lines = []
            while j < len(blocks):
                next_block = blocks[j].strip()
                if not next_block:
                    break
                if self._is_info_block(next_block):
                    info_lines.append(next_block)
                    j += 1
                else:
                    break

            if info_lines:
                full_info = ' '.join(info_lines)
                info = self._parse_info(full_info)
                teacher = info['teacher']
                weeks = info['weeks']
                location = info['location']

            if block:
                courses.append(Course(
                    name=block,
                    teacher=teacher,
                    weeks=weeks,
                    location=location
                ))

            i = j if j > i + 1 else i + 1

        return courses

    def _is_info_block(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return False

        teachers = ['赵勃', '谭立国', '刘绍琴', '陈书晴', '安荣', '朱慧', '田也壮', '王芳', '崔煜', '李文华']
        for t in teachers:
            if t in text:
                return True

        if re.search(r'\[[\d,\-，]+\]周', text):
            return True

        return False

    def _parse_info(self, text: str) -> Dict:
        result = {'teacher': '', 'weeks': [], 'location': ''}
        text = text.strip()

        teachers = ['赵勃', '谭立国', '刘绍琴', '陈书晴', '安荣', '朱慧', '田也壮', '王芳', '崔煜', '李文华']
        for t in teachers:
            if t in text:
                result['teacher'] = t
                break

        week_match = re.search(r'\[([\d,\-，]+)\]周', text)
        if week_match:
            week_str = week_match.group(1).replace('，', ',')
            for part in week_str.split(','):
                part = part.strip()
                if '-' in part:
                    try:
                        start, end = part.split('-')
                        result['weeks'].extend(range(int(start), int(end) + 1))
                    except:
                        pass
                else:
                    try:
                        result['weeks'].append(int(part))
                    except:
                        pass

        loc_patterns = [
            r'正心\d+',
            r'[\u4e00-\u9fa5]+\d+',
            r'[A-Za-z]+\d+',
        ]
        for pattern in loc_patterns:
            loc_match = re.search(pattern, text)
            if loc_match:
                result['location'] = loc_match.group(0)
                break

        return result

    def get_courses_for_week(self, week: int) -> Dict[tuple, List[Course]]:
        result = {}
        for (day, period), courses in self.schedule.items():
            week_courses = []
            for course in courses:
                if week in course.weeks:
                    week_courses.append(course)
            if week_courses:
                result[(day, period)] = week_courses
        return result


PERIODS = ['第1,2节', '第3,4节', '第5,6节', '第7,8节', '第9,10节', '第11,12节']
DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
