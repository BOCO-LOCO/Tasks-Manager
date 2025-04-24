import pymysql


conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "mydb")
    
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_complete BOOLEAN DEFAULT FALSE,
    created_at DATE,
    done_at DATE DEFAULT NULL,
    priority ENUM('low', 'medium', 'high') DEFAULT 'Medium',
    category ENUM('studying', 'personal', 'work') DEFAULT 'personal',
    CONSTRAINT unique_title UNIQUE(title) )  
    """) #Constraint unique title to avoid the duplicate and multiple effect rows
    
print(">>>Table created successfully")
#trigger for auto match the created_at column with the current date
try:
    cursor.execute("""
                CREATE TRIGGER set_created_at
                BEFORE INSERT ON tasks
                FOR EACH ROW
                SET NEW.created_at = IFNULL(NEW.created_at, CURRENT_DATE)
                """)
    print(">>>Trigger created successfully")
except pymysql.Error as er:
    if "trigger already exists" in str(er).lower():
        print(f"⚠️ Trigger Creation Failed...{er}")

conn.commit()   