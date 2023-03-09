# This script will setup the environment for the project

# Requirements:
# - gitgub cli
# - GCP functions
# - Mason OneDrive
# - anaconda

# 1. Install github cli


# 2. Clone the private GitHub repository
gh repo clone GoswamiSagarD/Team-Prophecy

# 3. Get Data
rm -rf Data/01_raw
# 3.1. Get the data from the GCP bucket

# 3.2. Get the data from the OneDrive folder
cd ..
robocopy TeamProphecyRawData "Team-Prophecy" /e
cd "Team-Prophecy"

# 4. Install conda
sudo apt-get update
sudo apt-get install wget
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
# 5. Create a conda environment from the YAML file
conda env create -n prophecy --file prophecy_env.yml

# 6. Activate the conda environment
conda activate prophecy

# 7. Create the Folder Structure
mkdir Data/02_processed
mkdir Data/03_final

# 8. Build the Dataset
python Code/src/DataEngineering/build_data.py

# 9. Create and update the log file
# adding username, datetime, and completition text to the log file
whoami >> log.txt
date >> log.txt
echo "Setup Completed" >> log.txt

# 10. Print the script execution time and completion message
echo "Setup Completed"
echo "Time taken to execute the script:  seconds"

# 11. Wait for 10 seconds and Exit the script
sleep 10
exit