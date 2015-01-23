# -*- coding: utf-8 -*-


## set up environment ##

import os, sys
sys.path.append( os.environ[u'AN_PR_PA__ENCLOSING_PROJECT_PATH'] )
import pprint, unittest
from annex_process_pageslips import utility_code



class Tester(unittest.TestCase):



  def test_convertJosiahLocationCode(self):
    '''input page-slip; output Annex customer-code (josiah 'location-code')'''

    josiah_location = 'ANNEX'
    expected = 'QS'
    result = utility_code.convertJosiahLocationCode( josiah_location )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_convertJosiahLocationCode()



  def test_convertJosiahPickupAtCode(self):
    '''input page-slip; output Annex 'delivery-stop-code' (josiah 'pickup-at-code')'''

    josiah_pickup_at_code = 'ROCK'
    expected = 'RO'
    result = utility_code.convertJosiahPickupAtCode( josiah_pickup_at_code )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    josiah_pickup_at_code = 'John Hay Library'
    expected = 'HA'
    result = utility_code.convertJosiahPickupAtCode( josiah_pickup_at_code )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_convertJosiahPickupAtCode()



  def test_determineCount(self):

    TEST_FILES_DIR_PATH = os.environ[u'AN_PR_PA__TEST_FILES_DIR_PATH']

    # single pageslip
    number_of_parsed_items = 1
    # file_reference = open( 'test_files/testFile01_singleEntry.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile01_singleEntry.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 1
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # single short pageslip
    number_of_parsed_items = 5
    # file_reference = open( 'test_files/testFile02_incorrectSciPickup.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile02_incorrectSciPickup.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 5
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # single pageslip, no '38...'
    number_of_parsed_items = 1
    # file_reference = open( 'test_files/testFile11_singleNo38.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile11_singleNo38.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 1
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips
    number_of_parsed_items = 6
    # file_reference = open( 'test_files/testFile03_itemNumberAddition.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile03_itemNumberAddition.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 6
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips, one missing last '38...' line
    number_of_parsed_items = 7
    # file_reference = open( 'test_files/testFile04_longNotes.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile04_longNotes.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 7
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips, first two without the usual 'Brown University' four address lines
    number_of_parsed_items = 6
    # file_reference = open( 'test_files/testFile12_missing_brown_address.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile12_missing_brown_address.txt') )
    data = file_reference.read()
    lines = data.split( '\n' )
    expected = 6
    result = utility_code.determineCount( number_of_parsed_items, lines )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_determineCount()



  def test_makeItemList(self):
    '''sending a file-reference; getting back a list of page-slip items'''

    TEST_FILES_DIR_PATH = os.environ[u'AN_PR_PA__TEST_FILES_DIR_PATH']

    # single pageslip
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile01_singleEntry.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 1   # meaning there's one page-slip in the processed_data list
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 39   # meaning there are 39 lines in the first (and only) page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # single short pageslip
    # file_reference = open( 'test_files/testFile02_incorrectSciPickup.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile02_incorrectSciPickup.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 1   # meaning there's one page-slip in the processed_data list
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 35   # meaning there are 39 lines in the first (and only) page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # single pageslip, no '38...'
    # file_reference = open( 'test_files/testFile11_singleNo38.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile11_singleNo38.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 1   # meaning there's one page-slip in the processed_data list
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 39   # meaning there are 39 lines in the first (and only) page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips
    # file_reference = open( 'test_files/testFile03_itemNumberAddition.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile03_itemNumberAddition.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 6   # meaning there's one page-slip in the processed_data list
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 39   # meaning there are 39 lines in the first page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips, one missing last '38...' line
    # file_reference = open( 'test_files/testFile04_longNotes.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile04_longNotes.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 7   # meaning there's one page-slip in the processed_data list
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 39   # meaning there are 39 lines in the first page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    expected = 39   # meaning there are 39 lines in the second (weird) page-slip
    result = len( processed_data[0] )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # multiple pageslips, first two without the usual 'Brown University' four address lines
    # file_reference = open( 'test_files/testFile12_missing_brown_address.txt' )
    file_reference = open( u'%s/%s' % (TEST_FILES_DIR_PATH, u'testFile12_missing_brown_address.txt') )
    processed_data = utility_code.makeItemList( file_reference )
    expected = 6   # this was returning 4 parsed page-slips in old code and in my new code
    result = len( processed_data )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_makeItemList()



  def test_parseBookBarcode(self):
    '''input page-slip; output book-barcode'''

    # numeric barcode with spaces
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = '31236070303881'
    result = utility_code.parseBookBarcode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # 'JH' barcode
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   Tue Nov 22 2005', '', '', '', '', '          barcode', '          name', '          BROWN UNIVERSITY', '          BOX 1234', '          PROVIDENCE, RI 02912-3198', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Breggin, Peter Roger,', '   Toxic psychiatry : why therapy, empathy, and love', "   IMPRINT: New York : St. Martin's Press,", '   PUB DATE: 1991', '   DESC:    464 p. ; 24 cm', '   CALL NO: ', '   VOLUME:  ', '   BARCODE: JH16TV', '   STATUS: AVAILABLE', '   REC NO:  .i12345189', '   LOCATION: ANNEX HAY', '   PICKUP AT: Rockefeller Library', '', '', '', '', '', '   38:4']
    expected = 'JH16TV'
    result = utility_code.parseBookBarcode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parseBookBarcode()



  def test_parseJosiahLocationCode(self):
    '''input page-slip; output Josiah location code (annex 'customer_code')'''

    # 'ANNEX'
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'QS'
    result = utility_code.parseJosiahLocationCode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # empty
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION:', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = '?'
    result = utility_code.parseJosiahLocationCode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # no match
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: abc', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'failure'
    result = utility_code.parseJosiahLocationCode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
    # end def test_parseJosiahLocationCode()



  # def test_parseJosiahLocationCode(self):
  #   '''input page-slip; output Josiah location code (annex 'customer_code')'''
  #
  #   # 'ANNEX'
  #   single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
  #   expected = 'QS'
  #   result = utility_code.parseJosiahLocationCode( single_pageslip )
  #   self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )
  #
  #   # end def test_parseJosiahLocationCode()



  def test_parseJosiahPickupAtCode(self):
    '''input page-slip lines; output Josiah pickup-at code (annex 'delivery-stop code')'''

    # 'ROCK'
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'RO'
    result = utility_code.parseJosiahPickupAtCode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # empty
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   Tue Nov 22 2005', '', '', '', '', '          1 1234 12345 1234', '          name', '          BROWN UNIVERSITY', '          BOX 1234', '          PROVIDENCE, RI 02912-3198', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Breggin, Peter Roger,', '   Toxic psychiatry : why therapy, empathy, and love', "   IMPRINT: New York : St. Martin's Press,\n", '   PUB DATE: 1991', '   DESC:    464 p. ; 24 cm', '   CALL NO: ', '   VOLUME:  ', '   BARCODE: JH16TV', '   STATUS: AVAILABLE', '   REC NO:  .i12345189', '   LOCATION: ANNEX', '   PICKUP AT:', '', '', '', '', '', '   38:4']
    expected = '?'
    result = utility_code.parseJosiahPickupAtCode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parseJosiahPickupAtCode()



  def test_parseNote(self):
    '''input: pageslip, output: note string'''

    # with note
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   NOTE: four score and ', '        seven years ago', '        something interesting happened', '', '', '   38']
    expected = 'four score and seven years ago something interesting happened'
    result = utility_code.parseNote( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # without note
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   ', '', '', '', '', '   38']
    expected = '?'
    result = utility_code.parseNote( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # if note contains quotes
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   NOTE: four score and ', '        seven years ago', '        something "interesting" happened', '', '', '   38']
    expected = "four score and seven years ago something 'interesting' happened"
    result = utility_code.parseNote( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parseNote()



  def test_parsePatronBarcode(self):
    '''input pageslip lines; output item barcode'''

    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'barcodeabc'
    result = utility_code.parsePatronBarcode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # blank barcode
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = '?'
    result = utility_code.parsePatronBarcode( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parsePatronBarcode()



  def test_parsePatronName(self):
    '''input pageslip lines; output patron name'''

    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'name'
    result = utility_code.parsePatronName( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parsePatronName()



  def test_parseRecordNumber(self):
    '''input page-slip; output record-number'''

    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcod', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']

    expected = '.i10295297'
    result = utility_code.parseRecordNumber( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parseRecordNumber()



  def test_parseTitle(self):
    '''input pageslip lines; output item title'''

    # with 'TITLE' prefix
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   TITLE:   Draft resistance and social change', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'Draft resistance and social change'
    result = utility_code.parseTitle( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # without 'TITLE' prefix (happens when title is long) or even AUTHOR or IMPRINT as sometimes happens
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   no_a-u-t-h-or:  Darlington, Marwood,', '   Irish Orpheus, the life of Patrick S. Gilmore, ba', '   no_i-m-p-r-i-n-t: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = 'Irish Orpheus, the life of Patrick S. Gilmore, ba'
    result = utility_code.parseTitle( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # title contains quotes
    single_pageslip = ['   Brown University', '   Gateway Services, Rockefeller Library', '   10 Prospect Street - Box A', '   Providence, RI 02912', '', '   05-27-05', '', '', '', '', '          barcode abc', '          name', '          BROWN UNIVERSITY', '          U LIBR-WEB SERV - BOX A', '          PROVIDENCE, RI 02912-9101', '', '', '   Please page this material and', '   forward to the circulation unit.', '', '', '   AUTHOR:  Darlington, Marwood,', '   TITLE:   Draft resistance "and" social change', '   IMPRINT: Philadelphia, Olivier-Maney-Klein', '   PUB DATE: [1950]', '   DESC:    130 p. illus., ports. 21 cm', '   CALL NO: ML422.G48 D3', '   VOLUME:  ', '   BARCODE: 3 1236 07030 3881', '   STATUS: AVAILABLE', '   REC NO:  .i10295297', '   LOCATION: ANNEX', '   PICKUP AT: ROCK', '   OPACMSG: ', '', '', '', '', '   38']
    expected = "Draft resistance 'and' social change"
    result = utility_code.parseTitle( single_pageslip )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_parseTitle()



  def test_prepareDateTimeStamp(self):
    '''sending a known time to check formatting'''

    from datetime import datetime
    test_date = datetime(2005, 7, 13, 13, 41, 39, 48634)   # 'Wed Jul 13 13:41:39 EDT 2005'

    expected = '2005-07-13T13:41:39'
    result = utility_code.prepareDateTimeStamp( test_date )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    expected = 19
    date_time_stamp = utility_code.prepareDateTimeStamp( test_date )
    result = len( date_time_stamp )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_prepareDateTimeStamp()



  def test_prepareLasDate(self):
    '''sending a known time to check formatting'''

    from datetime import datetime

    # with date
    test_date = datetime(2005, 7, 13, 13, 41, 39, 48634)   # 'Wed Jul 13 13:41:39 EDT 2005'
    expected = 'Wed Jul 13 2005'
    result = utility_code.prepareLasDate( test_date )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # without date
    returned_date_string = utility_code.prepareLasDate()
    expected = 15
    result = len( returned_date_string )
    self.assertEqual( expected, result, '\n- expected is: %s\n  - result is: %s' % (expected, result) )

    # end def test_prepareLasDate()


  # end class Tester()



if __name__ == "__main__":
  unittest.main()



# bottom
