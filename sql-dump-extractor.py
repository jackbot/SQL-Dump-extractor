#!/usr/bin/env python

# SQL file dumper - extracts single SQL dumps from a larger multiple database dump
# Jack Weeden <ajack.org> 2011

import sys
import os.path

def listDatabases(path):
	""" Reads in an SQL dump from a file and creates a list of the database names and their positions in the file """

	print 'Loading file...\n'
	databases = []
	line_count = 0
	sql_file = open(path)
	lines = sql_file.readlines()

	for line in lines:
		line_count += 1
		if line[0:12] == '-- Database:':
			# We've found the beginning of a database
			the_db = (line_count, extractDbName(line)) # Tuple of first line of this db in the whole file and its name
			databases.append(the_db)
	sql_file.close()
	
	# Check to see if there were any databases in the file
	if len(databases) == 0:
		print 'No databases found (or file contains a single database)'
		exit(0)

	# Print out the findings and prompt for a number of database to extract
	i = 1
	for db in databases:
		print "[%s] %s" % (str(i), db[1])
		i += 1
	
	the_db = -1
	while the_db < 0 or the_db > len(databases):
		# Number entered is outside the range of the databases found
		try:
			the_db = int(raw_input('\nExtract database: '))
		except ValueError:
			print 'Enter the number of a database to extract'
	the_db -= 1
	extractDatabase(lines, databases, the_db, databases[the_db][1], databases[the_db][0])
	
	
def extractDbName(db_name):
	""" Takes a line from a MySQL dump file and returns the database name. """
	
	ret = ''
	backtick_count = 0
	for i in db_name:
		if i == '`':
			backtick_count += 1
		if backtick_count == 2:
			return ret
		else:
			if backtick_count == 1 and i != '`': ret += i


def extractDatabase(sql_file, databases, num, name, start_line):
	""" Extracts the nth database from the sql file """
	
	if num == len(databases) - 1:
		# We've selected the last database, so the last line is the last line of the whole file
		sql_dump = sql_file[start_line:]
	else:
		# We've not selected the last database, so the last line is the first line of the next database
		end_line = databases[num+1][0]-1
		sql_dump = sql_file[start_line:end_line]
		
	# Dump the database to a new file. Check if it exists first
	out_filename = name + '.sql'
	
	if os.path.isfile(out_filename):
		confirmation = ''
		while confirmation not in ['y', 'n']:
			confirmation = raw_input('File exists. Overwrite? [y/n]: ')
			
		if confirmation == 'n':
			sys.exit(0)
		
	out_file = f = open(name + '.sql', 'w')
	for line in sql_dump:
		out_file.write(line)
	out_file.close()
	print 'Dump written to ' + name + '.sql'



def usage():
	print 'Usage: ' + sys.argv[0] + ' sql_dump_filename'	
	
		
if __name__ == "__main__":

	if len(sys.argv) != 2:
		usage()
	else:
		# Check if the file exists
		if os.path.isfile(sys.argv[1]):
			listDatabases(sys.argv[1])
		else:
			print sys.argv[1] + ' is not a file'

