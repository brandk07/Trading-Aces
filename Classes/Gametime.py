from Defs import fontlist
import pygame

class GameTime:
    DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
    MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
    def __str__(self) -> str:
        return f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'
    def increase_time(self, seconds):
        self.second += seconds
        while self.second >= self.SECONDS_PER_MINUTE:
            self.second -= self.SECONDS_PER_MINUTE
            self.minute += 1
            if self.minute >= self.MINUTES_PER_HOUR:
                self.minute = 0
                self.hour += 1
                if self.hour >= self.HOURS_PER_DAY:
                    self.hour = 0
                    self.day += 1
                    days_in_month = self.DAYS_PER_MONTH[self.month - 1]
                    if self.month == 2 and self.is_leap_year():
                        days_in_month += 1
                    if self.day > days_in_month:
                        self.day = 1
                        self.month += 1
                        if self.month > 12:
                            self.month = 1
                            self.year += 1

    def is_leap_year(self):
        if self.year % 4 != 0:
            return False
        elif self.year % 100 != 0:
            return True
        elif self.year % 400 != 0:
            return False
        else:
            return True

    def get_month_name(self):
        return self.MONTH_NAMES[self.month - 1]

    def get_day_name(self):
        days_since_monday = (self.get_total_minutes() // self.MINUTES_PER_DAY) % 7
        return self.DAY_NAMES[days_since_monday]

    def get_time_string(self):
        return f"{self.get_month_name()} {self.day}, {self.hour}:{self.minute:02d}:{self.second:02d}"
    
    def get_total_minutes(self):
        days_since_jan1 = sum(self.DAYS_PER_MONTH[:self.month - 1]) + self.day - 1
        if self.month > 2 and self.is_leap_year():
            days_since_jan1 += 1
        total_minutes = days_since_jan1 * self.MINUTES_PER_DAY + self.hour * self.MINUTES_PER_HOUR + self.minute
        return total_minutes
    
    def drawgametime(self,screen:pygame.Surface,onlytime:bool):
        if self.hour < 12:
            am_pm = "AM"
        else:
            am_pm = "PM"
        hour_12 = self.hour % 12
        if hour_12 == 0:
            hour_12 = 12
        if onlytime:
            numtime_text, _ = fontlist[50].render(f'{hour_12}:{self.minute:02d} {am_pm}', (255, 255, 255))
        else:
            numtime_text, _ = fontlist[50].render(f'{hour_12}:{self.minute:02d}:{self.second:02d} {am_pm} {self.get_day_name()}', (255, 255, 255))
        numtime_rect = numtime_text.get_rect(center=(100, 950))
        polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
        pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
        pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
        pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
        screen.blit(numtime_text, numtime_rect)
