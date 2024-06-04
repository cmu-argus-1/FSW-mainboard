"""
middleware.py: Middleware class for handling faults at the driver level.

This module provides an abstract middelware class that is implemented by
each of the custom middleware classes for each component driver.

The goal of the middleware is to catch the exceptions generated by the driver
and convert them into uniquely known exceptions that can be handled by the
flight software.

Author: Harry Rosmann

"""

from ..diagnostics.diagnostics import Diagnostics
from micropython import const
from handlers import Handler

# The default number of retries for the middleware
# NOTE: Keep this value low to prevent loss of timing
FAULT_HANDLE_RETRIES = const(1)


class Middleware:
    """Middleware: Middleware class for handling faults at the driver level.

    This class provides a middleware class that wraps the driver instance and
    catches the exceptions generated by the driver. The middleware class then
    converts the exceptions into uniquely known exceptions that can be handled
    by the flight software.
    """

    def __init__(self, cls_instance: Diagnostics, exception: Exception, handler: Handler):
        """__init__: Constructor for the DriverMiddleware class.

        :param cls_instance: The instance of the driver class to wrap
        :param exception: The unique exception raised if fault not handled
        """
        self.exception = exception
        self.handler = handler
        self._wrapped_instance = cls_instance
        self._wrapped_attributes = {}
        self.wrap_attributes()

    def get_instance(self):
        """get_instance: Get the wrapped instance of the driver."""
        return self._wrapped_instance

    def wrap_attributes(self):
        """wrap_attributes: Wrap the attributes of the driver instance."""
        for name in dir(self._wrapped_instance):
            attr = getattr(self._wrapped_instance, name)
            if callable(attr) or isinstance(attr, property):
                self._wrapped_attributes[name] = self.wrap_attribute(attr)

    def __getattr__(self, name):
        """__getattr__: Get the attribute of the driver instance.

        :param name: The name of the attribute to get
        """
        if name in self._wrapped_attributes:
            return self._wrapped_attributes[name]
        return getattr(self._wrapped_instance, name)

    def wrap_attribute(self, attr):
        """wrap_attribute: Wrap the attribute of the driver instance.

        :param attr: The attribute to wrap
        """
        if callable(attr):
            return self.wrap_method(attr)
        elif isinstance(attr, property):
            return property(
                fget=self.wrap_method(attr.fget) if attr.fget else None,
                fset=self.wrap_method(attr.fset) if attr.fset else None,
                fdel=self.wrap_method(attr.fdel) if attr.fdel else None,
                doc=attr.__doc__,
            )
        return attr

    def wrap_method(self, method):
        """wrap_method: Wrap the method of the driver instance.

        :param method: The method to wrap
        """

        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                flags = self._wrapped_instance.status()
                print(flags)
                # Try to handle fault
                if not self.handle_fault(method, *args, **kwargs):
                    raise self.exception(e)

                # Second layer of exception handling
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    # Don't try to recover this time
                    raise self.exception(e)

        if self.handler.is_handled(method):
            return self.handler.handle_method(method)
        return wrapper

    def handle_fault(self, method, *args, **kwargs) -> bool:
        """handle_fault: Handle the exception generated by the fault.

        :returns: True the value requested, otherwise raises exception
        """
        if not self._wrapped_instance.resetable:
            return False

        tries = 0
        while tries < FAULT_HANDLE_RETRIES:
            try:
                self._wrapped_instance.reset()
                method(*args, **kwargs)  # Run the method again
                return True
            except Exception:
                tries += 1
        return False  # Fault could not be handled after retries
