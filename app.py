# HTBooks GmbH & Co. KG
# 10.10.2022

from flask import Flask, render_template, redirect, request, make_response
import util.db
import util.auth
import util.config

app = Flask(__name__)

@app.route("/")
def index():
    if util.config.AUTH_COOKIE_NAME in request.cookies:
        # Decode and !!!Deserialize!!! the session object from the authentication cookie
        user = util.auth.cookieToSession(request.cookies.get(util.config.AUTH_COOKIE_NAME))
        return render_template("index.html", user=user)

    return render_template("index.html")

@app.route("/catalog")
def catalog():
    if util.config.AUTH_COOKIE_NAME in request.cookies:
        books = util.db.getBooks()
        # Decode and !!!Deserialize!!! the session object from the authentication cookie
        user = util.auth.cookieToSession(request.cookies.get(util.config.AUTH_COOKIE_NAME))
        return render_template("catalog.html", books=books, user=user)

    return redirect("/login")

@app.route("/admin")
def admin():
    # Check if the authentication cookie exists in the user's browser
    if util.config.AUTH_COOKIE_NAME in request.cookies:
        # Decode and !!!Deserialize!!! the session object from the authentication cookie
        user = util.auth.cookieToSession(request.cookies.get(util.config.AUTH_COOKIE_NAME))
        # Render the admin page template, passing the user session object to the template
        return render_template("admin.html", user=user)

    # If no authentication cookie is found, redirect the user to the login page
    return redirect("/login")

@app.route("/signup")
def signup():
    if util.config.AUTH_COOKIE_NAME in request.cookies:
        return redirect("/")
        
    return render_template("signup.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    # Check if the user is already logged in by verifying the authentication cookie
    if util.config.AUTH_COOKIE_NAME in request.cookies:
        return redirect("/")  # Redirect to home page if the user is already authenticated

    # Handle POST request (login form submission)
    if request.method == 'POST':
        # Validate the username and password using the authentication utility
        if util.auth.checkLogin(request.form['username'], request.form['password']):
            # If login is successful, create a response that redirects to the home page
            resp = make_response(redirect("/"))
            # Create a new session object for the authenticated user
            sess = util.auth.Session(request.form['username'])
            # Convert the session object to an encoded cookie string
            # decode(): Convert bytes to string
            auth = util.auth.sessionToCookie(sess).decode()
            # Set the authentication cookie in the response
            resp.set_cookie(util.config.AUTH_COOKIE_NAME, auth)
            return resp  # Return the response to the client with the auth cookie

    # Render the login page template if the request is a GET or authentication fails
    return render_template("login.html")

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie(util.config.AUTH_COOKIE_NAME, '', expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)