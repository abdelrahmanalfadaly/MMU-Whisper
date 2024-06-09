import mysql.connector
config = {
    'user': 'root',
    'password': 'Belal78@',
    'host':'localhost',
    'database': 'mmu'
}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to the database")
        cursor = connection.cursor()  
        cursor.execute("Select * from classes")
        result = cursor.fetchall()
        for row in result:
            print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed")
