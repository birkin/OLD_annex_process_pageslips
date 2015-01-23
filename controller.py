# -*- coding: utf-8 -*-


## set up environment ##

import os, sys
sys.path.append( os.environ[u'AN_PR_PA__ENCLOSING_PROJECT_PATH'] )
import datetime, shutil, string
from annex_process_pageslips import utility_code

PATH_TO_ARCHIVES_ORIGINALS_DIRECTORY = os.environ[u'AN_PR_PA__PATH_TO_ARCHIVES_ORIGINALS_DIRECTORY']
PATH_TO_ARCHIVES_PARSED_DIRECTORY = os.environ[u'AN_PR_PA__PATH_TO_ARCHIVES_PARSED_DIRECTORY']
PATH_TO_PARSED_ANNEX_COUNT_DIRECTORY = os.environ[u'AN_PR_PA__PATH_TO_PARSED_ANNEX_COUNT_DIRECTORY']
PATH_TO_PARSED_ANNEX_DATA_DIRECTORY = os.environ[u'AN_PR_PA__PATH_TO_PARSED_ANNEX_DATA_DIRECTORY']
PATH_TO_SOURCE_FILE = os.environ[u'AN_PR_PA__PATH_TO_SOURCE_FILE']
PATH_TO_SOURCE_FILE_DIRECTORY = os.environ[u'AN_PR_PA__PATH_TO_SOURCE_FILE_DIRECTORY']


## check that all paths are legit

utility_code.updateLog( message='START', message_importance='high' )

check_a = utility_code.checkDirectoryExistence( PATH_TO_SOURCE_FILE_DIRECTORY )
check_b = utility_code.checkDirectoryExistence( PATH_TO_ARCHIVES_ORIGINALS_DIRECTORY )
check_c = utility_code.checkDirectoryExistence( PATH_TO_ARCHIVES_PARSED_DIRECTORY )
check_d = utility_code.checkDirectoryExistence( PATH_TO_PARSED_ANNEX_DATA_DIRECTORY )
check_e = utility_code.checkDirectoryExistence( PATH_TO_PARSED_ANNEX_COUNT_DIRECTORY )
if check_a == 'exists' and check_b == 'exists' and check_c == 'exists' and check_d == 'exists' and check_e == 'exists':
  utility_code.updateLog( message='- path check passed' )
else:
  message='- path check failed; quitting'
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )



## check for file

try:
  file_reference = open( PATH_TO_SOURCE_FILE )
  # data_as_string = file_reference.read()
  # print 'data_as_string is: %s' % data_as_string
  # lines = data_as_string.split( '\n' )
  # print 'lines is: %s' % lines
  utility_code.updateLog( message='- annex requests found', message_importance='high' )
except Exception, e:
  message='- no annex requests found; quitting'
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )



## prepare the date string

date_stamp = utility_code.prepareDateTimeStamp( datetime.datetime.now() )
utility_code.updateLog( message='- date_stamp is: %s' % date_stamp )



## copy original to archives

original_archive_file_path = '%s/REQ-ORIG_%s.dat' % ( settings.PATH_TO_ARCHIVES_ORIGINALS_DIRECTORY, date_stamp )   # i.e. '/path/REQ-ORIG_2005-05-19T15/08/09.dat'
try:
  shutil.copyfile( settings.PATH_TO_SOURCE_FILE, original_archive_file_path )
  os.chmod( original_archive_file_path, 0640 )
  utility_code.updateLog( message='- source file copied to original archives' )
except Exception, e:
  message = '- copy of original file from "%s" to "%s" unsuccessful; exception is: %s' % ( settings.PATH_TO_SOURCE_FILE, original_archive_file_path, e )
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exist( message )
copy_check = utility_code.checkFileExistence( original_archive_file_path )
if copy_check == 'exists':
  utility_code.updateLog( message='- original file copied to: %s' % original_archive_file_path )
else:
  message = '- copy of original file from "%s" to "%s" unsuccessful; exception is: %s' % ( settings.PATH_TO_SOURCE_FILE, original_archive_file_path, copy_check )
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exist( message )



## post original-data to db

data = file_reference.read()
utility_code.updateLog( message='- original-data is: %s' % data )
post_result = 'init'
try:
  post_result = utility_code.postFileData( identifier=date_stamp, file_data=data, update_type='original_file' )
  utility_code.updateLog( message='- original_file post_result is: %s' % post_result )
except Exception, e:
  utility_code.updateLog( message='- original_file post_result exception is: %s' % e )
  sys.exit( 'error on original-file post; exception is: %s' % e )
if not post_result == 'success':
  utility_code.updateLog( message='- post_result not "success"; quitting' )
  sys.exit( 'error on original-file post; post_result not "success"; exception is: %s' % e )



####### parseFile


## process the file

  ## get a list of pageslip lines

  ## create the itemArrayList, with each item having a raw arrayList of its pageslip lines

  ## loop through each item, filling in each item's attributes from its pageslip info (log is also updated)

  ## write out the info to the file

  ## verify the count of the written file and update log



## parse pageslip file

# get a list of pageslip objects -- each pageslip a list of lines
lines = data.split( '\n' )
item_list = utility_code.makeItemList( lines )
utility_code.updateLog( message='- %s records to be processed' % len(item_list) )
# print '- %s records to be processed' % len(item_list)
# print '- data is: %s' % data
# print '- item_list is: %s' % str(item_list)

# process each pageslip
new_item_list = []
pageslip_count = 0
for item in item_list:
  try:
    record_number = utility_code.parseRecordNumber(item)
    book_barcode = utility_code.parseBookBarcode(item)
    las_delivery_stop = utility_code.parseJosiahPickupAtCode(item)
    las_customer_code = utility_code.parseJosiahLocationCode(item)
    patron_name = utility_code.parsePatronName(item)
    patron_barcode = utility_code.parsePatronBarcode(item)
    title = utility_code.parseTitle(item)
    las_date = utility_code.prepareLasDate()
    note = utility_code.parseNote(item)
    full_line = '''"%s","%s","%s","%s","%s","%s","%s","%s","%s"''' % ( record_number, book_barcode, las_delivery_stop, las_customer_code, patron_name, patron_barcode, title, las_date, note )
    new_item_list.append( full_line )
    pageslip_count = pageslip_count + 1
    if pageslip_count % 10 == 0:
      utility_code.updateLog( message='- %s pageslips processed' % pageslip_count )
      print '.'
  except Exception, e:
    utility_code.updateLog( message='- iterating through item_list; problem with item "%s"; exception is: %s' % (item, e), message_importance='high' )
utility_code.updateLog( message='- %s items parsed' % pageslip_count )
# print '- %s items parsed' % pageslip_count



## post parsed data to db

string_data = ''
count = 0
for line in new_item_list:
  # print '- line is: %s\n' % line
  if count == 0:
    string_data = line
  else:
    string_data = string_data + '\n' + line
  count = count + 1
string_data = string_data + '\n'   # the final newline is likely not necessary but unixy, and exists in old system

# print '- string_data is: %s' % string_data

try:
  post_result = utility_code.postFileData( identifier=date_stamp, file_data=string_data, update_type='parsed_file' )
  utility_code.updateLog( message='- parsed_file post_result is: %s' % post_result )
except Exception, e:
  utility_code.updateLog( message='- parsed_file post_result exception is: %s' % e, message_importance='high' )
  sys.exit( 'error on parsed-file post' )
if not post_result == 'success':
  utility_code.updateLog( message='- post_result of parsed file not "success"; quitting', message_importance='high' )
  sys.exit( 'error on parsed-file post' )



## write parsed file to archives

try:
  parsed_file_name = 'REQ-PARSED_%s.dat' % date_stamp
  parsed_file_archive_path = '%s/%s' % ( settings.PATH_TO_ARCHIVES_PARSED_DIRECTORY, parsed_file_name )
  f = open( parsed_file_archive_path, 'w' )
  f.write( string_data )
  f.close()
  copy_check = utility_code.checkFileExistence( parsed_file_archive_path )
  os.chmod( parsed_file_archive_path, 0640 )   # rw-/r--/---
  if copy_check == 'exists':
    utility_code.updateLog( message='- parsed file archived to: %s' % parsed_file_archive_path )
  else:
    message = '- write of parsed file to "%s" unsuccessful' % parsed_file_archive_path
    utility_code.updateLog( message=message, message_importance='high' )
    sys.exit( message )
except Exception, e:
  message='- problem on save of parsed file; quitting; exception is: %s' % e
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )



## determine count
confirmed_count = utility_code.determineCount( len(new_item_list), lines )   # lines is from '''## parse pageslip file''' section
if confirmed_count == 0:   # if two methods of determining count don't match, zero is returned
  message='- problem on determining count; quitting'
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )
utility_code.updateLog( message='- count confirmed to be: %s' % confirmed_count )



## save count file to annex count-receiving folder

try:
  count_file_name = 'REQ-PARSED_%s.cnt' % date_stamp
  count_file_las_destination_path = '%s/%s' % ( settings.PATH_TO_PARSED_ANNEX_COUNT_DIRECTORY, count_file_name )
  f = open( count_file_las_destination_path, 'w' )
  f.write( str(confirmed_count) + '\n' )
  f.close()
  os.chmod( parsed_file_archive_path, 0666 )   # rw-/rw-/rw-
  utility_code.updateLog( message='- count file written to: %s' % count_file_las_destination_path )
except Exception, e:
  message='- problem on save of count file; quitting; exception is: %s' % e
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )

# try:
#   count_file_name = 'REQ-PARSED_%s.cnt' % date_stamp
#   count_file_las_destination_path = '%s/%s' % ( settings.PATH_TO_PARSED_ANNEX_COUNT_DIRECTORY, count_file_name )
#   f = open( count_file_las_destination_path, 'w' )
#   f.write( str(len(new_item_list)) + '\n' )
#   f.close()
#   os.chmod( parsed_file_archive_path, 0666 )   # rw-/rw-/rw-
#   utility_code.updateLog( message='- count file written to: %s' % count_file_las_destination_path )
# except Exception, e:
#   message='- problem on save of count file; quitting; exception is: %s' % e
#   utility_code.updateLog( message=message, message_importance='high' )
#   sys.exit( message )



## copy parsed file to annex file-receiving folder

parsed_file_las_destination_path = '%s/%s' % ( settings.PATH_TO_PARSED_ANNEX_DATA_DIRECTORY, parsed_file_name )
try:
  shutil.copyfile( parsed_file_archive_path, parsed_file_las_destination_path )
  os.chmod( parsed_file_archive_path, 0666 )   # rw-/rw-/rw-
  utility_code.updateLog( message='- parsed file copied to: %s' % parsed_file_las_destination_path )
  # copy_check = utility_code.checkFileExistence( parsed_file_las_destination_path )
  # if copy_check == 'exists':   # decided not to do copy_check because the file could be processed very quickly.
  #   utility_code.updateLog( message='- parsed file copied to: %s' % parsed_file_las_destination_path )
  # else:
  #   message = '- copy of parsed file to "%s" unsuccessful' $ parsed_file_las_destination_path
  #   utility_code.updateLog( message=message, message_importance='high' )
  #   sys.exit( message )
except Exception, e:
  message='- problem on copy of parsed file to %s; quitting; exception is: %s' % ( parsed_file_las_destination_path, e )
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exit( message )



## delete original

try:
  os.remove( settings.PATH_TO_SOURCE_FILE )
  copy_check = utility_code.checkFileExistence( settings.PATH_TO_SOURCE_FILE )   # should not exist
  if copy_check == 'exists':
    message = '- delete of original file at "%s" failed, as determined by copy_check' % settings.PATH_TO_SOURCE_FILE
    utility_code.updateLog( message=message, message_importance='high' )
    sys.exist( message )
  else:
    utility_code.updateLog( message='- source file at "%s" deleted' % settings.PATH_TO_SOURCE_FILE )
except Exception, e:
  message = '- delete of original file at "%s" failed; exception is: %s' % ( settings.PATH_TO_SOURCE_FILE, e )
  utility_code.updateLog( message=message, message_importance='high' )
  sys.exist( message )


## report end of script

utility_code.updateLog( message='- script completed successfully', message_importance='high' )
