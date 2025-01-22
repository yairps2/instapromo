import psycopg2, os
from psycopg2.extras import execute_values

################ SETTINGS #############
database = "instapromo" #os.getenv("DATABASE_NAME")
database_user = "instapromo" #os.getenv("DATABASE_USER")
database_password = "instapromo" #os.getenv("DATABASE_PASSWORD")
########################################

def add_user(user_info: list):
    try:
        username = user_info[0]
        full_name = user_info[1]
        follower_count = user_info[2]
        biography = user_info[3]
        public_email = user_info[4]
        phone = user_info[5]
        bio_links = [link.url for link in user_info[6]]
        bio_emails = user_info[7]

        # Ensure bio_links and bio_emails are lists of strings
        bio_links = [str(link) for link in bio_links]
        bio_emails = [str(email) for email in bio_emails]

        # Connect to the database
        conn = psycopg2.connect(
            dbname=database, user=database_user, password=database_password
        )
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            print(f"User with username '{username}' already exists.")
            return

        # Insert the user into the Users table
        cursor.execute(
            """
            INSERT INTO users (username, full_name, follower_count, bio, public_email, phone)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """,
            (username, full_name, follower_count, biography, public_email, phone),
        )
        user_id = cursor.fetchone()[0]

        # Insert bio links into the UserBioLinks table
        if bio_links:
            bio_links_data = [(user_id, link) for link in bio_links]
            execute_values(
                cursor,
                "INSERT INTO UserBioLinks (user_id, link) VALUES %s",
                bio_links_data,
            )

        # Insert bio emails into the UserBioEmails table
        if bio_emails:
            bio_emails_data = [(user_id, email) for email in bio_emails]
            execute_values(
                cursor,
                "INSERT INTO UserBioEmails (user_id, email) VALUES %s",
                bio_emails_data,
            )

        # Commit the transaction
        conn.commit()
        print(f"User '{username}' added successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
