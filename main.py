import requests
from datetime import datetime
import smtplib
import time

My_email=" " ##Enter your email address
My_pswd=" "  ##Enter your password
my_lat=-33.959991
my_long=18.504793

def iss_overhead():
    response= requests.get(url="http://api.open-notify.org/iss-now.json")
    if response!=200:
        response.raise_for_status()
    data= response.json()
    iss_longitude=float(data["iss_position"]["longitude"])
    iss_latitude=float(data["iss_position"]["latitude"])
    if my_lat-5<=iss_latitude<=my_lat+5 and my_long-5<=iss_longitude<=my_long+5:
        return True


def is_night():
    paremeters = {
        "long": my_long,
        "lat": my_lat,
        "formatted": 0,
    }
    response=requests.get(url="https://api.sunrise-sunset.org/json?",params=paremeters)
    if response!=200:
        response.raise_for_status()
    data=response.json()
    sunrise= int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset= int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now=datetime.now()
    if time_now<=sunrise and time_now>=sunset:
        return True

while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        connection= smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(My_email,My_pswd)
        connection.sendmail(
            from_addr=My_email,
            to_addrs=My_email,
            msg="Subject:Look up\n\n The ISS is above you right now in the sky!!"
        )