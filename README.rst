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
Search through content of 8 PDF ebooks for the word *hold*
which is accomplished with the regex ``\bhold\b``. Thus for
examples, we want *hold* but not *holdings*.

Searching content of PDF files with ``pdftotext``
-------------------------------------------------
Summary of results
^^^^^^^^^^^^^^^^^^
+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | 1.146          |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

With cache
^^^^^^^^^^
.. code:: bash

   $ search-ebooks ~/ebooks/ --query "\bhold\b" -f pdf --use-cache
   
**Output:**

.. image:: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :target: https://raw.githubusercontent.com/raul23/images/master/search-ebooks/readme/tests/pdftotext_with_cache.png
   :align: left
   :alt: ``pdftotext`` with cache

Without cache
^^^^^^^^^^^^^
Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------

Examples
========
