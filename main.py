import requests
import sqlite3
import csv
import matplotlib.pyplot as plt

# ==========================================================
# TASK 1: API to SQLite (Books)
# ==========================================================


def task1_api_to_db():
    print("\n--- Running Task 1: API to SQLite (Books) ---")
    api_url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            books_raw = response.json()[:10]

            conn = sqlite3.connect('assignment_data.db')
            cursor = conn.cursor()

            cursor.execute('DROP TABLE IF EXISTS books')
            cursor.execute(
                'CREATE TABLE books (id INTEGER, title TEXT, author TEXT, year INTEGER)')

            for item in books_raw:
                # In API year, author were not present so try to fill it by small changes 
                cursor.execute('INSERT INTO books VALUES (?, ?, ?, ?)',
                               (item['id'], item['title'], f"Author_{item['userId']}", 2026))

            conn.commit()
            conn.close()
            print("Task 1 Complete: Books stored in 'assignment_data.db'")
    except Exception as e:
        print(f"Task 1 Error: {e}")

# ==========================================================
# TASK 2: Data Processing & Visualization (Students)
# ==========================================================


def task2_visualization():
    print("\n--- Running Task 2: Real API Fetch (Students) ---")

    api_url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            raw_data = response.json()[:5]  # Fetching 5 students data 

            student_list = []
            for user in raw_data:
                student_list.append({
                    "name": user['name'],
                    # Logic: 75, 80, 85... we want to provide different marks so *5 will make this variation  
                    "score": 70 + (user['id'] * 5)  
                })

            names = [s['name'] for s in student_list]
            scores = [s['score'] for s in student_list]

            # 4. Average calculate karna
            avg = sum(scores) / len(scores)
            print(f"API Data Processed. Average Score: {avg:.2f}")

            # 5. Visualization (Bar Chart)
            plt.figure(figsize=(10, 6))
            plt.bar(names, scores, color='lightcoral', edgecolor='red')
            plt.axhline(y=avg, color='blue', linestyle='--',
                        label=f'Average: {avg}')

            plt.title('Student Test Scores')
            plt.xlabel('Student Names')
            plt.ylabel('Scores')
            plt.legend()
            plt.show()
        else:
            print("Error: Could not connect with API.")

    except Exception as e:
        print(f"Task 2 Error: {e}")


# ==========================================================
# TASK 3: CSV Data Import to Database (Users)
# ==========================================================


def task3_csv_to_db():
    print("\n--- Running Task 3: CSV Import (Users) ---")
    csv_file = "users.csv"  

    try:
        conn = sqlite3.connect('assignment_data.db')
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('CREATE TABLE users (name TEXT, email TEXT)')

        with open(csv_file, mode='r') as f:
            reader = csv.DictReader(f)
            # Inserting Row by row 
            for row in reader:
                cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)',
                               (row['name'], row['email']))

        conn.commit()
        conn.close()
        print(
            f"Task 3 Complete: Data from '{csv_file}' imported to 'users' table.")
    except FileNotFoundError:
        print(f"Error: '{csv_file}' nahi mili! Check directory.")
    except Exception as e:
        print(f"Task 3 Error: {e}")


# Main Trigger
if __name__ == "__main__":
    task1_api_to_db()
    task3_csv_to_db()
    task2_visualization()
