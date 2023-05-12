from .models import *
from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Ho_Chi_Minh')


def my_scheduled_job():
    print("zzzzz Jobs run")
    timeStamp = f"3min-{datetime.now(tz):%H:%M}"
    newNumb = NumberDemo.objects.create(name=timeStamp)
    print(newNumb)
    breakpoint()
