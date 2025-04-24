from random import choice
import db
import pymysql
from db import cursor, conn


#function to decoration the task that viewed 
def print_tasks(task):
    id, title, description, is_complete, created_at, dont_at, priority, category = task #unpack the tuple that get from the fatchall()
    status = "Yes" if is_complete else "No"
    print(f"\n🆔 ID         : {id}\n📝 Title      : {title}\n📖 Description: {description}")
    print(f"✅ Complete   : {status}\n📅 Create Date: {created_at}\n🗓️  Done Date  : {dont_at}\n🚦 Priority   : {priority}\n🗂️  Category   : {category}")
    
#add function
def add_task():
    try:
        print(".....ADD TASKS.....")
        title = input(".....ENTER THE TITLE: ").strip().lower()
        description = input("....DESCRIBE YOUR TASK: ").strip().lower()
        priority = input("....ENTER THE PRIORITY (Low, Medium, High): ").strip().lower()
        category = input("....ENTER THE CATEGORY (Studying, Personal, Work): ").strip().lower()
        if not title.strip():
            print("....TASK NAME CANNOT BE EMPTY....")
            input("Prss Enter to continue...")
            return
        
        query = "INSERT INTO tasks(title, description, priority, category) VALUES (%s, %s, %s, %s)"
        
        cursor.execute(query, (title, description, priority or None, category or None))
        conn.commit()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at")
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            print("✅ Task Added Successfully...")
            for task in result:
                print_tasks(task)
            input("\nPress Enter to continue...\n")
            return
    except pymysql.Error as err:
        print(f"❌ The Task Name is already Used...{err}")    
        input("Prss Enter to continue...")    
        

#the view function   
def view_tasks():
    filters = {
        "1": ("SELECT * FROM tasks ORDER BY created_at",()),
        "2": ("SELECT * FROM tasks WHERE category = %s", lambda: (input("Enter the category(Studying, Personal, Work): ").strip().lower(),)),
        "3": ("SELECT * FROM tasks WHERE priority = %s", lambda: (input("Enter the priority(Low, Medium, High): ").strip().lower(),)),
        "4": ("SELECT * FROM tasks WHERE is_complete = True ORDER BY created_at",()),
        "5": ("SELECT * FROM tasks WHERE is_complete = False ORDER BY created_at",())
    }
    
    print("\n.....VIEW TASKS MENU.....")
    option = input("1️⃣  View All Tasks\n2️⃣  View by Category 🗂️\n3️⃣  View by Priority 🚦\n4️⃣  View Completed ✅\n5️⃣  View Incomplete ❌\n0️⃣  Back to Main Menu\n>>>>: ").strip().lower()
    
    if option in filters:
        query, params = filters[option]
        if callable(params):
            params = params()
        
        cursor.execute(query, params)
    
        result = cursor.fetchall()
        if result:
            for task in result:
                print_tasks(task)
        else:
            print("\n....NO TASKS FOUND....\n")
    else:
        print("\n....INVALID OPTION....\n")
        
    input("\npress enter to continue...\n")
    return
            
            
#delete function   

def delete_task():
    try:
        print(".....DELETE TASKS.....")
        choice = input("1:....DELETE ONE....\n2:....DELETE ALL....\n>>>>: ").strip().lower()
        if choice == "1" or choice == "delete" or choice == "delete task" or choice == "delete one":
            name = input("TITLE OF THE TASK YOU WANNA DELETE...: ").strip().lower()
            query = "DELETE FROM tasks WHERE LOWER(title) = %s"
            cursor.execute(query, (name,))
            conn.commit()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at")
            result = cursor.fetchall()
            if cursor.rowcount > 0:
                print("\n✅ Task Was Successfully Deleted....\n")
                for task in result:
                    print_tasks(task)
            else:
                print("\n....NO TASKS FOUND....\n")
            input("\npress enter to continue...\n")
            return
        elif choice == "delete all" or choice == "2" or choice == "delete all task":
            query = "DELETE FROM tasks"
            cursor.execute(query)
            conn.commit()
            if cursor.rowcount > 0:
                print("....ALL TASKS ARE DELETED....\n")
            else: 
                print("\n....NOTHING DELETED....\n")
                
            cursor.execute("SELECT * FROM tasks ORDER BY created_at")
            result = cursor.fetchall()
            for row in result:
                print_tasks(row)
                input("\n....Press Enter To Continue....\n")
                return
    except pymysql.Error as err:
        print(f"An error occurred while accessing the database...{err}")    
        
            
#update function
def update_task():
    print(".....UPDATE TASKS.....")
    choice = input("\n1:<....UPDATE....>\n2:<....MARK TASK AS COMPLETE....>\n>>>>: ").strip().lower()
    if choice =="1" or choice == "update" or choice == "update task":
        options = {
            "title": "title",
            "description": "description",
            "create date": "created_at",
            "done date": "done_at"
        }
        while True:
            try:
                field = input("WHAT DO U WANNA UPDATE....\n>>>TITLE\n>>>DESCRIPTION\n>>>CREATE DATE\n>>>DONE DATE\n>>>PRIORITY\n>>>: ").strip().lower()           
                old_value = input("ENTER THE OLD VALUE....: ").strip().lower()
                new_value = input("ENTER THE NEW VALUE....: ").strip().lower()
                
                if field in options:
                    value = options[field]
                    query = f"UPDATE tasks SET {value} = %s WHERE {value} = %s AND ID IS NOT NULL"
                    cursor.execute(query, (new_value, old_value))
                    conn.commit()
                    if cursor.rowcount > 0:
                        print(f"✅ {cursor.rowcount} rows was changed...")
                    else:
                        print("❌ Nothing Was Changed...")
                    cursor.execute("SELECT * FROM tasks ORDER BY created_at")
                    result = cursor.fetchall()
                    for row in result:
                        print_tasks(row)
                    input("PRESS ENTER TO CONTINUE...")
                    break
                        
                else : 
                    print("....INVALID OPTION....")
                        
                exit = input("<....UPDATE....>or<....QUIT....>\n>>>>: ")
                if exit == "q" or exit == "quit":
                    return
                else:
                    continue
                
        
                      
            except pymysql.err.DataError as er:
                print(f"....INVALID FORMAT....\r\n....Please Check The Valid Date Format 'YYYY-MM-DD' OR Check Priority Values Must Be (Low, Medium, High)....\r\n{er}")
            except pymysql.Error as err:
                print(f"An error occurred while accessing the database...{err}")
            
    elif choice == "2" or choice == "mark task as complete" or choice == "mark task":
        task = input("ENTER THE TASK TITLE YOU WANNA MARK AS COMPLETE....: ").strip().lower()
        query = "UPDATE tasks SET is_complete = True, done_at = CURRENT_DATE WHERE LOWER(title) = %s"
        cursor.execute(query, (task,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Task marked as complete.\n")
        else:
            print("❌ NO TASK WITH THIS NAME...")
        
        cursor.execute("SELECT * FROM tasks ORDER BY is_complete ASC")
        result = cursor.fetchall()
        for row in result:
            print_tasks(row)
            
    else:
        print("....INVALID OPTION....")
        input("\npress enter to continue...\n")
                
        

