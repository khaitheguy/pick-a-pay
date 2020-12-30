# application.py - generate html pages using flask

import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "GET":
		return render_template('/index.html')
		
	else:
		# Get the minimum salary requested by the user
		try:
			min_salary = int(request.form.get('salary'))
			
		except:
			# Assume a minimum salary of $0 if input is invalid or empty
			min_salary = 0

		# Connect to jobs database
		conn = sqlite3.connect('jobs.db')
		
		# Force sqlite3 to return a dictionary instead of a tuple
		conn.row_factory = sqlite3.Row
		
		db = conn.cursor()
		
		# Query jobs from the database
		db.execute('''SELECT * FROM jobs
					WHERE mthly_gross_wage_50_pctile >= ?
					GROUP BY mthly_gross_wage_50_pctile''', (min_salary, ))
		
		# Get the data for the jobs as a list of dictionaries
		rows = db.fetchall()
		
		# Close the database connection
		conn.close()
		
		# Display the jobs on a page
		return render_template('/jobs.html', records=len(rows), rows=rows)