import database
import scheduler
import scheduler.trigger
import scraper
import datetime
import math


def dummy(x):
    print("HI", x)


def do(wkn: str):
    database.Database().insert(scraper.get(wkn))


def main():
    sched = scheduler.Scheduler()
    # sched.cyclic(datetime.timedelta(seconds=1), do("A1CX3T"))
    with open("stocks.txt", "r") as file:
        data = file.readlines()
    for a, line in enumerate(data, start=1):
        sched.once(datetime.datetime.now() + datetime.timedelta(seconds=10), do, args=line.strip())
        print(sched)
        sched.cyclic(datetime.timedelta(minutes=60, seconds=(math.log(a, 10) * 20 + math.ceil(a)) / 10), do,
                     args=line.strip())
        print(sched)
    while True:
        sched.exec_jobs()


if __name__ == "__main__":
    main()
