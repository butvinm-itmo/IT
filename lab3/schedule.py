from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from uniparser.struct import Element


class WeekDayName(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Campus(Enum):
    LOMO = 0
    KRONVA = 1


class LessonFormat(Enum):
    OFFLINE = 0
    ONLINE = 1
    OFFLINE_AND_ONLINE = 2


class WeekType(Enum):
    EVEN = 0
    ODD = 1


class Lesson(Element):
    subject: str
    teacher: str
    format_: LessonFormat = LessonFormat.OFFLINE
    location: Campus
    start_time: datetime
    duration: timedelta


class Day(Element):
    name: WeekDayName

    _children = [Lesson]


class Week(Element):
    type_: Optional[WeekType]

    _children = [Day]


class GroupSchedule(Element):
    group: str

    _children = [
        Week.specify(type_=WeekType.EVEN),
        Week.specify(type_=WeekType.ODD),
    ]


class UniversitySchedule(Element):    
    _children = [
        GroupSchedule,
    ]
