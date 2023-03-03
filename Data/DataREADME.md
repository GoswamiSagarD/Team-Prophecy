# Data Readme

The Data folder is stored in the following manner:

## 01raw Folder

The `01raw` Folder stores the raw data with no processing done. Each data is stored in a separate folder. There are three sub-folders within this folder:

1. `CourseData`
2. `EnrollmentData`
3. `ProfessorData`

## 02processed Folder

The `02processed` Folder stores the processed data. The code to process data is stored in the `Code/01DataEngineering`, that reads the data from the `01raw`, performs data engineering, and wrangling, and exports the processed data into this folder. The Data Analytics will be done using the data from this folder, until the final processed data is available.

Apart from the partly processed data, this folder also stores the outputs of different analytics used to generate visualizations for the EDA (Exploratory Data Analysis) and the metrics for the Machine Learning Models.

## 03final Folder

The `03final` Folder stores the final processed data used for the analytics. This data is thoroughly cleaned and processed, and is used for final deployment.
