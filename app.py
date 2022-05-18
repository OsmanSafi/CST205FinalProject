from flask import Flask, render_template, request, redirect, flash, url_for, session
import json
import requests, aiohttp
from io import BytesIO
from urllib.request import urlopen
import urllib.parse
from imageConversions import *
import io
import PIL
from PIL import Image 
import numpy 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CST_205_FINAL_PROJECT'

    return app




app = create_app()

accessKey = "WP9eVA46vbsFbNzyJlF3LtURMwTc-SVnHt9l6tQ1mNg"
secretKey = "imwAU6CXNRSEgkupxT3MGfEDmL1dTkFIJyvK91a-4Dc"

# https://api.unsplash.com/search/photos?query=funny&client_id=WP9eVA46vbsFbNzyJlF3LtURMwTc-SVnHt9l6tQ1mNg

searchTerm = ''   
    

def accessAPI(searchTerm):
    
    APIurl = 'https://api.unsplash.com/search/photos?query=' + searchTerm + '&client_id=' + accessKey
    
    response = urlopen(APIurl)
    
    #contains total response from unsplash API
    jsonData = json.loads(response.read())
    
    unsplashSearchResults = jsonData['results']
    
    pictureUrls = []
    
    for i in unsplashSearchResults:
        pictureUrls.append(i['urls']['regular'])
    
    return pictureUrls

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    
    
    if request.method == 'POST':
        searchTerm = request.form.get('searchTerm')
        ImageNumber = 0
        
        if len(searchTerm) > 16:
            flash('Invalid Search', category='error')
            
        elif len(searchTerm) < 2:
            flash('Invalid Search Term', category='error')    
        else:
            flash('Searching Now', category='success')
            
            return redirect(url_for('search', searchTerm = searchTerm, ImageNumber= ImageNumber))
    
    return render_template('landingPage.html')

@app.route('/searchResults/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def search(searchTerm, ImageNumber):
    
    ImgN = int(ImageNumber)
    pictureUrls = accessAPI(searchTerm)
    
    displayImage = pictureUrls[ImgN]
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))

    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)


@app.route('/sepia/<searchTerm>/<ImageNumber>', methods=['GET','POST'])
def sepiaConversion(searchTerm, ImageNumber):
    
    ImgN = int(ImageNumber)
    pictureList = accessAPI(searchTerm)
    baseImage = pictureList[ImgN] 
    
    
    urllib.request.urlretrieve(baseImage + ".png", "picture.png")

    importedImage = Image.open('picture.png')


    convertedImage = sepia(importedImage)
    
    displayImage = pil2datauri(convertedImage)
      
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    
    
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)
    

@app.route('/gamma/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def gammaConversion(searchTerm, ImageNumber):
    ImgN = int(ImageNumber)
    pictureList = accessAPI(searchTerm)
    baseImage = pictureList[ImgN] 
    
    urllib.request.urlretrieve(baseImage + ".png", "picture.png")

    importedImage = Image.open('picture.png')


    convertedImage = Gamma(importedImage)
    
    displayImage = pil2datauri(convertedImage)
    
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)
    

@app.route('/negative/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def negativeConversion(searchTerm, ImageNumber): 
    ImgN = int(ImageNumber)
    pictureList = accessAPI(searchTerm)
    baseImage = pictureList[ImgN] 
    
    urllib.request.urlretrieve(baseImage + ".png", "picture.png")

    importedImage = Image.open('picture.png')


    convertedImage = sepia(importedImage)
    
    displayImage = pil2datauri(convertedImage)
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)
    

@app.route('/grayScale/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def grayScaleConversion(searchTerm, ImageNumber):   
    
    ImgN = int(ImageNumber)
    pictureList = accessAPI(searchTerm)
    baseImage = pictureList[ImgN] 
    
    urllib.request.urlretrieve(baseImage + ".png", "picture.png")

    importedImage = Image.open('picture.png')

    convertedImage = sepia(importedImage)
    
    displayImage = pil2datauri(convertedImage)
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)
    
    
@app.route('/next/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def nextImage(searchTerm, ImageNumber):
    ImgN = int(ImageNumber) + 1
    pictureList = accessAPI(searchTerm)
    
    if ImgN > 9:
        ImgN = 0
    
    
    displayImage = pictureList[ImgN] 
    
    
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage) 


@app.route('/back/<searchTerm>/<ImageNumber>', methods=['GET', 'POST'])
def previousImage(searchTerm, ImageNumber): 
    ImgN = int(ImageNumber) -1
    pictureList = accessAPI(searchTerm)
    displayImage = pictureList[ImgN] 
    
    if request.method == 'POST':
        if request.form['btn'] == 'Sepia':
            return redirect(url_for('sepiaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gamma':
            return redirect(url_for('gammaConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Negative':
            return redirect(url_for('negativeConversion',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'Gray':
            return redirect(url_for('grayScaleConversion',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'next':
            return redirect(url_for('nextImage',searchTerm= searchTerm,ImageNumber= ImgN))
            
        if request.form['btn'] == 'back':
            return redirect(url_for('previousImage',searchTerm= searchTerm,ImageNumber= ImgN))

        if request.form['btn'] == 'return':
            return redirect(url_for('landingPage'))
    return render_template('searchResultsPage.html', searchTerm = searchTerm, displayImage = displayImage)





app.run(debug=True) 

