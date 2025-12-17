import sqlite3 

conn = sqlite3.connect("student_info.db")
cursor = conn.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS info(
               students_name TEXT,
               students_number TEXT,
               students_address TEXT,
               students_father TEXT,
               students_mother TEXT,
               students_classes TEXT,
               students_ages INTEGER
               )
               """)

student_list = [
    ("Bob Jones", "607-456-1084", "25347 10th st Johnson Texas 34528", "Andrew Jones", "Sally Jones", "Chemistry, Economics", 23)
]

cursor.executemany("insert into info values(?,?,?,?,?,?,?)", student_list)

conn.commit()

for row in cursor.execute("Select * FROM info"):
    print (row)

conn.close()