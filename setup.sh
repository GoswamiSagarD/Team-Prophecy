# git clone 

# Creating a conda environment from the YAML file
conda env create -n prophecy --file prophecy_env.yml

# Activating the conda environment
conda activate prophecy

# Replacing the raw data with a fresh copy
rm -rf Data/01_raw