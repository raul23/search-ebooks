=============
search-ebooks
=============

.. raw:: html

  <p align="center">
    <br> 🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
  </p>

`search-ebooks`_ is a command-line program that searches through content
and metadata of various types of ebooks (``djvu``, ``epub``, ``txt``, 
``pdf``). It is based on the `pyebooktools`_ Python package for building 
ebook management scripts.

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

* The utilities mentioned in the **Supported search-backends** column
  are used to extract the text before it is searched on. ``epubtxt`` is
  the only one that is not a standalone utility like the others.
* More specifically, ``epubtxt`` consists in uncompressing first the 
  ``epub`` file with `unzip`_ since ``epub``\s are zipped HTML files. Then, 
  the extracted text is searched on with Python's `re`_ library. I tried to 
  use `zipgrep`_ to do both the unzipping and searching but I couldn't make 
  it to work with regular expressions such as ``\bpattern\b``.
* The **default** search methods (except for ``epub``) are used since 
  they are quicker to extract text than *calibre*\'s `ebook-convert`_. But 
  if these default utilities are not installed, then the searching relies on 
  ``ebook-convert`` for converting the documents to ``txt``
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
the converted files (``txt``) of the ebooks and hence the searching can be greatly 
speep up.
   
Dependencies
============
Python dependencies
-------------------
* **Platforms:** macOS [soon linux]
* **Python**: >= **3.6**
* `diskcache`_ >= **5.2.1** for caching persistently the converted files into
  ``txt``
* `pyebooktools`_ >= **0.1.0a3** for converting files to ``txt`` (see
  `convert_to_txt.py`_) along with its library `lib.py`_ that has useful
  functions for building ebook management scripts.

Other dependencies
-------------------
As explained in the documentation for 
`pyebooktools <https://github.com/raul23/pyebooktools#other-dependencies>`__, 
you need recent version of:

* `calibre`_ to convert ebook files to ``txt`` and get metadata from ebooks
  
And optionally, you might need recent versions of:

* (**Highly recommended**) `poppler`_, `catdoc`_ and `DjVuLibre`_ 
  can be installed for faster than calibre's conversion of ``.pdf``, ``.doc``
  and ``.djvu`` files respectively to ``.txt``.
  
  `:warning:`
   
    On macOS, you don't need ``catdoc`` since `textutil`_ is already
    present
  
* `Tesseract`_ for running OCR on books - version 4 gives better results
  even though it's still in alpha. OCR is disabled by default since it 
  is a slow resource-intensive process.

.. TODO: add these options
.. * `Lucene`_ for a powerful search library
.. (for Tesseract) and another engine can be configured if preferred.

Cache
=====
Cache is used especially to save the converted ebook files into ``txt`` to avoid
re-converting them which is a time consuming process, especially if
it is a document with hundreds of pages. `DiskCache`_, a disk and file backed
cache library, is used by the ``search-ebooks`` script.

The cache is also used to save the results of *calibre*\'s `ebook-meta`_
when searching the metadata of ebooks such as their authors and tags.

The ``search-ebooks`` script can use the cache with the ``--use-cache`` flag.

`:information_source:`

  The MD5 hashes of the ebook files are used as keys to the file-based cache.

A file-based cache library was choosen instead of a memory-based 
cache like `Redis`_ because the converted files (``txt``) needed to be 
persistent to speed up subsequent searches and since we are storing huge
quantities of data (e.g. we can have thousands of ebooks to search from), 
a memory-based cache might not be suited. In order to avoid using too much 
disk space, you can set the cache size with the ``--cache-size-limit`` flag
which by default is set to 1 GB.

As an example to see how much disk space you might need to cache the ``txt`` 
conversion of one thousand ebooks, let's say that on average each ``txt`` 
file (what is actually being cached) uses approximately 700 KB which roughly 
corresponds to a file with 350 pages. Thus, you will need a cache size of at 
least 700 MB to be able to store the ``txt`` conversion of one thousand ebooks.

Also `DiskCache`_ has interesting features compared to other file-based 
cache libraries such as being thread-safe and process-safe and supporting 
multiple eviction policies. See `Features`_ for a more complete list.

See `DiskCache Cache Benchmarks`_ for comparaisons to `Memcached`_ and 
`Redis`_.

.. _cache-warning-label:

`:warning:`

  * When enabling the cache with the ``--use-cache`` flag, the script
    ``search-ebooks`` has to cache the converted ebooks (``txt``) if they were not
    already saved in previous runs. Therefore, the speed up of the
    searching will be seen in subsequent executions of the script.
  * Keep in mind that caching has its caveats. For instance if the ebook
    is modified (e.g. tags were added) then the ``search-ebooks`` script has to run 
    ``ebook-meta`` again since the keys in the cache are the MD5 hashes of the ebooks. 
  * There is no problem in the
    cache growing without bounds since its size is set to a maximum of 1 GB by default (check
    the ``--cache-size-limit`` option) and its eviction policy determines what items get to be
    evicted to make space for more items which by default it is the least-recently-stored
    eviction policy (check the ``--eviction-policy`` option).

Tips
====
Use ``--regex`` for regex-based search
--------------------------------------
Use the ``--regex`` flag to perform regex-based search of ebook contents and metadata.
Thus: 

* ``--query "a battle"`` will find any line that **contains** the words 
  "a battle". 
* ``--query "^a battle" --regex`` will find any line that **starts** 
  with the words "a battle" because the ``--regex`` flag considers the 
  search query as a regex.

`:information_source:`

  By default, the ``search-ebooks`` script considers the search queries as 
  non-regex, i.e. it searches for the given query anywhere in the text by
  not processing any regex tokens (e.g. ``$`` or ``^``).
    
`:star:`

  When searching ebook contents and metadata at the same time, note that both
  types of search are linked by **ANDs**. For instance, the following command
  will search for the "reason" string on those ebooks whose filenames start 
  with "The" and whose tags contain "history":
  
  .. code:: bash

     $ search-ebooks ~/ebooks/ --query "reason" --filename "^The" --tags "history" --regex -i --use-cache
    
Search for a string that spans multiple lines
---------------------------------------------
Let's say we want to search for the string "turned into a democracy" in the
following text:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/string_multiple_lines.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/string_multiple_lines.png
   :align: left
   :alt: Find string than can span multiple lines in a text

The difficulty in searching the given string is that sometimes it spans multiple
lines and you want to make the regex as general as possible in matching the string
no matter where the newline(s) happens in the string.

|

If we use the simple search query without tokens 
``"turned into a democracy"``, we will only match the first occurrence
of the given string, as shown in the following `regex101.com demo <https://regex101.com/r/gSmRPc/1>`__:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/simple_query_result.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/simple_query_result.png
   :align: left
   :alt: Result of executing a simple search query without tokens, just the string

|

To match all occurrences of the string no matter how many lines it spans, 
the following regex will do the trick: ``"turned\s+into\s+a\s+democracy"``.
We replaced the space between the words with whitespaces (one or unlimited), as 
shown in the following `regex101.com demo <https://regex101.com/r/cwmfOm/1>`__:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/correct_query_result.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/correct_query_result.png
   :align: left
   :alt: Result of executing a search query where spaces between words are replaced white multiple whitespaces

|

We can now try it out with the ``search-ebooks`` script which will search the
``~/ebooks/`` folder from the `Examples`_:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "turned\s+into\s+a\s+democracy" --regex -i --use-cache
   
**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/output_script.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/output_script.png
   :align: left
   :alt: Output of ``search-ebooks`` script when using the correct search query with appropriate tokens

`:information_source:`

  Only the ebook *Politics_ A Treatise on Government by Aristotle* whose two 
  versions ``epub`` and ``txt`` correspond to the same translation could 
  match the given string "turned into a democracy" which is found in the 
  following part of the ``txt`` version:
  
  .. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/aristotle_politics_section_match_txt.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/aristotle_politics_section_match_txt.png
   :align: left
   :alt: section where the match was found in the book *Politics_ A Treatise on Government by Aristotle.txt*
  
  |
  
  and in the text conversion of the ``epub`` file:
  
  .. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/aristotle_politics_section_match_epub.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tips/aristotle_politics_section_match_epub.png
   :align: left
   :alt: section where the match was found in the book *Politics_ A Treatise on Government by Aristotle.epub*
  
Advanced tip: perform "full word" search with regex
---------------------------------------------------
The ``search-ebooks`` script accepts regular expressions for the search queries
through the ``--regex`` flag.
Thus you can perform specific searches such as a "full word" search (also
called "whole words only" search) or a "starts with" search by making use of 
regex-based search queries.

This is how you would perform some of the important types of search based on 
regular expressions:

+---------------------------+--------------------------------------------------------------+----------------------------------------------+
| Search type               | Regex                                                        | Examples                                     |
+===========================+==============================================================+==============================================+
| "full word" search        | ``\bword\b``: surround the word with the `\\b`_ anchor       | ``--query "\bknowledge\b" --regex``:         |
|                           |                                                              | will match exactly the word "knowledge" thus |
|                           |                                                              | words like "acknowledge" or "knowledgeable"  |
|                           |                                                              | will be rejected                             |
+---------------------------+--------------------------------------------------------------+----------------------------------------------+
| "starts with" search      | ``^string``: add the caret ``^`` before the string           | ``--query "^Th" --regex``:                   |
|                           | to match lines that start with the given string              | will find all lines that start with          |
|                           |                                                              | the characters "Th"                          |
+---------------------------+--------------------------------------------------------------+----------------------------------------------+
| "ends with" search        | ``string$``: add the dollar sign ``$`` at the end of         | ``--query "through the$" --regex``:          |
|                           | the string to match all lines that start with the given      | will find all lines that end with            |
|                           | string                                                       | the words "through the"                      |
+---------------------------+--------------------------------------------------------------+----------------------------------------------+
| "contains pattern" search | * ``string``: a regex without tokens will find the           | * ``--query "^The|disputed.$" --regex``:     |
|                           |   string anywhere in the text even if it is part of a word.  |   will find all lines that                   |
|                           | * ``string1|string2``: searches for the literal text         |   either start with "The" or end             |
|                           |   *string1* or *string2*. The vertical bar is called         |   with "disputed."                           |
|                           |   the `alternation operator`_.                               | * ``--filename "Aristotle|Plato" --regex``:  |
|                           |                                                              |   will select those ebooks whose filenames   |
|                           |                                                              |   contain either "Aristotle" or "Plato"      |
+---------------------------+--------------------------------------------------------------+----------------------------------------------+

`:information_source:`

  The ``--regex`` flag in the examples allow you to perform **regex-based** search 
  of ebook contents and metadata, i.e. the ``search-ebooks`` treats the search 
  queries as regular expressions.

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
  *The Republic by Plato.pdf* which both consist of only two images for 
  testing purposes.

Search ebooks with certain filenames
------------------------------------
We want to search for the word "knowledge" but only for those ebooks whose
filenames contain either "Aristotle" or "Plato" and also we want the search
to be case insensitive (i.e. ignore case):

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bknowledge\b" --filename "Aristotle|Plato" --regex -i --use-cache

`:information_source:`

  * ``--regex`` treats the search query and metadata (e.g. filename) as regex.
  * ``\bknowledge\b`` matches exactly the word "knowledge", i.e. it performs a 
    `“whole words only” search`_. Thus, words like "acknowledge" or "knowledgeable"
    are rejected.
  * The ``-i`` flag ignores case when searching in ebook **contents** and **metadata**.
  * Since we already converted the files to ``txt`` in previous runs,
    we make use of the cache with the ``--use-cache`` flag.

|

**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_filenames_satisfy_pattern.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_filenames_satisfy_pattern.png
   :align: left
   :alt: Output for example: filenames satisfy a given pattern

`:information_source:`

  * The ``txt`` and ``pdf`` versions of *The Ethics of Aristotle by Aristotle*
    show different number of matches because they are not the same translations
    and hence the word "knowledge" might come from the introduction (written by 
    another author) or the translator's footnotes, depending on the version of
    the text.
  * On the other hand, the ``txt`` and ``epub`` versions of *Politics_ A 
    Treatise on Government by Aristotle* show the same number of matches because
    they are both the same translation.
  * As explained previously, *The Republic by Plato.pdf* is not included in
    the matches because it is a file with images only and since
    we didn't use the ``--ocr`` flag, the file couldn't be converted to ``txt``.
    The next example makes use of the ``--ocr`` flag.

Search documents with images 
----------------------------
We will execute the `previous query`_ but this time we will include the
file *The Republic by Plato.pdf* (which contains images) in the search by 
using the ``--ocr`` flag which will convert the images to text with `Tesseract`_:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bknowledge\b" --filename "Aristotle|Plato" --regex -i --use-cache --ocr true

`:information_source:`
 
  * The ``--ocr`` flag allows you to search ``.pdf``, ``.djvu`` and image files but it
    is disabled by default because `OCR`_ is a slow resource-intensive process.
  * The ``--ocr`` flag takes on three values: ``{always,true,false}`` where:
  
    * ``always``: try OCR-ing first the ebook before trying the simple conversion tools
    * ``true``: use OCR for books that failed to be converted to ``txt`` or were 
      converted to empty files by the simple conversion tools
    * ``false``: try the simple conversion tools only. No OCR.
    
    More info in `pyebooktools README`_.

|

**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ocr_images.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ocr_images.png
   :align: left
   :alt: Output for example: OCR PDF file with images

`:information_source:`

  * Since the file *The Republic by Plato.pdf* was not already processed, the cache 
    didn't have its text conversion at the start of the script. But by the end of the
    script, the text conversion was saved in the cache.
  * As you can see from the seach time, OCR is a slow process. Thus, use it wisely!
  
Search ebook metadata
---------------------
Search for the regex "confront|treason" in ebook contents but only for 
those ebooks that have the "drama" **and** "history" tags:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "confront|treason" --tags "^(.*drama)(.*history).*$" --regex -i --use-cache

`:information_source:`

  * The regex for the **AND** operator is a little more complex than an OR-based regex which 
    only uses a vertical bar ``|``. [2]_
  * *calibre*\'s `ebook-meta`_ is used by the ``search-ebooks`` script to get ebook metadata
    such as ``Title`` and ``Tags``. The cache not only save
    the text conversion but also ebook metadata.
  * The ``--tags`` option acts like a filter by only executing the "confront|treason" regex on 
    those ebooks that have at least the two tags "drama" and "history".

|

**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_metadata_with_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_metadata_witth_cache.png
   :align: left
   :alt: Output for example: search ebook metadata

`:information_source:`

  * The results of `ebook-meta`_ were already cached from previous runs of the ``search-ebooks`` script
    by using the ``--use-cache`` flag. Hence, the running time of the script can be speed up not only
    by caching the text conversion of ebooks but also the results of ``ebook-meta``.
  * Here is the output of ``ebook-meta`` when running it on
    *Julius Caesar by William Shakespeare.epub*:
    
    .. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ebook_meta.png
       :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_ebook_meta.png
       :align: left
       :alt: Output of ``ebook-meta``
    
  * All the other 16 ebooks from the `~/ebooks/`_ folder were rejected for
    not satisfying the two regexes (``--query`` and ``--tags``).
  * *Julius Caesar by William Shakespeare.pdf* doesn't have any tag, unlike its ``epub`` counterpart.
  * *Julius Caesar by William Shakespeare.epub* only matches once for the
    word "treason".

|

If we don't cache *calibre*\'s `ebook-meta`_ and the converted files (``txt``), 
the searching time is greater:

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_metadata_without_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/examples/output_metadata_witthout_cache.png
   :align: left
   :alt: Output for example: search ebook metadata without cache
   
`:information_source:`

  See `cache <#cache-warning-label>`_ for important info to know about using the ``--use-cache`` flag.

Roadmap
=======
Starting from first priority tasks:

Short-term
----------
1. |ss| Add examples for searching text content and metadata of ebooks |se|
   
2. Add instructions on how to install the ``searchebooks`` package

3. Add support for `Lucene`_ as a search backend
   
   `PyLucene`_ will be used to access ``Lucene``\'s text indexing and searching
   capabilities from Python

Medium-term
-----------
1. Test on linux
2. Create a `docker`_ image for this project
3. Read also metadata from *calibre*\'s ``metadata.opf`` if found
4. Add tests on `Travis CI`_
5. Eventually add documentation on `Read the Docs`_

Long-term
---------
1. Add support for multiprocessing so you can have multiple ebook files
   being searched in parallel based on the number of cores
2. Implement a GUI, specially to make navigation of search results easier 
   since you can have thousands of matches for a given search query
  
   Though, for the moment not sure which GUI library to choose from 
   (e.g. `Kivy`_, `TkInter`_)

License
=======
This program is licensed under the GNU General Public License v3.0. For more
details see the `LICENSE`_ file in the repository.

References
==========
.. [1] ``txt``, ``html``, ``rtf``, ``rtfd``, ``doc``, ``wordml``, or ``webarchive``. 
       See `<https://ss64.com/osx/textutil.html>`__
.. [2] Regex from `stackoverflow`_ (but without positive lookahead)

.. URLs
.. _\\b: https://www.regular-expressions.info/wordboundaries.html
.. _“whole words only” search: https://www.regular-expressions.info/wordboundaries.html
.. _alternation operator: https://www.regular-expressions.info/alternation.html
.. _calibre: https://calibre-ebook.com/
.. _catdoc: https://www.wagner.pp.ru/~vitus/software/catdoc/
.. _convert_to_txt.py: https://github.com/raul23/pyebooktools/blob/master/pyebooktools/convert_to_txt.py
.. _DiskCache: http://www.grantjenks.com/docs/diskcache/
.. _DiskCache Cache Benchmarks: http://www.grantjenks.com/docs/diskcache/cache-benchmarks.html
.. _DjVuLibre: http://djvu.sourceforge.net/
.. _djvutxt: http://djvu.sourceforge.net/doc/man/djvutxt.html
.. _docker: https://docs.docker.com/
.. _ebook-convert: https://manual.calibre-ebook.com/generated/en/ebook-convert.html
.. _ebook-meta: https://manual.calibre-ebook.com/generated/en/ebook-meta.html
.. _Features: http://www.grantjenks.com/docs/diskcache/index.html#features
.. _Kivy: https://kivy.org/
.. _lib.py: https://github.com/raul23/pyebooktools/blob/master/pyebooktools/lib.py
.. _LICENSE: ./LICENSE
.. _Lucene: https://lucene.apache.org/
.. _Memcached: https://memcached.org/
.. _OCR: https://en.wikipedia.org/wiki/Optical_character_recognition
.. _other related text files: https://ss64.com/osx/textutil.html
.. _pdftotext: https://www.xpdfreader.com/pdftotext-man.html
.. _poppler: https://poppler.freedesktop.org/
.. _pyebooktools: https://github.com/raul23/pyebooktools
.. _pyebooktools README: https://github.com/raul23/pyebooktools#options-for-ocr
.. _PyLucene: https://lucene.apache.org/pylucene/
.. _re: https://docs.python.org/3/library/re.html
.. _Read the Docs: https://readthedocs.org/
.. _Redis: https://redis.io/
.. _stackoverflow: https://stackoverflow.com/a/37692545/14664104
.. _Tesseract: https://github.com/tesseract-ocr/tesseract
.. _textutil: https://ss64.com/osx/textutil.html
.. _TkInter: https://wiki.python.org/moin/TkInter
.. _Travis CI: https://travis-ci.com/
.. _unzip: https://linux.die.net/man/1/unzip
.. _zipgrep: https://linux.die.net/man/1/zipgrep

.. Local URLs
.. _~/ebooks/: #examples
.. _cache: #cache
.. _examples: #examples
.. _previous query: #search-ebooks-whose-filenames-satisfy-a-given-pattern
.. _search-ebooks: ./searchebooks/scripts/search-ebooks

.. |ss| raw:: html

   <strike>

.. |se| raw:: html

   </strike>
