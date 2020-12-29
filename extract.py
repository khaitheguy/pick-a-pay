# extract.py - Transfer data from a csv format to a sqlite database

from csv import DictReader
import sqlite3

# Connect and gain access to the database file
conn = sqlite3.connect('jobs.db')

db = conn.cursor()

# Create table if it has not been done yet
db.execute('''CREATE TABLE IF NOT EXISTS jobs
			(year YEAR, major_occ TEXT, ind1 TEXT, occ_desc TEXT, mthly_gross_wage_50_pctile NUMERIC, mthly_basic_wage_50_pctile TEXT)''')

# Save changes to the database
conn.commit()

# Open the csv file and get its data
with open('job_data.csv', 'r') as csv_file:
	rows = DictReader(csv_file)
	
	# Copy each row into the database file
	for row in rows:
		
		# Arrange data to insert into the database
		data = (row['year'],
				row['major_occ'],
				row['ind1'],
				row['occ_desc'],
				row['mthly_gross_wage_50_pctile'],
				row['mthly_basic_wage_50_pctile'])
				
		# Insert arranged data into table
		db.execute('''INSERT INTO jobs (year, major_occ, ind1, occ_desc, mthly_gross_wage_50_pctile, mthly_basic_wage_50_pctile)
					VALUES (?, ?, ?, ?, ?, ?)''', data)

	conn.commit()

# Close the connection
conn.close()