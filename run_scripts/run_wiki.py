#### OS and commanline arguments
import sys
import multiprocessing as mp
import gzip
import subprocess
from pathlib import Path
import argparse
import logging
import os

sys.path.append('./')

#### DeepGLO model imports
from DeepGLO.metrics import *
from DeepGLO.DeepGLOv2 import *
from DeepGLO.LocalModel import *
import pandas as pd
import numpy as np
import pickle

import random

np.random.seed(111)
torch.cuda.manual_seed(111)
torch.manual_seed(111)
random.seed(111)

import json


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def bool2str(b):
    if b:
        return "true"
    else:
        return "false"


Ymat = np.load("./datasets/wiki.npy")
vbsize = 2048  ## vertical batch size
hbsize = 256  ## horizontal batch size
num_channels_X = [32, 32, 32, 32, 1]  ## number of channels for local model
num_channels_Y = [32, 32, 32, 32, 1]  ## number of channels for hybrid model
kernel_size = 7  ## kernel size for local models
dropout = 0.2  ## dropout during training
rank = 128  ## rank of global model
kernel_size_Y = 7  ## kernel size of hybrid model
lr = 0.0005  ## learning rate
val_len = 14  ## validation length
end_index = Ymat.shape[1] - 14 * 4  ## models will not look beyond this during training
start_date = "2012-1-1"  ## start date time for the time-series
freq = "D"  ## frequency of data
covariates = None  ## no covraites specified
use_time = True  ## us time covariates
dti = None  ## no specified time covariates (using default)
svd = True  ## factor matrices are initialized by NMF
period = 7  ## periodicity of 7 is expected, leave it out if not known
y_iters = 300  ## max. number of iterations while training Tconv models
init_epochs = 100  ## max number of iterations while initializing factors
forward_cov = False


logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main(args):
    DG = DeepGLO(
        Ymat,
        vbsize=vbsize,
        hbsize=hbsize,
        num_channels_X=num_channels_X,
        num_channels_Y=num_channels_Y,
        kernel_size=kernel_size,
        dropout=dropout,
        rank=rank,
        kernel_size_Y=kernel_size_Y,
        lr=lr,
        val_len=val_len,
        end_index=end_index,
        normalize=normalize,
        start_date=start_date,
        freq=freq,
        covariates=covariates,
        use_time=use_time,
        dti=dti,
        svd=svd,
        period=period,
        forward_cov=forward_cov,
    )

    DG.train_all_models(y_iters=y_iters, init_epochs=init_epochs)

    result_dic = DG.rolling_validation(
        Ymat=Ymat, tau=14, n=4, bsize=100, cpu=False, alpha=0.5
    )
    print(result_dic)

    out_path = Path(
        ".",
        "results",
        "result_dictionary_wiki_" + bool2str(normalize) + ".pkl",
    )
    pickle.dump(result_dic, open(out_path, "wb"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--normalize",
        type=str2bool,
        required=True,
        help="normalize for training or not",
    )
    args = parser.parse_args()
    global normalize
    normalize = args.normalize
    main(args)
