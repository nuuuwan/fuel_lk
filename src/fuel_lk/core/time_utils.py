from utils import timex

FORMAT = '%Y-%m-%d %H:%M'
TIMEZONE_OFFSET = timex.TIMEZONE_OFFSET_LK

def get_times(t_str):

    try:
        t_ut = timex.parse_time(t_str, FORMAT, TIMEZONE_OFFSET)
        t_str2 = timex.format_time(t_ut, FORMAT, TIMEZONE_OFFSET)
    except ValueError:
        t_ut = None
        t_str2 = None

    return t_ut, t_str2
