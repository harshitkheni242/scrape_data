import mysql.connector as conn
from mysql.connector import Error
from datetime import datetime
from contextlib import closing
import re


# This Hotel Management Class use init method auto call and check connection
class HotelManagement:
    def __init__(self):
        try:
            self.connection = conn.connect(host="localhost", user="root", port="3306", password="tP_kc8mn",
                                           database="hotel", auth_plugin='mysql_native_password')
        except Error as e:
            print("Error connecting to MySQL database:", e)
            exit()

        try:
            with closing(self.connection.cursor()) as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                                        room_id INT PRIMARY KEY AUTO_INCREMENT,
                                        room_number INT,
                                        room_type VARCHAR(50),
                                        location VARCHAR(100),
                                        max_guests INT,
                                        rent DECIMAL(10, 2),
                                        status VARCHAR(20)
                        )''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                                        booking_id INT AUTO_INCREMENT PRIMARY KEY,
                                        cname VARCHAR(100),
                                        id_type VARCHAR(20),
                                        id_no VARCHAR(20),
                                        address VARCHAR(100),
                                        phone VARCHAR(15),
                                        gender VARCHAR(10),
                                        d_checkin DATE,
                                        room_id INT,
                                        checkoutdate DATE,
                                        FOREIGN KEY(room_id) REFERENCES rooms(room_id)
                        )''')

                print("Tables checked/created successfully")
        except Error as e:
            print("Error creating tables:", e)
        finally:
            cursor.close()

    def showmenu(self):
        while True:
            print("@" * 30)
            print("----    HOTEL    ----")
            print("@" * 30)
            print("Press 1 - Create a New Room")
            print("Press 2 - Show All Rooms")
            print("Press 3 - Show All Vacant Rooms")
            print("Press 4 - Show All Occupied Rooms")
            print("Press 5 - Book a Room")
            print("Press 6 - Show Booking")
            print("Press 7 - Check Out")
            print("Press 8 - Exit")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.createroom()
                elif choice == 2:
                    self.showrooms()
                elif choice == 3:
                    self.showvacantrooms()
                elif choice == 4:
                    print(self.showoccupiedrooms())
                elif choice == 5:
                    self.bookroom()
                elif choice == 6:
                    self.showbookings()
                elif choice == 7:
                    self.checkout()
                elif choice == 8:
                    break
            except ValueError:
                print("Invalid input Please enter a valid numeric option")

    def createroom(self):
        print(" --- ENTER ROOM DETAILS  --- ")
        room_no = int(input("Enter Room no: "))
        room_type = input("Enter Room Type(Simple/Delux/Super Delux): ")
        max_guests = int(input("Enter maximum number of guests: "))
        location = input("Enter Location details floor: ")
        rent = float(input("Enter Per Day Charges: "))
        status = "Vacant"

        try:
            with closing(self.connection.cursor()) as cursor:
                query = ("INSERT INTO rooms (room_number, room_type, location, max_guests, rent, status) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
                data = (room_no, room_type, location, max_guests, rent, status)
                cursor.execute(query, data)
                self.connection.commit()
                print("--- Room Created Successfully ---")
        except Error as e:
            print("Room Details Not Inserted:", e)


    def showrooms(self):
        print(
            f"{'Room Id':>10}{'Room Number':>15}{'Room Type':>15}"
            f"{'Floor Location':>20}{'Guests':>10}{'Rent':>10}{'Status':>10} ")
        query = "SELECT * FROM rooms"
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"{row[0]:>5}{row[1]:>15}{row[2]:>22}{row[3]:>11}{row[4]:>15}{row[5]:>15}{row[6]:>10}")
        cursor.close()

    def showbookings(self):
        search_data = input("Serching data Yes/NO: ")
        if 'yes' == search_data.lower():
            enter_name = input("Enter name and search data: ")
            print(
                f"{'Booking Id':>10}{'Customer Name':>15}{'Id Type':>15}{'Id Number':>15}{'Address':>10}"
                f"{'Phone No':>15}{'Gender':>10}{'Checkin Date':>10}{'Room Id':>10}{'Checkout Date':>10}{'Email':>10} ")
            query = f"SELECT * FROM bookings WHERE cname LIKE '%{enter_name}%'"
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                for row in results:
                    booking_id = row[0] if row[0] else ''
                    customer_name = row[1] if row[1] else ''
                    id_type = row[2] if row[2] else ''
                    id_number = row[3] if row[3] else ''
                    address = row[4] if row[4] else ''
                    phone_no = row[5] if row[5] else ''
                    gender = row[6] if row[6] else ''
                    (checkin_date) = row[7]
                    room_id = row[8] if row[8] else ''
                    checkout_date = row[9] if row[9] else ''
                    email = row[10] if row[10] else ''
                    print(f"{booking_id:>5}{customer_name:>15}{id_type:>22}{id_number:>11}{address:>15}"
                          f"{phone_no:>15}{gender:>8}{str(checkin_date):>11}{room_id:>30}{str(checkout_date):>15}{email:>8}")
                cursor.close()
            else:
                print("Data not available")

        else:
            print(
                f"{'Booking Id':>10}{'Customer Name':>15}{'Id Type':>15}{'Id Number':>25}{'Address':>10}"
                f"{'Phone No':>10}{'Gender':>11}{'Checkin Date':>15}{'Room Id':>12}{'Checkout Date':>15}{'Email':>15} "
            )
            query = "SELECT * FROM bookings"
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                booking_id = row[0] if row[0] else ''
                customer_name = row[1] if row[1] else ''
                id_type = row[2] if row[2] else ''
                id_number = row[3] if row[3] else ''
                address = row[4] if row[4] else ''
                phone_no = row[5] if row[5] else ''
                gender = row[6] if row[6] else ''
                checkin_date = row[7] if row[7] else ''
                room_id = row[8] if row[8] else ''
                checkout_date = row[9] if row[9] else ''
                email = row[10] if row[10] else ''
                print(
                    f"{booking_id:>5}{customer_name:>15}{id_type:>18}{id_number:>22}{address:>10}{phone_no:>12}"
                    f"{gender:>5}{str(checkin_date):>15}{room_id:>10}{str(checkout_date):>15}{email:>8}")
            cursor.close()

    def showvacantrooms(self):
        print(
            f"{'Room Id':>10}{'Room Number':>15}{'Room Type':>15}"
            f"{'Floor Location':>20}{'Guests':>10}{'Rent':>10}{'Status':>10} ")
        query = "SELECT * FROM rooms WHERE status='Vacant'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"{row[0]:>5}{row[1]:>15}{row[2]:>22}{row[3]:>10}{row[4]:>15}{row[5]:>15}{row[6]:>8}")

        cursor.close()

    def showoccupiedrooms(self):
        print(
            f"{'Room Id':>10}{'Room Number':>15}{'Room Type':>15}"
            f"{'Floor Location':>20}{'Guests':>10}{'Rent':>10}{'Status':>10} ")
        query = "SELECT * FROM rooms WHERE status='Occupied'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"{row[0]:>5}{row[1]:>15}{row[2]:>22}{row[3]:>10}{row[4]:>15}{row[5]:>15}{row[6]:>8}")
        cursor.close()

    def bookroom(self):
        print("-" * 40)
        print("       BOOKING A ROOM ")
        print("-" * 40)

        try:
            with closing(self.connection.cursor()) as cursor:
                queryvacantrooms = "SELECT room_id, room_number FROM rooms WHERE status='Vacant'"
                cursor.execute(queryvacantrooms)
                vacantrooms = cursor.fetchall()

                if vacantrooms:
                    print("Available Vacant Rooms:")
                    print(f"{'Room ID':<10}{'Room Number':<15}")
                    for room in vacantrooms:
                        print(f"{room[0]:<10}{room[1]:<15}")

                    room_id = int(input("Enter the Room ID to book: "))
                    if any(room_id == room[0] for room in vacantrooms):
                        cname = input("Enter the Customer Name: ")

                        while True:
                            try:
                                id_proof = input(
                                    "Enter the ID submitted (Pan/License/aadhaar/Passport) and number space separated: "
                                    "").split()

                                if "pan" == id_proof[0].lower() and len(id_proof[1]) != 10:
                                    print('Pan details is invalid')

                                elif "license" == id_proof[0].lower() and len(id_proof[1]) != 16:
                                    print('License details is invalid')

                                elif "aadhaar" == id_proof[0].lower() and len(id_proof[1]) != 12:
                                    print('Aadhar details is invalid')

                                elif "passport" == id_proof[0].lower() and len(id_proof[1]) != 8:
                                    print('Passport details is invalid')

                                else:
                                    break
                            except (ValueError, IndexError) as e:
                                print("Enter a valid id proof details", e)

                        address = input("Enter Address: ")
                        regex = r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,7}\b'
                        while True:
                            email = input("Enter Valid Email id : ")
                            if re.fullmatch(regex, email):
                                break
                            else:
                                print("Enter valid email")
                                continue

                        phone = input("Enter Phone number: ")
                        while len(phone) != 10:
                            print("Please enter a 10-digit phone number")
                            phone = input("Enter Phone number: ")

                        gender = input("Enter Gender Male/Female/Other: ")
                        d_checkin = datetime.now().date()
                        print(d_checkin)
                        query_insert_booking = ("INSERT INTO bookings "
                                                "(cname, id_type, id_no, address, email, phone, gender, d_checkin, room_id)"
                                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

                        data = (cname, id_proof[0], id_proof[1], address, email, phone, gender, d_checkin, room_id)
                        cursor.execute(query_insert_booking, data)

                        query_update_status = "UPDATE rooms SET status='Occupied' WHERE room_id=%s"
                        cursor.execute(query_update_status, (room_id,))

                        self.connection.commit()
                        print("-" * 50)
                        print("      ROOM BOOKED")
                        print("-" * 50)
                    else:
                        print("Invalid Room ID. Please select a valid room ID")
                else:
                    print("No vacant rooms available for booking")
        except Error as e:
            print("Error booking room:", e)
        finally:
            cursor.close()

    def checkout(self):
        room_id = int(input("Enter the room id: "))
        checkout_date = datetime.now().date()

        try:
            with closing(self.connection.cursor()) as cursor:
                query_checkin = "SELECT d_checkin FROM bookings WHERE room_id = %s"
                cursor.execute(query_checkin, (room_id,))
                checkin_date1 = cursor.fetchone()

                if checkin_date1:
                    checkin_date = checkin_date1[0]

                    total_days = (checkout_date - checkin_date).days

                    query_rent = "SELECT rent FROM rooms WHERE room_id = %s"
                    cursor.execute(query_rent, (room_id,))
                    rent_row = cursor.fetchone()

                    if rent_row:
                        rent = rent_row[0]

                        total_payment = rent * total_days

                        queryupdatestatus = "UPDATE rooms SET status='Vacant' WHERE room_id = %s"
                        cursor.execute(queryupdatestatus, (room_id,))

                        queryupdate_checkoutdate = "UPDATE bookings SET checkoutdate = %s WHERE room_id = %s"
                        cursor.execute(queryupdate_checkoutdate, (checkout_date, room_id))

                        self.connection.commit()

                        print("-" * 50)
                        print("       CHECKOUT DETAILS")
                        print("-" * 50)
                        print(f"Check-In Date: {checkin_date}")
                        print(f"Checkout Date: {checkout_date}")
                        print(f"Duration of Stay: {total_days} days")
                        print(f"Room Rent per day: {rent}")
                        print(f"Total Payment: {total_payment}")
                        print("-" * 50)
                    else:
                        print("Rent details not found")
                else:
                    print("No check-in date found")
        except Error as e:
            print("Error checkingout:", e)
        finally:
            if cursor:
                cursor.close()


hotel = HotelManagement()

if hotel.connection.is_connected():
    hotel.showmenu()
