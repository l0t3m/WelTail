#################### Imports: ####################

import db, datetime, time



#################### General Functions: ####################

def getUserData(username):
    for user in db.get_TableDicts("SELECT * FROM users"):
        if user['username'] == username:
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



#################### Time / Unix Functions: ####################

def generateUnixTime(minutes):
    return 60 * minutes

def generate_firstAlert(minutes):
    now = int(datetime.datetime.now().timestamp())
    return int(now) + int(generateUnixTime(minutes))

def generate_nextAlert(oldAlert:int, intervalValue:int):
    now = int(datetime.datetime.now().timestamp())
    return now + intervalValue - ((now - oldAlert)) % int(intervalValue)



#################### temp: ####################

def generateCountdown(unixTime):
    '''Returns the time left in seconds.'''
    now = int(datetime.datetime.now().timestamp())
    return (int(unixTime) - now)

