import schedule
import time

def job():
    print("I'm working...")

schedule.every().minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)