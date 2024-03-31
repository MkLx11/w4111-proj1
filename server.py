
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/poject1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#
# Modify these with your own credentials you received from TA!
DATABASE_USERNAME = "ym2991"
DATABASE_PASSWRD = "ym2991"
DATABASE_HOST = "35.212.75.104" # change to 34.28.53.86 if you used database 2 for part 2
DATABASE_NAME = "proj1part2"
DATABASEURI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/{DATABASE_NAME}"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
with engine.connect() as conn:
	create_table_command = """
	CREATE TABLE IF NOT EXISTS rate_and_review (
            review_id SERIAL PRIMARY KEY,
            itinerary_id INTEGER NOT NULL,
            traveler_id INTEGER NOT NULL,
            rate INTEGER NOT NULL CHECK (rate >= 1 AND rate <= 5),
            review TEXT,
            FOREIGN KEY (itinerary_id) REFERENCES itinerary(itinerary_id),
            FOREIGN KEY (traveler_id) REFERENCES travelers(traveler_id)
        );

	"""
	res = conn.execute(text(create_table_command))
	#insert_table_command = """INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace')"""
	#res = conn.execute(text(insert_table_command))
	# you need to commit for create, insert, update queries to reflect
	conn.commit()


@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request 
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print("uh oh, problem connecting to database")
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
'''@app.route('/')
def index():
	"""
	request is a special object that Flask provides to access web request information:

	request.method:   "GET" or "POST"
	request.form:     if the browser submitted a form, this contains the data in the form
	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

	See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
	"""

	# DEBUG: this is debugging code to see what request looks like
	print(request.args)


	#
	# example of a database query
	#
	select_query = "SELECT name from test"
	cursor = g.conn.execute(text(select_query))
	names = []
	for result in cursor:
		names.append(result[0])
	cursor.close()

	#
	# Flask uses Jinja templates, which is an extension to HTML where you can
	# pass data to a template and dynamically generate HTML based on the data
	# (you can think of it as simple PHP)
	# documentation: https://realpython.com/primer-on-jinja-templating/
	#
	# You can see an example template in templates/index.html
	#
	# context are the variables that are passed to the template.
	# for example, "data" key in the context variable defined below will be 
	# accessible as a variable in index.html:
	#
	#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
	#     <div>{{data}}</div>
	#     
	#     # creates a <div> tag for each element in data
	#     # will print: 
	#     #
	#     #   <div>grace hopper</div>
	#     #   <div>alan turing</div>
	#     #   <div>ada lovelace</div>
	#     #
	#     {% for n in data %}
	#     <div>{{n}}</div>
	#     {% endfor %}
	#
	context = dict(data = names)


	#
	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html
	#
	return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
	return render_template("another.html")'''

'''# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
	# accessing form inputs from user
	name = request.form['name']
	
	# passing params in for each variable into query
	params = {}
	params["new_name"] = name
	g.conn.execute(text('INSERT INTO test(name) VALUES (:new_name)'), params)
	g.conn.commit()
	return redirect('/')


@app.route('/login')
def login():
	abort(401)
	this_is_never_executed()'''




@app.route('/')
def home():
        # DEBUG: this is debugging code to see what request looks like
        print(request.args)
        # Render the homepage (travel.html)
        return render_template('travel.html',  message="Welcome to Everywhere You Go!")

'''@app.route('/search-destination')
def search_destination():
        # Render the page for searching destinations (destination.html)
        # This might later involve passing search results to the template.
        return render_template('destination.html')'''

'''@app.route('/view-itinerary')
def view_itinerary():
        # Render the page for viewing itineraries (itinerary.html)
        # This might later involve fetching itineraries from the database and passing them to the template.
        return render_template('itinerary.html')'''

'''@app.route('/rate-and-review')
def rate_and_review():
        # Render the page for rating and reviewing (rate_and_review.html)
        # This might later involve passing specific itinerary details to the template for review.
        return render_template('rate_and_review.html')'''

'''@app.route('/get-recommendations', methods=['GET', 'POST'])
def get_recommendations():
        # Render the page for getting recommendations (recommendation.html)
        # This might later involve processing form data (destination and budget) to fetch recommendations.
        return render_template('recommendation.html')'''




# Query to search destination
@app.route('/search-destination', methods=['GET'])
def search_destination():
    destination_name = request.args.get('destination').strip().lower()

    with engine.connect() as conn:
        destination_query = text("SELECT * FROM destination WHERE lower(name) = :name")
        destination_result = g.conn.execute(destination_query, {'name': destination_name}).fetchone()

        destination = destination_result if destination_result else None

        flights, accommodations, activities = [], [], []
        if destination_result:
            # Assuming you have foreign keys or a method to link these entities with destination
            flights_query = text("""
                SELECT * FROM flight f JOIN destination d on f.destination = d.airport WHERE lower(d.name) = :name
            """)
            flights = g.conn.execute(flights_query, {'name': destination_name}).fetchall()

            accommodations_query = text("""
                SELECT * FROM accommodation WHERE lower(city) = :name
            """)
            accommodations = g.conn.execute(accommodations_query, {'name': destination_name}).fetchall()

            activities_query = text("""
                SELECT * FROM activity WHERE lower(city) = :name
            """)
            activities = g.conn.execute(activities_query, {'name': destination_name}).fetchall()

    return render_template('destination.html',
                           destination=destination_result,
                           flights=flights,
                           accommodations=accommodations,
                           activities=activities)

@app.route('/view-itinerary', methods=['GET', 'POST'])
def view_itinerary():
    if request.method == 'POST':
        # Extract form data
        itinerary_id = request.form.get('itinerary_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        budget = request.form.get('budget')

        # Insert new itinerary into the database
        with engine.connect() as conn:
            insert_query = text("""
                INSERT INTO itinerary (itinerary_id, start_date, end_date, budget)
                VALUES (:itinerary_id,:start_date, :end_date, :budget)
            """)
            g.conn.execute(insert_query, {'itinerary_id':itinerary_id,'start_date': start_date, 'end_date': end_date, 'budget': budget})
            g.conn.commit()

            # Redirect back to the itineraries page to see the updated list
            return redirect('/view-itinerary')

    # Retrieve existing itineraries from the database
    itineraries = []       
    with engine.connect() as conn:
        select_query = text("""
            SELECT itinerary.*, f.flight_ID, a.name,v.name AS activity_name, agency.name AS agency_name, agency.email AS agency_email
            FROM itinerary LEFT JOIN manage ON itinerary.itinerary_id = manage.itinerary_id
            LEFT JOIN includes_flight f ON itinerary.itinerary_id = f.itinerary_id
            LEFT JOIN includes_accommodation ON itinerary.itinerary_id = includes_accommodation.itinerary_id
            LEFT JOIN accommodation a ON includes_accommodation.accommodation_id = a.accommodation_id
            LEFT JOIN includes_activities i ON i.itinerary_id = itinerary.itinerary_id
            LEFT JOIN activity v ON v.activity_id = i.activity_id
            LEFT JOIN agency ON manage.agency_id = agency.agency_id
        """)
        itineraries = g.conn.execute(select_query).fetchall()
    return render_template('itinerary.html', itineraries=itineraries)

'''@app.route('/rate-and-review', methods=['GET', 'POST'])
def rate_and_review():
    if request.method == 'POST':
        traveler_id = request.form.get('traveler_id')
        itinerary_id = request.form.get('itinerary_id')
        rate = request.form.get('rate')
        review = request.form.get('review')

        with engine.connect() as conn:
            insert_query = text("""
                INSERT INTO rate_and_review (itinerary_id, rate, review)
                VALUES (:itinerary_id, :rate, :review)
            """)
            conn.execute(insert_query, {'itinerary_id': itinerary_id, 'rate': rate, 'review': review})
            conn.commit()
        # Redirect to refresh and show the updated list of reviews
            return redirect('/rate-and-review')
    
    reviews = []
    with engine.connect() as conn:
        select_query = text("SELECT * FROM rate_and_review ORDER BY review_id DESC")
        reviews = conn.execute(select_query).fetchall()
    
    return render_template('rate_and_review.html', reviews=reviews)'''

@app.route('/rate-and-review', methods=['GET', 'POST'])
def rate_and_review():
    if request.method == 'POST':
        itinerary_id = request.form.get('itinerary_id')
        traveler_id = request.form.get('traveler_id')
        rate = request.form.get('rate')
        review = request.form.get('review')

        with engine.connect() as conn:
            # Verify the traveler has booked the itinerary
            booking_check = text("""
                SELECT EXISTS (
                    SELECT 1 FROM books
                    WHERE traveler_id = :traveler_id AND itinerary_id = :itinerary_id
                )
            """)
            can_review = g.conn.execute(booking_check, {'traveler_id': traveler_id, 'itinerary_id': itinerary_id}).scalar()
            print(can_review)
            print(type(can_review))
            
            if can_review:
                insert_query = text("""
                    INSERT INTO rate_and_review (itinerary_id, traveler_id, rate, review)
                    VALUES (:itinerary_id, :traveler_id, :rate, :review)
                """)
                g.conn.execute(insert_query, {'itinerary_id': itinerary_id, 'traveler_id': traveler_id, 'rate': rate, 'review': review})
                g.conn.commit()
                
        return redirect('/rate-and-review')

    # Fetch and display reviews along with traveler information
    reviews = []
    with engine.connect() as conn:
        select_query = text("""
            SELECT rr.*, t.name AS traveler_name
            FROM rate_and_review rr
            JOIN travelers t ON rr.traveler_id = t.traveler_id
            ORDER BY rr.review_id DESC
        """)
        reviews = g.conn.execute(select_query).fetchall()

    return render_template('rate_and_review.html', reviews=reviews)


def is_valid_number(s):
    """Check if the string s can be converted to a float."""
    try:
        float(s)
        return True
    except ValueError:
        return False
@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    destination = request.form['destination'].lower()
    budget = float(request.form['budget']) if is_valid_number(request.form['budget']) else 0 # Ensure budget is treated as a float
    duration = int(request.form['duration'])

    # Format the budget as a string with two decimal places
    formatted_budget = "{:.2f}".format(budget)


    with engine.connect() as conn:
        query = text("""
            SELECT f.flight_id, a.name, v.name AS activity_name,(f.price + a.price*:duration+v.price) AS total_price
            FROM destination d LEFT JOIN flight f ON d.airport = f.destination
            LEFT JOIN accommodation a ON a.city = d.name
            LEFT JOIN activity v ON v.city = d.name
            WHERE lower(d.name) = :destination
            AND (f.price + a.price * :duration + v.price) <= :budget
        """)
        recommendations = g.conn.execute(query, {'destination': destination, 'budget': formatted_budget, 'duration': duration}).fetchall()

    # Pass the formatted budget string to the template for display
    return render_template('recommendation.html', recommendations=recommendations, destination=destination, budget=formatted_budget, duration=duration)






if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

			python server.py

		Show the help text using:

			python server.py --help

		"""

		HOST, PORT = host, port
		print("running on %s:%d" % (HOST, PORT))
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

run()
