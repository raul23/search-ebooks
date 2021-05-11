======
README
======
Using **command-line tools** only, search through content and metadata of different 
types of ebooks.

.. contents:: **Contents**
   :depth: 3
   :local:
   :backlinks: top

Search through content
======================
Search ``djvu`` files
---------------------
- Use `djvutxt`_ to extract text and pipe it to ``grep``
- Use `ebook-convert`_ (from calibre) to extract text and pipe it to ``grep``

Search ``epub`` files
---------------------
- Use ``find`` and ``zipgrep``:

  .. code-block:: terminal

     find . -name '*.epub' -exec zipgrep pattern {} \;
  
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
  
- Use `ebook-convert`_ (from calibre) to extract text and pipe it to ``grep``

Search ``pdf`` files
--------------------
- Use `pdftotext`_ to extract text and pipe it to ``grep``
- Use `ebook-convert`_ (from calibre) to extract text and pipe it to ``grep``

Search through metadata
=======================
* Use `ebook-meta`_ which supports almost any ebook formats for reading metadata:

     azw, azw1, azw3, azw4, cb7, cbr, cbz, chm, docx, epub, fb2, fbz, html, htmlz, 
     imp, lit, lrf, lrx, mobi, odt, oebzip, opf, pdb, pdf, pml, pmlz, pobi, prc, 
     rar, rb, rtf, snb, tpz, txt, txtz, updb, zip

NOTES
=====
* Some desktop applications for searching ebook files:

  * `DocFetcher`_: open source, cross-platform, supports among
    other document formats ``epub``, ``pdf``, and ``rtf``.
    
  * `Quality Check plugin`_ for calibre: "search across your ePubs 
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
.. _ebook-meta: https://manual.calibre-ebook.com/generated/en/ebook-meta.html
.. _pdftotext: https://www.xpdfreader.com/pdftotext-man.html
.. _Quality Check plugin: https://www.mobileread.com/forums/showthread.php?t=125428
