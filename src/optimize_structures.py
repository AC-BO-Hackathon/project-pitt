import argparse
import os
import time
import numpy as np
import mobo

import objective


path_results = '../results'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_layers', type=int, required=True)
    parser.add_argument('--num_init', type=int, required=True)
    parser.add_argument('--num_iter', type=int, required=True)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    num_layers = args.num_layers
    num_init = args.num_init
    num_iter = args.num_iter
    seed = args.seed

    obj = objective.Objective(num_layers)
    bounds = obj.bounds
    dim = obj.dim

    def fun_target(bx):
        return obj(bx)[0]

    print('', flush=True)
    print(f'num_layers {num_layers}', flush=True)
    print(f'num_init {num_init}', flush=True)
    print(f'num_iter {num_iter}', flush=True)
    print(f'seed {seed}', flush=True)
    print(f'dim {dim}', flush=True)
    print('bounds', flush=True)
    print(bounds, flush=True)
    print('', flush=True)

    str_file = f'mobo_layers_{num_layers}_init_{num_init}_iter_{num_iter}_seed_{seed:04d}.npy'

    model_bo = mobo.MOBO(
        bounds,
        str_cov='matern52',
        str_acq='ei',
        normalize_Y=True,
    )

    X = model_bo.get_initials('uniform', num_init, seed=seed)
    Y = []
    times = []

    for bx in X:
        time_start = time.monotonic()
        Y.append(fun_target(bx))
        time_end = time.monotonic()
        times.append(time_end - time_start)
    Y = np.array(Y)
    assert X.ndim == 2
    assert Y.ndim == 2
    assert X.shape[0] == Y.shape[0] == num_init
    assert X.shape[1] == dim
    assert Y.shape[1] == 2

    for ind_iter in range(0, num_iter):
        time_start = time.monotonic()
        next_point, _ = model_bo.optimize(X, Y, seed=(seed * 101) + ind_iter)
        by = fun_target(next_point)

        X = np.concatenate([X, [next_point]], axis=0)
        Y = np.concatenate([Y, [by]], axis=0)

        assert X.ndim == 2
        assert Y.ndim == 2
        assert X.shape[0] == Y.shape[0]
        assert X.shape[1] == dim
        assert Y.shape[1] == 2

        time_end = time.monotonic()
        times.append(time_end - time_start)

        print('', flush=True)
        print(f'Iteration {ind_iter+1:04d}: transmittance {by[0] * -1.0:.4f} shielding_effectiveness {by[1] * -1.0:.4f} time {time_end - time_start:.4f}', flush=True)

    times = np.array(times)

    materials = np.array(obj.materials)
    thicknesses = np.array(obj.thicknesses)
    negative_transparencies = np.array(obj.negative_transparencies)
    negative_shielding_effectivenesses = np.array(obj.negative_shielding_effectivenesses)

    dict_all = {
        'num_layers': num_layers,
        'num_init': num_init,
        'num_iter': num_iter,
        'seed': seed,
        'dim': dim,
        'bounds': bounds,
        'X': X,
        'Y': Y,
        'materials': materials,
        'thicknesses': thicknesses,
        'negative_transparencies': negative_transparencies,
        'negative_shielding_effectivenesses': negative_shielding_effectivenesses,
        'times': times,
    }

    np.save(os.path.join(path_results, str_file), dict_all)
