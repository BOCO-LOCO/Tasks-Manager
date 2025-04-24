import pymysql 
import db
from functions import *

try: 
    while True:
        print("\nHELLO, AND WELCOME TO YOUR TASK MANAGER!\n")
        services = {
            add_task : ["1","add"],
            view_tasks : ["2", "view"],
            update_task : ["3","update"],
            delete_task : ["4", "delete"],
            exit : ["5","exit"]
        }

        choice = input("1: 📝 Add a task\n2: 👀 View tasks\n3: ✏️  Update task\n4: 🗑️  Delete task\n5: 👋 Exit\n>>>>>").strip().lower()
        
        if choice == "5" or choice == "exit":
            print("GOOD BYE...")
            exit()
        for key, values in services.items():
            try:
                if choice in values:
                    key()
                    
            except ValueError as err:
                print(f"something went wrong: {err}")
            

        
except pymysql.Error as err:
    print("something went wrong...:", err)   
    
    
finally:
    db.conn.close()