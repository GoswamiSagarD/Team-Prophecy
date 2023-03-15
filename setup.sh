# This script will setup the environment for the project
####################################################################################################
# Requirements:
#   - wsl for Windows only
#   - conda
#   - git
####################################################################################################
# Clone the Project Repository
####################################################################################################
# Using curl
echo "################################################################################"
echo "Cloning the repository using curl..."
cd ".."
curl -u "Authorization: token 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" https://github.com/GoswamiSagarD/Team-Prophecy.git
git clone -b main https://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@github.com/GoswamiSagarD/Team-Prophecy.git
####################################################################################################
# Using github cli
#
####################################################################################################
# Ingest the Raw Data
####################################################################################################
# Using OneDrive
echo "################################################################################"
echo "Ingesting the raw data from OneDrive..."
cp -r "TeamProphecyRawData/Data" "Team-Prophecy"
mkdir "Team-Prophecy/Data/02_processed" "Team-Prophecy/Data/03_final"
cd "Team-Prophecy"
####################################################################################################
# Using GCP
#
####################################################################################################
# Create and Update the Conda Environment
####################################################################################################
#   Check if environment exists
echo "################################################################################"
echo "Setting up the Conda environment..."
if conda info --envs | grep -q "prophecy"; then
  # Update environment from YAML file
  conda env update --file "prophecy_env.yml"
else
  # Create environment from YAML file
  conda env create -f "prophecy_env.yml"
fi
####################################################################################################
# Activate the Conda Environment
source activate prophecy
####################################################################################################
# Build the Dataset
####################################################################################################
echo "################################################################################"
echo "Building the dataset..."
python build_data.py
echo "Done! The project is go for Data Science! Late Night Coding didn't kill me, but it did make this happen."
echo "- Sagar Goswami"
sleep 30
exit
####################################################################################################