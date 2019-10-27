# DeepGLO

This repository implements the proposed models in the paper https://arxiv.org/abs/1905.03806. It also contains scripts to reproduce the results of the model DeepGLO reported in the paper. 

## Requirements

1. The repository assumes that you have Pytorch installed with CUDA support. Please follow the instructions at https://pytorch.org/ to install the correct version for your system. 
2. The other required packages are numpy, scikit-learn, scipy, pandas and matplotlib. Please install these packages before using this package. 


## Package Details

1. The TCN (LeveledInit) model is implemented in DeepGLO.LocalModel
2. The overall model is implemented in DeepGLO.DeepGLO

All the input arguments are commented in the source files and usage instructions can be found in the scripts  `/run_scripts/run_<dataset>.py`. 


## Datasets

The datasets can be downloaded by the following commands:


`cd datasets`

`bash download-data.sh`


## Python Scripts

1. In order to reproduce the results from the paper in the normalized setting, execute the commands:

`python run_scripts/run_<dataset>.py --normalize True` 


2. In order to reproduce the results from the paper in the unnormalized setting, execute the commands:

`python run_scripts/run_<dataset>.py --normalize False` 


Here, dataset can be replaced by the corresponding dataset. For instance for the `electricity` dataset, the command can be: 

`python run_scripts/run_electricity.py --normalize False`

### License

This repository follows the BSD license. 


