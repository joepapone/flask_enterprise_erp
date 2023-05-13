from decimal import Decimal
import statistics

from .models import Cal
from .socket_client import conn_socket


# function decorator
def count_raw(func):
    def wrapper(*args, **kwargs):
        # increment count
        wrapper.count += 1
        #wrapper.values.append(wrapper.count) # test mean
        if func() != '---':
            wrapper.values.append(func())
            wrapper.mean = statistics.mean(wrapper.values)
        wrapper.store = False

        # reset counter and list
        if wrapper.count ==10:
            wrapper.count = 0
            wrapper.values = []
            wrapper.store = True
        #print(' Count = {0}\n Values = {1}\n Mean = {2}\n Store = {3}'.format(wrapper.count,wrapper.values, wrapper.mean, wrapper.store))

        # call function being decorated and return result
        return func(*args, **kwargs)

    # initialize variables
    wrapper.count = 0
    wrapper.mean = 0
    wrapper.values = []
    wrapper.store = False

    # return the new decorated function
    return wrapper


def calc_weight(cal: dict, raw_value: str) -> str:
    '''
    Calculate weight based on stored calibration slope and bias, and
    load cell voltage value provided by A/D converter and microcontroller
    via web socket.
    '''
    weight = None
    try:
        #print('raw: {}'.format(raw_value))
        slope = (cal.span - cal.zero)/(Decimal(cal.raw_span) - Decimal(cal.raw_zero))
        bias = cal.offset
        weight = slope*Decimal(raw_value) + bias

    except (ZeroDivisionError, TypeError, NameError) as e:
        print('Failed to execute formula {}\n'.format(e))

    return weight


@count_raw
def get_raw() -> Decimal:
    '''
    Get raw value
    '''
    server_data = conn_socket()
    if server_data == None:
        print('Socket server failed')
        return '---'

    else:
        # convert raw value
        raw_value = Decimal(server_data.decode())

        print(' {0}. Raw value: {1}'.format(get_raw.count, round(raw_value,3)))
        return round(raw_value,3)


def get_weight() -> Decimal:
    '''
    Get weight value
    '''
    server_data = conn_socket()
    if server_data == None:
        print('Socket server failed')
        return '---'

    else:
        # load calibration data from database
        cal = Cal.query.get(1)

        # convert calculated weight value
        weight_value = Decimal(calc_weight(cal, server_data.decode()))

        print('Weight: {0} kg from raw value {1}'.format(round(weight_value,0), server_data))
        return round(weight_value,0)


def get_mean() -> Decimal:
    '''
    Get raw value's average value
    '''
    return round(get_raw.mean,3)