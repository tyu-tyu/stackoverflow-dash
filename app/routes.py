from app import app
from flask import render_template, request, json
from werkzeug.exceptions import HTTPException
#routing for the application
@app.route('/')
def index():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['question_date_range'] = lookups.get_index_date_range()
	result_data['table_row_count'] = lookups.get_table_row_count()
	return render_template('index.html.jinja', data=result_data)


@app.route('/ajax/load_index')
def load_index():
	result_data = {}
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['table_row_count'] = lookups.get_table_row_count()
	result_data['top_tags'] = lookups.get_top_tags(10)
	result_data['top_badges'] = lookups.get_top_badges(10)
	result_data['question_details'] = lookups.get_index_question_details()
	result_data['user_years'] = lookups.get_user_years()
	return result_data


@app.route('/ajax/update_index_bar_chart')
def update_index_bar_chart():
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	if request.args.get('type') == 'tags':
		result_data = lookups.get_top_tags(request.args.get('count'))
	else:
		result_data = lookups.get_top_badges(request.args.get('count'))
	return result_data

@app.route('/trending')
def trending():
	return render_template('trending.html.jinja')

@app.route('/tags')
def tags():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['question_date_range'] = lookups.get_index_date_range()
	return render_template('tags.html.jinja', data=result_data)

@app.route('/ajax/load_tags')
def load_tags():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['tag_list'] = lookups.get_tag_list()
	result_data['top_tags'] = lookups.get_filtered_tags()
	return result_data

@app.route('/ajax/filtered_tags', methods=['GET', 'POST'])
def filter_tags():
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data = lookups.get_filtered_tags(request.form)
	return result_data

@app.route('/posts')
def posts():
	from app.classes.lookup import lookup
	result_data =  {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['question_date_range'] = lookups.get_index_date_range()
	return render_template('posts.html.jinja', data=result_data)

@app.route('/ajax/load_posts')
def load_posts():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['tag_list'] = lookups.get_tag_list()
	result_data['post_keywords'] = lookups.get_post_keywords()
	result_data['top_posts'] = lookups.get_top_posts()
	result_data['table_row_count'] = lookups.get_table_row_count()
	result_data['question_details'] = lookups.get_index_question_details()
	return result_data

@app.route('/ajax/filtered_posts', methods=['GET', 'POST'])
def filter_posts():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['post_keywords'] = lookups.get_post_keywords(request.form)
	result_data['top_posts'] = lookups.get_top_posts(request.form)
	result_data['table_row_count'] = lookups.get_filtered_question_count(request.form)
	result_data['question_details'] = lookups.get_filtered_question_details(request.form)
	result_data['success'] = True
	return result_data

@app.route('/users')
def users():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['question_date_range'] = lookups.get_index_date_range()
	return render_template('users.html.jinja', data=result_data)

@app.route('/ajax/load_users')
def load_users():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['tag_list'] = lookups.get_tag_list()
	result_data['user_keywords'] = lookups.get_user_keywords()
	result_data['user_years'] = lookups.get_user_years()
	result_data['top_badges'] = lookups.get_top_badges(50)
	return result_data

@app.route('/ajax/filtered_users', methods=['GET', 'POST'])
def filter_users():
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data = {}
	result_data['user_keywords'] = lookups.get_user_keywords(request.form)
	result_data['user_years'] = lookups.get_user_years(request.form)
	result_data['filtered_top_badges'] = lookups.get_filtered_top_badges(request.form)
	result_data['success'] = True
	return result_data

@app.route('/locations')
def locations():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['question_date_range'] = lookups.get_index_date_range()
	return render_template('locations.html.jinja', data=result_data)


@app.route('/ajax/load_locations')
def load_locations():
	from app.classes.lookup import lookup
	result_data = {}
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data['tag_list'] = lookups.get_tag_list()
	result_data['locations'] = lookups.get_location_scores()
	return result_data

@app.route('/ajax/filtered_locations', methods=['GET', 'POST'])
def filter_locations():
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	result_data = {}
	result_data['locations'] = lookups.get_location_scores(request.form)
	result_data['success'] = True
	return result_data

@app.errorhandler(HTTPException)
def handle_exception(e):
	from app.classes.lookup import lookup
	lookups = lookup(app.config['CURSOR'],app.config['REDIS'])
	response = e.get_response()
	response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
	lookups.error_log(response.data)

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html.jinja')