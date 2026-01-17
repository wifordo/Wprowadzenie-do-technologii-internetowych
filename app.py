from flask import Flask, render_template, request
from moviesManager import show_all_movies, remove_movie

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        movies_to_remove_ids = request.form.getlist('movieToRemove')
        for movie_id in movies_to_remove_ids:
            remove_movie(movie_id)

    movies = show_all_movies()
    return render_template("home.html", movies=movies)


from flask import Flask, render_template, request, redirect, url_for
from moviesManager import show_all_movies, add_movie

@app.route('/addMovie', methods=['GET', 'POST'])
def addMovie():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        actors = request.form.get('actors')

        add_movie(title, year, actors)
        return redirect(url_for('home'))

    return render_template('add.html')


if __name__ == "__main__":
    app.run()