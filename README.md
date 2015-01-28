ReadMe contents
---------------

on this page...
- qualifier
- process overview
- contacts
- [license](#license)


Qualifier
---------

This is ancient code updated just enough to get onto github. It's one of my first (2005) python projects; I went a bit overboard in abandonment of classes in my flight from java.


Code/context overview
---------------------

Patrons sometimes request, from our III opac, items which are stored at the Annex, Brown Library's offsite storage facility.

A (separate) script periodically FTPs opac request page-slips to the Annex server.

This code processes the III page-slips into source data files for the Annex inventory control software.

The 'controller' script...
- archives the original page-slip file
- parses the file
- archives the parsed file
- saves the parsed data and count data to las destinations
- updates via post a tracker url
- deletes the original file


Contacts
--------

Domain contact: bonnie_buzzell@brown.edu

Programmer: birkin_diana@brown.edu


<a id="license"></a>

License
-------

The MIT License (MIT)

Copyright (c) 2015 Brown University Library

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
