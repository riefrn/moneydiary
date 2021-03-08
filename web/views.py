from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from moneydiary.settings import TIME_ZONE
from django.utils import timezone
import datetime
import arrow
from api.models import Period, Spending, WeeklyExpenses, Transaction, Note
from api.utils import daterange, last_day_of_month


def index(request):
    list_spending = Spending.get_list_spending()

    # time = timezone.now()
    # print("time 1", time)
    return render(request, 'backoffice/index.html', {'list_spending': list_spending})


def listsweeklyexpenses(request):
    list_weekly_expenses = WeeklyExpenses.get_list_weekly_expenses()
    return render(request, 'backoffice/backoffice-weekly-expenses.html', {'list_weekly_expenses': list_weekly_expenses})


def addweeklyexpenses(request):
    if request.method == 'POST':
        spending = request.POST['spending']
        name = request.POST['name']
        get_spending = Spending.objects.get(id=spending)

        created_date = timezone.now()
        updated_date = timezone.now()

        add_weekly_expenses = WeeklyExpenses(spending=get_spending, name=name,
                                             created_date=created_date, updated_date=updated_date)

        add_weekly_expenses.save()
        return redirect('backoffice-list-weekly-expenses')
    else:
        list_spending = Spending.get_spending_list()
        return render(request, 'backoffice/add-weekly-expenses.html', {
            'list_spending': list_spending,
        })


def editweeklyexpenses(request, weekly_expenses_id):
    if request.method == 'POST':
        spending = request.POST['spending']
        name = request.POST['name']
        get_spending = Spending.objects.get(id=spending)

        updated_date = timezone.now()

        update_weekly_expenses = WeeklyExpenses.objects.get(
            id=weekly_expenses_id)

        update_weekly_expenses.name = name
        update_weekly_expenses.spending = get_spending

        update_weekly_expenses.updated_date = updated_date
        update_weekly_expenses.save()

        return redirect('backoffice-list-weekly-expenses')
    else:
        list_spending = Spending.get_spending_list()
        list_weekly_expenses = WeeklyExpenses.get_detail_weekly_expenses(
            weekly_expenses_id)
        # print(list_weekly_expenses)
        return render(request, 'backoffice/edit-weekly-expenses.html', {'list_weekly_expenses': list_weekly_expenses, 'weekly_expenses_id': weekly_expenses_id, 'list_spending': list_spending})


def deleteweeklyexpenses(request):
    weekly_expenses_id = request.POST['weekly_expenses_id']
    get_weekly_expenses = WeeklyExpenses.objects.get(
        id=weekly_expenses_id)
    get_weekly_expenses.enabled = False
    get_weekly_expenses.save()

    return redirect('backoffice-list-weekly-expenses')


def liststransaction(request):
    active_schedule = Period.objects.filter(completed=False).first()
    list_transaction = Transaction.get_list_transaction(active_schedule)
    return render(request, 'backoffice/backoffice-transaction.html', {'list_transaction': list_transaction})


def addtransactionindex(request, spending_id):
    if request.method == 'POST':
        active_schedule = Period.objects.filter(completed=False).first()
        item = request.POST['item']
        price = request.POST['price']
        weekly_expenses = request.POST['weekly_expenses']
        get_spending = Spending.objects.get(id=spending_id)
        get_weekly_expenses = WeeklyExpenses.objects.get(id=weekly_expenses)
        created_date = timezone.now()
        updated_date = timezone.now()
        add_transaction = Transaction(item=item, price=price, spending=get_spending, weekly_expenses=get_weekly_expenses, period=active_schedule,
                                      created_date=created_date, updated_date=updated_date)

        add_transaction.save()
        return redirect('index')
    else:
        list_spending = Spending.get_detail_spending(spending_id)
        list_weekly_expenses = WeeklyExpenses.get_weekly_expenses_list_by_spending(
            spending_id)
        return render(request, 'backoffice/add-transaction-index.html', {
            'list_weekly_expenses': list_weekly_expenses, 'list_spending': list_spending, 'spending_id': spending_id,
        })


def addtransaction(request):
    if request.method == 'POST':
        active_schedule = Period.objects.filter(completed=False).first()
        item = request.POST['item']
        price = request.POST['price']
        spending = request.POST['spending']
        weekly_expenses = request.POST['weekly_expenses']
        get_spending = Spending.objects.get(id=spending)
        get_weekly_expenses = WeeklyExpenses.objects.get(id=weekly_expenses)
        created_date = timezone.now()
        updated_date = timezone.now()
        add_transaction = Transaction(item=item, price=price, spending=get_spending, weekly_expenses=get_weekly_expenses, period=active_schedule,
                                      created_date=created_date, updated_date=updated_date)

        add_transaction.save()
        return redirect('backoffice-list-transaction')
    else:
        list_spending = Spending.get_spending_list()
        list_weekly_expenses = WeeklyExpenses.get_list_weekly_expenses()
        return render(request, 'backoffice/add-transaction.html', {
            'list_spending': list_spending,
            'list_weekly_expenses': list_weekly_expenses,
        })


def edittransaction(request, transaction_id):
    if request.method == 'POST':
        spending = request.POST['spending']
        weekly_expenses = request.POST['weekly_expenses']
        item = request.POST['item']
        price = request.POST['price']
        get_spending = Spending.objects.get(id=spending)
        get_weekly_expenses = WeeklyExpenses.objects.get(id=weekly_expenses)

        updated_date = timezone.now()

        update_transaction = Transaction.objects.get(
            id=transaction_id)

        update_transaction.item = item
        update_transaction.price = price
        update_transaction.spending = get_spending
        update_transaction.weekly_expenses = get_weekly_expenses

        update_transaction.updated_date = updated_date
        update_transaction.save()

        return redirect('backoffice-list-transaction')
    else:
        list_spending = Spending.get_spending_list()
        list_weekly_expenses = WeeklyExpenses.get_list_weekly_expenses()
        list_transaction = Transaction.get_detail_transaction(
            transaction_id)
        return render(request, 'backoffice/edit-transaction.html', {'list_transaction': list_transaction, 'transaction_id': transaction_id,
                                                                    'list_spending': list_spending, 'list_weekly_expenses': list_weekly_expenses})


def deletetransaction(request):
    transaction_id = request.POST['transaction_id']
    get_transaction = Transaction.objects.get(
        id=transaction_id)
    get_transaction.enabled = False
    get_transaction.save()

    return redirect('backoffice-list-transaction')


def listperiodtransaction(request):
    list_spending = Spending.get_spending_list()
    list_weekly_expenses = WeeklyExpenses.get_weekly_expenses_list()
    current_date = timezone.now()
    desc_current_date_third = arrow.get(current_date).to(TIME_ZONE)
    desc_current_date = desc_current_date_third.strftime("%Y-%m-%d")
    desc_current_date_second = desc_current_date_third.strftime("%d-%b-%Y")

    current_month = str(desc_current_date_third.strftime('%m'))
    current_year = str(desc_current_date_third.strftime('%Y'))

    filter_start_date_of_month = "%s-%s-01" % (current_year, current_month)
    filter_start_date_of_month_second = datetime.datetime.strptime(
        filter_start_date_of_month, '%Y-%m-%d')

    filter_end_date_of_month = last_day_of_month(
        filter_start_date_of_month_second)
    filter_end_date_of_month = filter_end_date_of_month.strftime("%Y-%m-%d")

    dt = datetime.datetime.strptime(desc_current_date, '%Y-%m-%d')
    dt_last = dt+datetime.timedelta(hours=23, minutes=59, seconds=59)
    filter_dt = dt.strftime('%Y-%m-%d')
    filter_dt_last = dt_last.strftime('%Y-%m-%d')
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=7)
    end_second = start + datetime.timedelta(days=6)

    today_plus_one_day = dt + datetime.timedelta(days=1)
    filter_current_date_plus_one_day = today_plus_one_day.strftime('%Y-%m-%d')

    filter_start_date_of_week = start.strftime('%Y-%m-%d')
    filter_end_date_of_week = end.strftime('%Y-%m-%d')

    filter_end_date_of_week_minus_one_day = end_second.strftime('%Y-%m-%d')
    if 'filter_start_date' in request.GET:
        if request.GET['filter_start_date']:
            filter_start_date_second = request.GET['filter_start_date']
            filter_start_date = datetime.datetime.strptime(
                filter_start_date_second, "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_start_date_second = ''
            filter_start_date = ''
    else:
        filter_start_date_second = ''
        filter_start_date = ''

    if 'filter_end_date' in request.GET:
        if request.GET['filter_end_date']:
            filter_end_date_second = request.GET['filter_end_date']
            filter_end_date = datetime.datetime.strptime(
                request.GET['filter_end_date'], "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_end_date_second = ''
            filter_end_date = ''
    else:
        filter_end_date_second = ''
        filter_end_date = ''
    if 'filter_data_transaction' in request.GET:
        if request.GET['filter_data_transaction']:
            filter_data_transaction = request.GET['filter_data_transaction']
        else:
            filter_data_transaction = '1'
    else:
        filter_data_transaction = '1'
    if 'filter_spending' in request.GET:
        if request.GET['filter_spending']:
            filter_spending = request.GET['filter_spending']
        else:
            filter_spending = ''
    else:
        filter_spending = ''
    if 'filter_weekly_expenses' in request.GET:
        if request.GET['filter_weekly_expenses']:
            filter_weekly_expenses = request.GET['filter_weekly_expenses']
        else:
            filter_weekly_expenses = ''
    else:
        filter_weekly_expenses = ''
    if filter_data_transaction == '1':
        list_transaction_data = Spending.list_spending_report_period(
            dt, dt_last, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Today"
    elif filter_data_transaction == '2':
        list_transaction_data = Spending.list_spending_report_period(
            filter_start_date_of_week, filter_end_date_of_week, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Week"
    elif filter_data_transaction == '3':
        list_transaction_data = Spending.list_spending_report_period(
            filter_start_date_of_month, filter_end_date_of_month, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Mounth"
    elif filter_data_transaction == '4':
        list_transaction_data = Spending.list_spending_report_period(
            filter_start_date, filter_end_date, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Custom"
    return render(request, 'backoffice/transaction-period.html', {'list_weekly_expenses': list_weekly_expenses,
                                                                  'list_spending': list_spending, 'filter_start_date': filter_start_date_second, 'filter_end_date': filter_end_date_second,
                                                                  'filter_data_transaction': filter_data_transaction, 'filter_spending': filter_spending, 'filter_weekly_expenses': filter_weekly_expenses,
                                                                  'list_transaction_data': list_transaction_data, 'desc_list_transaction': desc_list_transaction})


def charttransaction(request):
    list_spending = Spending.get_spending_list()
    list_weekly_expenses = WeeklyExpenses.get_weekly_expenses_list()
    current_date = timezone.now()
    desc_current_date_third = arrow.get(current_date).to(TIME_ZONE)
    desc_current_date = desc_current_date_third.strftime("%Y-%m-%d")
    desc_current_date_second = desc_current_date_third.strftime("%d-%b-%Y")

    current_month = str(desc_current_date_third.strftime('%m'))
    current_year = str(desc_current_date_third.strftime('%Y'))

    filter_start_date_of_month = "%s-%s-01" % (current_year, current_month)
    filter_start_date_of_month_second = datetime.datetime.strptime(
        filter_start_date_of_month, '%Y-%m-%d')

    filter_end_date_of_month = last_day_of_month(
        filter_start_date_of_month_second)
    filter_end_date_of_month = filter_end_date_of_month.strftime("%Y-%m-%d")

    dt = datetime.datetime.strptime(desc_current_date, '%Y-%m-%d')
    dt_last = dt+datetime.timedelta(hours=23, minutes=59, seconds=59)
    filter_dt = dt.strftime('%Y-%m-%d')
    filter_dt_last = dt_last.strftime('%Y-%m-%d')
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=7)
    end_second = start + datetime.timedelta(days=6)

    today_plus_one_day = dt + datetime.timedelta(days=1)
    filter_current_date_plus_one_day = today_plus_one_day.strftime('%Y-%m-%d')

    filter_start_date_of_week = start.strftime('%Y-%m-%d')
    filter_end_date_of_week = end.strftime('%Y-%m-%d')

    filter_end_date_of_week_minus_one_day = end_second.strftime('%Y-%m-%d')
    if 'filter_start_date' in request.GET:
        if request.GET['filter_start_date']:
            filter_start_date_second = request.GET['filter_start_date']
            filter_start_date = datetime.strptime(
                filter_start_date_second, "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_start_date_second = ''
            filter_start_date = ''
    else:
        filter_start_date_second = ''
        filter_start_date = ''

    if 'filter_end_date' in request.GET:
        if request.GET['filter_end_date']:
            filter_end_date_second = request.GET['filter_end_date']
            filter_end_date = datetime.strptime(
                request.GET['filter_end_date'], "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_end_date_second = ''
            filter_end_date = ''
    else:
        filter_end_date_second = ''
        filter_end_date = ''
    if 'filter_data_transaction' in request.GET:
        if request.GET['filter_data_transaction']:
            filter_data_transaction = request.GET['filter_data_transaction']
        else:
            filter_data_transaction = '1'
    else:
        filter_data_transaction = '1'
    if 'filter_spending' in request.GET:
        if request.GET['filter_spending']:
            filter_spending = request.GET['filter_spending']
        else:
            filter_spending = ''
    else:
        filter_spending = ''
    if 'filter_weekly_expenses' in request.GET:
        if request.GET['filter_weekly_expenses']:
            filter_weekly_expenses = request.GET['filter_weekly_expenses']
        else:
            filter_weekly_expenses = ''
    else:
        filter_weekly_expenses = ''
    list_transaction_period_today = {'label': [], 'dataset': []}
    list_transaction_period_week = {'label': [], 'dataset': []}
    list_transaction_period_month = {'label': [], 'dataset': []}
    list_chart_spending_today = {'chart': [], 'label': [], 'dataset': ''}
    list_chart_spending_week = {'chart': [], 'label': [], 'dataset': ''}
    list_chart_spending_month = {'chart': [], 'label': [], 'dataset': ''}
    if filter_data_transaction == '1':
        list_chart_spending_today = Transaction.get_total_transaction_per_spending(
            filter_dt, filter_current_date_plus_one_day)
        list_transaction_period_today = Transaction.get_total_transaction_per_period_id(
            filter_start_date_of_week, filter_end_date_of_week_minus_one_day, filter_spending)
        # total_transaction_period = Spending.get_total_transaction_per_period(
        #     filter_dt, filter_dt_last, filter_spending, filter_weekly_expenses)
        # print(list_transaction_period_today)
        desc_list_transaction = "Today"
    elif filter_data_transaction == '2':
        list_chart_spending_week = Transaction.get_total_transaction_per_spending(
            filter_start_date_of_week, filter_end_date_of_week_minus_one_day)
        list_transaction_period_week = Transaction.get_total_transaction_per_period_id(
            filter_start_date_of_week, filter_end_date_of_week_minus_one_day, filter_spending)
        # print(list_transaction_period_week)
        # print(list_transaction_period_week)
        # total_transaction_period = Spending.get_total_transaction_per_period_id(
        #     filter_start_date_of_week, filter_end_date_of_week_minus_one_day, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Week"
    elif filter_data_transaction == '3':
        list_transaction_period_month = Transaction.get_total_transaction_per_period_id(
            filter_start_date_of_month, filter_end_date_of_month, filter_spending)
        list_chart_spending_month = Transaction.get_total_transaction_per_spending(
            filter_start_date_of_month, filter_end_date_of_month)
        # total_transaction_period = Spending.get_total_transaction_per_period_id(
        #     filter_start_date_of_month, filter_end_date_of_month, filter_spending, filter_weekly_expenses)
        desc_list_transaction = "Mounth"
    # elif filter_data_transaction == '4':
    #     if filter_start_date and filter_end_date:
    #         total_transaction_period = Spending.get_total_transaction_per_period_id(
    #             filter_start_date, filter_end_date, filter_spending, filter_weekly_expenses)
    #     desc_list_transaction = "Custom"
    return render(request, 'backoffice/chart-transaction.html', {'list_weekly_expenses': list_weekly_expenses,
                                                                 'list_spending': list_spending, 'filter_start_date': filter_start_date, 'filter_end_date': filter_end_date,
                                                                 'filter_data_transaction': filter_data_transaction, 'filter_spending': filter_spending, 'filter_weekly_expenses': filter_weekly_expenses,
                                                                 #  'transaction_per_spending': transaction_per_spending,
                                                                 'list_chart_spending_today': list_chart_spending_today,
                                                                 'list_chart_spending_week': list_chart_spending_week,
                                                                 'list_chart_spending_month': list_chart_spending_month,
                                                                 'list_transaction_period_today': list_transaction_period_today,
                                                                 'list_transaction_period_week': list_transaction_period_week,
                                                                 'list_transaction_period_month': list_transaction_period_month,
                                                                 #  'total_transaction_period': total_transaction_period,
                                                                 #  'desc_list_transaction': desc_list_transaction
                                                                 })


def transactionperiod(request):
    list_spending = Spending.get_spending_list()
    current_date = timezone.now()
    desc_current_date_third = arrow.get(current_date).to(TIME_ZONE)
    desc_current_date = desc_current_date_third.strftime("%Y-%m-%d")
    desc_current_date_second = desc_current_date_third.strftime("%d-%b-%Y")

    current_month = str(desc_current_date_third.strftime('%m'))
    current_year = str(desc_current_date_third.strftime('%Y'))

    filter_start_date_of_month = "%s-%s-01" % (current_year, current_month)
    filter_start_date_of_month_second = datetime.datetime.strptime(
        filter_start_date_of_month, '%Y-%m-%d')

    filter_end_date_of_month = last_day_of_month(
        filter_start_date_of_month_second)
    filter_end_date_of_month = filter_end_date_of_month.strftime("%Y-%m-%d")

    dt = datetime.datetime.strptime(desc_current_date, '%Y-%m-%d')
    dt_last = dt+datetime.timedelta(hours=23, minutes=59, seconds=59)
    filter_dt = dt.strftime('%Y-%m-%d')
    filter_dt_last = dt_last.strftime('%Y-%m-%d')
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=7)
    end_second = start + datetime.timedelta(days=6)

    today_plus_one_day = dt + datetime.timedelta(days=1)
    filter_current_date_plus_one_day = today_plus_one_day.strftime('%Y-%m-%d')

    filter_start_date_of_week = start.strftime('%Y-%m-%d')
    filter_end_date_of_week = end.strftime('%Y-%m-%d')

    if 'filter_data_transaction' in request.GET:
        if request.GET['filter_data_transaction']:
            filter_data_transaction = request.GET['filter_data_transaction']
        else:
            filter_data_transaction = '1'
    else:
        filter_data_transaction = '1'

    if 'filter_spending' in request.GET:
        if request.GET['filter_spending']:
            filter_spending = request.GET['filter_spending']
        else:
            filter_spending = ''
    else:
        filter_spending = ''

    if 'filter_start_date' in request.GET:
        if request.GET['filter_start_date']:
            filter_start_date_second = request.GET['filter_start_date']
            filter_start_date = datetime.datetime.strptime(
                filter_start_date_second, "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_start_date_second = ''
            filter_start_date = ''
    else:
        filter_start_date_second = ''
        filter_start_date = ''

    if 'filter_end_date' in request.GET:
        if request.GET['filter_end_date']:
            filter_end_date_second = request.GET['filter_end_date']
            filter_end_date = datetime.datetime.strptime(
                request.GET['filter_end_date'], "%d-%b-%Y").strftime('%Y-%m-%d')
        else:
            filter_end_date_second = ''
            filter_end_date = ''
    else:
        filter_end_date_second = ''
        filter_end_date = ''

    if filter_data_transaction == '1':
        list_transaction = Transaction.get_list_transaction_period(
            filter_dt, filter_current_date_plus_one_day, filter_spending)
        desc_list_transaction = "Today"
    elif filter_data_transaction == '2':
        list_transaction = Transaction.get_list_transaction_period(
            filter_start_date_of_week, filter_end_date_of_week, filter_spending)
        desc_list_transaction = "Week"
    elif filter_data_transaction == '3':
        list_transaction = Transaction.get_list_transaction_period(
            filter_start_date_of_month_second, filter_end_date_of_month, filter_spending)
        desc_list_transaction = "Month"
    elif filter_data_transaction == '4':
        list_transaction = Transaction.get_list_transaction_period(
            filter_start_date, filter_end_date, filter_spending)
        desc_list_transaction = "Custom"
    return render(request, 'backoffice/backoffice-transaction-period.html', {'list_transaction': list_transaction,
                                                                             'desc_list_transaction': desc_list_transaction,
                                                                             'filter_data_transaction': filter_data_transaction,
                                                                             'list_spending': list_spending,
                                                                             'filter_spending': filter_spending,
                                                                             'filter_start_date': filter_start_date_second,
                                                                             'filter_end_date': filter_end_date_second,
                                                                             })


def deletetransactionperiod(request):
    transaction_id = request.POST['transaction_id']
    # filter_spending = request.POST['filter_spending']
    # filter_data_transaction = request.POST['filter_data_transaction']
    get_transaction = Transaction.objects.get(
        id=transaction_id)
    get_transaction.enabled = False
    get_transaction.save()
    # if filter_spending == 'all' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=all&filter_data_transaction=1'
    # elif filter_spending == 'all' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=all&filter_data_transaction=2'
    # elif filter_spending == 'all' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=all&filter_data_transaction=3'
    # elif filter_spending == '' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=&filter_data_transaction=1'
    # elif filter_spending == '' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=&filter_data_transaction=2'
    # elif filter_spending == '' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=&filter_data_transaction=3'
    # elif filter_spending == '1' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=1&filter_data_transaction=1'
    # elif filter_spending == '1' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=1&filter_data_transaction=2'
    # elif filter_spending == '1' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=1&filter_data_transaction=3'
    # elif filter_spending == '2' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=2&filter_data_transaction=1'
    # elif filter_spending == '2' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=2&filter_data_transaction=2'
    # elif filter_spending == '2' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=2&filter_data_transaction=3'
    # elif filter_spending == '3' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=3&filter_data_transaction=1'
    # elif filter_spending == '3' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=3&filter_data_transaction=2'
    # elif filter_spending == '3' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=3&filter_data_transaction=3'
    # elif filter_spending == '4' and filter_data_transaction == '1':
    #     next = 'list-transaction-period/?filter_spending=4&filter_data_transaction=1'
    # elif filter_spending == '4' and filter_data_transaction == '2':
    #     next = 'list-transaction-period/?filter_spending=4&filter_data_transaction=2'
    # elif filter_spending == '4' and filter_data_transaction == '3':
    #     next = 'list-transaction-period/?filter_spending=4&filter_data_transaction=3'

    return redirect('backoffice-list-transaction-period')


def listsnote(request):
    list_note = Note.get_list_note()
    return render(request, 'backoffice/backoffice-note.html', {'list_note': list_note})


def addnote(request):
    if request.method == 'POST':
        title = request.POST['title']

        created_date = timezone.now()
        updated_date = timezone.now()

        add_note = Note(title=title,
                        created_date=created_date, updated_date=updated_date)

        add_note.save()
        return redirect('backoffice-list-note')
    else:
        return render(request, 'backoffice/add-note.html', {})


def editnote(request, note_id):
    if request.method == 'POST':
        title = request.POST['title']

        updated_date = timezone.now()

        update_note = Note.objects.get(
            id=note_id)

        update_note.title = title

        update_note.updated_date = updated_date
        update_note.save()

        return redirect('backoffice-list-note')
    else:
        list_note = Note.get_detail_note(
            note_id)
        # print(list_note)
        return render(request, 'backoffice/edit-note.html', {'list_note': list_note, 'note_id': note_id, })


def deletenote(request):
    note_id = request.POST['note_id']
    get_note = Note.objects.get(
        id=note_id)
    get_note.enabled = False
    get_note.save()

    return redirect('backoffice-list-note')


def filterweeklyexpenses(request):
    if 'spending' in request.POST:
        if request.POST['spending']:
            spending = request.POST['spending']
        else:
            spending = ""
    else:
        spending = ""
    if 'q' in request.POST:
        keys = request.POST['q']
    else:
        keys = ""

    get_weekly_expenses_list = WeeklyExpenses.get_weekly_expenses_by_spending(
        spending, keys)

    list_weekly_expenses = []
    for weekly_expenses_list in get_weekly_expenses_list:
        weekly_expenses_id = weekly_expenses_list.id
        weekly_expenses_name = weekly_expenses_list.name

        weekly_expenses_data = {
            'weekly_expenses_id': weekly_expenses_id,
            'weekly_expenses_name': weekly_expenses_name
        }

        list_weekly_expenses.append(weekly_expenses_data)

    return JsonResponse(list_weekly_expenses, safe=False)
