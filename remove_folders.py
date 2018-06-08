import os, sys
import datetime
from functions import *
import shutil

def remove_old_folders():
	# create list of folders in temp folder
	this_basedir = os.path.abspath(os.path.dirname(__file__))
	path = os.path.join(this_basedir,'static','temp')
	old_files = os.listdir(path)

	# remove any files from list that aren't created by the program
	old_files2 = [x for x in old_files if len(x) == 16]

	# get current date
	temp_timestamp = str(datetime.datetime.now())
	timestamp = simplify_timestamp(temp_timestamp)

	# pull out the 'day of the month' from the timestamp
	today = timestamp[6:8]

	# create timestamp for two days ago, removing two days of the month
	two_days_ago = int(timestamp) - 200000000

	# create int for numverical comparison
	two_days_ago = int(two_days_ago)

	# delete all folders that are more than two days old (if it's not the first or second)
	print(two_days_ago)
	if today != '01' or today != '02':
		for folder in old_files2.copy():
			if int(folder) < two_days_ago:
				# print('here we go\n')
				shutil.rmtree(os.path.join(this_basedir, 'static', 'temp', folder))
				pass
