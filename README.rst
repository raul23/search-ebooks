=============
search-ebooks
=============

.. raw:: html

  <p align="center">
    <br> 🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
  </p>

Command-line program that searches through content and metadata of
different types of ebooks.

.. contents:: **Contents**
   :depth: 2
   :local:
   :backlinks: top
   
Dependencies
============
* **Platforms:** macOS [soon linux]
* **Python**: >= 3.6
* ``diskcache`` >= 5.2.1 for caching persistently the converted files into ``.txt``

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

As an example to see how much disk space you might need to cache 1000 ``.txt``
files all at once, let's say that on average each ``.txt`` file uses
approximately 700 KB which roughly corresponds to a PDF file with 350 pages. 
Thus, you will need a cache size of at least 700 MB.

Also `DiskCache`_ has its own interesting features compared to other file-based 
cache libraries such as being thread-safe and process-safe and supporting 
multiple eviction policies. See `Features`_ for a more complete list.

See `DiskCache Cache Benchmarks`_ for comparaisons to `Memcached`_ and 
`Redis`_.

Tests
=====
Search through the content of eight PDF files for the word **hold**
which is accomplished with the regex ``\bhold\b``. Thus for
example, we want *hold* but not *holdings* nor *behold*.

If we wanted all occurrences of **hold** no matter where it appears 
in the text content, then the ``hold`` query would do the work.

Searching content of PDF files with ``pdftotext``
-------------------------------------------------
We will use the `pdftotext`_ utility to convert PDF files to ``.txt`` in order
to search through content for a given search query.

By default, the ``seach-ebooks`` script uses ``pdftotext`` since it is way
faster than *calibre*\'s `ebook-convert`_ to convert files to ``.txt``.

The ``pdftotext``'s results are given for two cases: with and without cache.

Summary of results for ``pdftotext``-based search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using cache, we are able to decrease the search time by **4.7**

+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | **1.146**      |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

With cache
^^^^^^^^^^
This is the command which makes use of ``pdftotext`` to search and cache to save the converted
PDF files into ``.txt``:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --use-cache
   
`:information_source:`

  - ``-f pdf`` is used to only process PDF files since the ``~/ebooks/`` folder might
    have all kinds of ebook files (e.g. ``.djvu`` and ``.epub``).
  - By default, the search uses the ``pdftotext`` utility to convert the PDF files
    to ``.txt`` and then search them for the given query.

|

**Output:** ``pdftotext`` and cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Without cache
^^^^^^^^^^^^^
This is the command which makes use of ``pdftotext`` to search but doesn't use cache:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf
   
**Output:** ``pdftotext`` and no cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------
This is the command which makes use of *calibre*\'s ``ebook-convert`` to search but doesn't use cache:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --psm calibre
 
`:information_source:`

  ``psm calibre`` specifies to use *calibre*\'s `ebook-convert`_ to convert
  PDF files to ``.txt`` (instead of ``pdftotext``) and then search them for the
  given query.
 
|

`:warning:`

  However, ``ebook-convert`` is too slow when converting PDF files to ``txt``.
  Also, ``ebook-convert`` will try to convert scanned ebooks that only contain images 
  and after a long time waiting for the result, it will output a small ``.txt`` file 
  that doesn't contain any of the file content. On the other hand, ``pdftotext`` will
  quickly warn you that the scanned ebook couldn't be converted to ``.txt``.
  
  Thus, ``pdftotext`` is used by default with the ``search-ebooks`` script
  to convert PDF files to ``.txt`` and search them for the given query.

Examples
========
TODO

Roadmap
=======
* Add support for multiprocessing
* Implement a GUI, specially to make navigation of search results easier 
  since you can have hundreds of matches for a given search query
  
  Though, for the moment not sure which GUI library to choose from 
  (e.g. `Kivy`_, `TkInter`_)

License
=======
This program is licensed under the GNU General Public License v3.0. For more details see 
the `LICENSE`_ file in the repository.

.. URLs
.. _DiskCache: http://www.grantjenks.com/docs/diskcache/
.. _DiskCache Cache Benchmarks: http://www.grantjenks.com/docs/diskcache/cache-benchmarks.html
.. _ebook-convert: https://manual.calibre-ebook.com/generated/en/ebook-convert.html
.. _Features: http://www.grantjenks.com/docs/diskcache/index.html#features
.. _Kivy: https://kivy.org/
.. _LICENSE: ./LICENSE
.. _Memcached: http://memcached.org/
.. _pdftotext: https://www.xpdfreader.com/pdftotext-man.html
.. _Redis: https://redis.io/
.. _TkInter: https://wiki.python.org/moin/TkInter
