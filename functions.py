#################### Imports: ####################

import db, datetime, time



#################### Main Functions: ####################

def getUserData(username:str=""):
    '''Gets an username, returns the actual user.'''
    if type(username) == str:
        for user in db.get_TableDicts("SELECT * FROM users"):
            if user['username'].lower() == username.lower():
                return user


def getPetActivities(user_id, pet_id):
    '''Returns all the activities for a specific pet.'''
    updateUserAlerts(user_id)
    activities = []
    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE pet_id = '{pet_id}';"):
        activities.append(activity)
    return activities


def getAllActivities(user_id):
    '''Returns all the activities for a specific user.'''
    updateUserAlerts(user_id)
    activities = []
    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}';"):
        activities.append(activity)
    return activities


def getUpcomingAlerts(user_id):
    '''Returns all of today's alerts for a specific user.'''
    updateUserAlerts(user_id)
    alerts = []
    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}' ORDER BY nextAlert;"):
        next = generateCountdown(int(activity['nextAlert']))
        if next <= generate_timeUntilEndOfDay():
            alerts.append(activity)
    return alerts



#################### General Functions: ####################

def updateUserAlerts(user_id):
    '''Checks if the user activities are up to date, if not, updates them.\n
    Returns the amount of activities fixed.'''
    updatedCounter = 0

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}'"):
        if int(activity['nextAlert']) < int(time.time()):
            if int(activity['repeat']) == 0:
                db.query(f"DELETE FROM activities WHERE activity_id = {activity['activity_id']}")
            else:
                next = generate_nextAlert(int(activity['nextAlert']), int(activity['repeatInterval']), int(datetime.datetime.now().timestamp()))
                db.query(f"UPDATE activities SET nextAlert = '{next}' WHERE activity_id = '{activity['activity_id']}'")
                updatedCounter += 1
            
    return updatedCounter


def activity_done(activity_id):
    activity = db.get_TableDicts(f"SELECT * FROM activities WHERE activity_id = '{activity_id}';")
    if activity[0]['repeat'] == 0:
        db.query(f"DELETE FROM activities WHERE activity_id = '{activity_id}';")
    else:
        next = generate_nextAlert(int(activity[0]['nextAlert']), int(activity[0]['repeatInterval']), int(activity[0]['nextAlert']))
        db.query(f"UPDATE activities SET nextAlert = '{next}' WHERE activity_id = '{activity[0]['activity_id']}'")


def reformat_activities(activities:list):
    '''Gets an activity list containing a dict. Returns the dict reformatted.\n
    Created for the petProfile endpoint.'''
    newList = []
    for activity in activities:
        nextAlert = convert_unixToTime(activity['nextAlert'])

        newDict = {
            "user_id": activity['user_id'],
            "pet_id": activity['pet_id'],
            "activity_id": activity['activity_id'],

            "pet_name": db.get_TableDicts(f"SELECT name FROM pets WHERE pet_id = '{activity['pet_id']}';")[0]['name'],
            "type": activity['type'].capitalize(),
            "name": activity['name'],
            "repeat": "Repeating" if activity['repeat'] == 1 else "Once",

            "date": f"{nextAlert.strftime('%d')}/{nextAlert.strftime('%m')}/{nextAlert.strftime('%Y')}",
            "weekday": nextAlert.strftime("%A"),
            "hour": nextAlert.strftime("%H"),
            "minute": nextAlert.strftime("%M"),
            "repeatInterval": activity['repeatInterval']
        }
        newList.append(newDict)
    return newList


def generate_greetingMessage():
    '''Generates a message based on the current time.'''
    hour = datetime.datetime.now().hour
    if hour >= 5 and hour <= 12:
        return "☀️ Good morning"
    elif hour >= 13 and hour <= 17:
        return "🌤️ Good afternoon"
    elif hour >= 18 and hour <= 21:
        return "⛅ Good evening"
    return "🌙 Good night"


def addActivity(user_id:int, pet_id:int, type:str, name:str, nextAlert:str, repeat:str="off", repeatType:str="hours", repeatAmount:str=0):
    newData = reformat_activity(nextAlert, repeat, repeatType,repeatAmount)
    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ({user_id}, {pet_id}, '{type}', '{name}', {newData[0]}, '{newData[1]}', '{newData[2]}');")


def updateActivity(activity_id:int, type:str, name:str, nextAlert:str, repeat:str, repeatType:str, repeatAmount:str=0):
    newData = reformat_activity(nextAlert, repeat, repeatType, repeatAmount)
    db.query(f"UPDATE activities SET type='{type}', name='{name}', repeat='{newData[0]}', nextAlert='{newData[1]}', repeatInterval={newData[2]} WHERE activity_id = {activity_id};")


def reformat_activity(nextAlert:str, repeat:str, repeatType:str, repeatAmount:str=0):
    '''Gets parameters directly from html's format. Returns them reformatted, ready for DB.\n
    Created for the addActivity and editActivity endpoint.'''
    repeatInterval = 0
    repeat = "1" if repeat == "on" else "0"
    if repeat == "1":
        if repeatType == "hours":
            repeatInterval = int(repeatAmount) * 3600
        elif repeatType == "days":
            repeatInterval = int(repeatAmount) * 86400
        elif repeatType == "weeks":
            repeatInterval = int(repeatAmount) * 604800
        else:
            repeatInterval = int(repeatAmount) * 2629743
    year, month, day = nextAlert[:-6].split("-")
    hour, minute = nextAlert[-5:].split(":")
    nextAlert = int((datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))).timestamp())
    return [repeat, nextAlert, repeatInterval]


def deformat_activity(activity:dict):
    '''Gets an activity. Converts the data into a new format.\n
    Created for the activity_edit endpoint.'''
    activity.update({'nextAlert':str(convert_unixToTime(activity['nextAlert'])).replace(" ", "T")})
    rInterval = int(activity['repeatInterval'])
    try:
        if rInterval < 86400:
            rType = "hours"
            rAmount = rInterval / 3600
        elif rInterval < 604800:
            rType = "days"
            rAmount = rInterval / 86400
        elif rInterval < 2629743:
            rType = "weeks"
            rAmount = rInterval / 604800
        else:
            rType = "months"
            rAmount = rInterval / 2629743
    except:
        rType = "hours"
        rAmount = 0
    activity.update({"repeatType" : rType})
    activity.update({"repeatAmount" : int(rAmount)})
    return activity



#################### Time / Unix Functions: ####################

def generate_firstAlert(seconds:int=0):
    '''Generates alert using the current time plus seconds given.'''
    now = int(datetime.datetime.now().timestamp())
    return (int(now) - (int(now) % 60)) + int(seconds)


def generate_nextAlert(oldAlert:int, intervalValue:int, unixTime:int):
    '''Generates next alert using the old alert.'''
    return unixTime + intervalValue - ((unixTime - oldAlert)) % int(intervalValue)


def generate_timeUntilEndOfDay():
    '''Checks how many seconds until the end of the current day.'''
    today = datetime.datetime.now()
    start = (datetime.datetime(today.year, today.month, today.day)).timestamp()
    end = start + 86400
    now = int(datetime.datetime.now().timestamp())
    return (int(end - now))


def convert_unixToTime(unixVal):
    '''Gets a unix value and turns it into a date.'''
    return datetime.datetime.fromtimestamp(int(unixVal))


def generateCountdown(unixTime:int):
    '''Checks how much time is left until the unix time given.'''
    now = int(datetime.datetime.now().timestamp())
    return (int(unixTime) - now)
