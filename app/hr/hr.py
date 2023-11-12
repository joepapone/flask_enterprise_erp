
from decimal import Decimal, getcontext

# ------------------------------------------------
#    Classes
# ------------------------------------------------

# Year month class
class YearMonth():
    def __init__(self, year, month):
        self.year = year
        self.month = month

# Earnings and Taxs class
class EarningsTaxes():
    def __init__(self, earnings, taxes, currency):
        self.earnings = earnings
        self.taxes = taxes
        self.currency = currency


# ------------------------------------------------
#    Methods
# ------------------------------------------------

# Calculate work time hours
def work_hours(work_log):
    """ 
    Calculate work time
    :param work_log: Work time log
    :return: Decimal number
    """

    # Initialize counter
    sec = 0
    # Interate list and sum time difference between two datetimes
    for item in work_log:
        sec += item.delta().total_seconds()

    # Integer value of hours
    return round(sec / (60 * 60))


# Calculate work time
def work_time(work_log, period):
    """ 
    Calculate work time
    :param work_log: Work time log
    :param period: Work period index
    :return: Decimal number
    """

    # Initialize counter
    sec = 0
    # Interate list and sum time difference between two datetimes
    for item in work_log:
        sec += item.delta().total_seconds()

    # Hour period
    if period == 1:
        # Float value of hours
        return round(sec / (60 * 60))

    # Day period
    elif period == 2:
        getcontext().prec = 4
        # Value for 8 working hours
        return  Decimal(sec / (60 * 60 * 8))

    # Week period
    elif period == 3:
        getcontext().prec = 4
        # Value for 5 working days
        return  Decimal(sec / (60 * 60 * 8 * 5))

    # Month period
    elif period == 4:
        getcontext().prec = 4
        # Value for 1 working month (depending on working days per month)
        return  Decimal(sec / (60 * 60 * 8 * 20))

    # Year
    elif period == 5:
        getcontext().prec = 4
        # Value for 12 working months
        return  Decimal(sec / (60 * 60 * 8 * 5 * 52))


# Calculate total amount
def total_amount(salary, benefit, time_log):

    earning_sum = 0
    tax_sum = 0
    currency = ''
    # Sum salary
    for i in salary:
        earning_sum += i.get_amount(time_log)
        tax_sum += 1
        currency = i.currency.currency_symbol
    
    print(sum)

    # Sum benefits
    for i in benefit:
        earning_sum += i.get_amount(time_log)
        tax_sum += 1

    print(sum)

    # Create object instance
    obj = EarningsTaxes(earning_sum, tax_sum, currency)

    return obj

'''
from sqlalchemy import func, extract
from datetime import date
from .models import Time_Log
from .. import db

    log = db.session.execute(db
                             .select(Time_Log)
                             .where(Time_Log.employee_id==employee_id)
                             .filter(extract('year', Time_Log.start_time) == date.today().year, extract('month', Time_Log.start_time) == date.today().month)
                             ).scalars().all()

'''