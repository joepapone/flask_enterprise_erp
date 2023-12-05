from datetime import datetime, date


# Days of the week
class DaysOfWeek():
    def __init__(self, num, name, is_today, is_holiday):
        self.num = num
        self.name = name
        self.is_today = is_today
        self.is_holiday = is_holiday
    
    def __repr__(self):
        return f'Day: {self.num}, {self.name}, {self.is_today} ({self.is_holiday})\n'


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

    '''
    <div id="modal-select" class="modal">
        <span onclick="document.getElementById('modal-select').style.display='none'" class="close" title="Year Modal" >×</span>
        <form class="modal-content" action="" method="POST" enctype=multipart/form-data id='form-select'>
            <div class="modal-content">
                <h1 id="title-select"></h1>
            </div>

            <div class=" {% if form.year.errors %}error{% endif %}">
                <div class="">
                    <label class="field-label" for="event_id">{{ form.year.label }}</label>
                </div>
                <div class="">
                    {{ form.year }}
                    {%- for error in form.year.errors %}
                    {%- if form.year.errors %}<div class="error-message">{{ error }}</div>{%- endif %}
                    {%- endfor %}
                </div>
            </div>

            <div class="clearfix">
                <button class="cancelbtn modal-button" type="button" 
                    onclick="document.getElementById('modal-select').style.display='none'">Cancel
                </button>
                <input class="deletebtn modal-button" type="submit" value="Submit" 
                    onclick="document.getElementById('modal-select').style.display='none'">
            </div>
        </form>
    </div>


    '''



#holidays = {datetime(2023, 12, 1), datetime(2023, 12, 8), datetime(2023, 12, 25)}

holidays = [datetime(2023, 12, 1).date(), datetime(2023, 12, 8).date(), datetime(2023, 12, 25).date()]
print(set_calendar_days(datetime(2023, 13, 1), holidays))