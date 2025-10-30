"""
Direct SQL Query Tool for volunteer_management.db
Run custom SQL queries on the database
"""

import sqlite3
import sys

def execute_query(query):
    """Execute a SQL query and display results"""
    try:
        conn = sqlite3.connect('volunteer_management.db')
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # If it's a SELECT query, fetch and display results
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            print("\n" + "="*80)
            print(f"QUERY RESULTS ({len(results)} rows)")
            print("="*80)
            
            # Print column headers
            print("\n" + " | ".join(columns))
            print("-" * 80)
            
            # Print rows
            for row in results:
                print(" | ".join(str(value) for value in row))
            
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            print(f"\nQuery executed successfully. Rows affected: {cursor.rowcount}")
        
        conn.close()
        
    except Exception as e:
        print(f"\nError executing query: {e}")

def show_tables():
    """Show all tables in the database"""
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    print("\nTABLES IN DATABASE:")
    print("-" * 80)
    execute_query(query)

def show_table_schema(table_name):
    """Show schema of a specific table"""
    query = f"PRAGMA table_info({table_name});"
    print(f"\nSCHEMA FOR TABLE: {table_name}")
    print("-" * 80)
    execute_query(query)

# Predefined useful queries
USEFUL_QUERIES = {
    '1': ('View all volunteers', 'SELECT id, name, email, skills FROM volunteers;'),
    '2': ('Count volunteers', 'SELECT COUNT(*) as total_volunteers FROM volunteers;'),
    '3': ('View shortlisted volunteers', 'SELECT name, email, match_score FROM shortlisted_volunteers s JOIN volunteers v ON s.volunteer_id = v.id ORDER BY match_score DESC;'),
    '4': ('Count shortlisted', 'SELECT COUNT(*) as total_shortlisted FROM shortlisted_volunteers;'),
    '5': ('View volunteers by skills (Python)', "SELECT name, email, skills FROM volunteers WHERE skills LIKE '%Python%';"),
    '6': ('Top 5 matches', 'SELECT v.name, v.email, s.match_score FROM shortlisted_volunteers s JOIN volunteers v ON s.volunteer_id = v.id ORDER BY s.match_score DESC LIMIT 5;'),
}

def main():
    """Main interactive SQL query interface"""
    print("\n" + "="*80)
    print(" SQL QUERY TOOL - volunteer_management.db")
    print("="*80)
    
    # Show tables
    show_tables()
    
    while True:
        print("\n" + "="*80)
        print(" OPTIONS")
        print("="*80)
        print("\nPredefined Queries:")
        for key, (description, _) in USEFUL_QUERIES.items():
            print(f"  {key}. {description}")
        
        print("\nOther Options:")
        print("  s. Show table schema")
        print("  c. Custom SQL query")
        print("  q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice in USEFUL_QUERIES:
            description, query = USEFUL_QUERIES[choice]
            print(f"\nExecuting: {description}")
            print(f"Query: {query}")
            execute_query(query)
        
        elif choice == 's':
            table = input("Enter table name (volunteers/shortlisted_volunteers/job_postings): ").strip()
            if table:
                show_table_schema(table)
        
        elif choice == 'c':
            print("\nEnter your SQL query (or 'back' to return):")
            query = input().strip()
            if query.lower() != 'back':
                execute_query(query)
        
        elif choice == 'q':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
