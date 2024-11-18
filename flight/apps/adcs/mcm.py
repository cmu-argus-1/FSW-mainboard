# Attitude Determination and Control Subsystem (ADCS)
# Magnetic Control Module


# TODO: implement controllers: B-dot, Bcross, Sun pointing
# TODO: implement desired moment allocation to voltages
# ...

# To apply the voltages to the coils, the following function is used:
# SATELLITE.APPLY_MAGNETIC_CONTROL({'XP': 5.0, 'XM': 5.1, 'YP': 4.8, 'YM': 5.0, 'ZP': 4.1, 'ZM': 4.1})

import copy
from typing import Tuple
from abc import ABC, abstractmethod

from ulab import numpy as np

from hal.configuration import SATELLITE


'''
Template controllers for spin stabilizing and sun pointing.
'''
class SpinStabilizingController(ABC):
    @classmethod
    @abstractmethod
    def get_dipole_moment_command(
        self,
        magnetic_field: np.ndarray,
        angular_velocity: np.ndarray,
    ) -> np.ndarray:
        raise NotImplementedError()


class SunPointingController(ABC):
    @classmethod
    @abstractmethod
    def get_dipole_moment_command(
        self,
        sun_vector: np.ndarray,
        magnetic_field: np.ndarray,
        angular_velocity: np.ndarray,
    ) -> np.ndarray:
        raise NotImplementedError()


'''
Spin stabilizing and sun pointing control laws.
'''
class BCrossController(SpinStabilizingController):
    _k = 1.0

    @classmethod
    def get_dipole_moment_command(
        self,
        magnetic_field: np.ndarray,
        angular_velocity: np.ndarray,
    ) -> np.ndarray:
        """
        B-cross law: https://arc.aiaa.org/doi/epdf/10.2514/1.53074.
        All sensor estimates are in the body-fixed reference frame.
        """
        unit_field = magnetic_field / np.linalg.norm(magnetic_field)
        ang_vel_err = angular_velocity - MomentumGuidance.angular_velocity_ref
        return -self._k * np.cross(unit_field, ang_vel_err)


class PDSunPointingController(SunPointingController):
    _PD_gains = np.array([
        [0.7071, 0.0, 0.0, 0.0028, 0.0, 0.0],
        [0.0, 0.7071, 0.0, 0.0, 0.0028, 0.0],
        [0.0, 0.0, 0.7071, 0.0, 0.0, 0.0028],
    ])


class MomentumGuidance():
    _J = np.array([
        0.001796, 0.0, 0.000716,
        0.0, 0.002081, 0.0,
        0.000716, 0.0, 0.002232,
    ])

    _ang_vel_norm_target = 0.175

    _ang_vel_norm_threshold = 0.262

    def _init_spin_axis(self) -> np.ndarray:
        eigvecs, eigvals = np.linalg.eig(self._J)
        spin_axis = eigvecs[:, np.argmax(eigvals)]
        if spin_axis[np.argmax(np.abs(spin_axis))] < 0:
            spin_axis = -spin_axis
        return spin_axis

    _spin_axis = _init_spin_axis()

    angular_velocity_reference = _spin_axis * _ang_vel_norm_target

    _ang_mtm_norm_target = np.linalg.norm(_J @ angular_velocity_reference)

    @classmethod
    def is_spin_stable(
        self,
        angular_velocity: np.ndarray,
    ) -> bool:
        h = self._J @ angular_velocity
        spin_err = np.linalg.norm( self._spin_axis - (h / self._ang_mtm_norm_target) )
        return spin_err < self._ang_vel_norm_threshold

    @classmethod
    def is_sun_pointing(
        self,
        sun_vector: np.ndarray,
        angular_velocity: np.ndarray,
    ) -> bool:
        h = self._J @ angular_velocity
        pointing_err = np.linalg.norm( sun_vector - (h / np.linalg.norm(h)) )
        return pointing_err < self._ang_vel_norm_target


class MagneticCoilAllocator():
    _Vs_ctrl = {
        'XP': 0.0, 'XM': 0.0,
        'YP': 0.0, 'YM': 0.0,
        'zP': 0.0, 'zM': 0.0,
    }

    _axis_idx  = {
        'X': {'P': 0, 'M': 1},
        'Y': {'P': 2, 'M': 3},
        'Z': {'P': 4, 'M': 5},
    }

    _default_alloc_mat = np.array([
        [0.5, 0.0, 0.0],
        [0.5, 0.0, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.0, 0.5],
        [0.0, 0.0, 0.5],
    ])

    _alloc_mat = copy.deepcopy(_default_alloc_mat)

    _Vs_max = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0])

    _sat = SATELLITE

    @classmethod
    def set_voltages(
        self,
        dipole_moment: np.ndarray,
    ) -> None:
        self._update_matrix()
        Vs = self._alloc_mat @ dipole_moment
        Vs_bd = np.clip(Vs, -self._Vs_max, self._Vs_max)
        for axis, face_idx in self._axis_idx.items():
            self._Vs_ctrl[axis + 'P'] = Vs_bd[face_idx['P']]
            self._Vs_ctrl[axis + 'M'] = Vs_bd[face_idx['M']]
        self._sat.APPLY_MAGNETIC_CONTROL(self._Vs_ctrl)

    @classmethod
    def _coils_on_axis_are_available(
        self,
        axis: str,
    ) -> Tuple[bool, bool]:
        P_avail = self._sat.TORQUE_DRIVERS_AVAILABLE(axis + 'P')
        M_avail = self._sat.TORQUE_DRIVERS_AVAILABLE(axis + 'M')
        return (P_avail, M_avail)

    @classmethod
    def _update_matrix(self) -> None:
        for axis, face_idx in self._axis_idx.items():
            P_avail, M_avail = self._coils_on_axis_are_available(axis)

            # Different combinations of active coils
            if P_avail and M_avail:
                self._alloc_mat[face_idx['P']] = self._default_alloc_mat[face_idx['P']]
                self._alloc_mat[face_idx['M']] = self._default_alloc_mat[face_idx['M']]

            elif P_avail and not M_avail:
                self._alloc_mat[face_idx['P']] = 2 * self._default_alloc_mat[face_idx['P']]
                self._alloc_mat[face_idx['M']] = np.zeros(3)

            elif not P_avail and M_avail:
                self._alloc_mat[face_idx['P']] = np.zeros(3)
                self._alloc_mat[face_idx['M']] = 2 * self._default_alloc_mat[face_idx['M']]

            elif not P_avail and not M_avail:
                self._alloc_mat[face_idx['P']] = np.zeros(3)
                self._alloc_mat[face_idx['M']] = np.zeros(3)
