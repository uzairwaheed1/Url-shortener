import string
import random
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
url_map = {}

def generate_short_url():
    """Generate a random string of 6 characters."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the long URL from the form submission
        long_url = request.form['long_url']

        # generate a short URL
        short_url = generate_short_url()

        # store the short URL and long URL in a dictionary
        while short_url in url_map:
           short_url = generate_short_url()
        url_map[short_url] = long_url
        print("URL Map:", url_map)

        # return the shortened URL to the user
        return render_template('index.html', short_url=request.host_url + short_url)

    return render_template('index.html')


@app.route('/<short_url>')
def redirect_to_url(short_url):
    # check if the short URL exists in the url_map dictionary
    if short_url in url_map:
        # get the long URL corresponding to the short URL from the dictionary
        long_url = url_map[short_url]
        # redirect to the long URL
        return redirect(long_url)
    else:
        # if the short URL doesn't exist, return a 404 error
        return render_template('error.html'), 404
    
if __name__ == '__main__':
    app.run(debug=True)