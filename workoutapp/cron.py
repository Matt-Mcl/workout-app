import re
import os
import time
import pytz
import django
import mechanize
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workoutapp.settings')

django.setup()

# This needs to come after django setup
from workouts.models import *

load_dotenv()

br = mechanize.Browser()

br.open("https://www.mywellness.com/cloud/Training/")

br.select_form(nr=0)

br.form['UserBinder.Username'] = os.getenv("STRENGTH_EMAIL")
br.form['UserBinder.Password'] = os.getenv("STRENGTH_PASSWORD")

br.submit()

today = datetime.now().strftime("%d/%m/%Y")
threedaysago = (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y")

response = br.open(f"https://www.mywellness.com/cloud/Training/LastPerformedWorkoutSession/?fromDate={threedaysago}&toDate={today}")

soup = BeautifulSoup(response.read(), "html.parser")

# Get list of workouts
workouts = soup.find_all("div", attrs={"class": "row odd"})

# Loop through workouts
for w in workouts:
    date = w.find("div", attrs={"class": "cell date"}).text

    sesssion_id = w.find("input", attrs={"name": "hdSessionIdCR"})["value"]

    response = br.open(f"https://www.mywellness.com/cloud/Training/PerformedWorkoutSession/?idCR={sesssion_id}&day={date}")

    soup = BeautifulSoup(response.read(), "html.parser")

    intensity_score = "".join([num.text for num in soup.find_all("span", attrs={"class": re.compile("number*")})])

    intensity_string = soup.find("div", attrs={"class": "goal"}).text.strip()

    workout_info = soup.find_all("dd")

    duration = workout_info[1].text.split(" ")[0]
    moves = workout_info[2].text.split(" ")[0]

    try:
        strength_workout = StrengthWorkout.objects.create(
            date=datetime.strptime(date, "%Y%m%d").replace(tzinfo=pytz.UTC),
            intensity_string=intensity_string,
            intensity=intensity_score,
            duration=duration,
            moves=moves
        )
    except django.db.utils.IntegrityError:
        # Workout already exists, continue
        continue

    # Get each exercise
    exercises = w.find_all("a", attrs={"class": "clearfix"})

    for e in exercises:
        name = e.find("span", attrs={"class": "note"}).text

        if name in ["Run", "Bike"]:
            continue

        # Get data from link
        time.sleep(1)
        response = br.open(e["href"])

        soup = BeautifulSoup(response.read(), "html.parser")

        sets = soup.find_all("td")

        # Loop through sets
        for item in range(0, len(sets), 5):

            strength_exercise = StrengthExercise.objects.create(
                name=name,
                set=sets[item].text,
                reps_to_do=sets[item+1].text,
                reps_done=sets[item+2].text,
                kg_to_do=sets[item+3].text,
                kg_done=sets[item+4].text
            )

            strength_workout.exercises.add(strength_exercise)
