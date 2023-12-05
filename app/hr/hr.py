
from decimal import Decimal, getcontext
from datetime import datetime, date

# ------------------------------------------------
#    Classes
# ------------------------------------------------

# Days of the week
class DaysOfWeek():
    def __init__(self, num, name, is_today, is_holiday):
        self.num = num
        self.name = name
        self.is_today = is_today
        self.is_holiday = is_holiday
    
    def __repr__(self):
        return f'Day: {self.num}, {self.name}, {self.is_today} ({self.is_holiday})\n'

# Year month class
class YearMonth():
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def get_month(self):
        dt = datetime(self.year, self.month, 1)
        return dt.strftime("%B")
    
    def __repr__(self):
        return f'Year: {self.year}, Month: {self.month}'

# Earnings and Taxs class
class EarningsTaxes():
    def __init__(self, earnings, taxes, currency):
        self.earnings = earnings
        self.taxes = taxes
        self.currency = currency


# ------------------------------------------------
#    Methods
# ------------------------------------------------

# Set calendar days
def set_calendar_days(selected: date, holidays: dict) -> DaysOfWeek:
    """ 
    Set month calandar
    :param selected: Selected date
    :param holidays: Holidays
    :return: Calendar week day names and holidays
    """

    # Set week day names starting with Monday
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # Inialize empty list
    ls = []

    # Get fist day of the month
    first_day = datetime(selected.year, selected.month, 1).weekday()

    # Add to list empty objects until first day of the month
    for i in range(0,6):
        if i == first_day:
            break
        else:
            ls.append(DaysOfWeek('', '', '', ''))
    
    # Add to list objects, with remaining days of the month
    for i in range(1,32):
        try:
            dt = datetime(selected.year, selected.month, i).date()
        except(ValueError):
            break

        # Monday == 0, Sunday == 6
        if dt == datetime.today().date() and dt not in holidays:
            ls.append(DaysOfWeek(i, week[dt.weekday()], 'active', ''))
        elif dt == datetime.today().date() and dt in holidays:
            ls.append(DaysOfWeek(i, week[dt.weekday()], 'active', 'holiday'))
        elif dt not in holidays:
            ls.append(DaysOfWeek(i, week[dt.weekday()], '', ''))
        elif dt in holidays:
            ls.append(DaysOfWeek(i, week[dt.weekday()], '', 'holiday'))

    return ls


# Get business days
def get_business_days(selected: date, holidays: dict) -> int:
    """ 
    Get business days for a selected month
    :param selected: Selected date
    :param holidays: Holidays
    :return: Business days, which exclude weekends and holidays
    """

    business_days = 0
    for i in range(1,32):
        try:
            dt = datetime(selected.year, selected.month, i)
        except(ValueError):
            break

        # Monday == 0, Sunday == 6
        if dt.weekday() < 5 and dt not in holidays:
            business_days +=1

    return business_days


# Calculate hours worked
def cal_hours_worked(log):
    """ 
    Calculate work time
    :param work_log: Attendance log
    :return: Decimal number
    """

    # Initialize counter
    sec = 0
    # Interate attendance log, and sum datetime differences
    for item in log:
        sec += item.delta().total_seconds()

    # Integer value of hours
    return round(sec / (60 * 60))


# Calculate attendance
def cal_attendance(log, total, period):
    """ 
    Calculate attendance
    :param log: Attendance log
    :param total: Total amount
    :param period: Period
    :return: Decimal number
    """

    total

    # Initialize counter
    sec = 0
    # Interate attendance log, and sum datetime differences
    for item in log:
        sec += item.delta().total_seconds()

    # Hours per day
    if period == 1:
        getcontext().prec = 4
        # Value for 8 working hours
        return  Decimal(sec / (60 * 60 * 8))

    # Hours per week
    elif period == 2:
        getcontext().prec = 4
        # Value for 5 working days
        return  Decimal(sec / (60 * 60 * 8 * 5))

    # Hours per month
    elif period == 3:
        getcontext().prec = 4
        # Value for 1 working month (depending on working days per month)
        return  Decimal(sec / (60 * 60 * 8 * 20))

    # Hours per year
    elif period == 5:
        getcontext().prec = 4
        # Value for 12 working months
        return  Decimal(sec / (60 * 60 * 8 * 5 * 52))


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


# Net income
def net_income(gross_income, adjustment, income_tax):
    """ 
    Calculate net income
    :param gross_income: Gross income, consisting of salary
    :param adjustment: Adjusment, consisting of allowances and deductions
    :param income_tax: Income tax, from salary and taxable allowances
    :return: Decimal number
    """

    # Calculate net income
    net_income = gross_income + adjustment - income_tax

    return net_income

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