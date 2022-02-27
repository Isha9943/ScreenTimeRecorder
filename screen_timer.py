from __future__ import print_function
import time
import os
from activity import *
import json
import datetime
import sys
import win32gui
import uiautomation as auto
import calendar

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True


def find_day(date):
    date = date.weekday()
    return calendar.day_name[date], date

def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


def get_active_window():
    _active_window_name = None
    window = win32gui.GetForegroundWindow()
    _active_window_name = win32gui.GetWindowText(window)
    return _active_window_name


def get_url():
    window = win32gui.GetForegroundWindow()
    # print(window)
    browser_control = auto.ControlFromHandle(window)
    # print(browser_control)
    edit = browser_control.Name.split('-')
    # print(edit)
    edit = edit[0]
    # print(edit)
    return 'https://' + edit


with open('activities.json','w') as f:
    f.close()

with open('weekly_activities.json','w') as f:
    f.close()

curr_weekly_activities = {
                     'Monday':[],
                     'Tuesday':[],
                     "Wednesday":[],
                     'Thursday':[],
                     'Friday':[],
                     'Saturday':[],
                     'Sunday':[]
                     }

prev_week_activities = {
                     'Monday':[],
                     'Tuesday':[],
                     "Wednesday":[],
                     'Thursday':[],
                     'Friday':[],
                     'Saturday':[],
                     'Sunday':[]
                     }
with open('weekly_activities.json', 'w') as f:
    json.dump(prev_week_activities, f, indent=4, )
    f.close()

for i in days:
    curr_weekly_activities[i] = []
    prev_week_activities[i] = []

if "activities.json":
    os.remove("activities.json")
    with open('activities.json','w') as f:
        f.close()
        pass

if "weekly_activities.json" :
    os.remove("weekly_activities.json")
    with open('weekly_activities.json','w') as f:
        f.close()
        pass

try:
    while True:
        prev_week_activities = curr_weekly_activities.copy()
        if "weekly_activities.json":
            os.remove("weekly_activities.json")
            with open('weekly_activities.json', 'w') as f:
                json.dump(prev_week_activities, f, indent=4)
                f.close()
        day, idx = find_day(datetime.datetime.now())
        if datetime.datetime.now().minute == 0 and datetime.datetime.now().second==0 and datetime.datetime.hour==0:
            curr_weekly_activities[days[idx-1]]=activeList.serialize()
            prev = idx-1
            if "activities.json":
                os.remove("activities.json")
                with open('activities.json', 'w') as f:
                    f.close()
                    pass

            if prev == -1:
                prev_week_activities = curr_weekly_activities.copy()
                curr_weekly_activities = {
                     'Monday':[],
                     'Tuesday':[],
                     "Wednesday":[],
                     'Thursday':[],
                     'Friday':[],
                     'Saturday':[],
                     'Sunday':[]
                     }
                if "weekly_activities.json":
                    os.remove("weekly_activities.json")
                    with open('weekly_activities.json', 'w') as f:
                        json.dump(prev_week_activities,f,indent=4)
                        f.close()



        curr_weekly_activities[days[idx]] = activeList.serialize()
        previous_site = ""
        new_window_name = get_active_window()
        if 'Google Chrome' in new_window_name:
            new_window_name = 'Google ( '+url_to_name(get_url())+')'
        elif 'Mozilla' in new_window_name:
            new_window_name = 'Mozilla ( ' + url_to_name(get_url()) + ')'

        if active_window_name != new_window_name:
            print(active_window_name,'\n')
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)

                if not exists:
                    activity = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
                    json_file.close()
            first_time = False
            active_window_name = new_window_name

        time.sleep(1)



except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
