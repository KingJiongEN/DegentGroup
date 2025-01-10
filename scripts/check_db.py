from sqlalchemy import create_engine, inspect
from teleAgent.core.config import settings

def check_database():
    print(f"Checking database at: {settings.DATABASE_URL}")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Get inspector
    inspector = inspect(engine)
    
    # Get all table names
    tables = inspector.get_table_names()
    
    print("\nFound tables:")
    for table in tables:
        print(f"\n📋 Table: {table}")
        # Get columns for each table
        columns = inspector.get_columns(table)
        print("  Columns:")
        for column in columns:
            print(f"    - {column['name']} ({column['type']})")
        
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table)
        if foreign_keys:
            print("  Foreign Keys:")
            for fk in foreign_keys:
                print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

if __name__ == "__main__":
    check_database() 