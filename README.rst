=============
search-ebooks
=============

.. raw:: html

  <p align="center">
    <br> 🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
  </p>

`search-ebooks`_ is a command-line program that searches through content
and metadata of different types of ebooks. It is based on the `pyebooktools`_
Python package for building ebook management scripts (e.g. conversion of ebooks 
to ``.txt`` in order to then search on them)

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
   
Introduction
============
``search-ebooks`` allows you to choose the search methods for the different ebook formats.
These are the supported search-backends for each type of ebooks:

+---------------+----------------------------------------------------------+
| File type     | Supported search-backends                                |
+===============+==========================================================+
| ``.djvu``     | 1. `djvutxt`_ (**default**)                              |
|               | 2. `ebook-convert`_                                      |
+---------------+----------------------------------------------------------+
| ``.epub``     | 1. `ebook-convert`_ (**default**)                        |
|               | 2. ``epubtxt``                                           |
+---------------+----------------------------------------------------------+
| ``.doc`` [1]_ | 1. `catdoc`_ or `textutil`_ (if on macOS) (**default**)  |
|               | 2. `ebook-convert`_                                      |
+---------------+----------------------------------------------------------+
| ``.pdf``      | 1. `pdftotext`_ (**default**)                            |
|               | 2. `ebook-convert`_                                      |
+---------------+----------------------------------------------------------+

`:information_source:`

  * The utilities mentioned in the **Supported search-backends** column
    are used to extract the text before it is searched on.
  * More specifically, ``epubtxt`` consists in uncompressing first the 
    ``epub`` file with `unzip`_ since ``epub``\s are zipped HTML files. Then, 
    the extracted text is searched on. I tried to use `zipgrep`_ to do
    both the unzipping and searching but I couldn't make it to work with
    regular expressions such as ``\bpattern\b``.
  * The **default** search methods (except for ``.epub``) are used since 
    they are quicker to extract text than *calibre*\'s `ebook-convert`_. But 
    if these default utilities are not installed, then the searching relies on 
    ``ebook-convert`` for converting the documents to ``.txt``
  * Eventually, I will add support for `Lucene`_ as a search backend since it 
    has "powerful indexing and search features, as well as spellchecking, hit 
    highlighting and advanced analysis/tokenization capabilities".

`:warning:`

  I didn't set ``epubtxt`` as a default search-backend for ``epub`` files 
  because it also includes the HTML tags in the extracted text even though 
  text extraction is faster than with `ebook-convert`_.
  
  Once I clean up the extracted text, I will set ``epubtxt`` as a default
  search method for ``epub`` files if it is still faster than ``ebook-convert``
  for text extraction.

|

All the utilities that extract text make use of a file-based `cache`_ to save
the converted ebook files to ``.txt`` and hence speed up the searching by a
lot. Depending on the number of files searched, the searching can even be 20
times faster with cache than without it (TODO: add tests to show performance
of searching with cache and no cache).
   
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
you need recent version of:

* `calibre`_ to convert ebook files to ``.txt`` and get metadata from ebooks
  
And optionally, you might need:

* (**Highly recommended**) `poppler`_, `catdoc`_ and `DjVuLibre`_ 
  can be installed for faster than calibre's conversion of ``.pdf``, ``.doc``
  and ``.djvu`` files respectively to ``.txt``.
* `Tesseract`_ for running OCR on books - version 4 gives better results
  even though it's still in alpha. OCR is disabled by default since it 
  is a slow resource-intensive process.
  
  `:warning:`
   
    On macOS, you don't need ``catdoc`` since `textutil`_ is already
    present

.. TODO: add these options
.. * `Lucene`_ for a powerful search library
.. (for Tesseract) and another engine can be configured if preferred.

Cache
=====
Cache is used to save the converted ebook files into ``.txt`` to avoid
re-converting them which is a time consuming process, specially if
it is a document with hundreds of pages. `DiskCache`_, a disk and file backed
cache library, is used by the ``search-ebooks`` script.

A file-based cache library was choosen instead of a memory-based 
cache like `Redis`_ because the converted files (``.txt``) needed to be 
persistent to speed up subsequent searches and since we are storing huge
quantities of data (e.g. we can have thousands of ebooks to search from), 
a memory-based cache might not be suited. In order to avoid using too much 
disk space, you can set the cache size with the ``--cache-size-limit`` flag
which by default it is set to 1 GB.

As an example to see how much disk space you might need to cache one thousand
``.txt`` files all at once, let's say that on average each ``.txt`` file uses
approximately 700 KB which roughly corresponds to a file with 350 pages. 
Thus, you will need a cache size of at least 700 MB.

Also `DiskCache`_ has interesting features compared to other file-based 
cache libraries such as being thread-safe and process-safe and supporting 
multiple eviction policies. See `Features`_ for a more complete list.

See `DiskCache Cache Benchmarks`_ for comparaisons to `Memcached`_ and 
`Redis`_.

Tips
====
TODO

Examples
========
We will present search examples that are not trivial in order to show the
potential of the ``search-ebooks`` script for executing complex queries.

This is the ``~/ebooks/`` folder that contains the files which we will search
from in the following examples:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/list_of_ebooks.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/list_of_ebooks.png
   :align: left
   :alt: List of ebooks to search from

`:information_source:`

  Of the total eight PDF files, two are files that contain only
  images: *Les Misérables by Victor Hugo.pdf* and 
  *The Republic by Plato.pdf*. which both consist of only two images for 
  testing purposes.

Search ebooks whose filenames satisfy a given pattern
-----------------------------------------------------
We want to search for the word *knowledge* but only for those ebooks whose
filenames contain either *Aristotle* or *Plato* and also we want to ignore
case:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bknowledge\b" --filename "Aristotle|Plato" -i --use-cache

`:information_source:`

  * ``\bknowledge\b`` matches exactly the word *knowledge*, i.e. it performs a 
    `“whole words only” search`_. Thus, words like *acknowledge* or *knowledgeable* 
    are rejected.
  * Since we already converted the files to ``.txt`` in previous runs,
    we make use of the cache with the ``--use-cache`` flag.

**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_filenames_satisfy_pattern.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_filenames_satisfy_pattern.png
   :align: left
   :alt: Output for example: filenames satisfy a given pattern

`:information_source:`

  * The ``txt`` and ``pdf`` versions of *The Ethics of Aristotle by Aristotle*
    show different number of matches because they are not the same translations
    and hence the word *knowledge* might come from the introduction (written by 
    another author) or the translator's footnotes.
  * On the other hand, the ``txt`` and ``epub`` versions of *Politics_ A 
    Treatise on Government by Aristotle* show the same number of matches because
    they are both the same translation.
  * As explained previously, *The Republic by Plato.pdf* is not included in
    the matches because it is a file with images only and since
    we didn't use the ``--ocr`` flag, the file couldn't be converted to ``.txt``.

Search documents with images 
----------------------------
We will execute the `previous query`_ but this time we will include the
file *The Republic by Plato.pdf* (which contains images) in the search by 
using the ``--ocr`` flag which will convert the images to text with `Tesseract`_:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bknowledge\b" --filename "Aristotle|Plato" -i --use-cache --ocr

`:information_source:`
 
  The ``--ocr`` flag allows you to search ``.pdf``, ``.djvu`` and image files but it
  is disabled by default because `OCR`_ is a slow resource-intensive process.
  Thus, use it wisely!

**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ocr_images.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ocr_images.png
   :align: left
   :alt: Output for example: OCR PDF file with images

Roadmap
=======
Starting from first priority tasks:

1. Add many tests with many ebooks (in the thousands maybe)

   **Status:** working on it

2. Add examples for searching text content and metadata of ebooks
   
   **Status:** working on it
   
3. Add instructions on how to install the ``searchebooks`` package

4. Add support for `Lucene`_ as a search backend
   
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
.. _“whole words only” search: https://www.regular-expressions.info/wordboundaries.html
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
.. _OCR: https://en.wikipedia.org/wiki/Optical_character_recognition
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
.. _unzip: https://linux.die.net/man/1/unzip
.. _zipgrep: https://linux.die.net/man/1/zipgrep

.. Local URLs
.. _cache: #cache
.. _previous query: #search-ebooks-whose-filenames-satisfy-a-given-pattern
.. _search-ebooks: ./searchebooks/search_ebooks.py
