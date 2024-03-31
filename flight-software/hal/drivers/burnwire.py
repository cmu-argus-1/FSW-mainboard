

"""
This module contains the BurnWires class which provides functionality for controlling burn wires.

Author: Harry Rosmann
Date: March 28, 2024
"""

from .diagnostics.diagnostics import Diagnostics
import digitalio, pwmio
from micropython import const
import time

class BurnWires(Diagnostics):
    """
    The BurnWires class provides functionality for controlling burn wires.

    Attributes:
        INITIAL_FREQUENCY_HZ (int): The initial frequency in Hz for the PWM signal.
        INITIAL_DUTY_PCT (int): The initial duty cycle percentage for the PWM signal.
        INITIAL_DURATION_S (int): The initial duration in seconds for burning.

        DUTY_CYCLE_OFF (int): The duty cycle value to turn off the burn wire.

    Methods:
        __init__(self, enable_pin, burn_xp, burn_xm, burn_yp, burn_ym): Initializes the BurnWires object.
        enable(self): Enables the burn wires through the relay.
        disable(self): Disables the burn wires through the relay.
        burn_xp(self): Burns the positive X-axis wire.
        burn_xm(self): Burns the negative X-axis wire.
        burn_yp(self): Burns the positive Y-axis wire.
        burn_ym(self): Burns the negative Y-axis wire.
    """

    # Initial values for the attributes
    INITIAL_FREQUENCY_HZ    = const(1000)
    INITIAL_DUTY_PCT        = const(50)
    INITIAL_DURATION_S      = const(1)

    # Duty cycle value to turn off the burn wire
    DUTY_CYCLE_OFF          = const(0)

    def __init__(self, enable_pin, burn_xp, burn_xm, burn_yp, burn_ym):
        """
        Initializes the BurnWires object.

        Args:
            enable_pin: The pin used to enable/disable the burn wires.
            burn_xp: The pin used for burning the positive X-axis wire.
            burn_xm: The pin used for burning the negative X-axis wire.
            burn_yp: The pin used for burning the positive Y-axis wire.
            burn_ym: The pin used for burning the negative Y-axis wire.
        """
        self.__pwm_frequency = self.INITIAL_FREQUENCY_HZ
        self.__duty_cycle = self.INITIAL_DUTY_PCT
        self.__burn_duration = self.INITIAL_DURATION_S

        self.__enable = self.__configure_enable(enable_pin)

        self.__burn_xp = self.__configure_burn_pin(burn_xp)
        self.__burn_xm = self.__configure_burn_pin(burn_xm)
        self.__burn_yp = self.__configure_burn_pin(burn_yp)
        self.__burn_ym = self.__configure_burn_pin(burn_ym)

        super().__init__()

    @property
    def frequency_hz(self):
        """
        Get the current frequency in Hz for the PWM signal.
        """
        return self.__pwm_frequency
    
    @frequency_hz.setter
    def frequency(self, frequency_hz):
        """
        Set the frequency in Hz for the PWM signal.

        Args:
            frequency_hz: The frequency in Hz for the PWM signal.
        """
        self.__pwm_frequency = frequency_hz
    
    @frequency_hz.getter
    def frequency(self):
        """
        Get the current frequency in Hz for the PWM signal.
        """
        return self.__pwm_frequency
    
    @property
    def duty_cycle_pct(self):
        """
        Get the current duty cycle percentage for the PWM signal.
        """
        return self.__duty_cycle
    
    @duty_cycle_pct.setter
    def duty_cycle(self, duty_cycle_pct):
        """
        Set the duty cycle percentage for the PWM signal.

        Args:
            duty_cycle_pct: The duty cycle percentage for the PWM signal.
        """
        self.__duty_cycle = duty_cycle_pct

    @duty_cycle_pct.getter
    def duty_cycle_pct(self):
        """
        Get the current duty cycle percentage for the PWM signal.
        """
        return self.__duty_cycle

    @property
    def duration_s(self):
        """
        Get the current duration in seconds for burning.
        """
        return self.__burn_duration
    
    @duration_s.setter
    def duration(self, duration_s):
        """
        Set the duration in seconds for burning.

        Args:
            duration_s: The duration in seconds for burning.
        """
        self.__burn_duration = duration_s

    @duration_s.getter
    def duration(self):
        """
        Get the current duration in seconds for burning.
        """
        return self.__burn_duration

    def enable(self):
        """
        Enables the burn wires through the relay.
        """
        self.__enable.drive_mode = digitalio.DriveMode.PUSH_PULL
        self.__enable.value = True

    def disable(self):
        """
        Disables the burn wires through the relay.
        """
        self.__enable.value = False
        self.__enable.drive_mode = digitalio.DriveMode.OPEN_DRAIN

    def __configure_enable(self, enable_pin):
        """
        Configures the enable pin for burn wires.

        Args:
            enable_pin: The pin used to enable/disable the burn wires.

        Returns:
            The configured enable pin.
        """
        enable_pin = digitalio.DigitalInOut(enable_pin)
        enable_pin.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)

        return enable_pin

    def __configure_burn_pin(self, burn_pin):
        """
        Configures a burn pin for burning wires.

        Args:
            burn_pin: The pin used for burning a wire.

        Returns:
            The configured burn pin.
        """
        # Set the duty cycle to 0 so it doesn't start burning
        burn_wire = pwmio.PWMOut(burn_pin, frequency=self.frequency, duty_cycle=self.DUTY_CYCLE_OFF)

        return burn_wire
    
    def __burn(self, burn_wire):
        """
        Burns a wire using the specified burn pin.

        Args:
            burn_wire: The burn pin used for burning a wire.
        """
        burn_wire.duty_cycle = self.duty_cycle
        time.sleep(self.duration)
        burn_wire.duty_cycle = self.DUTY_CYCLE_OFF

    def burn_xp(self):
        """
        Burns the positive X-axis wire.
        """
        self.__burn(self.__burn_xp)
    
    def burn_xm(self):
        """
        Burns the negative X-axis wire.
        """
        self.__burn(self.__burn_xm)

    def burn_yp(self):
        """
        Burns the positive Y-axis wire.
        """
        self.__burn(self.__burn_yp)

    def burn_ym(self):
        """
        Burns the negative Y-axis wire.
        """
        self.__burn(self.__burn_ym)

    
