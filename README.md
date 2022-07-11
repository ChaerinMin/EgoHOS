# EgoHOS
[Project Page](https://chail.github.io/latent-composition/) |  [Paper] | [Bibtex]

Fine-Grained Egocentric Hand-Object Segmentation \
*European Conference on Computer Vision (ECCV), 2022*\
[Lingzhi Zhang](https://owenzlz.github.io/), [Shenghao Zhou](https://scholar.google.com/citations?user=kWdwbUYAAAAJ&hl=en), [Simon Stent](https://scholar.google.com/citations?user=f3aij5UAAAAJ&hl=en), [Jianbo Shi](https://www.cis.upenn.edu/~jshi/)

## Prerequisites
- Linux
- Python 3
- NVIDIA GPU + CUDA CuDNN

**Table of Contents:**<br>
1. [Setup](#setup) - download pretrained models and resources
2. [Datasets](#datasets) - download our egocentric hand-object segmentation datasets
3. [Usage](#pretrained) - quickstart with pretrained models<br>


## Setup
- Clone this repo:
```bash
git clone https://github.com/owenzlz/EgoHOS
```

- Install dependencies:
	- our code follows the mmsegmentation codebase, so you will need an environment compatible with mmsegmentation (https://mmsegmentation.readthedocs.io/en/latest/).
```bash
pip install -U openmim
mim install mmcv-full
cd mmsegmentation
pip install -v -e .
```

- Download resources:
	- we provide a script for downloading the pretrained checkpoints. 
```bash
bash download_checkpoints.sh
```


## Datasets
- Download our dataset from GDrive links. 
```bash
gdown ...
```


## Usage

Depending on the application scenarios, you can choose to run one of these commands to generate the segmentation predictions. 

- Predict left and right hands
```bash
bash ...
```

- Predict dense contact boundary between and hands and interacting objects
```bash
bash ...
```

- Predict hands and (1st order) interacting objects 
```bash
bash ...
```

- Predict hands and (both 1st and 2nd orders) interacting objects 
```bash
bash ...
```
