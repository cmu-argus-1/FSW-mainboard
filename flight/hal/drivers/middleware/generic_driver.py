from hal.drivers.diagnostics.diagnostics import Diagnostics
from digitalio import DigitalInOut


FAULT_HANDLE_RETRIES = 3


class driver_cant_handle_exception(Exception):
    """
    to be used when the handler attempts to handle a method that wasn't given to it
    as a handlable method
    """
    def __init__(self, exception: Exception):
        self.exception = exception
        super().__init__()

    def __str__(self):
        return f"{type(self.exception).__name__}: {self.exception}"


class Driver(Diagnostics):
    # set of strings containing method names
    # dict of method name to checker function and method-specific exception to give to middlware

    def __init__(self, enable: DigitalInOut = None) -> None:
        self.handleable = {}
        self.checkers = {}
        super().__init__(enable)

    def handler(self, method):
        if method.__name__ not in self.handleable:
            raise driver_cant_handle_exception("tried to handle unhandleable method")
        checker, m_exception = self.checkers[method.__name__]

        def handle(*args, **kwargs):
            try:
                res = method(*args, **kwargs)
                flags = self.get_flags()
                if checker(res, flags):
                    return res
                else:
                    raise m_exception("erroneus result")
            except Exception:
                flags = self.get_flags()
                for flag in flags:
                    fixer = flags[flag]
                    if fixer is not None:
                        fixer()
                try:
                    if val := self.retry(method, *args, **kwargs):
                        if checker(val, flags):
                            return val
                        else:
                            raise m_exception("erroneus result")
                    else:
                        raise m_exception("couldn't retry")
                except Exception as e:
                    raise m_exception(e)

        return handle

    @property
    def get_flags(self) -> dict:
        """
        should return a dictionary of (raised flag -> fixer function)
        or if flag cannot be fixed in software (raised flag -> None)
        """
        raise NotImplementedError

    def retry(self, method, *args, **kwargs) -> bool:
        """handle_fault: Handle the exception generated by the fault.

        :returns: True the value requested, otherwise raises exception
        """
        if not self.resetable:
            return None

        tries = 0
        while tries < FAULT_HANDLE_RETRIES:
            try:
                self.reset()
                value = method(*args, **kwargs)  # Run the method again
                return value
            except Exception:
                tries += 1
        return None  # Fault could not be handled after retries
