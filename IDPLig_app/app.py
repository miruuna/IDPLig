from flask import Flask, render_template, request, redirect, url_for, flash
from models import db

app = Flask(__name__)

# ROUTES
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/data')
def data():
    # Get search query if any
    query = request.args.get('search', '')
    # Get page number for pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of items per page
    
    # Get data based on search query
    if query:
        idp_data = db.search_idp_data(query)
    else:
        idp_data = db.get_all_idp_data()
    
    # Get statistics
    stats = db.get_idp_statistics()
    
    return render_template("data.html", 
                         idp_data=idp_data, 
                         stats=stats,
                         search_query=query)

@app.route('/idp/<idp_id>')
def view_idp(idp_id):
    """View details of a specific IDP"""
    idp = db.get_idp_by_id(idp_id)
    if idp:
        return render_template('idp_details.html', idp=idp)
    flash('IDP not found!', 'danger')
    return redirect(url_for('data'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

