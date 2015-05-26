__author__ = 'amigos'
from flask import g, url_for, redirect, render_template, request
from flask import Blueprint
from config import MAX_SEARCH_RESULTS
from profile import app
from profile.models import User, Teacher
from profile.models import ROLE_TEACHER, ROLE_STUDENT


search_page = Blueprint('search', __name__, template_folder='templates')


"""
retrieve data via ajax
@app.route('/echo/', methods=['GET'])
def echo():
    global search_model
    ret_data = request.args.get('echoValue')
    search_model = ret_data
    return jsonify(results=ret_data)
"""


@app.route('/search/', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('/'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

# resources - for ajax and different models
# resources = Resources(teachers=Teacher)

"""
for different models
@app.route('/search_results/<search_model>/<query>')
def search_results(query, search_model):
    model = resources.get_context(str(search_model))
    results = model.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results, search_model=search_model)
"""


@app.route('/search_results/<query>')
def search_results(query):
    results = User.query.filter_by(role=ROLE_TEACHER).whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)
