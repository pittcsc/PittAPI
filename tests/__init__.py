import warnings

warnings.simplefilter('ignore')

DEFAULT_TIMEOUT = 30


class PittServerError(TimeoutError):
    """Raise when a Pitt server is down or timing out"""
    pass
