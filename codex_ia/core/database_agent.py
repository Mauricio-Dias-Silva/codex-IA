from typing import List, Dict, Any, Optional
import sqlalchemy
from sqlalchemy import create_engine, text, inspect
from urllib.parse import quote_plus

class DatabaseAgent:
    """
    [LEVEL 8] Database Administrator.
    Role: Manages connections to SQL databases and executes queries.
    """
    
    def __init__(self):
        self.engine = None
        self.connection = None
        self.inspector = None

    def connect(self, connection_config: Dict[str, str]) -> Dict[str, Any]:
        """
        Connects to a database.
        Config expects: type (sqlite/mysql/postgres), host, port, user, password, database, file_path (for sqlite)
        """
        try:
            db_type = connection_config.get('type', 'sqlite')
            
            if db_type == 'sqlite':
                path = connection_config.get('file_path')
                if not path:
                    return {"success": False, "error": "SQLite Requires file path"}
                uri = f"sqlite:///{path}"
            
            elif db_type in ['mysql', 'postgresql']:
                user = quote_plus(connection_config.get('user', ''))
                password = quote_plus(connection_config.get('password', ''))
                host = connection_config.get('host', 'localhost')
                port = connection_config.get('port', '')
                db_name = connection_config.get('database', '')
                
                driver = 'mysql+pymysql' if db_type == 'mysql' else 'postgresql'
                if port:
                    uri = f"{driver}://{user}:{password}@{host}:{port}/{db_name}"
                else:
                    uri = f"{driver}://{user}:{password}@{host}/{db_name}"
            else:
                return {"success": False, "error": f"Unsupported database type: {db_type}"}

            self.engine = create_engine(uri)
            self.connection = self.engine.connect()
            self.inspector = inspect(self.engine)
            
            return {"success": True, "message": f"Connected to {db_type} successfully."}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_schema(self) -> Dict[str, Any]:
        """Returns the list of tables and columns."""
        if not self.inspector:
            return {"error": "Not connected"}
            
        schema = {}
        try:
            for table_name in self.inspector.get_table_names():
                columns = []
                for col in self.inspector.get_columns(table_name):
                    columns.append({
                        "name": col['name'],
                        "type": str(col['type'])
                    })
                schema[table_name] = columns
            return {"schema": schema}
        except Exception as e:
            return {"error": str(e)}

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Executes a raw SQL query."""
        if not self.connection:
            return {"error": "Not connected"}
            
        try:
            # Simple safety check: only allow SELECT for now unless explicitly overridden (not implemented)
            # Actually, let's allow everything but be careful.
            
            result = self.connection.execute(text(query))
            
            if result.returns_rows:
                keys = list(result.keys())
                rows = [dict(zip(keys, row)) for row in result.fetchall()]
                return {"columns": keys, "rows": rows}
            else:
                self.connection.commit()
                return {"message": "Query executed successfully (No rows returned)."}
                
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        if self.connection:
            self.connection.close()
