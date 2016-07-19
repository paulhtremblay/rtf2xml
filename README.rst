===========
VERSION:
===========

2.0

========
OVERVIEW
========

The script rtf2xml converts Microsoft RTF to XML. 

By default, the script outputs to a raw XML, which faitfully represents the
strucutre of the original RTF document.



============
INSTALLATION
============

1. Type::
    
    python setup.py install

FOR earlier versions::

  pip install rtf2xml 

NOTE: I have not yet uploaded rtf2xml to the Python PyPi. I am waiting to get a
permissions issue resolved. The installation downloaded with pip will work for
python 2, but not python 3.



=========
QUICK USE
=========

To convert an RTF document to raw XML type:

rtf2xml  my_file.rtf

====================
Bugs, limitations
====================

* Won't properly convert legacy RTF with multi-byte representations.

  The script rtf2xml will convert older RTF that has 8-bit
  representations, which includes most (all?) of the languages of
  Europe. However, rtf2xml cannot convert older files in the Japanese
  or Chinese language. It can convert newer files in these languages,
  but the older RTF gives no unicode markings, making conversion
  impossible. 

* Will often misrepresent RTF produced with Open Office. 

  Open Office RTF produces some characters as double question marks 
  (??). Other RTF readers can filter out these charcters, but the 
  script rtf2xml cannot, and in my opinion, these double question
  marks do not follow Microsoft's guidelines. 

* Won't convert pictures. 

  See the documentation on this limitation.
