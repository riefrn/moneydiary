import json
import datetime
import time
from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from django.db.models import Q
from .models import Period, Spending, Transaction
import datetime


@periodic_task(crontab(minute='*/1'))
def test():
    today = datetime.date.today()
    current_time = datetime.datetime.now()
    # print(current_time)
    # print("Today's date:", today)
    # print("Today's time hour:", current_time.time().hour)
    # print("Today's time minute:", current_time.time().minute)
    work_period = Period.objects.filter(completed=0).first()
    if work_period:
        if work_period.period_date != today:
            print("update")
            changePeriod()
        else:
            print("gak update")
        print(work_period.period_date)
    else:
        s = changePeriod()
    pass


def changePeriod():
    active_schedule = Period.objects.filter(completed=False).first()
    if active_schedule is None:
        # return HttpResponse("There is no active period")
        # active_schedule = Period.objects.filter(completed=False).first()
        # latest_active_period = Period.objects.filter(completed=True).order_by('id').first()
        if active_schedule is None:
            active_schedule = Period()
            active_schedule.save()
            # spending = Spending.objects.filter(enabled=True).all()
            # for spend in spending:
            # if latest_active_period is not None:
            #     latest_work_order = WorkOrder.objects.filter(schedule=work, period=latest_active_period).first()
            #     if latest_work_order is not None:
            #         current = latest_work_order.current

            # new_transaction = Transaction(
            #     spending=spend, period=active_schedule)

            # new_transaction.save()
        else:
            print("masih ada yg aktif")
            # messages.ERROR('period is still active')

    else:
        active_schedule.completed = True
        active_schedule.save()
        active_schedule_new = Period()
        active_schedule_new.save()
        # spending = Spending.objects.filter(enabled=True).all()
        # for spend in spending:
        #     new_transaction = Transaction(
        #         spending=spend, period=active_schedule_new)

        #     new_transaction.save()
        # return HttpResponse(str(active_schedule.period_date) + " is closed")

    return True  # do your thing here
