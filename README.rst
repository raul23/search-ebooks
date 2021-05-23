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

Results
=======
Summary of results
------------------
Search through text content of PDF ebooksfor the query ``\bhold\b``

+-----------------------------+----------------+
|             Case            | Time (seconds) |
+=============================+================+
| ``pdftotext`` with cache    | 1.146          |
+-----------------------------+----------------+
| ``pdftotext`` without cache | 5.389          |
+-----------------------------+----------------+

Searching content of PDF files with ``pdftotext``
-------------------------------------------------
With cache
^^^^^^^^^^
Without cache
^^^^^^^^^^^^^
Searching content of PDF files with calibre's ``ebook-convert``
---------------------------------------------------------------

Examples
========
