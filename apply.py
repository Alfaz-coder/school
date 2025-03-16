import mysql.connector
import streamlit as st
import os

# Database connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="alfaz"
    )
    mycursor = mydb.cursor()
    print("Connection Established")
except mysql.connector.Error as err:
    st.error(f"Error: {err}")

# Streamlit App
def main():
    st.title("CRUD Operations With MySQL")

    # Sidebar for CRUD operations
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

    if option == "Create":
        st.subheader("Create a Record")
        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")
        if st.button("Create"):
            if name and email:
                sql = "INSERT INTO emp (name, email) VALUES (%s, %s)"
                val = (name, email)
                try:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Record Created Successfully!!!")
                except mysql.connector.Error as err:
                    st.error(f"Error: {err}")
            else:
                st.warning("Please fill in all fields.")

    elif option == "Read":
        st.subheader("Read Records")
        mycursor.execute("SELECT * FROM emp")
        result = mycursor.fetchall()
        if result:
            st.table(result)
        else:
            st.info("No records found.")

    elif option == "Update":
        st.subheader("Update a Record")
        mycursor.execute("SELECT id, name, email FROM emp")
        records = mycursor.fetchall()
        if records:
            st.write("Existing Records:")
            st.table(records)
            id = st.number_input("Enter ID to Update", min_value=1)
            name = st.text_input("Enter New Name")
            email = st.text_input("Enter New Email")
            if st.button("Update"):
                sql = "UPDATE emp SET name=%s, email=%s WHERE id=%s"
                val = (name, email, id)
                try:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Record Updated Successfully!!!")
                except mysql.connector.Error as err:
                    st.error(f"Error: {err}")
        else:
            st.info("No records found to update.")

    elif option == "Delete":
        st.subheader("Delete a Record")
        mycursor.execute("SELECT id, name, email FROM emp")
        records = mycursor.fetchall()
        if records:
            st.write("Existing Records:")
            st.table(records)
            id = st.number_input("Enter ID to Delete", min_value=1)
            if st.button("Delete"):
                confirm = st.checkbox("Are you sure you want to delete this record?")
                if confirm:
                    sql = "DELETE FROM emp WHERE id=%s"
                    val = (id,)
                    try:
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Record Deleted Successfully!!!")
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
                else:
                    st.warning("Deletion canceled.")
        else:
            st.info("No records found to delete.")

if __name__ == "__main__":
    try:
        main()
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")