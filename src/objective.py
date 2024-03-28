import numpy as np

import radio_frequency
import visible_light
import constants


class Objective:
    def __init__(self, num_layers):
        assert isinstance(num_layers, int)

        self.num_layers = num_layers
        self.dim = self.num_layers * 2

        self.X = []
        self.materials = []
        self.thicknesses = []

        self.negative_transparencies = []
        self.negative_shielding_effectivenesses = []

        self.bound_materials = constants.BOUND_MATERIALS
        self.bound_thicknesses = constants.BOUND_THICKNESSES
        self.bounds = np.array([
                self.bound_materials
            ] * num_layers + [
                self.bound_thicknesses
            ] * num_layers
        )
        assert self.dim == self.bounds.shape[0]

    def sample(self, num_samples, seed):
        samples = np.random.RandomState(seed).uniform(low=0.0, high=1.0, size=(num_samples, self.dim))
        samples = (self.bounds[:, 1] - self.bounds[:, 0]) * samples + self.bounds[:, 0]
        return samples

    def convert(self, bx):
        assert bx.shape[0] == self.dim

        materials = bx[:self.num_layers]
        thicknesses = bx[self.num_layers:]

        materials = materials.astype(np.int64)
        thicknesses = thicknesses.astype(np.int64).astype(np.float64)

        list_materials = []
        for material in materials:
            list_materials.append(constants.MATERIALS[material])
        list_materials.append(material_substrate)
        materials = np.array(list_materials)

        assert thicknesses.shape[0] == materials.shape[0] == (self.num_layers + 1)
        for material, thickness in zip(materials, thicknesses):
            assert material in constants.MATERIALS
            assert constants.BOUND_THICKNESSES[0] <= thickness
            assert thickness <= constants.BOUND_THICKNESSES[1]

        return thicknesses, materials

    def output(self, bx):
        assert isinstance(bx, np.ndarray)
        assert bx.ndim == 1
        assert bx.shape[0] == self.dim

        print(bx, flush=True)
        thicknesses, materials = self.convert(bx)

        self.X.append(bx)
        self.materials.append(materials)
        self.thicknesses.append(thicknesses)

        print('', flush=True)
        for ind, elem in enumerate(zip(thicknesses, materials)):
            thickness, material = elem
            print(f'thickness {ind+1} ({material}): {thickness} nm', flush=True)

        trans = visible_light.calculate_transparency(materials, thicknesses)
        effec = radio_frequency.calculate_shielding_effectiveness(materials, thicknesses)

        neg_trans = -1.0 * trans
        neg_effec = -1.0 * effec

        self.negative_transparencies.append(neg_trans)
        self.negative_shielding_effectivenesses.append(neg_effec)

        return neg_trans, neg_effec

    def __call__(self, X):
        X = np.atleast_2d(X)

        outputs = []
        for bx in X:
            by = self.output(bx)
            outputs.append(by)

        outputs = np.array(outputs)
        return outputs
