import sqlite3

DB_NAME = "movies.db"


def show_all_movies():
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()
    db.close()
    return movies

def findMovie(text):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    pattern = f"%{text}%"
    cursor.execute("""
        SELECT * FROM movies
        WHERE title LIKE ?
           OR actors LIKE ?
    """, (pattern, pattern))

    for row in cursor:
        print(f"{row[1]}, {row[2]}, {row[3]}")

    db.close()


def add_movie(title, year, actors):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO movies (title, year, actors)
        VALUES (?, ?, ?)
    """, (title, year, actors))

    db.commit()
    db.close()

def remove_movie(movie_id):
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()

        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        db.commit()
        db.close()
