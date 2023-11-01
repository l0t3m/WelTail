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

            next = generate_nextAlert(int(activity['nextAlert']), int(activity['repeatInterval']))
            db.query(f"UPDATE activities SET nextAlert = '{next}' WHERE activity_id = '{activity['activity_id']}'")
            updatedCounter += 1
            
    return updatedCounter


def getUpcomingAlerts(user_id):
    updateUserAlerts(user_id)
    alerts = []

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = '{user_id}'"):
        next = generateCountdown(int(activity['nextAlert']))
        if next <= generate_timeUntilEndOfDay():
            alerts.append(activity)
    
    return alerts



#################### Time / Unix Functions: ####################

def generate_firstAlert(seconds):
    now = int(datetime.datetime.now().timestamp())
    return int(now) + int(seconds)


def generate_nextAlert(oldAlert:int, intervalValue:int):
    now = int(datetime.datetime.now().timestamp())
    return now + intervalValue - ((now - oldAlert)) % int(intervalValue)


def generate_timeUntilEndOfDay():
    today = datetime.datetime.now()
    start = (datetime.datetime(today.year, today.month, today.day)).timestamp()
    end = start + 86400

    now = int(datetime.datetime.now().timestamp())
    return (int(end - now))



#################### temp: ####################

def generateCountdown(unixTime:int):
    '''Returns the time left in seconds.'''
    now = int(datetime.datetime.now().timestamp())
    return (int(unixTime) - now)

