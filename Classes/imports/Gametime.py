from Defs import fontlist
import pygame
from datetime import datetime, timedelta
from dateutil import parser
from Classes.imports.Bar import SliderBar

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
HOLIDAYS = [(1,1),(1,15),(2,19),(3,29),(5,27),(6,19),(7,4),(9,2),(11,28),(12,25)]
def secsTo930(dt):
    hour = dt.hour
    minute = dt.minute
    hour_diff = (9 - hour) % 24
    combined_minutes = (hour_diff * 60) + (30 - minute)
    if combined_minutes > 0:
        seconds = combined_minutes * 60
    else:
        seconds = (combined_minutes + 1440) * 60  # Add 1 day and adjust minutes

    return seconds
def getTimeStrs(t:datetime):
    return {
    'year': str(t.year),
    'month': MONTHS[t.month-1],
    'day': str(t.day),
    'time': f'{t.hour if t.hour <= 12 else t.hour-12}:{t.minute:02d}',
    'dayname': WEEKDAYS[t.weekday()],
    'monthname': MONTHS[t.month-1],
    'ampm': 'AM' if t.hour < 12 else 'PM'
    }

DFORMAT = "%m/%d/%Y %I:%M:%S %p"
class GameTime:
    def __init__(self,time:str,gamespeed) -> None:
        # self.time = datetime.strptime(time,DFORMAT)
        self.speedBar = SliderBar(gamespeed,[(247, 223, 0),(110,110,110)],barcolor=[(255,255,255),(200,200,200)])# the bar for the gameplay speed
        self.time = parser.parse(time)

        self.fastforwarding = False# used for refrence in other classes

    def __str__(self) -> str:
        return self.time.strftime(DFORMAT)
    def getDate(self):
        return self.time.strftime("%m/%d/%Y")

    def setTimeStr(self,time:str):
        self.time = datetime.strptime(time,DFORMAT)
    
    def getCurrentQuarter(self):
        """"Returns the current quarter of the year : 1-4"""
        return (self.time.month-1)//3+1

    def advanceTime(self,autoFastForward:bool,fastforwardspeed:int):
        """Advances the time by a certain amount of seconds and returns if it is a new day"""
        fastforward = self.fastforwarding
        if autoFastForward and not self.isOpen()[0]:
            if (secs:=secsTo930(self.time)) < fastforwardspeed:
                seconds = secs
            else:
                seconds = fastforwardspeed
            self.fastforwarding = True
        else:
            seconds = self.speedBar.getValue()# seconds to advance
            self.fastforwarding = False
        self.time += timedelta(seconds=seconds)
        return (self.fastforwarding) and (fastforward != self.fastforwarding)# returns if fastforwarding is stopped (new trading day) and 
    
    def getTime(self):
        return self.time.strftime(DFORMAT)
        # return self.time

    def isOpen(self,time:datetime=None):
        """Checks if the market is open or not
        returns a tuple of (bool,reason)"""
        assert time == None or isinstance(time,datetime), "time must be a datetime object"
        if time == None:
            time = self.time
        if (time.month,time.day) in HOLIDAYS:
            return False, 'Holiday'
        if WEEKDAYS[time.weekday()] in ['Saturday','Sunday']:
            return False, 'Weekend'
        if not(((time.hour == 9 and time.minute >= 30) or time.hour > 9) and time.hour < 16):
            return False, 'Off Hours'
        return True, 'Open'
    
    def timeAt(self,secondsago):
        """returns the time at a certain amount of seconds ago"""
        return (self.time - timedelta(seconds=secondsago)).strftime(DFORMAT)
    
    def getTimeStrings(self, dt=None):
        """
        Returns formatted time strings as a dictionary.
        Args:
            dt: Optional datetime object. Uses self.time if None
        Returns: Dictionary with formatted time components
        """
        t = dt if dt else self.time
        return getTimeStrs(t)
        
        
    
    # def getRenders(self,sizes):
    #     """Sizes is (yearsize,monthsize,daysize,timesize,daynamesize,monthnamesize)"""
    #     year = fontlist[sizes[0]].render(str(self.time.year),(200,200,200))[0]
    #     month = fontlist[sizes[1]].render(MONTHS[self.time.month-1],(200,200,200))[0]
    #     day = fontlist[sizes[2]].render(str(self.time.day)+',',(200,200,200))[0]
    #     minute = fontlist[sizes[3]].render(f'{self.time.hour if self.time.hour <= 12 else self.time.hour-12}:{self.time.minute:02d}',(200,200,200))[0]
    #     dayname = fontlist[sizes[4]].render(WEEKDAYS[self.time.weekday()]+',',(200,200,200))[0]
    #     monthname = fontlist[sizes[5]].render(MONTHS[self.time.month-1],(200,200,200))[0]
    #     ampm = fontlist[sizes[3]].render('AM' if self.time.hour < 12 else 'PM',(200,200,200))[0]

    #     return [year,month,day,minute,dayname,monthname,ampm]

    def skipText(self):
        """Used for drawing the bar for the game speed"""
        return "SKIPPING" if self.fastforwarding else True




# from Defs import fontlist
# import pygame
# DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# MINUTES_PER_HOUR = 60
# HOURS_PER_DAY = 24
# MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
# SECONDS_PER_MINUTE = 60
# MINUTES_PER_HOUR = 60
# HOURS_PER_DAY = 24
# MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
# MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# HOLIDAYS = [(1,1),(1,15),(2,19),(3,29),(5,27),(6,19),(7,4),(9,2),(11,28),(12,25)]
# def interpolate_color(color1, color2, ratio):
#     """Interpolate between two colors"""
#     return tuple(max(0, min(255, int(c1 * (1 - ratio) + c2 * ratio))) for c1, c2 in zip(color1, color2))
# class GameTime:    

#     def __init__(self, year, month, day, hour, minute, weekday):
#         self.weekdayoffset = DAY_NAMES.index(weekday)-7
#         self.rendercache = {}
#         self.year = year
#         self.month = month
#         self.day = day
#         self.hour = hour
#         self.minute = minute
#         self.second = 0
#         self.colonrenders = [fontlist[i].render(':',(200,200,200))[0] for i in range(1,200)]

#         self.mdhfunc = lambda size,color : [fontlist[size].render(str(i)+',',color)[0] for i in range(1,32)]
#         self.numfunc = lambda size,color : [fontlist[size].render("0"+str(i) if i < 10 else str(i),color)[0] for i in range(0,60)]
#         self.ampmfunc = lambda size,color : [fontlist[size].render('AM',color)[0],fontlist[size].render('PM',color)[0]]
#         self.yearfunc = lambda size,color : [fontlist[size].render("Year "+str(self.year),color)[0]]
#         self.daynamesfunc = lambda size,color : {dayname : fontlist[size].render(dayname+',',color)[0] for dayname in DAY_NAMES}
#         self.monthnamesfunc = lambda size,color : {monthname : fontlist[size].render(monthname,color)[0] for monthname in MONTH_NAMES}

#         self.daynames = {}# size : [name : render]
#         self.monthnames = {}# size : [name : render]

#         self.fastforward = False
#         self.mdhrenders = {}# size : [renders]
#         self.lasttimerender = (None,None)
#         # self.renderednumbers = {}# size : [renders]
#         # self.ampmtext = {}# size : [renders]
#         self.renderedyear = {}# size : [[year,render],[differentyear,render],etc...]
#     def __str__(self) -> str:
#         return f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'
#     def add_second(self):
#         self.second += 1
#         if self.second >= 60: 
#             self.add_minute(); self.second = 0
#     def add_minute(self):
#         self.minute += 1
#         if self.minute >= 60: 
#             self.add_hour(); self.minute = 0
#     def add_hour(self):
#         self.hour += 1
#         if self.hour > 24: 
#             self.add_day(); self.hour = 1
#     def add_day(self):
#         self.day += 1
#         if self.is_leap_year() and self.month == 2:
#             if self.day > 29: 
#                 self.add_month(); self.day = 1
#         elif self.day > DAYS_PER_MONTH[self.month-1]: 
#             self.add_month(); self.day = 1
#     def add_month(self):
#         self.month += 1
#         if self.month > 12: 
#             self.add_year(); self.month = 1
#     def add_year(self):
#         self.year += 1

    
#     def increase_time(self,seconds:int,autofastforward):
        # for i in range(seconds):
        #     self.add_second()
        # if not self.isOpen()[0] and autofastforward:
        #     self.fastforward = True
        
#         return self.year, self.month, self.day, self.hour, self.minute, self.second


#     def is_leap_year(self):
#         if self.year % 4 == 0:
#             if self.year % 400 == 0:
#                 return True
#             elif self.year % 100 == 0:
#                 return False
#             return True
#         return False

#     def getrenders(self,monthsize,daysize,yearsize,timesize,daynamesize,monthnamesize):
#         """returns a list of renders for the month,day,time(minute:Day Am/Pm), dayname, monthname parameters are the sizes of the renders (in return order)"""
#         if daynamesize not in self.daynames:# if the day name size is not in the cache
#             self.daynames[daynamesize] = self.daynamesfunc(daynamesize,(150,150,150))
#         dayname = self.daynames[daynamesize][self.get_day_name()]

#         if monthnamesize not in self.monthnames:# if the month name size is not in the cache
#             self.monthnames[monthnamesize] = self.monthnamesfunc(monthnamesize,(150,150,150))
#         monthname = self.monthnames[monthnamesize][self.get_month_name()]

#         if monthsize not in self.mdhrenders:# if the month size is not in the cache
#             self.mdhrenders[monthsize] = self.mdhfunc(monthsize,(150,150,150))
#         month = self.mdhrenders[monthsize][self.month-1]

#         if daysize not in self.mdhrenders:# if the day size is not in the cache
#             self.mdhrenders[daysize] = self.mdhfunc(daysize,(150,150,150))
#         day = self.mdhrenders[daysize][self.day-1]

#         if yearsize not in self.renderedyear:# if the year size is not in the cache
#             # size : [[year,render],[differentyear,render],etc...]
#             self.renderedyear[yearsize] = [[self.year,self.yearfunc(yearsize,(150,150,150))]]
#             year = self.renderedyear[yearsize][0][1]
#         else:# if the year size is in the cache
#             if self.year in (justnum:=[year[0] for year in self.renderedyear[yearsize]]):# if the year is already in the cache
#                 year = self.renderedyear[yearsize][justnum.index(self.year)][1]
#             else:# if the year is not in the size cache
#                 self.renderedyear[yearsize].append([self.year,self.yearfunc(yearsize,(150,150,150))])
#                 year = self.renderedyear[yearsize][-1][1]

#         time = f'{self.hour if self.hour <= 12 else self.hour-12}:{self.minute:02d} {str("AM" if self.hour < 12 else "PM")}'
#         if time == self.lasttimerender[0]:
#             time_render = self.lasttimerender[1]
#         else:
#             # make the color of the time render go from a light yellow to dark blue depending on the time of day
#             color1 = (238, 255, 0)
#             color2 = (128, 0, 255)
#             ratio = (((self.hour)*60+(self.minute)) / (24*60))
#             color = interpolate_color(color1, color2, ratio)
#             # print(color)
#             time_render = fontlist[timesize].render(time,color)[0]
#             self.lasttimerender = (time,time_render)


#         return [month,day,year[0],time_render,dayname,monthname]

    # def isOpen(self):
    #     """Checks if the market is open or not
    #     returns a tuple of (bool,reason)"""
    #     # if (self.month,self.day) in HOLIDAYS:
    #     #     return False, 'Holiday'
    #     # if self.get_day_name() in ['Saturday','Sunday']:
    #     #     return False, 'Weekend'
    #     # if not(((self.hour == 9 and self.minute >= 30) or self.hour > 9) and self.hour < 16):
    #     #     return False, 'Off Hours'
    #     return True, 'Open'
#     def timeAt(self,secondsago):
#         """returns the time at a certain amount of seconds ago"""
#         year = self.year
#         month = self.month
#         day = self.day
#         hour = self.hour
#         minute = self.minute
#         second = self.second
#         for i in range(secondsago):
#             second -= 1
#             if second < 0:
#                 second = 59
#                 minute -= 1
#                 if minute < 0:
#                     minute = 59
#                     hour -= 1
#                     if hour < 0:
#                         hour = 23
#                         day -= 1
#                         if day < 1:
#                             day = DAYS_PER_MONTH[month-1]
#                             month -= 1
#                             if month < 1:
#                                 month = 12
#                                 year -= 1
#         return year,month,day,hour,minute,second
    

#     def get_month_name(self):
#         return MONTH_NAMES[self.month - 1]

#     def get_day_name(self):
#         days_since_monday = ((self.get_total_minutes() // MINUTES_PER_DAY)+self.weekdayoffset) % 7
#         return DAY_NAMES[days_since_monday]

#     def get_time_string(self):
#         return f"{self.get_month_name()} {self.day}, {self.hour}:{self.minute:02d}:{self.second:02d}"
    
#     def get_total_minutes(self):
#         days_since_jan1 = sum(DAYS_PER_MONTH[:self.month - 1]) + self.day - 1
#         if self.month > 2 and self.is_leap_year():
#             days_since_jan1 += 1
#         total_minutes = days_since_jan1 * MINUTES_PER_DAY + self.hour * MINUTES_PER_HOUR + self.minute
#         return total_minutes
    
#     def drawgametime(self,screen:pygame.Surface,onlytime:bool):
#         if self.hour < 12:
#             am_pm = "AM"
#         else:
#             am_pm = "PM"
#         hour_12 = self.hour % 12
#         if hour_12 == 0:
#             hour_12 = 12
#         if onlytime:
#             numtime_text, _ = fontlist[50].render(f'{hour_12}:{self.minute:02d} {am_pm}', (255, 255, 255))
#         else:
#             numtime_text, _ = fontlist[50].render(f'{hour_12}:{self.minute:02d}:{self.second:02d} {am_pm} {self.get_day_name()}', (255, 255, 255))
#         numtime_rect = numtime_text.get_rect(center=(100, 950))
#         polygon_points = [(25, 925), (175, 925), (175, 975), (25, 975)]
#         pygame.draw.polygon(screen, (80, 80, 80), polygon_points)
#         pygame.draw.polygon(screen, (255, 255, 255), polygon_points, 5)
#         pygame.draw.polygon(screen, (0, 0, 0), polygon_points, 1)
#         screen.blit(numtime_text, numtime_rect)
    
