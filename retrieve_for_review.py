import yagmail
import credentials
import pathlib
import shutil
import datetime
from functions import *
import os
import time

temp_timestamp = str(datetime.datetime.now())
timestamp = simplify_timestamp(temp_timestamp)
timestamp = timestamp[:-8]
print(timestamp)

# setup credentials for sending email
gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP( gmail_user, gmail_password)

# set variables
basedir = pathlib.Path.cwd()
output_filename = 'Heroes_for_review_' + timestamp
target_directory = basedir / 'static' / 'uploads' / 'submitted'
hero_card_list = list(target_directory.glob('*.png'))

# create zip file
shutil.make_archive(output_filename, 'zip', target_directory)

complete_output_filename = output_filename + '.zip'
zip_for_mailing = basedir / complete_output_filename

print(zip_for_mailing)
zip_for_mailing = str(zip_for_mailing)

# begin email notifications
contents = ['Here are this weeks heroes to review', zip_for_mailing]

yag.send(['mrgregory1@gmail.com', 'rgregory@fnwsu.org'], 'New Heroes for Review', contents)
print('sent main emails')

time.sleep(180)



for hero in hero_card_list:
	hero.unlink()
