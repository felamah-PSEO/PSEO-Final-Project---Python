import sqlite3
import tkinter as tk

class student_info:
    def __init__(self):
        #Creating the main window
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x500")
        self.main_window.title("Student Info")

        # Only the student info is inside this canvas
        self.canvas = tk.Canvas(self.main_window, height=300)  
        self.scrollbar = tk.Scrollbar(self.main_window, orient="vertical", command=self.canvas.yview)  

        self.scrollable_frame = tk.Frame(self.canvas) 

        # Update scroll region when content changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Place the scrollable frame inside the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")  
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  

        # Pack the canvas and scrollbar
        self.canvas.pack(side="top", fill="both", expand=True)  
        self.scrollbar.pack(side="right", fill="y") 

        
        # Frames for buttons
        self.middle_frame = tk.Frame(self.main_window)
        self.middle_frame.pack(pady=10)  

        self.bottom_frame = tk.Frame(self.main_window) 
        self.bottom_frame.pack()

        # ---------- BUTTONS ----------
        self.button1 = tk.Button(self.middle_frame, text="Add Info", command=self.add_info)
        self.button1.pack(side="left", padx=5)

        self.button2 = tk.Button(self.middle_frame, text="Edit", command=self.edit_info)
        self.button2.pack(side="left", padx=5)

        self.button3 = tk.Button(self.middle_frame, text="Delete", command=self.delete_info)
        self.button3.pack(side="left", padx=5)

        self.refresh_button = tk.Button(self.middle_frame, text="Refresh", command=self.read_student_info)
        self.refresh_button.pack(side="left", padx=5)

        self.button4 = tk.Button(self.bottom_frame, text="Quit", command=self.main_window.destroy)
        self.button4.pack(pady=10)

        # Load data
        self.read_student_info()



    #Function to read student info 
    def read_student_info(self):
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Connecting to DB
        conn = sqlite3.connect("student_info.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info")
        rows = cursor.fetchall()
        conn.close()

        field_names = ["Name", "Number", "Address", "Father", "Mother", "Classes", "Age"]

        #Displaying all information in a label
        for row in rows:
            # Creates a "card" for each student
            card = tk.Frame(self.scrollable_frame, bd = 2, relief = "groove", bg = "#fdfdfd", pady = 10, padx = 10)
            card.pack(fill = "x", pady = 8, padx = 15)

            # Puts the info on different lines
            for i, label_text in enumerate(field_names):
                # Bold Labels
                tk.Label(card, text=f"{label_text}:", font=("Arial", 10, "bold"), bg="#fdfdfd", fg="#333").grid(row=i, column=0, sticky="w")

                # Student Data
                tk.Label(card, text=f"{row[i]}", font=("Arial", 10), bg="#fdfdfd", fg="black").grid(row=i, column=1, sticky="w", padx=10)

    #Function to add info
    def add_info(self):
        self.second_window = tk.Toplevel(self.main_window)
        self.second_window.geometry("300x400") #<--- Change size of pop up window
        self.second_window.config() #<---Change color
        self.second_window.title("Add Info")

        #Frames in pop up window
        self.top_frame2 = tk.Frame(self.second_window)
        self.bottom_frame2 = tk.Frame(self.second_window)

        self.top_frame2.pack()
        self.bottom_frame2.pack()

        #Labels and entries to add info
        name_label = tk.Label(self.top_frame2, text = "Student's Name: ", ) #Change color and information of name label
        name_label.pack()
        name_entry = tk.Entry(self.top_frame2)
        name_entry.pack()

        number_label = tk.Label(self.top_frame2, text = "Student's Number: ")
        number_label.pack()
        number_entry = tk.Entry(self.top_frame2)
        number_entry.pack()

        address_label = tk.Label(self.top_frame2, text = "Student's Address: ")
        address_label.pack()
        address_entry = tk.Entry(self.top_frame2)
        address_entry.pack()

        dad_label = tk.Label(self.top_frame2, text = "Student's Dad: ")
        dad_label.pack()
        dad_entry = tk.Entry(self.top_frame2)
        dad_entry.pack()

        mom_label = tk.Label(self.top_frame2, text = "Student's Mom: ")
        mom_label.pack()
        mom_entry = tk.Entry(self.top_frame2)
        mom_entry.pack()

        classes_label = tk.Label(self.top_frame2, text = "Student's Classes: ")
        classes_label.pack()
        classes_entry = tk.Entry(self.top_frame2)
        classes_entry.pack()

        age_label = tk.Label(self.top_frame2, text = "Student's Age: ")
        age_label.pack()
        age_entry = tk.Entry(self.top_frame2)
        age_entry.pack()

        message_label = tk.Label(self.top_frame2, text = "")
        message_label.pack()

        #Function to save entries to db
        def save_entries():
            name = name_entry.get()
            number = number_entry.get()
            address = address_entry.get()
            dad = dad_entry.get()
            mom = mom_entry.get()
            classes = classes_entry.get()
            age = age_entry.get()

            if name and number and address and dad and mom and classes and age:
                conn = sqlite3.connect("student_info.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO info (students_name, students_number, students_address, students_father, students_mother, students_classes, students_ages) VALUES (?,?,?,?,?,?,?)", (name, number, address, dad, mom, classes, age))
                conn.commit()
                conn.close()

                #Automatically refresh main window
                self.read_student_info()

                #Clearing entries after saving
                name_entry.delete(0, tk.END)
                number_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END)
                dad_entry.delete(0, tk.END)
                mom_entry.delete(0, tk.END)
                classes_entry.delete(0, tk.END)
                age_entry.delete(0, tk.END)

                #Showing confirmation
                message_label.config(text = "Entry added sucessfully", fg = "green")
            else:
                message_label.config(text = "Please make sure to fill everything out", fg = "red")

        #save button
        self.save_button = tk.Button(self.bottom_frame2, text = "SAVE", command = save_entries)
        self.save_button.pack()

        #Close button
        self.close_button = tk.Button(self.bottom_frame2, text = "CLOSE", command = self.second_window.destroy)
        self.close_button.pack()


    def edit_info(self):
        # Open edit window
        edit_window = tk.Toplevel(self.main_window)
        edit_window.geometry("300x500")#<---------Change size for edit window
        edit_window.config()#<-----Change color
        edit_window.title("Edit Student Info")

        # Ask for name to search
        search_label = tk.Label(edit_window, text="Enter student name to edit:")
        search_label.pack()

        search_entry = tk.Entry(edit_window)
        search_entry.pack()

        result_frame = tk.Frame(edit_window)
        result_frame.pack()

        message_label = tk.Label(edit_window, text="")
        message_label.pack()

        # Function that loads student info into entry boxes
        def load_student():
            name = search_entry.get()

            conn = sqlite3.connect("student_info.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM info WHERE students_name=?", (name,))
            record = cursor.fetchone()
            conn.close()

            # If no student found
            if record is None:
                message_label.config(text="Student not found.", fg="red")
                return

            # Clear previous widgets
            for widget in result_frame.winfo_children():
                widget.destroy()

            # Create entry boxes pre-filled with database info
            labels = ["Name", "Number", "Address", "Father", "Mother", "Classes", "Age"]
            entries = ["Name"]

            for i, value in enumerate(record):
                tk.Label(result_frame, text=labels[i]).pack()
                entry = tk.Entry(result_frame)
                entry.insert(0, value)
                entry.pack()
                entries.append(entry)

            # Update button inside load_student()
            def update_student():
                new_data = [e.get() for e in entries]

                conn = sqlite3.connect("student_info.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE info
                    SET students_name=?,
                        students_number=?,
                        students_address=?,
                        students_father=?,
                        students_mother=?,
                        students_classes=?,
                        students_ages=?
                    WHERE students_name=?
                """, (*new_data, record[0]))
                conn.commit()
                conn.close()

                message_label.config(text="Student updated successfully!", fg="green")

                # Refresh main window
                self.read_student_info()

            update_button = tk.Button(result_frame, text="Save Changes", command=update_student)
            update_button.pack()

        # Search button
        search_button = tk.Button(edit_window, text="Search", command=load_student)
        search_button.pack()

        # Close Button
        close_button = tk.Button(edit_window, text = "Close", command = edit_window.destroy)
        close_button.pack()

    def delete_info(self):
        # Create delete window
        delete_window = tk.Toplevel(self.main_window)
        delete_window.geometry("600x300")
        delete_window.title("Delete Student")

        tk.Label(delete_window, text="Enter the student's name to delete:").pack()

        search_entry = tk.Entry(delete_window)
        search_entry.pack()

        result_frame = tk.Frame(delete_window)
        result_frame.pack()

        message_label = tk.Label(delete_window, text="")
        message_label.pack()

        # Function to load student info
        def load_student():
            name = search_entry.get()

            conn = sqlite3.connect("student_info.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM info WHERE students_name=?", (name,))
            record = cursor.fetchone()
            conn.close()

            # If not found
            if record is None:
                message_label.config(text="Student not found.", fg="red")
                return

            # Clear previous info
            for widget in result_frame.winfo_children():
                widget.destroy()

            # Show student info for confirmation
            info_text = (
                f"Name: {record[0]}\n"
                f"Number: {record[1]}\n"
                f"Address: {record[2]}\n"
                f"Father: {record[3]}\n"
                f"Mother: {record[4]}\n"
                f"Classes: {record[5]}\n"
                f"Age: {record[6]}"
                )

            tk.Label(result_frame, text="Student found:\n\n" + info_text).pack()

            # Delete button
            def confirm_delete():
                conn = sqlite3.connect("student_info.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM info WHERE students_name=?", (name,))
                conn.commit()
                conn.close()

                message_label.config(text="Student deleted successfully!", fg="green")

                # Refresh main window
                self.read_student_info()

                # Clear display
                for widget in result_frame.winfo_children():
                    widget.destroy()

            tk.Button(result_frame, text="CONFIRM DELETE", fg="red", command=confirm_delete).pack()

        # Search button
        tk.Button(delete_window, text="Search", command=load_student).pack()

        #Close button
        close_button = tk.Button(delete_window, text = "Close", command = delete_window.destroy)
        close_button.pack()







info = student_info()
tk.mainloop()
