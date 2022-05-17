from flask import Flask, render_template, request, redirect, flash, url_for, session
import json
import requests
from PIL import Image 
from urllib.request import urlopen
import urllib.parse

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CST_205_FINAL_PROJECT'

    return app


app = create_app()

accessKey = "WP9eVA46vbsFbNzyJlF3LtURMwTc-SVnHt9l6tQ1mNg"
secretKey = "imwAU6CXNRSEgkupxT3MGfEDmL1dTkFIJyvK91a-4Dc"

# https://api.unsplash.com/search/photos?query=funny&client_id=WP9eVA46vbsFbNzyJlF3LtURMwTc-SVnHt9l6tQ1mNg

searchTerm = ''

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    
    
    if request.method == 'POST':
        searchTerm = request.form.get('searchTerm')
        
        if len(searchTerm) > 16:
            flash('Invalid Search', category='error')
            
        elif len(searchTerm) < 2:
            flash('Invalid Search Term', category='error')    
        else:
            flash('Searching Now', category='success')
            
            return redirect(url_for('search', searchTerm = searchTerm))
    
    return render_template('landingPage.html')

@app.route('/searchResults/<searchTerm>', methods=['GET', 'POST'])
def search(searchTerm):
    
    APIurl = 'https://api.unsplash.com/search/photos?query=' + searchTerm + '&client_id=' + accessKey
    
    response = urlopen(APIurl)
    
    #contains total response from unsplash API
    jsonData = json.loads(response.read())
    
    unsplashSearchResults = jsonData['results']
    
    pictureUrls = []
    
    for i in unsplashSearchResults:
        pictureUrls.append(i['urls']['regular'])
    
    
    displayImage = pictureUrls[0]
    


    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)



@app.route('searchResults/sepia/<searchTerm>/<displayImage>')
def sepia(searchTerm, displayImage):
    return 0
    


app.run(debug=True) 

