from fastapi import FastAPI
from typing import Any
import sqlite3

app = FastAPI()


def get_db():
    return sqlite3.connect("movies-extended.db")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}"}


@app.get("/sum")
def sum_numbers(x: int = 0, y: int = 10):
    return x + y


@app.get("/sub")
def subtract_numbers(x: int = 0, y: int = 10):
    return x - y


@app.get("/multi")
def multiply_numbers(x: int = 0, y: int = 10):
    return x * y


@app.get("/movies")
def get_movies():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, director, year, description FROM movie"
    )
    rows = cursor.fetchall()
    conn.close()

    output = []
    for row in rows:
        movie = {
            "id": row[0],
            "title": row[1],
            "director": row[2],
            "year": row[3],
            "description": row[4]
        }
        output.append(movie)

    return output


@app.get("/movies/{movie_id}")
def get_single_movie(movie_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, director, year, description FROM movie WHERE id = ?",
        (movie_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"error": "Movie not found"}

    movie = {
        "id": row[0],
        "title": row[1],
        "director": row[2],
        "year": row[3],
        "description": row[4]
    }

    return movie


@app.get("/actors")
def get_actors():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, surname FROM actor"
    )
    rows = cursor.fetchall()
    conn.close()

    output = []
    for row in rows:
        actor = {
            "id": row[0],
            "name": row[1],
            "surname": row[2]
        }
        output.append(actor)

    return output


@app.get("/actors/{actor_id}")
def get_single_actor(actor_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, surname FROM actor WHERE id = ?",
        (actor_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"error": "Actor not found"}

    actor = {
        "id": row[0],
        "name": row[1],
        "surname": row[2]
    }

    return actor


@app.post("/actors")
def add_actor(params: dict[str, Any]):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO actor (name, surname) VALUES (?, ?)",
        (params["name"], params["surname"])
    )

    conn.commit()
    actor_id = cursor.lastrowid
    conn.close()

    return actor_id


@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, params: dict[str, Any]):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE actor SET name = ?, surname = ? WHERE id = ?",
        (params["name"], params["surname"], actor_id)
    )

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return {"error": "Actor not found"}

    return {"message": "Actor updated successfully"}


@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM actor WHERE id = ?",
        (actor_id,)
    )

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return {"error": "Actor not found"}

    return {"message": "Actor deleted successfully"}


@app.get("/movies/{movie_id}/actors")
def get_movie_actors(movie_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT actor.id, actor.name, actor.surname
        FROM actor
        JOIN movie_actor_through
            ON actor.id = movie_actor_through.actor_id
        WHERE movie_actor_through.movie_id = ?
        """,
        (movie_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    output = []
    for row in rows:
        actor = {
            "id": row[0],
            "name": row[1],
            "surname": row[2]
        }
        output.append(actor)

    return output
