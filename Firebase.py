import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("gymbot-c8ad7-firebase-adminsdk-w62qj-b1e546c2b8.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gymbot-c8ad7-default-rtdb.europe-west1.firebasedatabase.app'
})

def get_workout(username, day):
    ref = db.reference(f'users/{username}/{day}')
    workout = ref.get()
    if workout:
        print(f"Workout found for {username} on {day}: {workout}")
    else:
        print(f"No workout found for {username} on {day}.")
    return workout

def update_workout(username, day, workout):
    ref = db.reference(f'users/{username}/{day}')
    ref.set(workout)
    print(f"Workout updated for {username} on {day}: {workout}")

def increment_week(username):
    ref = db.reference(f'users/{username}/week')
    week = ref.get()
    week = int(week) + 1
    ref.set(week)
    print(f"Week updated for {username} to week number {week}")

def reset_week(username):
    ref = db.reference(f'users/{username}/week')
    week = ref.get()
    week = 1
    ref.set(week)
    print(f"Week reset for {username} to week number {week}")

def get_week(username):
    ref = db.reference(f'users/{username}/week')
    return ref.get()
