'''utility functions'''
import hmac


STRONG_NAME_KEY = 'aghkZXZ-Tm9uZXIRCxIEQmxvZxiAgICAgMyhCAw'

def make_secure_val(val):
    """returns a hmac value for given value."""
    return '%s|%s' % (val, hmac.new(STRONG_NAME_KEY, val).hexdigest())


def check_secure_val(secure_val):
    """Checks if passed secure value matches the hmac
    and the same strong name key."""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

