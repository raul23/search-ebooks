import os


# ==================
# 1. General options
# ==================
input_data = None

# 1.1 General control flags
# =========================
quiet = False
verbose = False
regex = False
ignore_case = False

# 1.2 Miscellaneous options
# =========================
ocr_enabled = 'false'
logging_level = 'info'
logging_formatter = 'only_msg'

# ===============
# 2. Edit options
# ===============
edit = False
app = None
reset = False
cfg = 'main'

# ================
# 3. Cache options
# ================
use_cache = True
cache_folder = os.path.expanduser('~/.searchebooks')
eviction_policy = 'least-recently-stored'
# In gigabytes (GB)
cache_size_limit = 1
clear_cache = False

# ==========================
# 4. Fulltext search options
# ==========================
# Use raw string (r'string') for search query to be able to use regex anchors like \b
query = r''
ebook_formats = ['djvu', 'epub', 'html', 'pdf', 'txt']
djvu_search_method = 'djvutxt'
msword_search_method = 'textutil'
epub_search_method = 'calibre'
pdf_search_method = 'pdftotext'
text_regex = False
text_ignore_case = False

# ==========================
# 5. Metadata search options
# ==========================
# IMPORTANT:
# - the metadata fields and the fulltext search query are linked with ANDs
#   between each other,
#   EXAMPLE: if query = 'science' and title = 'physics', then all ebooks with
#   'science' in their content AND 'physics' in their title will be returned
#
# - Use raw string (r'string') for any metadata to be able to use regex anchors
#   like \b, e.g. title = r'\bMathematics\b'
#
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
metadata_regex = False
metadata_ignore_case = False
