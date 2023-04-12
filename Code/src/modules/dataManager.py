# Module to automatically load the data from the data folder

# Importing the required libraries
import os
import pandas as pd
import pprint
from Code.src.modules.db_ops import ConnectDB

# Class to manage the data
class DataManager:

    def __init__(self):
        """Initialize the DataManager class. This class is used to store the information about all the databases, and import them in a specified format.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.data_dict = {
            'course' : {
                'd_name' : 'Courses Information',
                'd_desc' : 'Course information obtained from Web Scraping the course catalog.',
                'd_state' : {
                    'processed' : {
                        'db' : os.path.join( 'Data', '02_processed', 'course4EDA.db' )
                    }
                }
            },
            'enrollment' : {
                'd_name' : 'Student Enrollment Status Data',
                'd_desc' : 'Student Enrollment Status Information processed by merging 110 CSV files obtained from Enrollment Management at George Mason University.',
                'd_state' : {
                    'processed' : {
                        'db' : os.path.join( 'Data', '02_processed', 'enrollment4EDA.db' ),
                        'csv' : os.path.join( 'Data', '02_processed', 'enrollment.csv' ),
                        'pkl' : os.path.join( 'Data', '02_processed', 'enrollment.pkl' )
                    }
                }
            },
            'professor' : {
                'd_name' : 'Professor Information',
                'd_desc' : 'Professor Information obtained from Enrollment Management at George Mason University.',
                'd_state' : {
                    'processed' : {
                        'db' : os.path.join( 'Data', '02_processed', 'professor4EDA.db' ),
                        'csv' : os.path.join( 'Data', '02_processed', 'professor.csv' ),
                        'pkl' : os.path.join( 'Data', '02_processed', 'professor.pkl' )
                    }
                }
            },
            'enrollmentfinalstatus' : {
                'd_name' : 'Student Final Enrollment Status Data',
                'd_desc' : 'Student Final Enrollment Status Information processed from the Enrollment Data.',
                'd_state' : {
                    'processed' : {
                        'db' : os.path.join( 'Data', '02_processed', 'enrollmentFinalStatus.db' ),
                        'csv' : os.path.join( 'Data', '02_processed', 'enrollmentFinalStatus.csv' ),
                        'pkl' : os.path.join( 'Data', '02_processed', 'enrollmentFinalStatus.pkl' )
                    }
                }
            },
            'finalsnapshot' : {
                'd_name' : 'Final Snapshot of Student Enrollment Status Data',
                'd_desc' : 'Final Snapshot of Student Enrollment Status Information processed from the Enrollment Data.',
                'd_state' : {
                    'processed' : {
                        'db' : os.path.join( 'Data', '02_processed', 'final_snapshot.db' ),
                        'csv' : os.path.join( 'Data', '02_processed', 'final_snapshot.csv' ),
                        'pkl' : os.path.join( 'Data', '02_processed', 'final_snapshot.pkl' )
                    }
                }
            }
        }
    

    def get_data(self, d_name, d_format, d_state = 'processed', get_path = False):
        """Get the data from the specified database in the specified format.

        Parameters
        ----------
        d_name : str
            Name of the database to be imported.
        d_format : str [db, pkl, csv]
            Format of the database to be imported.
        d_state : str [processed, final]
            State of the database to be imported.
        """
        
        # Raise an error if the arguments are invalid
        if d_name.lower() not in self.data_dict.keys():
            raise ValueError("Invalid database name. Please check the database name and try again.\nTry using the get_data_info() method to get the list of available databases.")
        if d_state.lower() not in ['processed', 'final']:
            raise ValueError("Invalid database state. Please check the database state and try again.\nTry using the get_data_info() method to get the list of available database states.")
        if d_state.lower() not in self.data_dict[d_name.lower()]['d_state'].keys():
            raise ValueError(f"Invalid database state. The database isn't available in {d_state} state yet.\nTry using the get_data_info() method to get the list of available database states.")
        if d_format.lower() not in ['db', 'pkl', 'csv']:
            raise ValueError("Invalid database format. Please check the database format and try again.\nTry using the get_data_info() method to get the list of available database formats.")
        if d_format.lower() not in self.data_dict[d_name.lower()]['d_state'][d_state.lower()].keys():
            raise ValueError(f"Invalid database format. The database isn't available in {d_format} format.\nTry using the get_data_info() method to get the list of available database formats.")
        
        # Get the path to the database
        path = self.data_dict[d_name.lower()]['d_state'][d_state.lower()][d_format.lower()]

        # Return the database in the specified format
        if get_path:
            # Return the path to the database if get_path is True
            return path
        if d_format.lower() == 'db':
            # Return the database connection if the format is db
            return ConnectDB(path)
        elif d_format.lower() == 'pkl':
            # Return the pandas dataframe from the pickle file if the format is pkl
            return pd.read_pickle(path)
        elif d_format.lower() in ['csv']:
            # Return the path to the csv file if the format is csv
            return path
    
    
    def get_data_info(self):
        """Get the information about all the databases."""
        pprint.pprint(self.data_dict)
