from utils import timex


def get_times(t_str):
    try:
        t_ut = timex.parse_time(t_str, '%Y-%m-%d %H:%M')
        t_str2 = timex.format_time(t_ut)
    except ValueError:
        t_ut = None
        t_str2 = None

    return t_ut, t_str2
