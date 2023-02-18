# Predicting CEC Graduate Course Demand

> **This project seeks to predict the future demand for courses in the College of Engineering and Computing (CEC).**

We are looking to analyze data provided by CEC Enrollment Management to find trends that achieve this goal for future courses and determine how many sections are necessary. Once we understand these trends, we will construct a dashboard for enrollment management to receive recommendations on which classes to offer. Enrollment Management will be able to upload files to keep data current, see recommendations of what courses have to offer, and how many sections should be available for each course. With this knowledge in the hands of Enrollment Management, they can better serve the student population to minimize waitlist numbers and provide students with the classes they most desire. Addressing this issue will allow students to graduate on time and enable enrollment management to be better prepared to address the changing needs of their students.

# Project Life-cycle

## Requirements


## Data

Following are the dataset used to predict the Course Enrollment in future:

### Datasets

#### Student Enrollment History

This dataset is provided by the Enrollment Management - Office of the Provost at George Mason University. The dataset contains the historical enrollment state of students in the previous semesters. The main features of the data are:

* 110 CSV Files (Student Enrollment Status)
* Approx. 7 Instances of Enrollment Status per semester
* Dataset Width: 28
* Dataset Length: 344119
* Total Usable Features: 18


### Data Preparation

The following steps were performed on the raw data as part of Data Preprocessing:

1. Merging the raw `Student Enrollment History` CSV files into `CombinedData` CSV file.
2. The `CombinedData` CSV File is used to perform EDA (Exploratory Data Analysis).
