import brahe
import numpy as np

from simulation.transformations import dcm_from_phi, dcm_from_q


def apply_SO3_noise(vec, std):
    """
    Adds S03-style noise to a vector by rotating it about a random axis.

    Args:
        vec: The vector to which noise will be added.
        std: The standard deviation of the noise.

    Returns:
        The noisy vector.
    """
    noise = std * np.random.randn(3)
    return dcm_from_phi(noise) @ vec


class SunSensor:
    def __init__(self, std_deg, offset=None):
        self.std = np.deg2rad(std_deg)
        self.offset = offset

    def measure(self, spacecraft):
        r_sun = brahe.sun_position(spacecraft.epoch)
        vec_sun_body = self.get_sun_vec_body(spacecraft.orbit_eci, r_sun, spacecraft.attitude)
        return apply_SO3_noise(vec_sun_body, self.std)

    def get_sun_vec_body(self, x_eci, sun_eci, attitude_q):
        # Vector from the spacecraft to the Sun in ECI frame
        vec_sun_eci = sun_eci - x_eci
        # Vector from the spacecraft to the Sun in body frame
        vec_sun_body = dcm_from_q(attitude_q) @ (vec_sun_eci / np.linalg.norm(vec_sun_eci))  # normalized
        return vec_sun_body

    # TODO Flux values


class GPS:
    def __init__(self, std):
        self.std = std

    def measure(self, spacecraft):
        pass


class Gyroscope:
    def __init__(self, rotate_std_deg, noise_std_degps, initial_bias_deg):
        # TODO bias dynamics
        self.offset = dcm_from_phi(np.deg2rad(rotate_std_deg) * np.random.randn(3))
        self.bias = np.deg2rad(initial_bias_deg) * np.random.randn(3) / np.linalg.norm(np.random.randn(3))
        self.noise = np.deg2rad(noise_std_degps) * np.random.randn(3)

    def measure(self, spacecraft):
        measured_value = self.offset * spacecraft.state[10:13] + self.bias + self.noise
        return measured_value


# TODO other sensors