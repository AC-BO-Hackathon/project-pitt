import numpy as np

from layerlumos.layerlumos import stackrt0
from layerlumos.utils_spectra import convert_frequencies_to_wavelengths
from layerlumos.utils_materials import load_material, interpolate_material

import constants


def calculate_transparency(materials, thicknesses):
    assert isinstance(materials, np.ndarray)
    assert isinstance(thicknesses, np.ndarray)
    assert materials.ndim == 1
    assert thicknesses.ndim == 1
    assert materials.shape[0] == thicknesses.shape[0]

    num_layers = thicknesses.shape[0]
    num_wavelengths = 100

    wavelengths = np.linspace(
        constants.WAVELENGTH_START_VISIBLE,
        constants.WAVELENGTH_END_VISIBLE,
        num_wavelengths
    )
    frequencies = convert_frequencies_to_wavelengths(wavelengths)
    n_k = np.ones((num_wavelengths, num_layers + 2), dtype=np.complex128)

    for ind_material, material in enumerate(materials):
        data_material = load_material(material)
        n_k_material = interpolate_material(data_material, frequencies)
        n_k[:, ind_material + 1] = n_k_material[:, 0] + 1j * n_k_material[:, 1]

    thicknesses = np.concatenate([
        [constants.THICKNESS_AIR],
        thicknesses * constants.NANO, 
        [constants.THICKNESS_AIR],
    ], axis=0)

    R_TE, T_TE, R_TM, T_TM = stackrt0(n_k, thicknesses, frequencies)

    T_avg = (T_TE + T_TM) / 2
    transparency = np.mean(T_avg)

    return transparency


if __name__ == '__main__':
    thicknesses = np.array([20, 10, 20])
    materials = np.array(['TiO2', 'Ag', 'TiO2'])

    transparency = calculate_transparency(materials, thicknesses)
    print(transparency)

    thicknesses = np.array([20, 10, 20, 10, 20, 10, 20 ,10, 20, 10, 20, 10])
    materials = np.array(['Ag', 'Al2O3', 'Al', 'Cr', 'Ni', 'Pd', 'Si3N4', 'SiO2', 'TiN', 'TiO2', 'Ti', 'W'])

    transparency = calculate_transparency(materials, thicknesses)
    print(transparency)
