======
README
======
Search through content and metadata of different types of ebooks.

.. contents:: **Contents**
   :depth: 3
   :local:
   :backlinks: top

Search through content
======================
Search ``djvu`` files
---------------------
- Use `djvutxt`_ to extract text and pipe it to ``grep``.

Search ``epub`` files
---------------------
- Use ``find`` and ``zipgrep``:

  .. code-block:: terminal

     find . -name "*.epub" -exec zipgrep pattern {} \;
   
  [ZIPGREP]_
  
  Or for a single file:
  
  .. code-block:: terminal
  
     find test.epub -exec zipgrep pattern {} \;

  **NOTE:** ``zipgrep`` doesn't work on ``mobi`` files (they are not related 
  to `zip` or `epub`) [MOBI]_

Search ``pdf`` files
--------------------
TODO

Search through metadata
=======================
Use ``ebook-meta`` which supports almost any ebook formats 
(`complete list of supported formats`_)

References
==========
.. [MOBI] https://bit.ly/2SBAru1
.. [ZIPGREP] https://unix.stackexchange.com/a/416207

.. URLs
.. _complete list of supported formats: https://manual.calibre-ebook.com/generated/en/ebook-meta.html
.. _djvutxt: http://djvu.sourceforge.net/doc/man/djvutxt.html
