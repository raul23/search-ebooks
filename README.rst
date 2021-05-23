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

Tests
=====
Search through the content of eight PDF files for the word **hold**
which is accomplished with the regex ``\bhold\b``. Thus for
example, we want *hold* but not *holdings*.

Searching content of PDF files with ``pdftotext``
-------------------------------------------------
We will use the ``pdftotext`` utility to convert PDF files to ``txt`` in order
to search through content for a given pattern.

By default, the ``seach-ebooks`` script uses ``pdftotext`` since it is way
faster than *calibre*\'s ``ebook-convert`` to convert files to ``txt``.

The ``pdftotext``'s results are given for two cases: with and without cache.
Cache is used to save the converted PDF files into ``txt`` so that we avoid
re-converting PDF files which is a very time consuming process, specially if
it is a huge document. 

Summary of results
^^^^^^^^^^^^^^^^^^
Using cache, we are able to decrease the search time by **4.7**

+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | 1.146          |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

With cache
^^^^^^^^^^
This is the command which makes use of cache:

.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --use-cache
   
**Output:** ``pdftotext`` and with cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Without cache
^^^^^^^^^^^^^
.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf
   
**Output:** ``pdftotext`` and without cache

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_without_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------

Examples
========
