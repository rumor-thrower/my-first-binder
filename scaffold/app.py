from flask import Flask, render_template, redirect, request, url_for
import psycopg

app = Flask(__name__)
connect = psycopg.connect("dbname=term user=postgres password=")
connect.autocommit = True # autocommit is enabled: each query is committed immediately like psql
cur = connect.cursor()
myid = None
movies = None
reviews = None

@app.route('/')
def main():
    global myid
    myid = None
    return render_template("index.html")

#region index.html (Sign In / Sign Up)
@app.route('/signing', methods=['post'])
def signing():
    send = request.form["send"]
    id = request.form["id"]
    pwd = request.form["password"]
    if send == "sign up":
        return signup(id, pwd)
    elif send == "sign in":
        return signin(id, pwd)
    return

def signup(id, pwd):
    # TODO
    pass

def signin(id, pwd):
    global myid
    cur.execute(f"select count(id) from users where id = '{id}' and password = '{pwd}'")
    result = cur.fetchall()
    if result[0][0] == 0:
        return render_template("index.html", warnings="가입되어 있지 않은 회원입니다. 가입부터 해주세요.")
    else:
        myid = id
        return redirect(url_for('movies'))

#endregion


#region movies.html (Movie List / Review List)
@app.route('/movies', methods=['get', 'post'])
def movies():
    global movies, reviews
    movies = movies_listing("latest")
    reviews = reviews_listing("latest")
    return render_template("movies.html", myid=myid, movies=movies, reviews=reviews)

@app.route('/movies/listing', methods=['post'])
def listing():
    global movies, reviews
    if "movieOpt" in request.form.keys():
        movieOpt = request.form["movieOpt"]
        movies = movies_listing(movieOpt)
    if "reviewOpt" in request.form.keys():
        reviewOpt = request.form["reviewOpt"]
        reviews = reviews_listing(reviewOpt)
    return render_template("movies.html", myid=myid, movies=movies, reviews=reviews)

def movies_listing(movieOpt):
    global movies
    if movieOpt == "latest":
        movies = movies_latest()
    elif movieOpt == "genre":
        movies = movies_genre()
    elif movieOpt == "ratings":
        movies = movies_ratings()
    return movies

def reviews_listing(reviewOpt):
    global reviews
    if reviewOpt == "latest":
        reviews = reviews_latest()
    elif reviewOpt == "title":
        reviews = reviews_title()
    elif reviewOpt == "ratings":
        reviews = reviews_ratings()
    return reviews

def movies_latest():
    # TODO: Return movie list sorted by release date (desc)
    pass

def movies_genre():
    # TODO: Return movie list sorted by genre (asc)
    pass

def movies_ratings():
    # TODO: Return movie list sorted by avg ratings (desc)
    pass

def reviews_latest():
    # TODO: Return review list sorted by review time (desc)
    pass

def reviews_title():
    # TODO: Return review list sorted by movie title (asc)
    pass

def reviews_ratings():
    # TODO: Return review list sorted by ratings (desc)
    pass

#endregion


#region movie_info.html (Movie Info / Write Review)
@app.route('/movies/<title>', methods=['get', 'post'])
def movie_info(title):
    if "mid" in request.form.keys():
        mid = request.form["mid"]
    else:
        mid = request.args["mid"]
    # TODO
    director = None
    genre = None
    rel_date = None
    avg_ratings = None
    reviews = None
    return render_template("movie_info.html", myid=myid, mid=mid, title=title, director=director, genre=genre, rel_date=rel_date, avg_ratings=avg_ratings, reviews=reviews)

@app.route('/movies/<title>/submit', methods=['post'])
def review_submit(title):
    global myid
    mid = request.form["mid"]
    review = request.form["review"]
    review = review.replace("'", "''") # escape single-quote
    ratings = request.form["ratings"]
    # TODO
    return redirect(url_for("movie_info", title=title, mid=mid))

#endregion


#region user_info.html (User Info / Follow / Mute)
@app.route('/users/<uid>', methods=['post', 'get'])
def user_info(uid):
    # TODO
    reviews = None
    followers = None
    following = None
    muted = None
    is_admin = False
    return render_template("user_info.html", myid=myid, uid=uid, reviews=reviews, followers=followers,
                           following=following, muted=muted, is_admin=is_admin)

@app.route('/users/<uid>/untie', methods=['post'])
def untie(uid):
    # TODO
    return redirect(url_for("user_info", uid=myid))

@app.route('/users/<uid>/follow_mute', methods=['post'])
def follow_mute(uid):
    # TODO
    return redirect(url_for("user_info", uid=uid))

@app.route('/users/<uid>/update_movies', methods=['post'])
def update_movies(uid):
    title = request.form["title"]
    director = request.form["director"]
    genre = request.form["genre"]
    rel_date = request.form["rel_date"]
    # TODO
    return redirect(url_for("user_info", uid=myid))

#endregion


# ============================================
# Additional Functions
# Implement at least 2 additional functions
# You need to create your own routes, templates, and SQL queries
# If you modify term.sql, describe the changes in your report
# ============================================


if __name__ == '__main__':
    app.run(debug=True)
