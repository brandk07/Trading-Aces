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
        self.rendercache = {}
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.mdhrenders = [fontlist[55].render(str(i),(255,255,255))[0] for i in range(1,32)]
        self.renderednumbers = [fontlist[55].render("0"+str(i) if i < 10 else str(i),(255,255,255))[0] for i in range(0,60)]
        self.ampmtext = [fontlist[50].render('AM',(255,255,255))[0],fontlist[50].render('PM',(255,255,255))[0]]
        self.renderedyear = [self.year,fontlist[55].render(str(self.year),(255,255,255))[0]]
    def __str__(self) -> str:
        return f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'
    def add_second(self):
        self.second += 1
        if self.second >= 60: 
            self.add_minute(); self.second = 0
    def add_minute(self):
        self.minute += 1
        if self.minute >= 60: 
            self.add_hour(); self.minute = 0
    def add_hour(self):
        self.hour += 1
        if self.hour > 24: 
            self.add_day(); self.hour = 1
    def add_day(self):
        self.day += 1
        if self.is_leap_year() and self.month == 2:
            if self.day > 29: 
                self.add_month(); self.day = 1
        elif self.day > self.DAYS_PER_MONTH[self.month-1]: 
            self.add_month(); self.day = 1
    def add_month(self):
        self.month += 1
        if self.month > 12: 
            self.add_year(); self.month = 1
    def add_year(self):
        self.year += 1


    def increase_time(self,seconds:int):
        for i in range(seconds):
            self.add_second()


    def is_leap_year(self):
        if self.year % 4 == 0:
            if self.year % 400 == 0:
                return True
            elif self.year % 100 == 0:
                return False
            return True
        return False

    def getrenders(self):
        month = self.mdhrenders[self.month-1]
        day = self.mdhrenders[self.day-1]
        if self.renderedyear[0] == self.year:
            year = self.renderedyear[1]
        else:
            year = self.renderedyear[1] = fontlist[55].render(str(self.year),(255,255,255))[0]
        hour = self.mdhrenders[self.hour-1 if self.hour <= 12 else self.hour-13]
        minute = self.renderednumbers[self.minute]
        ampm = self.ampmtext[0 if self.hour < 12 else 1]
        return [month,day,year,hour,minute,ampm]




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
    
