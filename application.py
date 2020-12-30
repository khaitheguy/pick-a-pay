# application.py - generate html pages using flask

import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "GET":
		# Connect to jobs database
		conn = sqlite3.connect('jobs.db')
		
		# Force sqlite3 to return a dictionary instead of a tuple
		conn.row_factory = sqlite3.Row
		
		db = conn.cursor()
		
		# Get the names of every industry listed
		db.execute('''SELECT DISTINCT ind1 FROM jobs''')
		rows = db.fetchall()
		
		# Close the database connection
		conn.close()
					
		return render_template('/index.html', rows=rows)
		
	else:
		# Get user form data
		try:
			min_salary = int(request.form.get('salary'))
			
		except:
			# Assume a minimum salary of $0 if input is invalid or empty
			min_salary = 0
			
		industry = request.form.get('industry')

		# Connect to jobs database
		conn = sqlite3.connect('jobs.db')
		
		# Force sqlite3 to return a dictionary instead of a tuple
		conn.row_factory = sqlite3.Row
		
		db = conn.cursor()
		
		# Query jobs from the database
		if industry:
			db.execute('''SELECT * FROM jobs
						WHERE mthly_gross_wage_50_pctile >= ? AND ind1 = ?
						GROUP BY mthly_gross_wage_50_pctile''', (min_salary, industry))
		
		else:
			db.execute('''SELECT * FROM jobs
						WHERE mthly_gross_wage_50_pctile >= ?
						ORDER BY mthly_gross_wage_50_pctile''', (min_salary, ))
		
		# Get the data for the jobs as a list of dictionaries
		rows = db.fetchall()
		
		# Close the database connection
		conn.close()
		
		# Capitalize text that is being used
		new_rows = []
		for row in rows:
			new_rows.append({'occ_desc': row['occ_desc'].title(), 'ind1': row['ind1'].title(), 'mthly_gross_wage_50_pctile': row['mthly_gross_wage_50_pctile']})
		
		# Display the jobs on a page
		return render_template('/jobs.html', records=len(rows), rows=new_rows)