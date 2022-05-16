from flask import Flask, render_template, request, redirect, flash, url_for


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
        
        if len(searchTerm) > 8:
            flash('Invalid Search', category='error')
            
        elif len(searchTerm) < 2:
            flash('Invalid Search Term', category='error')    
        else:
            flash('Searching Now', category='success')
            
            return redirect(url_for('search'))
    
    return render_template('landingPage.html')

@app.route('/searchResults', methods=['GET', 'POST'])
def search():
    
    
    
    return render_template('searchResultsPage.html')

app.run(debug=True) 

