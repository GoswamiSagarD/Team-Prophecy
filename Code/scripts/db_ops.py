# Configuring a SQLite Database operations
class ConnectDB:
    def __init__(self, db_path):
        import sqlite3
        self.sql_connection = sqlite3.connect(db_path)
        self.sql_cursor = self.sql_connection.cursor()

    def run_query(self, query, committing=False):
        """
        Run a query on the database
        
        Args:
            query (str): The query to run
            committing (bool): Whether to commit the query or not
        Returns:
            list: The results of the query
        """
        query_execution = self.sql_cursor.execute(query)
        if committing:
            self.sql_connection.commit()
        
        return query_execution

    def commit(self):
        """
        Commit the changes to the database
        
        Args:
            None
        Returns:
            None
        """
        self.sql_connection.commit()