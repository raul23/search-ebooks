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
   :depth: 3
   :local:
   :backlinks: top

Tests
=====
Searching content of PDF files with ``pdftotext``
-------------------------------------------------
Summary of results
^^^^^^^^^^^^^^^^^^
Search through content of 8 PDF ebooks for the word *hold*
which is accomplished with the regex ``\bhold\b``

+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | 1.146          |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

With cache
^^^^^^^^^^
Without cache
^^^^^^^^^^^^^
Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------

Examples
========
