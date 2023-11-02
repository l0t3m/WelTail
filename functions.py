#################### Imports: ####################

import db, datetime, time



#################### General Functions: ####################

def getUserData(username):
    for user in db.get_TableDicts("SELECT * FROM users"):
        if user['username'].lower() == username.lower():
            return user


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


def getUpcomingAlerts(user_id):
    '''Returns all the alerts for today.'''
    updateUserAlerts(user_id)
    alerts = []

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}'"):
        next = generateCountdown(int(activity['nextAlert']))
        if next <= generate_timeUntilEndOfDay():
            alerts.append(activity)
    
    return alerts


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


def reformat_Activities(activities:list):
    '''Gets an activity list, containing dict. Returns the dicts reformatted.'''
    newList = []

    for activity in activities:
        newDict = {
            "user_id": activity['user_id'],
            "pet_id": activity['pet_id'],
            "activity_id": activity['activity_id'],
            "type": activity['type'],
            "name": activity['name'],
            "repeat": "true" if activity['repeat'] == 1 else "false",
            "time": convert_unixToTime(activity['nextAlert'])
        }

        newList.append(newDict)
    return newList


def activity_done(activity_id):
    activity = db.get_TableDicts(f"SELECT * FROM activities WHERE activity_id = '{activity_id}';")
    
    if activity[0]['repeat'] == 0:
        db.query(f"DELETE FROM activities WHERE activity_id = '{activity_id}';")
    else:
        next = generate_nextAlert(int(activity[0]['nextAlert']), int(activity[0]['repeatInterval']), int(activity[0]['nextAlert']))
        db.query(f"UPDATE activities SET nextAlert = '{next}' WHERE activity_id = '{activity[0]['activity_id']}'")



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
