import pyfiglet


def format_time(t):
    minutes = " ".join(list("{:02d}".format(t.minutes)))
    seconds = " ".join(list("{:02d}".format(t.seconds)))
    return pyfiglet.figlet_format("{} : {}".format(minutes, seconds))


def value_exceeds_max(value, max_value) -> bool:
    return int(value) > max_value


def is_int(value):
    try:
        int(value)
    except ValueError:
        return False
    return True
