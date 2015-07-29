# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint, smtplib, urllib, urllib2
from email.Header import Header
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class ItemListMaker( object ):
  """ Breaks pageslip file into list of requests, where each request is a list of lines. """

  def __init__( self ):
    self.items = []
    self.item = []
    self.last_line = ''

  def make_item_list( self, text ):
    """ Turns utf8-text into list of requests, where each request is a list of lines. """
    unicode_lines = self.make_lines( text )
    for line in unicode_lines:
      if self.check_start( line ) == True:
        self.items.append( self.item )  # copies current item to items
        self.item = []  # clear item
      self.conditionally_append_line_to_item( line )
      self.last_line = line
    self.items.append( self.item )  # adds last item
    self.clean_items()
    # logger.debug( 'items, `%s`' % pprint.pformat( self.items) )
    return self.items

  def make_lines( self, text ):
    """ Turns text into lines.
        Called by make_item_list() """
    assert type(text) == str
    unicode_text = text.decode( 'utf-8' )
    lines = unicode_text.split( '\n' )
    return lines

  def check_start( self, line ):
    """ Determines if line is beginning of an item.
        Called by make_item_list() """
    # logger.debug( 'line, `%s`' % line )
    line = line.strip()
    return_val = False
    if (line in ['Brown University', 'Brown University Library' ]) and ('AUTHOR' not in line) and ('AUTHOR' not in self.last_line):
      return_val = True
    elif line.strip()[0:3] in [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ] and len(self.item) < 1:
      return_val = True
    elif len(self.item) > 1 and self.item[-1].strip()[0:4] in [ '38:1', '38:2', '38:3', '38:4', '38:5', '38:6', '38:7', '38:8', '38:9', '38:0' ]:
      return_val = True
    # logger.debug( 'return_val, `%s`' % return_val )
    return return_val

  def conditionally_append_line_to_item( self, line ):
    """ Appends line to item if it's not a blank start to a new item.
        Called by make_item_list() """
    if len(self.item) == 0 and line.strip() == '':
      pass
    else:
      self.item.append( line )  # adds line to existing or new item
    return

  def clean_items( self ):
    """ Removes empty items and removes empty trailing lines from each item.
        Called by make_item_list() """
    new_items = []
    for item in self.items:
      if len(item) > 0:
        item = self.remove_empty_lines( item )
        new_items.append( item )
    self.items = new_items
    return

  def remove_empty_lines( self, item ):
    """ Removes empty lines from end of page-slip.
        Called by clean_items() """
    item.reverse()  # switches line order for easy looping
    new_item = []
    check_flag = True
    for line in item:
      if line.strip() == '' and check_flag == True:  # doesn't copy empty line
        pass
      else:  # otherwise, copies and stops checking, since the trailing empty lines have been removed
        check_flag = False
        new_item.append( line )
    new_item.reverse()  # switches back to proper line order
    return new_item

  # end class ItemListMaker()


class Parser( object ):
    """ Parses data-fields from a single pageslip's lines.
      TODO: refactor rest of parsing functions into here. """

    def parse_note( self, pageslip_lines ):
        """ Extracts possible note from lines of a single pageslip.
            Called by controller.py """
        initial_note = self.grab_note( pageslip_lines )
        cleaned_note = self.clean_note( initial_note )
        return cleaned_note

    def grab_note( self, pageslip_lines ):
        """ Grabs initial note string.
            Called by parse_note() """
        note = ''
        ready_flag = 'red'
        for line in pageslip_lines:
          if 'PICKUP AT:' in line:
            ready_flag = 'yellow'
          elif 'NOTE:' in line and ready_flag == 'yellow':
            ready_flag = 'green'
            note = line.replace( 'NOTE:', '' ).strip()
          elif ready_flag == 'green' and len( line.strip() ) > 0 and '38' not in line:
            note = note + ' ' + line.strip()
        return note

    def clean_note( self, initial_note ):
        """ Removes spaces from note, or sets default note.
            Called by parse_note() """
        cleaned_note = initial_note.replace( '  ', ' ' )
        cleaned_note = cleaned_note.replace( '"', u"'" )
        if len( cleaned_note.strip() ) == 0:
          cleaned_note = 'no_note'
        return cleaned_note

    def parse_bookbarcode( self, single_page_slip ):
        """ Parses book-barcode from lines of a single pageslip.
            Called by controller.py """
        book_barcode = 'init'
        for line in single_page_slip:
          stripped_line = line.strip()
          if 'BARCODE:' in stripped_line:
            temp_string = stripped_line[8:]   # gets everything after 'BARCODE:'
            temp_string = temp_string.strip()   # removes outside whitespace, leaving barcode possibly containing space-characters
            return_val = temp_string.replace( ' ', '' )
            break
        return return_val

    def parse_josiah_location_code( self, single_page_slip ):
        '''
        - Purpose: to extract an las 'customer-code' from a page-slip's josiah 'location-code'.
        - Called by: opac_to_las_python_parser_code.controller
        '''
        return_val = '?'
        for line in single_page_slip:
            stripped_line = line.strip()
            if 'LOCATION:' in stripped_line:
                temp_string = stripped_line[9:]   # gets everything after 'LOCATION:'
                temp_string = temp_string.strip()   # removes outside whitespace, leaving Josiah location
                if not temp_string == '':
                    return_val = convertJosiahLocationCode( temp_string )
                break
        return return_val

    def parse_title( self, pageslip_lines ):
        """ Extracts item title from lines of a pageslip.
            Called by: opac_to_las_python_parser_code.controller() """
        counter = 0
        title_line = ''
        for line in pageslip_lines:
            if 'TITLE:' in line:
                title_line = line.replace( 'TITLE:', '' )
                break
            elif 'PUB DATE:' in line:   # means that the title was too long to have a label
                title_line = pageslip_lines[ counter - 2 ]   # two lines above 'PUB DATE:'
                break
            counter = counter + 1
        stripped_title = title_line.strip()
        dequoted_title = stripped_title.replace( '"', "'" )
        return dequoted_title

    # end class Parser


## non-class functions ##


def checkDirectoryExistence( directory_path ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: confirm existence of directories before starting processing.
  '''

  if os.path.exists(directory_path):
    return 'exists'
  else:
    updateLog( message='- directory_path "%s" does not exist' % directory_path, message_importance='high' )
    return 'does_not_exist'

  # end def checkDirectoryExistence()



def checkFileExistence( file_path ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: to confirm existence of supposedly-copied files in new location
  '''
  try:
    file = open( file_path )
    return 'exists'
  except Exception, e:
    return e

  # end def checkFileExistence()



def convertJosiahLocationCode( code ):
  '''
  - Purpose: input - josiah_location_code; output - las customer_code
  - Called by: utility_code.parseJosiahLocationCode()
  '''
  JOSIAH_LOCATION_TO_LAS_CUSTOMER_CODE_CONVERTER_API_URL_PREFIX = os.environ['AN_PR_PA__JOSIAH_LOCATION_TO_LAS_CUSTOMER_CODE_CONVERTER_API_URL_PREFIX']
  full_url = '%s%s' % ( JOSIAH_LOCATION_TO_LAS_CUSTOMER_CODE_CONVERTER_API_URL_PREFIX, urllib.quote(code) )
  try:
    string_data = urllib.urlopen( full_url ).read()
    json_data = json.loads( string_data )
    result = json_data['result']['returned_las_code']
    return result
  except Exception, e:
    message = 'problem coverting josiah-location-code, `%s`' % code
    logger.debug( message )
    logger.error( 'exception, `%s`' % unicode(repr(e)) )
    subject = 'annex process pageslips warning (pageslips went through)'
    m = Mailer( subject, message )
    m.send_email()
    updateLog( message='- in convertJosiahLocationCode(); %s' % message )
    return 'unknown_location'
  # end def convertJosiahLocationCode()



def convertJosiahPickupAtCode( code ):
  '''
  - Purpose: input - josiah pickup-at code; output - las delivery-stop code
  - Called by: utility_code.parseJosiahPickupAtCode()
  '''

  JOSIAH_PICKUP_AT_TO_LAS_DELIVERY_STOP_CONVERTER_API_URL_PREFIX = os.environ['AN_PR_PA__JOSIAH_PICKUP_AT_TO_LAS_DELIVERY_STOP_CONVERTER_API_URL_PREFIX']

  full_url = '%s%s' % ( JOSIAH_PICKUP_AT_TO_LAS_DELIVERY_STOP_CONVERTER_API_URL_PREFIX, urllib.quote(code) )

  try:
    string_data = urllib.urlopen( full_url ).read()
    json_data = json.loads( string_data )
    result = json_data['result']['returned_las_code']
    return result
  except Exception, e:
    updateLog( message='- in convertJosiahPickupAtCode(); exception is: %s' % e )
    return 'failure, exception is: %s' % e

  # end def convertJosiahPickupAtCode()



def determineCount( number_of_parsed_items, pageslip_lines ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: to verify that the number of items parsed meshes with the count indicator on the pageslip.
  '''

  current_count_estimate_from_lines = 0
  for line in pageslip_lines:
    trimmed_line = line.strip()
    if trimmed_line[0:3] == '38:':
      current_count_estimate_from_lines = int( trimmed_line[3:] )

  if current_count_estimate_from_lines == 0:
    current_count_estimate_from_lines = 1

  if not current_count_estimate_from_lines == number_of_parsed_items:
    updateLog( message='- in utility_code.determineCount(); count discrepancy; number_of_parsed_items is "%s"; 38-method yields "%s"' % ( number_of_parsed_items, current_count_estimate_from_lines ), message_importance='high' )
    return 0
  else:
    return current_count_estimate_from_lines

  # end def determineCount()



# def parseJosiahLocationCode( single_page_slip ):
#   '''
#   - Purpose: to extract an las 'customer-code' from a page-slip's josiah 'location-code'.
#   - Called by: opac_to_las_python_parser_code.controller
#   '''

#   return_val = '?'
#   for line in single_page_slip:
#     stripped_line = line.strip()
#     if 'LOCATION:' in stripped_line:
#       temp_string = stripped_line[9:]   # gets everything after 'LOCATION:'
#       temp_string = temp_string.strip()   # removes outside whitespace, leaving Josiah location
#       if not temp_string == '':
#         return_val = convertJosiahLocationCode( temp_string )
#       break

#   return return_val

#   # end def parseJosiahLocationCode()



def parseJosiahPickupAtCode( single_page_slip ):
  '''
  - Purpose: to extract an las 'delivery-stop-code' from a page-slip's josiah 'pickup-at-code'.
  - Called by: opac_to_las_python_parser_code.controller
  '''

  return_val = '?'
  for line in single_page_slip:
    stripped_line = line.strip()
    if 'PICKUP AT:' in stripped_line:
      temp_string = stripped_line[10:]   # gets everything after 'PICKUP AT:'
      temp_string = temp_string.strip()   # removes outside whitespace, leaving Josiah pickup-at code
      if not temp_string == '':
        return_val = convertJosiahPickupAtCode( temp_string )
      break

  return return_val

  # end def parseJosiahPickupAtCode()



def parsePatronBarcode( pageslip_lines ):
  '''
  - Purpose: to extract the patron name from the lines of a pageslip.
  - Called by: opac_to_las_python_parser_code.controller
  '''

  name = 'init'
  name_line = 'init'
  line_counter = 0
  blank_line_counter = 0

  for line in pageslip_lines:
    if len( line.strip() ) == 0:
      blank_line_counter = blank_line_counter + 1
    else:
      blank_line_counter = 0
    if blank_line_counter == 4:   # means we've had 4 blank lines
      patron_barcode_line = pageslip_lines[ line_counter + 1 ]
      break
    line_counter = line_counter + 1

  patron_barcode = patron_barcode_line.strip()
  spaceless_patron_barcode = patron_barcode.replace( ' ', '' )
  if spaceless_patron_barcode == '':   # patron barcode sometimes doesn't exist
    return '?'
  else:
    return spaceless_patron_barcode

  # end def parsePatronBarcode()



def parsePatronName( pageslip_lines ):
  '''
  - Purpose: to extract the patron name from the lines of a pageslip.
  - Called by: opac_to_las_python_parser_code.controller
  '''

  name = 'init'
  name_line = 'init'
  line_counter = 0
  blank_line_counter = 0

  for line in pageslip_lines:
    if len( line.strip() ) == 0:
      blank_line_counter = blank_line_counter + 1
    else:
      blank_line_counter = 0
    if blank_line_counter == 4:   # means we've had 4 blank lines
      name_line = pageslip_lines[ line_counter + 2 ]
      break
    line_counter = line_counter + 1

  name = name_line.strip()
  return name

  # end def parsePatronName()



def parseRecordNumber( single_page_slip ):
  '''
  - Purpose: to extract a record number from a page-slip.
  - Called by: opac_to_las_python_parser_code.controller
  '''

  record_number = 'init'
  for line in single_page_slip:
    stripped_line = line.strip()
    if 'REC NO:' in stripped_line:
      record_number = stripped_line[-10:]
      break

  return record_number

  # end def parseRecordNumber()



# def parseTitle( pageslip_lines ):
#   '''
#   - Purpose: to extract the item title from the lines of a pageslip.
#   - Called by: opac_to_las_python_parser_code.controller
#   '''

#   counter = 0
#   title_line = ''

#   for line in pageslip_lines:
#     if 'TITLE:' in line:
#       title_line = line.replace( 'TITLE:', '' )
#       break
#     elif 'PUB DATE:' in line:   # means that the title was too long to have a label
#       title_line = pageslip_lines[ counter - 2 ]   # two lines above 'PUB DATE:'
#       break
#     counter = counter + 1

#   stripped_title = title_line.strip()
#   dequoted_title = stripped_title.replace( '"', "'" )

#   return dequoted_title

#   # end def parseTitle()



def postFileData( identifier, file_data, update_type ):
  '''
  - Purpose: to post the file data from the opened-&-read file.
  - Called by: opac_to_las_python_parser_code.controller
  '''

  ADMIN_LOG_URL = os.environ['AN_PR_PA__ADMIN_LOG_URL']
  ADMIN_LOG_KEY = os.environ['AN_PR_PA__ADMIN_LOG_KEY']

  if update_type == 'original_file':
    values = {
      'key': ADMIN_LOG_KEY,
      'identifier': identifier,
      'original_file_data': file_data
      }
  else:
    values = {
      'key': ADMIN_LOG_KEY,
      'identifier': identifier,
      'parsed_file_data': file_data
      }

  try:
    data = urllib.urlencode(values)
    request = urllib2.Request( ADMIN_LOG_URL, data )
    response = urllib2.urlopen(request)
    returned_data = response.read()
    return returned_data
  except Exception, e:
    return '- in postFileData(); exception is: %s' % e

  # end def sampleOriginalDataPostingScript()




def prepareDateTimeStamp( date_stamp ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: to create a time-stamp string for the files to be archived, like '2005-07-13T13-41-39'
  '''

  iso_datestamp = date_stamp.isoformat()
  custom_datestamp = iso_datestamp[0:19]

  return str( custom_datestamp )

  # end def prepareDateTimeStamp()



def prepareLasDate( date_object=None ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: to create a date string like 'Wed Jul 01 2005'. In practice, no date will be passed in, but the 'date_object=None' allows for easy testing.
  '''

  if date_object == None:
    date_object = datetime.datetime.now()

  return date_object.strftime( '%a %b %d %Y' )

  # end def prepareLasDate()



def updateLog( message, message_importance='low', identifier='' ):
  '''
  - Called by: opac_to_las_python_parser_code.controller
  - Purpose: update web-accessible log.
  '''

  LOG_ENTRY_MINIMUM_IMPORTANCE_LEVEL = os.environ['AN_PR_PA__LOG_ENTRY_MINIMUM_IMPORTANCE_LEVEL']
  LOG_KEY = os.environ['AN_PR_PA__LOG_KEY']
  LOG_URL = os.environ['AN_PR_PA__LOG_URL']

  update_log_flag = 'init'

  if message_importance == 'high':
    update_log_flag = 'yes'
  elif (message_importance == 'low' and LOG_ENTRY_MINIMUM_IMPORTANCE_LEVEL == 'low' ):
    update_log_flag = 'yes'
  else:
    pass   # there definitely are many other conditions that will get us here -- but the whole point is not to log everything.

  if update_log_flag == 'yes':
    try:
      values = { 'message':message, 'identifier':identifier, 'key':LOG_KEY }
      data = urllib.urlencode(values)
      request = urllib2.Request(LOG_URL, data)
      response = urllib2.urlopen(request)
      returned_data = response.read()
      return returned_data
    except Exception, e:
      pass   # TO_DO: output exception to a log-file
      # raise Exception( '- in utility_code(); exception is: %s' % e )

  # end def updateLog()


class Mailer( object ):
    """ Specs email handling. """

    def __init__( self, UNICODE_SUBJECT, UNICODE_MESSAGE ):
        self.UTF8_SMTP_SERVER = os.environ['AN_PR_PA__UTF8_SMTP_SERVER']
        self.UTF8_RAW_TO_JSON = os.environ['AN_PR_PA__UTF8_RAW_TO_JSON']  # json (ensures reliable formatting/encoding), eg: '["addr1@domain.edu", "addr2@domain.com"]'
        self.UTF8_FROM_REAL = os.environ['AN_PR_PA__UTF8_FROM_REAL']  # real 'from' address smtp server will use, eg: 'addr3@domain.edu'
        self.UTF8_FROM_HEADER = os.environ['AN_PR_PA__UTF8_FROM_HEADER']  # apparent 'from' string user will see, eg: 'some_system'
        self.UTF8_REPLY_TO_HEADER = os.environ['AN_PR_PA__UTF8_REPLY_TO_HEADER']
        self.UNICODE_SUBJECT = UNICODE_SUBJECT
        self.UNICODE_MESSAGE = UNICODE_MESSAGE
        logger.debug( 'Mailer instantiated' )

    def send_email( self ):
        """ Sends email. """
        try:
            TO = self._build_mail_to()  # list of utf-8 entries
            MESSAGE = self.UNICODE_MESSAGE.encode( 'utf-8', 'replace' )  # utf-8
            payload = self._assemble_payload( TO, MESSAGE )
            s = smtplib.SMTP( self.UTF8_SMTP_SERVER )
            s.sendmail( self.UTF8_FROM_REAL, TO, payload.as_string() )
            s.quit()
            logger.debug( 'mail sent' )
            return True
        except Exception as e:
            logger.error( 'problem sending mail, exception, `%s`' % unicode(repr(e)) )
            return False

    def _build_mail_to( self ):
        """ Builds and returns 'to' list of email addresses.
            Called by send_email() """
        to_emails = json.loads( self.UTF8_RAW_TO_JSON )
        utf8_to_list = []
        for address in to_emails:
            utf8_to_list.append( address.encode('utf-8') )
        return utf8_to_list

    def _assemble_payload( self, TO, MESSAGE ):
        """ Puts together and returns email payload.
            Called by send_email(). """
        payload = MIMEText( MESSAGE )
        payload['To'] = ', '.join( TO )
        payload['From'] = self.UTF8_FROM_HEADER
        payload['Subject'] = Header( self.UNICODE_SUBJECT, 'utf-8' )  # SUBJECT must be unicode
        payload['Reply-to'] = self.UTF8_REPLY_TO_HEADER
        return payload

    # end class Mailer
