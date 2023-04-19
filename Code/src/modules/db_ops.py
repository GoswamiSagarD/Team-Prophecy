# Configuring a SQLite Database operations
class ConnectDB:
    """
    Connect to a SQLite database and run queries on it. An abstraction layer to simplify the process of running queries on SQLite databases.

    Args:
        db_path (str): The path to the database
    Returns:
        None
    """
    
    def __init__(self, db_path):
        import sqlite3
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def runQuery(self, query, fetchall=True, committing=False):
        """
        Run a query on the database
        
        Args:
            query (str): The query to run
            committing (bool): Whether to commit the query or not
        Returns:
            list: The results of the query
        """
        import pandas as pd
        query_execution = self.cursor.execute(query)
        if committing:
            self.connection.commit()
        
        if fetchall:
            return pd.DataFrame(
                query_execution.fetchall(),
                columns=[i[0] for i in query_execution.description]
            )
        else:
            return query_execution

    def commitDB(self):
        """
        Commit the changes to the database
        
        Args:
            None
        Returns:
            None
        """
        self.connection.commit()