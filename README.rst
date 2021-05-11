======
README
======
Using command-line tools only, search through content and metadata of different types of ebooks.

.. contents:: **Contents**
   :depth: 3
   :local:
   :backlinks: top

Search through content
======================
Search ``djvu`` files
---------------------
- Use `djvutxt`_ to extract text and pipe it to ``grep``
- Use `ebook-convert`_ (from Calibre) to extract text and pipe it to ``grep``

Search ``epub`` files
---------------------
- Use ``find`` and ``zipgrep``:

  .. code-block:: terminal

     find . -name "*.epub" -exec zipgrep pattern {} \;
  
  To print only the filenames (not the matching lines):
  
  .. code-block:: terminal
  
     find . -name '*.epub'  -exec zipgrep -q {pattern} {} \; -print
  
  **NOTE:** by using the ``-q, --quiet`` flag, ``zipgrep`` "will only 
  search a file until a match has been found, making searches 
  potentially less expensive."
  
  Or for a single file:
  
  .. code-block:: terminal
  
     find test.epub -exec zipgrep pattern {} \;

  **NOTE:** ``zipgrep`` doesn't work on ``mobi`` files (they are not related 
  to `zip` or `epub`)
  
- Use `ebook-convert`_ (from Calibre) to extract text and pipe it to ``grep``

Search ``pdf`` files
--------------------
TODO

Search through metadata
=======================
Use ``ebook-meta`` which supports almost any ebook formats 
(`complete list of supported formats`_)

NOTES
=====
* Some desktop applications for searching ebook files:

  * `DocFetcher`_: open source, cross-platform, supports among
    other document formats ``epub``, ``pdf``, and ``rtf``.
    
  * `Quality Check plugin`_ for Calibre: "search across your ePubs 
    for ad hoc criteria to find text or specifically named items 
    using regular expressions."

References
==========
.. [MAN_EGREP] https://www.unix.com/man-page/osx/1/egrep/
.. [MOBI_NOT_ZIP] https://bit.ly/2SBAru1
.. [ZIPGREP] https://unix.stackexchange.com/a/416207
.. [ZIPGREP_QUIET] https://unix.stackexchange.com/a/452491

.. URLs
.. _complete list of supported formats: https://manual.calibre-ebook.com/generated/en/ebook-meta.html
.. _djvutxt: http://djvu.sourceforge.net/doc/man/djvutxt.html
.. _DocFetcher: http://docfetcher.sourceforge.net/en/index.html
.. _ebook-convert: https://manual.calibre-ebook.com/generated/en/ebook-convert.html
.. _Quality Check plugin: https://www.mobileread.com/forums/showthread.php?t=125428
