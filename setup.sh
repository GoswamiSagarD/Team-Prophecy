# This script will setup the environment for the project

# Requirements:
# - gitgub cli
# - GCP functions
# - Mason OneDrive
# - anaconda

# 1. Install github cli
sudo apt -y install bzip2 git libxml2-dev
sudo apt -y install python3 pip
sudo apt -y install gcloud gsutil

sudo pip3 install beautifulsoup4 gcloud glob2 virtualenv
sudo pip3 install google-api-core google-auth google-cloud-compute google-cloud-core google-cloud-storage

# 2. Clone the private GitHub repository
curl -u "Authorization: token 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" https://github.com/GoswamiSagarD/Team-Prophecy.git
git clone -b master https://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@github.com/GoswamiSagarD/Team-Prophecy.git
cd Team-Prophecy
#gh repo clone GoswamiSagarD/Team-Prophecy

# 3. Get Data
rm -rf Data/01_raw
# 3.1. Get the data from the GCP bucket
gcloud auth activate-service-account --key-file Code/src/prop/tprophecy-378622-d5cd14144d34.json
gsutil update
gsutil config -e
gsutil cp gs://cec_wl_upload_1/CEC*.csv Data/01_raw
# 3.2. Get the data from the OneDrive folder
#cd ..
#robocopy TeamProphecyRawData "Team-Prophecy" /e
#cd "Team-Prophecy"

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