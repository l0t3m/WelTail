#################### Imports: ####################

import db, datetime, time



#################### Main Functions: ####################

def getUserData(username):
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
    '''Returns all the alerts for today.'''
    updateUserAlerts(user_id)
    alerts = []

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}' ORDER BY nextAlert"):
        next = generateCountdown(int(activity['nextAlert']))
        if next <= generate_timeUntilEndOfDay():
            alerts.append(activity)
    
    return alerts



#################### General Functions: ####################

def updateUserAlerts(user_id):
    '''Checks if the user activities are up to date, if not, fixes them. \n
    Returns the amount of activities fixed.'''
    updatedCounter = 0

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}'"):
        if int(activity['nextAlert']) < int(time.time()):
            if int(activity['repeat']) == 0:
                db.query(f"DELETE FROM activities WHERE activity_id = {activity['activity_id']}")

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


def reformat_Activities(activities:list):
    '''Gets an activity list, containing dict. Returns the dicts reformatted.'''
    newList = []

    for activity in activities:
        newDict = {
            "user_id": activity['user_id'],
            "pet_id": activity['pet_id'],
            "activity_id": activity['activity_id'],

            "pet_name": db.get_TableDicts(f"SELECT name FROM pets WHERE pet_id = '{activity['pet_id']}';")[0]['name'],
            "type": activity['type'].capitalize(),
            "name": activity['name'],
            "repeat": "Repeating" if activity['repeat'] == 1 else "Once",
            "hour": convert_unixToTime(activity['nextAlert']).strftime("%H"),
            "minute": convert_unixToTime(activity['nextAlert']).strftime("%M"),
            "repeatInterval": activity['repeatInterval']
        }
        newList.append(newDict)
    return newList


def generate_greetingMessage():
    hour = datetime.datetime.now().hour

    if hour >= 5 and hour <= 12:
        return "☀️ Good morning"
    elif hour >= 13 and hour <= 17:
        return "🌤️ Good afternoon"
    elif hour >= 18 and hour <= 21:
        return "⛅ Good evening"
    return "🌙 Good night"


def addActivity(user_id, pet_id, type, name, nextAlert:str, repeat:str, repeatType:str, repeatAmount):
    repeat = "1" if repeat == "on" else "0"

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
    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ({user_id}, {pet_id}, '{type}', '{name}', {repeat}, '{nextAlert}', '{repeatInterval}');")


def deformat_Activity(activity:dict):
    '''Gets an activity.\n Converts the data into new format.'''
    # "repeatInterval": "21600",
    activity.update({'nextAlert':str(convert_unixToTime(activity['nextAlert'])).replace(" ", "T")})

    rInterval = int(activity['repeatInterval'])
    
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
    
    activity.update({"repeatType" : rType})
    activity.update({"repeatAmount" : int(rAmount)})
    
    return activity


#################### Time / Unix Functions: ####################

def generate_firstAlert(seconds):
    now = int(datetime.datetime.now().timestamp())
    return int(now) + int(seconds)


def generate_nextAlert(oldAlert:int, intervalValue:int, unixTime:int):
    return unixTime + intervalValue - ((unixTime - oldAlert)) % int(intervalValue)


def generate_timeUntilEndOfDay():
    today = datetime.datetime.now()
    start = (datetime.datetime(today.year, today.month, today.day)).timestamp()
    end = start + 86400

    now = int(datetime.datetime.now().timestamp())
    return (int(end - now))


def convert_unixToTime(unixVal):
    return datetime.datetime.fromtimestamp(int(unixVal))


def generateCountdown(unixTime:int):
    '''Returns the time left in seconds.'''
    now = int(datetime.datetime.now().timestamp())
    return (int(unixTime) - now)
