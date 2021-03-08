from django.db import models
from moneydiary.settings import TIME_ZONE
from django.conf import settings
from django.utils import timezone
import arrow
import json
from django.db.models import Q, Sum
from datetime import datetime, date, timedelta
from api.utils import daterange, last_day_of_month


class Period(models.Model):
    period_date = models.DateField(default=timezone.now)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()
    completed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return u'%s' % (self.period_date)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()

        return super(Period, self).save(*args, **kwargs)

    @classmethod
    def get_period_list(cls):
        list_period = Period.objects.filter(completed=False).first()
        return list_period

    @classmethod
    def get_list_period(cls):
        list_period = Period.objects.filter(completed=False).first()

        period_list = []
        for listperiod in list_period:
            period_id = listperiod.id
            period_date = listperiod.date
            period_completed = listperiod.completed
            period_created_date = listperiod.created_date
            period_desc_created_date = arrow.get(
                period_created_date).to(TIME_ZONE)
            period_desc_created_date = period_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            period_updated_date = listperiod.updated_date
            period_desc_updated_date = arrow.get(
                period_updated_date).to(TIME_ZONE)
            period_desc_updated_date = period_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            period_data = {
                'id': period_id,
                'date': period_date,
                'completed': period_completed,
            }
            period_list.append(period_data)
        return period_list

    @classmethod
    def get_detail_period(cls, period_id):
        listperiod = cls.objects.get(id=period_id)
        period_id = listperiod.id
        period_date = listperiod.date
        period_completed = listperiod.completed

        period_created_date = listperiod.created_date
        period_desc_created_date = arrow.get(
            period_created_date).to(TIME_ZONE)
        period_desc_created_date = period_desc_created_date.strftime(
            "%d-%b-%Y %H:%M")

        period_updated_date = listperiod.updated_date
        period_desc_updated_date = arrow.get(
            period_updated_date).to(TIME_ZONE)
        period_desc_updated_date = period_desc_updated_date.strftime(
            "%d-%b-%Y %H:%M")

        list_period = {
            'id': period_id,
            'date': period_date,
            'completed': period_completed,
            'created_date': period_created_date,
            'desc_created_date': period_desc_created_date,
            'updated_date': period_updated_date,
            'desc_updated_date': period_desc_updated_date,

        }
        return list_period


class Spending(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    enabled = models.BooleanField(default=True, null=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()

    def __str__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()

        return super(Spending, self).save(*args, **kwargs)

    @classmethod
    def get_spending_list(cls):
        list_spending = cls.objects.filter(enabled=True).order_by('id')
        return list_spending

    @classmethod
    def get_list_spending(cls):
        list_spending = cls.objects.filter(enabled=True).order_by('id')
        active_period = Period.objects.filter(completed=False).first()
        spending_list = []
        for listspending in list_spending:
            spending_id = listspending.id
            spending_name = listspending.name
            spending_enabled = listspending.enabled
            if spending_id == 1:
                spending_status = '<i class="nc-icon nc-diamond text-primary"></i>'
            elif spending_id == 2:
                spending_status = '<i class="nc-icon nc-cart-simple text-secondary"></i>'
            elif spending_id == 3:
                spending_status = '<i class="nc-icon nc-controller-modern text-success"></i>'
            elif spending_id == 4:
                spending_status = '<i class="nc-icon nc-ambulance text-danger"></i>'
            else:
                spending_status = ''
            list_transaction = Transaction.objects.filter(Q(enabled=True) &
                                                          Q(period=active_period) & Q(spending=spending_id))
            get_total_price = list_transaction.aggregate(
                total_price=Sum('price'))
            len_transaction = len(list_transaction)
            if get_total_price['total_price']:
                total_price = get_total_price['total_price']
            else:
                total_price = 0
            if float(total_price) > 0.0:
                total_transaction_desc_price_second = "{0:,.2f}".format(
                    total_price)
                total_transaction_desc_price = "Rp " + total_transaction_desc_price_second

                if '.00' in total_transaction_desc_price:
                    total_transaction_desc_price = total_transaction_desc_price.replace(
                        '.00', '')
            else:
                total_transaction_desc_price = "Rp 0"
            transaction_list = []
            for lt in list_transaction:
                if lt.price:
                    transaction_price = lt.price
                else:
                    transaction_price = 0
                if float(transaction_price) > 0.0:
                    transaction_desc_price_second = "{0:,.2f}".format(
                        transaction_price)
                    transaction_desc_price = "Rp " + transaction_desc_price_second

                    if '.00' in transaction_desc_price:
                        transaction_desc_price = transaction_desc_price.replace(
                            '.00', '')
                else:
                    transaction_desc_price = "Rp 0"
                transaction_data = {
                    'price': transaction_price,
                    'desc_price': transaction_desc_price,
                }
                transaction_list.append(transaction_data)
            spending_created_date = listspending.created_date
            spending_desc_created_date = arrow.get(
                spending_created_date).to(TIME_ZONE)
            spending_desc_created_date = spending_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            spending_updated_date = listspending.updated_date
            spending_desc_updated_date = arrow.get(
                spending_updated_date).to(TIME_ZONE)
            spending_desc_updated_date = spending_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            spending_data = {
                'id': spending_id,
                'name': spending_name,
                'enabled': spending_enabled,
                'spending_status': spending_status,
                'transaction_list': transaction_list,
                'len_transaction': len_transaction,
                'total_price': total_price,
                'desc_total_price': total_transaction_desc_price,
            }
            spending_list.append(spending_data)
        return spending_list

    @classmethod
    def get_detail_spending(cls, spending_id):
        listspending = cls.objects.get(id=spending_id)
        spending_id = listspending.id
        spending_name = listspending.name
        spending_enabled = listspending.enabled

        spending_created_date = listspending.created_date
        spending_desc_created_date = arrow.get(
            spending_created_date).to(TIME_ZONE)
        spending_desc_created_date = spending_desc_created_date.strftime(
            "%d-%b-%Y %H:%M")

        spending_updated_date = listspending.updated_date
        spending_desc_updated_date = arrow.get(
            spending_updated_date).to(TIME_ZONE)
        spending_desc_updated_date = spending_desc_updated_date.strftime(
            "%d-%b-%Y %H:%M")

        list_spending = {
            'id': spending_id,
            'name': spending_name,
            'enabled': spending_enabled,
            'created_date': spending_created_date,
            'desc_created_date': spending_desc_created_date,
            'updated_date': spending_updated_date,
            'desc_updated_date': spending_desc_updated_date,

        }
        return list_spending

    @classmethod
    def list_spending_report_period(cls, filter_start_date='', filter_end_date='', filter_spending='', filter_weekly_expenses=''):
        list_spending = cls.objects.filter(enabled=True)
        if filter_spending:
            if filter_spending != 'all':
                list_spending = list_spending.filter(
                    id=filter_spending)

        if filter_weekly_expenses:
            if filter_weekly_expenses != 'all':
                list_spending = list_spending.filter(
                    weekly_expenses_spending=filter_weekly_expenses)
        spending_list = []
        grand_total_spending = 0
        for listspending in list_spending:
            spending_id = listspending.id
            spending_name = listspending.name
            list_transaction = Transaction.get_summary_transaction(
                filter_start_date, filter_end_date, spending_id, filter_weekly_expenses)
            total_spending = list_transaction['total_price']
            grand_total_spending += total_spending
            if float(total_spending) > 0.0:
                desc_total_spending_second = "{0:,.2f}".format(
                    total_spending)
                desc_total_spending = "Rp " + desc_total_spending_second

                if '.00' in desc_total_spending:
                    desc_total_spending = desc_total_spending.replace(
                        '.00', '')
            else:
                desc_total_spending = "Rp 0"
            if float(grand_total_spending) > 0.0:
                desc_grand_total_spending_second = "{0:,.2f}".format(
                    grand_total_spending)
                desc_grand_total_spending = "Rp " + desc_grand_total_spending_second

                if '.00' in desc_grand_total_spending:
                    desc_grand_total_spending = desc_grand_total_spending.replace(
                        '.00', '')
            else:
                desc_grand_total_spending = "Rp 0"
            spending_data = {
                'id': spending_id,
                'name': spending_name,
                'desc_total_price': desc_total_spending,
                'grand_total_spending': grand_total_spending,
                'desc_grand_total_spending': desc_grand_total_spending,
            }
            spending_list.append(spending_data)
        return spending_list

    @classmethod
    def get_total_transaction_per_period(cls, filter_start_date, filter_end_date, filter_spending='', filter_weekly_expenses=''):
        convert_start_date = datetime.strptime(
            filter_start_date, '%Y-%m-%d').date()
        convert_end_date = datetime.strptime(
            filter_end_date, '%Y-%m-%d').date()

        end_date_plus_one_day = convert_end_date + timedelta(days=1)

        calc_date = 1

        list_spending = Spending.get_spending_list()
        spending_list = []
        for ls in list_spending:
            spending_name = ls.name
            spending_id = ls.id
            transaction_chart_label = []
            transaction_chart_dataset = []
            calc = 0
            for single_date in daterange(convert_start_date, end_date_plus_one_day):
                proposal_date = single_date.strftime('%Y-%m-%d')
                desc_proposal_date = single_date.strftime('%d %b')

                list_transaction = Transaction.get_summary_transaction(
                    proposal_date, '', spending_id, filter_weekly_expenses)
                # print(list_transaction)
                # print(list_transaction['real_price'])
                transaction_chart_label.append(desc_proposal_date)
                transaction_chart_dataset.append(
                    float(list_transaction['total_price']))
                calc += 1
                transaction_chart_list = {
                    'label': transaction_chart_label,
                    'dataset': transaction_chart_dataset,
                    'calc': calc
                }
            spending_data = {
                'name': json.dumps(spending_name),
                'transaction_chart_list': json.dumps(transaction_chart_list),
            }
            spending_list.append(spending_data)
        return spending_list


class WeeklyExpenses(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    spending = models.ForeignKey(
        Spending, related_name='weekly_expenses_spending', blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    enabled = models.BooleanField(default=True, null=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()

    def __str__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()

        return super(WeeklyExpenses, self).save(*args, **kwargs)

    @classmethod
    def get_weekly_expenses_list(cls):
        list_weekly_expenses = cls.objects.filter(
            enabled=True).order_by('name')
        return list_weekly_expenses

    @classmethod
    def get_list_weekly_expenses(cls):
        list_weekly_expenses = cls.objects.filter(
            enabled=True).order_by('name')

        weekly_expenses_list = []
        for listweeklyexpenses in list_weekly_expenses:
            weekly_expenses_id = listweeklyexpenses.id
            weekly_expenses_name = listweeklyexpenses.name
            weekly_expenses_enabled = listweeklyexpenses.enabled
            if listweeklyexpenses.spending.id:
                list_spending_id = listweeklyexpenses.spending.id
            else:
                list_spending_id = ""
            list_spending = Spending.get_detail_spending(list_spending_id)
            spending_id = list_spending['id']
            spending_name = list_spending['name']
            weekly_expenses_created_date = listweeklyexpenses.created_date
            weekly_expenses_desc_created_date = arrow.get(
                weekly_expenses_created_date).to(TIME_ZONE)
            weekly_expenses_desc_created_date = weekly_expenses_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            weekly_expenses_updated_date = listweeklyexpenses.updated_date
            weekly_expenses_desc_updated_date = arrow.get(
                weekly_expenses_updated_date).to(TIME_ZONE)
            weekly_expenses_desc_updated_date = weekly_expenses_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            weekly_expenses_data = {
                'id': weekly_expenses_id,
                'name': weekly_expenses_name,
                'enabled': weekly_expenses_enabled,
                'spending_id': spending_id,
                'spending_name': spending_name,
                'created_date': weekly_expenses_created_date,
                'desc_created_date': weekly_expenses_desc_created_date,
                'updated_date': weekly_expenses_updated_date,
                'desc_updated_date': weekly_expenses_desc_updated_date,
            }
            weekly_expenses_list.append(weekly_expenses_data)
        return weekly_expenses_list

    @classmethod
    def get_weekly_expenses_list_by_spending(cls, spending_id):
        list_weekly_expenses = cls.objects.filter(
            enabled=True, spending=spending_id).order_by('name')
        return list_weekly_expenses

    @classmethod
    def get_detail_weekly_expenses(cls, weekly_expenses_id):
        listweeklyexpenses = cls.objects.get(id=weekly_expenses_id)
        weekly_expenses_id = listweeklyexpenses.id
        weekly_expenses_name = listweeklyexpenses.name
        weekly_expenses_enabled = listweeklyexpenses.enabled

        if listweeklyexpenses.spending.id:
            list_spending_id = listweeklyexpenses.spending.id
        else:
            list_spending_id = ""
        list_spending = Spending.get_detail_spending(list_spending_id)
        spending_id = list_spending['id']
        spending_name = list_spending['name']

        weekly_expenses_created_date = listweeklyexpenses.created_date
        weekly_expenses_desc_created_date = arrow.get(
            weekly_expenses_created_date).to(TIME_ZONE)
        weekly_expenses_desc_created_date = weekly_expenses_desc_created_date.strftime(
            "%d-%b-%Y %H:%M")

        weekly_expenses_updated_date = listweeklyexpenses.updated_date
        weekly_expenses_desc_updated_date = arrow.get(
            weekly_expenses_updated_date).to(TIME_ZONE)
        weekly_expenses_desc_updated_date = weekly_expenses_desc_updated_date.strftime(
            "%d-%b-%Y %H:%M")

        list_weekly_expenses = {
            'id': weekly_expenses_id,
            'name': weekly_expenses_name,
            'enabled': weekly_expenses_enabled,
            'spending_id': spending_id,
            'spending_name': spending_name,
            'created_date': weekly_expenses_created_date,
            'desc_created_date': weekly_expenses_desc_created_date,
            'updated_date': weekly_expenses_updated_date,
            'desc_updated_date': weekly_expenses_desc_updated_date,

        }
        return list_weekly_expenses

    @classmethod
    def get_weekly_expenses_by_spending(cls, spending_id='', keys=''):
        list_weekly_expenses = WeeklyExpenses.objects.all()

        if spending_id:
            list_weekly_expenses = list_weekly_expenses.filter(
                spending=spending_id)

        if keys:
            list_weekly_expenses = list_weekly_expenses.filter(
                name__icontains=keys)

        return list_weekly_expenses


class Transaction(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(default=0)
    spending = models.ForeignKey(
        Spending, related_name='transaction_spending', blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    weekly_expenses = models.ForeignKey(
        WeeklyExpenses, related_name='weekly_expenses_transaction', blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    enabled = models.BooleanField(default=True, null=True)
    period = models.ForeignKey(Period, related_name='transaction_period',
                               blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()

    def __str__(self):
        return u'%s' % (self.spending)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()

        return super(Transaction, self).save(*args, **kwargs)

    @classmethod
    def get_transaction_list(cls):
        list_transaction = cls.objects.filter()
        return list_transaction

    @classmethod
    def get_list_transaction(cls, period):
        list_transaction = cls.objects.filter(
            Q(enabled=True) & Q(period=period))
        # print(list_transaction)
        transaction_list = []
        for listtransaction in list_transaction:
            transaction_id = listtransaction.id
            transaction_item = listtransaction.item
            transaction_price = listtransaction.price
            if float(transaction_price) > 0.0:
                transaction_desc_price_second = "{0:,.2f}".format(
                    transaction_price)
                transaction_desc_price = "Rp " + transaction_desc_price_second

                if '.00' in transaction_desc_price:
                    transaction_desc_price = transaction_desc_price.replace(
                        '.00', '')
            else:
                transaction_desc_price = "Rp 0"
            transaction_spending = listtransaction.spending
            transaction_weekly_expenses = listtransaction.weekly_expenses
            transaction_period = listtransaction.period
            transaction_enabled = listtransaction.enabled
            transaction_created_date = listtransaction.created_date
            transaction_desc_created_date = arrow.get(
                transaction_created_date).to(TIME_ZONE)
            transaction_desc_created_date = transaction_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            transaction_updated_date = listtransaction.updated_date
            transaction_desc_updated_date = arrow.get(
                transaction_updated_date).to(TIME_ZONE)
            transaction_desc_updated_date = transaction_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            transaction_data = {
                'id': transaction_id,
                'item': transaction_item,
                'price': transaction_price,
                'transaction_desc_price': transaction_desc_price,
                'spending': transaction_spending,
                'weekly_expenses': transaction_weekly_expenses,
                'enabled': transaction_enabled,
                'created_date': transaction_created_date,
                'desc_created_date': transaction_desc_created_date,
                'updated_date': transaction_updated_date,
                'desc_updated_date': transaction_desc_updated_date,


            }
            transaction_list.append(transaction_data)
        return transaction_list

    @classmethod
    def get_detail_transaction(cls, transaction_id):
        listtransaction = cls.objects.get(id=transaction_id)
        transaction_id = listtransaction.id
        transaction_item = listtransaction.item
        transaction_price = listtransaction.price
        transaction_spending = listtransaction.spending
        transaction_spending_id = listtransaction.spending.id
        transaction_weekly_expenses = listtransaction.weekly_expenses
        transaction_weekly_expenses_id = listtransaction.weekly_expenses.id
        transaction_period = listtransaction.period
        transaction_enabled = listtransaction.enabled

        transaction_created_date = listtransaction.created_date
        transaction_desc_created_date = arrow.get(
            transaction_created_date).to(TIME_ZONE)
        transaction_desc_created_date = transaction_desc_created_date.strftime(
            "%d-%b-%Y %H:%M")

        transaction_updated_date = listtransaction.updated_date
        transaction_desc_updated_date = arrow.get(
            transaction_updated_date).to(TIME_ZONE)
        transaction_desc_updated_date = transaction_desc_updated_date.strftime(
            "%d-%b-%Y %H:%M")

        list_transaction = {
            'id': transaction_id,
            'item': transaction_item,
            'price': transaction_price,
            'spending': transaction_spending,
            'weekly_expenses': transaction_weekly_expenses,
            'spending_id': transaction_spending_id,
            'weekly_expenses_id': transaction_weekly_expenses_id,
            'enabled': transaction_enabled,
            'created_date': transaction_created_date,
            'desc_created_date': transaction_desc_created_date,
            'updated_date': transaction_updated_date,
            'desc_updated_date': transaction_desc_updated_date,

        }
        return list_transaction

    @classmethod
    def get_total_transaction_per_spending(cls, filter_start_date, filter_end_date):
        convert_start_date = datetime.strptime(
            filter_start_date, '%Y-%m-%d').date()

        start_month = convert_start_date.strftime("%m").lstrip('0')
        start_year = convert_start_date.strftime("%Y")

        convert_end_date = datetime.strptime(
            filter_end_date, '%Y-%m-%d').date()

        end_month = convert_end_date.strftime("%m").lstrip('0')
        end_year = convert_end_date.strftime("%Y")

        list_spending = Spending.get_spending_list()

        spending_data_set = []
        chart_list = []
        chart_label = ['Rp']
        for listspending in list_spending:
            spending_id = listspending.id
            spending_name = str(listspending.name)

            total_transaction = 0
            for single_date in daterange(convert_start_date, convert_end_date):
                proposal_date = single_date.strftime('%Y-%m-%d')
                desc_proposal_date = single_date.strftime('%d %b')

                list_total_transaction = Transaction.get_summary_transaction(
                    filter_start_date, filter_end_date, spending_id, '')
                grandtotal = float(list_total_transaction['real_price'])
            chart_data = {
                'y': spending_name,
                'a': grandtotal,
            }
            chart_list.append(chart_data)

        list_chart = {
            'chart': json.dumps(chart_list),
            'label': json.dumps(chart_label),
            'dataset': '',
        }
        return list_chart

    @classmethod
    def get_summary_transaction(cls, filter_start_date='', filter_end_date='', filter_spending='', filter_weekly_expenses=''):
        list_transaction = cls.objects.filter(enabled=True)
        list_transaction = list_transaction.values('id', 'price').distinct()
        if filter_start_date and filter_end_date:
            if filter_start_date == filter_end_date:
                list_transaction = list_transaction.filter(
                    created_date=filter_start_date)
            else:

                list_transaction = list_transaction.filter(created_date__gte=filter_start_date,
                                                           created_date__lte=filter_end_date)
        elif filter_start_date and not filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__gte=filter_start_date)
        elif not filter_start_date and filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__lte=filter_end_date)
        if filter_spending:
            if filter_spending != 'all':
                list_transaction = list_transaction.filter(
                    spending_id=filter_spending)

        if filter_weekly_expenses:
            if filter_weekly_expenses != 'all':
                list_transaction = list_transaction.filter(
                    weekly_expenses=filter_weekly_expenses)

        total_price = 0
        real_price = 0
        for ls in list_transaction:
            if ls['price']:
                transaction_price = ls['price']
            else:
                transaction_price = 0
            real_price += float(transaction_price)
            total_price += float(transaction_price)
        # if float(total_price) > 0.0:
        #     if '.0' in str(total_price):
        #         desc_total_price = str(
        #             total_price).rstrip('0').rstrip('.')
        #     else:
        #         desc_total_price = total_price

        #     desc_total_price = "{:,}".format(float(desc_total_price))
        # else:
        #     desc_total_price = "0"
        # print(total_price)
        transaction_list = {
            'total_price': total_price,
            'real_price': real_price,
        }
        return transaction_list

    @classmethod
    def get_summary_transaction_id(cls, filter_start_date='', filter_end_date='', filter_spending='', filter_weekly_expenses=''):
        list_transaction = cls.objects.filter(enabled=True)
        list_transaction = list_transaction.values('id', 'price').distinct()
        if filter_start_date and filter_end_date:
            if filter_start_date == filter_end_date:
                list_transaction = list_transaction.filter(
                    created_date=filter_start_date)
            else:
                list_transaction = list_transaction.filter(created_date__gt=filter_start_date,
                                                           created_date__lt=filter_end_date)
        elif filter_start_date and not filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__gte=filter_start_date)
        elif not filter_start_date and filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__lte=filter_end_date)
        if filter_spending:
            if filter_spending != 'all':
                list_transaction = list_transaction.filter(
                    spending_id=filter_spending)
        if filter_weekly_expenses:
            if filter_weekly_expenses != 'all':
                list_transaction = list_transaction.filter(
                    weekly_expenses=filter_weekly_expenses)
        total_price = 0
        real_price = 0
        price = 0
        for ls in list_transaction:
            if ls['price']:
                price = ls['price']
            else:
                price = 0
            if ls['price']:
                transaction_price = ls['price']
            else:
                transaction_price = 0
            real_price += float(transaction_price)
            total_price += float(transaction_price)
        if float(total_price) > 0.0:
            if '.0' in str(total_price):
                desc_total_price = str(
                    total_price).rstrip('0').rstrip('.')
            else:
                desc_total_price = total_price

            desc_total_price = "{:,}".format(float(desc_total_price))
        else:
            desc_total_price = "0"
        transaction_list = {
            'price': price,
            'total_price': total_price,
            'real_price': real_price,
        }
        return transaction_list

    @classmethod
    def get_total_transaction_per_period_id(cls, filter_start_date, filter_end_date, filter_spending):
        convert_start_date = datetime.strptime(
            filter_start_date, '%Y-%m-%d').date()
        convert_end_date = datetime.strptime(
            filter_end_date, '%Y-%m-%d').date()

        end_date_plus_one_day = convert_end_date + timedelta(days=1)
        calc_date = 1

        transaction_chart_label = []
        transaction_chart_dataset = []
        for single_date in daterange(convert_start_date, end_date_plus_one_day):
            proposal_date = single_date.strftime('%Y-%m-%d')
            desc_proposal_date = single_date.strftime('%d %b')

            list_total_transaction = Transaction.get_summary_transaction_id(
                proposal_date, '', filter_spending, '')
            transaction_chart_dataset.append(
                float(list_total_transaction['price']))
            transaction_chart_label.append(desc_proposal_date)
            # print('11', filter_spending)
        transaction_chart_list = {
            'label': transaction_chart_label,
            'dataset': transaction_chart_dataset
        }

        return transaction_chart_list

    @classmethod
    def get_list_transaction_period(cls, filter_start_date='', filter_end_date='', filter_spending=''):
        list_transaction = cls.objects.filter(enabled=True)
        if filter_start_date and filter_end_date:
            if filter_start_date == filter_end_date:
                list_transaction = list_transaction.filter(
                    created_date=filter_start_date)
            else:
                list_transaction = list_transaction.filter(created_date__gte=filter_start_date,
                                                           created_date__lte=filter_end_date)
        elif filter_start_date and not filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__gte=filter_start_date)
        elif not filter_start_date and filter_end_date:
            list_transaction = list_transaction.filter(
                created_date__lte=filter_end_date)
        # list_transaction = list_transaction.filter(created_date__gte=filter_start_date,
        #                                            created_date__lte=filter_end_date)
        if filter_spending:
            if filter_spending != 'all':
                list_transaction = list_transaction.filter(
                    spending_id=filter_spending)
        # print(list_transaction)
        list_transaction = list_transaction.order_by('-created_date')
        transaction_list = []
        for listtransaction in list_transaction:
            transaction_id = listtransaction.id
            transaction_item = listtransaction.item
            transaction_price = listtransaction.price
            if float(transaction_price) > 0.0:
                transaction_desc_price_second = "{0:,.2f}".format(
                    transaction_price)
                transaction_desc_price = "Rp " + transaction_desc_price_second

                if '.00' in transaction_desc_price:
                    transaction_desc_price = transaction_desc_price.replace(
                        '.00', '')
            else:
                transaction_desc_price = "Rp 0"
            transaction_spending = listtransaction.spending
            transaction_weekly_expenses = listtransaction.weekly_expenses
            transaction_period = listtransaction.period
            transaction_enabled = listtransaction.enabled
            transaction_created_date = listtransaction.created_date
            transaction_desc_created_date = arrow.get(
                transaction_created_date).to(TIME_ZONE)
            transaction_desc_created_date = transaction_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            transaction_updated_date = listtransaction.updated_date
            transaction_desc_updated_date = arrow.get(
                transaction_updated_date).to(TIME_ZONE)
            transaction_desc_updated_date = transaction_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            transaction_data = {
                'id': transaction_id,
                'item': transaction_item,
                'price': transaction_price,
                'desc_transaction_price': transaction_desc_price,
                'spending': transaction_spending,
                'weekly_expenses': transaction_weekly_expenses,
                'enabled': transaction_enabled,
                'created_date': transaction_created_date,
                'desc_created_date': transaction_desc_created_date,
                'updated_date': transaction_updated_date,
                'desc_updated_date': transaction_desc_updated_date,


            }
            transaction_list.append(transaction_data)
        return transaction_list


class Note(models.Model):
    title = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True, null=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField()

    def __str__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()

        self.updated_date = timezone.now()

        return super(Note, self).save(*args, **kwargs)

    @classmethod
    def get_note_list(cls):
        list_note = cls.objects.filter(
            enabled=True).order_by('-created_date')
        return list_note

    @classmethod
    def get_list_note(cls):
        list_note = cls.objects.filter(
            enabled=True).order_by('-created_date')

        note_list = []
        for listnote in list_note:
            note_id = listnote.id
            note_title = listnote.title
            note_enabled = listnote.enabled
            note_created_date = listnote.created_date
            note_desc_created_date = arrow.get(
                note_created_date).to(TIME_ZONE)
            note_desc_created_date = note_desc_created_date.strftime(
                "%d-%b-%Y %H:%M")

            note_updated_date = listnote.updated_date
            note_desc_updated_date = arrow.get(
                note_updated_date).to(TIME_ZONE)
            note_desc_updated_date = note_desc_updated_date.strftime(
                "%d-%b-%Y %H:%M")

            note_data = {
                'id': note_id,
                'title': note_title,
                'enabled': note_enabled,
                'created_date': note_created_date,
                'desc_created_date': note_desc_created_date,
                'updated_date': note_updated_date,
                'desc_updated_date': note_desc_updated_date,
            }
            note_list.append(note_data)
        return note_list

    @classmethod
    def get_detail_note(cls, note_id):
        listnote = cls.objects.get(id=note_id)
        note_id = listnote.id
        note_title = listnote.title
        note_enabled = listnote.enabled

        note_created_date = listnote.created_date
        note_desc_created_date = arrow.get(
            note_created_date).to(TIME_ZONE)
        note_desc_created_date = note_desc_created_date.strftime(
            "%d-%b-%Y %H:%M")

        note_updated_date = listnote.updated_date
        note_desc_updated_date = arrow.get(
            note_updated_date).to(TIME_ZONE)
        note_desc_updated_date = note_desc_updated_date.strftime(
            "%d-%b-%Y %H:%M")

        list_note = {
            'id': note_id,
            'title': note_title,
            'enabled': note_enabled,
            'created_date': note_created_date,
            'desc_created_date': note_desc_created_date,
            'updated_date': note_updated_date,
            'desc_updated_date': note_desc_updated_date,

        }
        return list_note
