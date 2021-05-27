Tests
=====
Search through the content of PDF files for the word **hold** which is
accomplished with the regex ``\bhold\b`` with case-sensitive enabled. 
Thus for example, we want *hold* but not *holdings* nor *behold*.

If we wanted all occurrences of **hold** no matter where it appears in the text
content, then the ``hold`` query would do the work.

This is the ``~/ebooks/`` folder that contains the files which we will search
from:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/list_of_ebooks.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/list_of_ebooks.png
   :align: left
   :alt: List of ebooks to search from

`:information_source:`

  * The folder contains ebooks of different types but we will only
    search the PDF files.
  * Of the total eight PDF files, two are scanned ebooks that contain only
    images: *Les Misérables by Victor Hugo.pdf* and *The Republic by Plato.pdf*.

Searching content of PDF files with ``pdftotext``
-------------------------------------------------
We will use the `pdftotext`_ utility to convert PDF files to ``.txt`` in order
to search through content for a given search query.

By default, the ``seach-ebooks`` script uses ``pdftotext`` since it is way
faster than *calibre*\'s `ebook-convert`_ to convert files to ``.txt``.

The ``pdftotext``'s results are given for two cases: with and without cache.

Summary of results for ``pdftotext``-based search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using cache, the search is **4.7** times quicker than without cache:

+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | **1.146**      |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

``pdftotext`` with cache
^^^^^^^^^^^^^^^^^^^^^^^^
This is the command which makes use of ``pdftotext`` to search and cache to
save the converted PDF files into ``.txt``:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --use-cache
   
`:information_source:`

  - ``-f pdf`` is used to only process PDF files since the ``~/ebooks/`` folder
    might have all kinds of ebook files (e.g. ``.djvu`` and ``.epub``).
  - By default, ``search-ebooks`` uses the ``pdftotext`` utility to convert the
    PDF files to ``.txt`` and then search them for the given query.
  - By default, ``search-ebooks`` does a case-sensitive search. You can use the
    ``-i`` flag if you want to ignore case.

|

**Output:** ``pdftotext`` and cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

`:information_source:`

  Two PDF files were not included in the search results because they were
  scanned ebooks that only contain images.

``pdftotext`` without cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is the command which makes use of ``pdftotext`` to search but doesn't use
cache:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf
   
**Output:** ``pdftotext`` and no cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------
This is the command which makes use of *calibre*\'s ``ebook-convert`` to search
but doesn't use cache:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --psm calibre
 
`:information_source:`

  ``--psm calibre`` specifies to use *calibre*\'s `ebook-convert`_ to convert
  PDF files to ``.txt`` (instead of ``pdftotext``) and then search them for the
  given query.
 
|

`:warning:`

  However, ``ebook-convert`` is too slow when converting PDF files to
  ``.txt``. Also, ``ebook-convert`` will try to convert scanned ebooks that
  only contain images and after a long time waiting for the result, it will
  output a small ``.txt`` file that doesn't contain any of the file content. On
  the other hand, ``pdftotext`` will quickly warn you that the scanned ebook
  couldn't be converted to ``.txt``.
  
  Thus, ``pdftotext`` is used by default with the ``search-ebooks`` script to
  convert PDF files to ``.txt`` and search them for the given query.
