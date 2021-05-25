import os


# ==================
# 1. General options
# ==================

# 1.1 General control flags
# =========================
quiet = False
verbose = False
ignore_case = False

# 1.2 Options for OCR
# ===================
ocr_enabled = 'false'
ocr_only_first_last_pages = (7, 3)
ocr_command = 'tesseract_wrapper'

# 1.3 Miscellaneous options
# =========================
logging_level = 'info'
logging_formatter = 'only_msg'
# Reverse sort
reverse = False

# ================
# 2. Cache options
# ================
use_cache = False
cache_folder = os.path.expanduser('~/.searchebooks')
eviction_policy = 'least-recently-stored'
# In gigabytes (GB)
cache_size_limit = 1
clear_cache = False

# =================
# 3. Search options
# =================
search_query = None
ebook_formats = ['djvu', 'epub', 'html', 'pdf', 'txt']
djvu_search_method = 'djvutxt'
msword_search_method = 'textutil'
epub_search_method = 'zipgrep'
pdf_search_method = 'pdftotext'

# ==========================
# 4. Advanced search options
# ==========================
authors = None
book_producer = None
category = None
comments = None
# date = None
filename = None
identifiers = None
isbn = None
language = None
published = None
publisher = None
rating = None
series = None
tags = None
title = None
