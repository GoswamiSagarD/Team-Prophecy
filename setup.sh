

# 1. git clone 

# 2. Get Data

# Replacing the raw data with a fresh copy / Replace with GCP
rm -rf Data/01_raw
# copying the data files / GCP
cd ..
robocopy TeamProphecyRawData "Team-Prophecy" /e
cd "Team-Prophecy"

# Creating a conda environment from the YAML file
conda env create -n prophecy --file prophecy_env.yml

# Activating the conda environment
conda activate prophecy

# Building the Data
python Code/src/build_data.py