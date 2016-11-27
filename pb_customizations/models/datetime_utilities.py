from datetime import datetime

def valid_date(datestring, time_format):
    try:
        datetime.strptime(datestring, time_format)
        return True
    except ValueError:
        return False
    
def compute_hours_mins(start_date_string, stop_date_string, time_format):
    hours, minutes = 0, 0
    if start_date_string and stop_date_string:
        start_date = datetime.strptime(start_date_string, time_format)
        stop_date = datetime.strptime(stop_date_string, time_format)
        seconds = (stop_date - start_date).seconds
        if seconds:
            hours = seconds/(60 * 60)
            minutes = (seconds/(60)) % 60
    return '%s:%s'%(hours, minutes)