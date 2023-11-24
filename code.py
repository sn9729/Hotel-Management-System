import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import random
import datetime

root = tk.Tk()
root.title("SRM HOTELS LTD")
root.geometry("500x500")  


records = mysql.connector.connect(host='localhost', user='root', password='hellosql123')
cursor = records.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS Records')
cursor.execute('USE Records')

cursor.execute('CREATE TABLE IF NOT EXISTS total_records(name varchar(20), age integer, aadhar_no bigint, room_no integer, DateTime_of_checkin DATETIME, DateTime_of_checkout DATETIME)')
records.commit()
cursor.execute('CREATE TABLE IF NOT EXISTS current_records(name varchar(20), age integer, aadhar_no bigint, room_no integer, DateTime_of_checkin DATETIME)')
records.commit()


password = 'admin_password'


cursor.execute("SELECT room_no FROM current_records;")
n = cursor.fetchall()
occupied_rooms = [i[0] for i in n]


def show_message(title, message):
    messagebox.showinfo(title, message)


def validRoom():
    if len(occupied_rooms) == 50:
        return "full"
    else:
        room = random.randint(1, 50)
        while room in occupied_rooms:
            room = random.randint(1, 50)
        return room

def Bill(d1, d2):
    difference = d2 - d1
    print("You stayed in Hotel for ", difference)
    hours_between = difference.total_seconds() / 3600
    bill = hours_between * 200
    total_bill = round(bill, 2)
    return total_bill

def Booking(room_no):
    if room_no == 'full':
        show_message("Room Booking", "Hotel is full! All rooms are occupied.\nSorry for your inconvenience.")
    else:
   
        occupied_rooms.append(room_no)

        booking_window = tk.Toplevel(root)
        booking_window.title("Booking")
        booking_window.geometry("500x500") 

        tk.Label(booking_window, text=f"Your room number is {room_no}").pack(pady=10)

        tk.Label(booking_window, text="Enter your details:").pack(pady=10)

        tk.Label(booking_window, text="Name:").pack()
        name_entry = tk.Entry(booking_window)
        name_entry.pack()

        tk.Label(booking_window, text="Age:").pack()
        age_entry = tk.Entry(booking_window)
        age_entry.pack()

        tk.Label(booking_window, text="Aadhar Card Number:").pack()
        aadhar_entry = tk.Entry(booking_window)
        aadhar_entry.pack()

        def submit_booking_details():
            name = name_entry.get()
            age = age_entry.get()
            aadhar_no = aadhar_entry.get()

          
            data = (name, age, aadhar_no, room_no, datetime.datetime.now().replace(microsecond=0))
            s = "INSERT INTO current_records (name, age, aadhar_no, room_no, DateTime_of_checkin) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(s, data)
            records.commit()

            show_message("Room Booking", f"Booking successful!\nThank you for choosing us. Happy stay!")

        tk.Button(booking_window, text="Submit", command=submit_booking_details).pack(pady=10)
        tk.Button(booking_window, text="Exit", command=booking_window.destroy).pack(pady=10)



def Service():
    services_window = tk.Toplevel(root)
    services_window.title("Services")
    services_window.geometry("500x500")  

    tk.Label(services_window, text="Select a service:").pack(pady=10)

    def room_cleaning():
        room_cleaning_window = tk.Toplevel(services_window)
        room_cleaning_window.title("Room Cleaning")
        room_cleaning_window.geometry("200x150") 

        tk.Label(room_cleaning_window, text="Enter room number:").pack(pady=5)
        room_entry = tk.Entry(room_cleaning_window)
        room_entry.pack(pady=5)

        def submit_room_cleaning():
            room = room_entry.get()
            if int(room) in occupied_rooms:
                show_message("Room Cleaning", "We will send cleaning staff to your room in 5 minutes. Please wait.")
            else:
                show_message("Room Cleaning", "Room is not occupied. Enter a valid room number.")

        tk.Button(room_cleaning_window, text="Submit", command=submit_room_cleaning).pack(pady=10)

    def food_service():
        food_service_window = tk.Toplevel(services_window)
        food_service_window.title("Food Service")
        food_service_window.geometry("200x150") 

        tk.Label(food_service_window, text="Enter room number:").pack(pady=5)
        room_entry = tk.Entry(food_service_window)
        room_entry.pack(pady=5)

        def submit_food_service():
            room = room_entry.get()
            if int(room) in occupied_rooms:
                show_message("Food Service", "Menu card will be delivered to your room.")
            else:
                show_message("Food Service", "Room is not occupied. Enter a valid room number.")

        tk.Button(food_service_window, text="Submit", command=submit_food_service).pack(pady=10)

    tk.Button(services_window, text="Room Cleaning", command=room_cleaning).pack(pady=5)
    tk.Button(services_window, text="Food Service", command=food_service).pack(pady=5)

def Checkout():
    checkout_window = tk.Toplevel(root)
    checkout_window.title("Checkout")
    checkout_window.geometry("500x500")  

    tk.Label(checkout_window, text="Enter your room number:").pack(pady=10)
    room_entry = tk.Entry(checkout_window)
    room_entry.pack(pady=10)

    def submit_checkout():
        room = room_entry.get()
        if int(room) in occupied_rooms:
            cursor.execute(f'SELECT * FROM current_records WHERE room_no = "{room}"')
            query = cursor.fetchall()
            query = query[0]
            cursor.execute(f"SELECT DateTime_of_checkin FROM current_records WHERE room_no = '{room}'")
            date = cursor.fetchall()
            for i in date:
                date_of_checkin = i[0]
            current_datetime = datetime.datetime.now().replace(microsecond=0)
            bill = Bill(date_of_checkin, current_datetime)
            show_message("Checkout", f"Your total bill is Rs. {bill}\nThank you for your stay. Hope you had a great time.")

            new_query = (*query, current_datetime)
            s = "INSERT INTO total_records (name, age, aadhar_no, room_no, DateTime_of_checkin, DateTime_of_checkout) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(s, new_query)
            cursor.execute(f"DELETE FROM current_records WHERE room_no='{room}'")
            records.commit()
            show_message("Checkout", "Checkout successful!")
        else:
            show_message("Checkout", "Please enter correct room number!")

    tk.Button(checkout_window, text="Submit", command=submit_checkout).pack(pady=10)


def admin_interface():
    password_attempt = simpledialog.askstring("Admin Interface", "Enter admin password:")
    if password_attempt == password:
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Interface")
        admin_window.geometry("500x500")

        tk.Label(admin_window, text="Enter admin option (1: Display current occupants, 2: Display records of people who left, 3: Exit):").pack(pady=10)


        def handle_admin_option():
            admin_input = int(admin_var.get())
            if admin_input == 1:

                cursor.execute("SELECT room_no, name, DateTime_of_checkin FROM current_records;")
                rec1 = cursor.fetchall()

                output_text = "Room Number   |   Customer Name   |   Check-in Time\n"
                output_text += "-" * 50 + "\n"

                for row in rec1:
                    output_text += f"{row[0]}               |   {row[1]}                   |   {row[2]}\n"

 
                output_window = tk.Toplevel(admin_window)
                output_window.title("Current Occupants")
                tk.Label(output_window, text=output_text).pack()

            elif admin_input == 2:

                cursor.execute("SELECT name, room_no, DateTime_of_checkin, DateTime_of_checkout FROM total_records;")
                rec2 = cursor.fetchall()

                output_text = "Customer Name   |   Room Number   |   Check-in Time                |   Check-out Time\n"
                output_text += "-" * 90 + "\n"

                for row in rec2:
                    output_text += f"{row[0]}                     |   {row[1]}               |   {row[2]}                           |   {row[3]}\n"


                output_window = tk.Toplevel(admin_window)
                output_window.title("Records of People Who Left")
                tk.Label(output_window, text=output_text).pack()

            elif admin_input == 3:
                admin_window.destroy()
            else:
                show_message("Admin Interface", "Enter valid option!")

        admin_var = tk.StringVar()
        tk.Entry(admin_window, textvariable=admin_var).pack(pady=10)
        tk.Button(admin_window, text="Submit", command=handle_admin_option).pack(pady=10)

    else:
        show_message("Admin Interface", "Invalid admin password!")


admin_button = tk.Button(root, text="Admin Interface", command=admin_interface)
admin_button.pack(pady=10)


booking_button = tk.Button(root, text="Book a Room", command=lambda: Booking(validRoom()))
booking_button.pack(pady=10)

services_button = tk.Button(root, text="Room Services", command=Service)
services_button.pack(pady=10)

checkout_button = tk.Button(root, text="Checkout", command=Checkout)
checkout_button.pack(pady=10)

root.mainloop()
