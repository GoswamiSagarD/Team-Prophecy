# importing the custom modules
from Code.src.DataEngineering.buildData import buildAllData



# For now, this module will simply process the raw data, and export it in various formats, to be used later for analysis.
# To make it simple for everyone, we decided to keep this processed data in Data/02_processed/ folder for all the analysis to be done.
# Any preprocessing specific to analytics is recommended to be done in the analytics module itself.
# If something goes wrong, you can simply delete the processed data folder, and rerun this module to rebuild the data.
# I know there are ways to further make it more modular, and I would for sure recommend you to do so.
# Our project had a major turnaround in the middle, and we had to literally scrap 90% of our work, and start from scratch.
# We have left a lot of comments to make sure, you guys don't have to go through the same pain.



buildAllData()