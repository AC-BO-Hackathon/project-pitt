# Multi-Objective Bayesian Optimization for Transparent Electromagnetic Interference Shielding with Thin-Film Structures

This repository is for implementing the project "Multi-Objective Bayesian Optimization for Transparent Electromagnetic Interference Shielding with Thin-Film Structures" at the [Bayesian Optimization Hackathon for Chemistry and Materials](https://ac-bo-hackathon.github.io/).

## Project Description

We investigate the problem of transparent electromagnetic interference shielding to protect electronic circuits or devices by finding an optimal nano-structure using Bayesian optimization. We parameterize a thin-film structure considering the material and thickness of each layer, and then optimize two objective functions with mulit-objective Bayesian optimization. In addition, we showcase our own transfer-matrix method package for computing the propagation of electromagnetic waves as well as our Bayesian optimization package.

## Team Members

1. [Jungtaek Kim](https://jungtaekkim.github.io/) (University of Pittsburgh, Team Leader)
2. Mingxuan Li (University of Pittsburgh)
3. Oliver Hinder (University of Pittsburgh)
4. Paul W. Leu (University of Pittsburgh)

## Brief Code Description

- `constants.py`: Declaring constants
- `optimize_structures.py`: Optimizing thin-film structures using multi-objective Bayesian optimization
- `plot_structures.py`: Plotting thin-film structures
- `mobo.py`: Defining multi-objective Bayesian optimization
- `plot_bayesian_optimization.py`: Plotting the results of Bayesian optimization over iterations
- `objective.py`: Defining an objective function
- `plot_pareto_frontiers.py`: Plotting Pareto frontiers
- `radio_frequency.py`: Defining a function regarding shiedling effectiveness
- `visible_light.py`: Defining a function regarding transmittance

## Required Packages

Required packages can be installed by commanding `pip install -r requirements.txt`.

- [numpy](https://github.com/numpy/numpy)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [bayeso](https://github.com/jungtaekkim/bayeso)
- [layerlumos](https://github.com/Mil152/LayerLumos/tree/main)

## References

- Mingxuan Li, Michael J. McCourt, Anthony J. Galante, and Paul W. Leu. Bayesian optimization of nanophotonic electromagnetic shielding with very high visible transparency. Optics Express, vol. 30, no. 18, pp. 33182-33194, 2022.
- Jungtaek Kim and Seungjin Choi. BayesO: A Bayesian optimization framework in Python. Journal of Open Source Software, vol. 8, no. 90, p. 5320, 2023.
- Jungtaek Kim, Mingxuan Li, Oliver Hinder, and Paul W. Leu. Datasets and benchmarks for nanophotonic structure and parametric design simulations. In Advances in Neural Information Processing Systems 36 (NeurIPS-2023), New Orleans, Louisiana, USA, December 10-16, 2023. Datasets and Benchmarks Track.
- Jungtaek Kim, Mingxuan Li, Yirong Li, Andrés Gómez, Oliver Hinder, and Paul W. Leu. Multi-BOWS: Multi-fidelity multi-objective Bayesian optimization with warm starts for nanophotonic structure design. Digital Discovery, vol. 3, no. 2, pp. 381-391, 2024.
