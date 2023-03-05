# Configuring a SQLite Database operations
class ConnectDB:
    """
    Connect to a SQLite database and run queries on it

    Args:
        db_path (str): The path to the database
    Returns:
        None
    """
    
    def __init__(self, db_path):
        import sqlite3
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def run_query(self, query, committing=False):
        """
        Run a query on the database
        
        Args:
            query (str): The query to run
            committing (bool): Whether to commit the query or not
        Returns:
            list: The results of the query
        """
        query_execution = self.cursor.execute(query)
        if committing:
            self.connection.commit()
        
        return query_execution

    def commit(self):
        """
        Commit the changes to the database
        
        Args:
            None
        Returns:
            None
        """
        self.connection.commit()