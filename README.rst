=============
search-ebooks
=============

.. raw:: html

  <p align="center">
    <br> 🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
  </p>

``search-ebboks`` is a command-line program that searches through content
and metadata of different types of ebooks.

It allows you to choose the search methods for the different ebook formats.
These are the supported search-backends for each type of ebooks:

+---------------+-----------------------------------------+-------------------+-------------------+
| File type     | Search-backend #1 (default)             | Search-backend #2 | Search-backend #3 |
+===============+=========================================+===================+===================+
| ``.djvu``     | `djvutxt`_                              | `ebook-convert`_  | `Lucene`_         |
+---------------+-----------------------------------------+                   |                   |
| ``.epub``     | `zipgrep`_                              |                   |                   |
+---------------+-----------------------------------------+                   |                   |
| ``.doc`` [1]_ | `catdoc`_ or `textutil`_ (if on macOS)  |                   |                   |
+---------------+-----------------------------------------+                   |                   |
| ``.pdf``      | `pdftotext`_                            |                   |                   |
+---------------+-----------------------------------------+-------------------+-------------------+

`:information_source:`

  * By default, the search methods from the **Search-backend #1** column 
    are used since they are quicker to extract text than *calibre*
  * The utilities mentioned in the **Search-backend** columns are used to 
    extract the text before it is search on. However, ``.epub`` files must
    first be uncompressed by ``zipgrep`` since they are zipped HTML files.
  * `Lucene`_ is not supported yet

|

All the utilities that extract text make use of a file-based `cache`_ to save
the converted ebook files to ``.txt`` and hence speed up the searching by a
lot. Depending on the number of files searched, the searching can even be 20
times faster with cache than without it.

The only search method that doesn't make use of the cache is the one based on
``zipgrep`` because it doesn't return the whole extracted text, but only the 
lines of the text that matched the given search query.

|

`:warning:`

  * For the moment, the ``search-ebooks`` script is only tested on **macOS**.
    It will be tested also on linux.
  * **More to come!** Check the `Roadmap <#roadmap>`_ to know what is coming
    soon.

|

.. contents:: **Contents**
   :depth: 2
   :local:
   :backlinks: top
   
Dependencies
============
Python dependencies
-------------------
* **Platforms:** macOS [soon linux]
* **Python**: >= **3.6**
* `diskcache`_ >= **5.2.1** for caching persistently the converted files into
  ``.txt``
* `pyebooktools`_ >= **0.1.0a3** for converting files to ``.txt`` (see
  `convert_to_txt.py`_) along with its library `lib.py`_ that has useful
  functions for building ebook management scripts.

Other dependencies
-------------------
As explained in the documentation for 
`pyebooktools <https://github.com/raul23/pyebooktools#other-dependencies>`__, 
you need recent versions of:

* `calibre`_ for converting ebook files to ``.txt``
  
And optionally, you might need:

* (**Highly recommended**) `poppler`_, `catdoc`_ and `DjVuLibre`_ 
  can be installed for faster than calibre's conversion of ``.pdf``, ``.doc``
  and ``.djvu`` files respectively to ``.txt``.
  
  `:warning:`
   
    On macOS, you don't need ``catdoc`` since `textutil`_ is already
    present

.. TODO: add these options
.. * `Lucene`_ for a powerful search library
.. * `Tesseract`_ for running OCR on books - version 4 gives better results
   even though it's still in alpha. OCR is disabled by default and another
   engine can be configured if preferred.

Cache
=====
Cache is used to save the converted ebook files into ``.txt`` to avoid
re-converting them which is a very time consuming process, specially if
it is a document with hundreds of pages. `DiskCache`_, a disk and file backed
cache library, is used by the ``search-ebooks`` script.

A file-based cache library was choosen instead of a memory-based 
cache like `Redis`_ because the converted files (``.txt``) needed to be 
persistent to speed up subsequent searches and since we are storing huge
quantities of data (e.g. we can have thousands of ebooks to search from), 
a memory-based cache might not be suited. In order to avoid using too much 
disk space, you can set the cache size which by default it is set to 1 GB.

As an example to see how much disk space you might need to cache one thousand
``.txt`` files all at once, let's say that on average each ``.txt`` file uses
approximately 700 KB which roughly corresponds to a file with 350 pages. 
Thus, you will need a cache size of at least 700 MB.

Also `DiskCache`_ has interesting features compared to other file-based 
cache libraries such as being thread-safe and process-safe and supporting 
multiple eviction policies. See `Features`_ for a more complete list.

See `DiskCache Cache Benchmarks`_ for comparaisons to `Memcached`_ and 
`Redis`_.

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

Examples
========
We will present search examples that are not trivial in order to show the
potential of the ``search-ebooks`` script for searching for complex types of 
query.

In all the examples, this is the list of ebooks we will search from:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/list_of_ebooks.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/list_of_ebooks.png
   :align: left
   :alt: List of ebooks to search from

Search ebooks whose filenames satisfy a given pattern
-----------------------------------------------------
We want to search for the word 'knowledge' but only for those ebooks whose
filenames contain either 'Aristotle' or 'Plato' and also we want to ignore
case:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query knowledge --filename "Aristotle|Plato" --use-cache -i

Roadmap
=======
Starting from first priority tasks:

1. Add many tests with more ebooks (in the thousands maybe)

   **Status:** working on it

2. Add tests and examples for searching metadata of ebooks
   
   **Status:** working on it
   
3. Add instructions on how to install the ``searchebooks`` package

4. Add support for `Lucene`_ as a search backend since it has
   "powerful indexing and search features, as well as spellchecking, hit
   highlighting and advanced analysis/tokenization capabilities".
   
   `PyLucene`_ will be used to access ``Lucene``\'s text indexing and searching
   capabilities from Python
   
5. Test on linux
6. Create a `docker`_ image for this project
7. Read also metadata from *calibre*\'s ``metadata.opf`` if found
8. Add tests on `Travis CI`_
9. Eventually add documentation on `Read the Docs`_
10. Add support for multiprocessing so you can have multiple ebook files
    being searched in parallel based on the number of cores
11. Implement a GUI, specially to make navigation of search results easier 
    since you can have thousands of matches for a given search query
  
    Though, for the moment not sure which GUI library to choose from 
    (e.g. `Kivy`_, `TkInter`_)

License
=======
This program is licensed under the GNU General Public License v3.0. For more
details see the `LICENSE`_ file in the repository.

References
==========
.. [1] ``txt``, ``html``, ``rtf``, ``rtfd``, ``doc``, ``wordml``, or ``webarchive``. See `<https://ss64.com/osx/textutil.html>`__

.. URLs
.. _calibre: https://calibre-ebook.com/
.. _catdoc: http://www.wagner.pp.ru/~vitus/software/catdoc/
.. _convert_to_txt.py: https://github.com/raul23/pyebooktools/blob/master/pyebooktools/convert_to_txt.py
.. _DiskCache: http://www.grantjenks.com/docs/diskcache/
.. _DiskCache Cache Benchmarks: http://www.grantjenks.com/docs/diskcache/cache-benchmarks.html
.. _DjVuLibre: http://djvu.sourceforge.net/
.. _djvutxt: http://djvu.sourceforge.net/doc/man/djvutxt.html
.. _docker: https://docs.docker.com/
.. _ebook-convert: https://manual.calibre-ebook.com/generated/en/ebook-convert.html
.. _Features: http://www.grantjenks.com/docs/diskcache/index.html#features
.. _Kivy: https://kivy.org/
.. _lib.py: https://github.com/raul23/pyebooktools/blob/master/pyebooktools/lib.py
.. _LICENSE: ./LICENSE
.. _Lucene: https://lucene.apache.org/
.. _Memcached: http://memcached.org/
.. _other related text files: https://ss64.com/osx/textutil.html
.. _pdftotext: https://www.xpdfreader.com/pdftotext-man.html
.. _poppler: https://poppler.freedesktop.org/
.. _pyebooktools: https://github.com/raul23/pyebooktools
.. _PyLucene: https://lucene.apache.org/pylucene/
.. _Read the Docs: https://readthedocs.org/
.. _Redis: https://redis.io/
.. _Tesseract: https://github.com/tesseract-ocr/tesseract
.. _textutil: https://ss64.com/osx/textutil.html
.. _TkInter: https://wiki.python.org/moin/TkInter
.. _Travis CI: https://travis-ci.com/
.. _zipgrep: https://linux.die.net/man/1/zipgrep

.. Local URLs
.. _cache: #cache
