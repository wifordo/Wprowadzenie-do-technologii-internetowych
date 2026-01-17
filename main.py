from fastapi import FastAPI
from typing import Any
import requests
import sqlite3

app = FastAPI()


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


@app.get("/geocode")
def geocode(lat: float, lon: float):
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "zoom": 18,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()


@app.get("/movies")
def get_movies():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, year, actors FROM movies")
    rows = cursor.fetchall()

    conn.close()

    output = []
    for row in rows:
        movie = {
            "id": row[0],
            "title": row[1],
            "year": row[2],
            "actors": row[3]
        }
        output.append(movie)

    return output

@app.get("/movies/{movie_id}")
def get_single_movie(movie_id: int):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, year, actors FROM movies WHERE id = ?",
        (movie_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {"error": "Movie not found"}

    movie = {
        "id": row[0],
        "title": row[1],
        "year": row[2],
        "actors": row[3]
    }

    return movie

@app.post("/movies")
def add_movie(params: dict[str, Any]):
    title = params["title"]
    year = params["year"]
    actors = params["actors"]

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
        (title, year, actors)
    )

    conn.commit()
    movie_id = cursor.lastrowid
    conn.close()

    return movie_id

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM movies WHERE id = ?",
        (movie_id,)
    )

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return {"error": "Movie not found"}

    return {"message": "Movie deleted successfully"}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    title = params["title"]
    year = params["year"]
    actors = params["actors"]

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE movies SET title = ?, year = ?, actors = ? WHERE id = ?",
        (title, year, actors, movie_id)
    )

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return {"error": "Movie not found"}

    return {"message": "Movie updated successfully"}

@app.delete("/movies")
def delete_all_movies():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM movies")
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected

