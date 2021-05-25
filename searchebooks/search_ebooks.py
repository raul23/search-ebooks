import re
import shlex
import subprocess
import time
from pathlib import Path

from pyebooktools.convert_to_txt import convert
from searchebooks.configs import default_config as default_cfg
from pyebooktools.lib import (
    BLUE, BOLD, GREEN, NC, VIOLET, YELLOW, get_ebook_metadata, get_hash)
from pyebooktools.utils.logutils import init_log

logger = init_log(__name__, __file__)


class SearchEbooks:
    def __init__(self):
        self.cache = None
        self.input_data = None
        self.djvu_search_method = default_cfg.djvu_search_method
        self.ebook_formats = default_cfg.ebook_formats
        self.eviction_policy = default_cfg.eviction_policy
        self.epub_search_method = default_cfg.epub_search_method
        self.ignore_case = default_cfg.ignore_case
        self.msword_search_method = default_cfg.msword_search_method
        self.ocr_enabled = default_cfg.ocr_enabled
        self.ocr_only_first_last_pages = default_cfg.ocr_only_first_last_pages
        self.ocr_command = default_cfg.ocr_command
        self.pdf_search_method = default_cfg.pdf_search_method
        # TODO: important, include reverse?
        self.reverse = default_cfg.reverse
        self.search_query = default_cfg.search_query
        self.use_cache = default_cfg.use_cache
        # ========
        # Metadata
        # ========
        self.metadata_to_check = []
        self.authors = default_cfg.authors
        self.book_producer = default_cfg.book_producer
        self.category = default_cfg.category
        self.comments = default_cfg.comments
        # self.date = default_cfg.date
        self.identifiers = default_cfg.identifiers
        self.isbn = default_cfg.isbn
        self.language = default_cfg.language
        self.publisher = default_cfg.publisher
        self.rating = default_cfg.rating
        self.series = default_cfg.series
        self.tags = default_cfg.tags
        self.title = default_cfg.title
        # 'date',
        self.metadata = ['authors', 'book_producer', 'category', 'comments',
                         'identifiers', 'isbn', 'language', 'published',
                         'publisher', 'rating', 'series', 'tags','title']
        self.filename = default_cfg.filename

    def _search_file_txt_content(self, file_path):
        # num_matches = 0
        # window_length = 200
        ext = file_path.suffix.split('.')[-1]
        # TODO: flags as attribute? (other places)
        flags = re.MULTILINE | re.IGNORECASE if self.ignore_case else re.MULTILINE
        search_result = {'filename': file_path.name,
                         'folder_path': file_path.parent,
                         'file_path': file_path,
                         'matches': 0}
        text = None
        if self.use_cache:
            hash = get_hash(file_path)
            cache_result = self.cache.get(hash)
            if cache_result is None:
                logger.debug('Text conversion was not found in cache')
            elif cache_result and cache_result[0] is not None:
                logger.debug('Text conversion was found in cache!')
                text = cache_result[0]
        if not text and ext == 'epub' and self.epub_search_method == 'zipgrep':
            zipgrep = 'zipgrep -i' if self.ignore_case else 'zipgrep'
            cmd = f'{zipgrep} {self.search_query} "{file_path}"'
            cmd_args = shlex.split(cmd)
            result = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if result.stderr:
                return 1
            else:
                text = result.stdout.decode()
                # TODO: important, explain remove lines with content.opf
                lines = [l for l in text.splitlines() if not l.count('content.opf')]
                text = '\n'.join(lines)
                matches = re.findall(self.search_query, text, flags)
                # TODO: important, uncomment for interactive
                # text = re.sub(f"({args.search_query})", f"{GREEN}{BOLD}\\1{NC}", text, flags=flags)
                search_result['matches'] = len(matches)
                return search_result
        if not text:
            text = convert(file_path,
                           djvu_convert_method=self.djvu_search_method,
                           msword_convert_method=self.msword_search_method,
                           pdf_convert_method=self.pdf_search_method,
                           **self.__dict__)
        if text == 1:
            return 1
        matches = re.findall(self.search_query, text, flags)
        search_result['matches'] = len(matches)
        # TODO: important, uncomment for interactive
        """
        import ipdb
        ipdb.set_trace()
        matches = re.finditer(self.search_query, text, flags)
        for match in matches:
            num_matches += 1
            start, end = match.span()
            length = end - start
            if start < window_length / 2:
                subtext = text[start - 0:int(start + length + window_length / 2)]
            else:
                subtext = text[int(start - window_length / 2):int(start + length + window_length / 2)]
            subtext = re.sub(f"({self.search_query})", f"{GREEN}{BOLD}\\1{NC}",
                             subtext, flags=flags)
            # TODO: important, use trans
            subtext = subtext.replace('\n', ' ').replace('\x0c', '').strip()
            ipdb.set_trace()
            # search_result['matches'].append(subtext)
        # search_result['matches'] = num_matches
        ipdb.set_trace()
        """
        return search_result

    def _search_file_metadata(self, file_path):
        flags = re.MULTILINE | re.IGNORECASE if self.ignore_case else re.MULTILINE
        if self.metadata_to_check:
            ebookmeta = get_ebook_metadata(file_path)
            if ebookmeta.stdout:
                for line in ebookmeta.stdout.splitlines():
                    field_name = line.split(':')[0].strip()
                    # TODO: important, use translate for 3 replace
                    field_name = field_name.lower().replace(' ', '_')
                    field_name = field_name.replace('(', '').replace(')', '')
                    if field_name not in self.metadata_to_check:
                        continue
                    # TODO: add try except block
                    pattern_field_value = self.__getattribute__(field_name)
                    if pattern_field_value:
                        field_value = line.split(':')[-1].strip()
                        match = re.search(pattern_field_value, field_value, flags)
                        if not match:
                            return 1
        # Filename not returned by ebookmeta
        if self.filename:
            match = re.search(self.filename, file_path.name, flags)
            if not match:
                return 1
        return 0

    def _search_file(self, file_path):
        # assert self.search_query
        if file_path.suffix.split('.')[-1] not in self.ebook_formats:
            return 1
        search_metadata_result = self._search_file_metadata(file_path)
        if search_metadata_result == 0:
            if not self.search_query:
                search_result = {'filename': file_path.name,
                                 'folder_path': file_path.parent,
                                 'file_path': file_path,
                                 'matches': 1}
                return search_result
            return self._search_file_txt_content(file_path)
        else:
            return 1

    def _check_metadata(self):
        for field_name in self.metadata:
            if self.__getattribute__(field_name):
                self.metadata_to_check.append(field_name)

    def search(self, input_data, cache=None, **kwargs):

        def process_result(start_t, num_res, total_secs):
            if search_result != 1:
                search_results.append(search_result)
                # num_res += len(search_result['matches'])
                num_res += search_result['matches']
            total_secs += time.time() - start_t
            return num_res, total_secs

        # TODO: add debug message about update attributes
        self.cache = cache
        self.__dict__.update(kwargs)
        self._check_metadata()
        input_data = Path(input_data)
        self.input_data = input_data
        search_results = []
        num_results = 0
        total_seconds = 0

        if self.input_data.is_file():
            start_time = time.time()
            search_result = self._search_file(input_data)
            num_results, total_seconds = process_result(
                start_time, num_results, total_seconds)
        else:
            for fp in input_data.rglob('*'):
                # print(fp)
                start_time = time.time()
                search_result = self._search_file(fp)
                num_results, total_seconds = process_result(
                    start_time, num_results, total_seconds)
            # search_results = sorted(search_results, key=lambda k: len(k['matches']),
            #                         reverse=True)
            if self.search_query:
                search_results = sorted(search_results, key=lambda k: k['matches'],
                                        reverse=True)
            else:
                search_results = sorted(search_results, key=lambda k: k['filename'])

        print(f'{YELLOW}Total of {num_results} matches '
              f'({round(total_seconds, 3)} seconds){NC}\n')
        for i, result in enumerate(search_results, start=1):
            msg = f"\n\t{VIOLET}Number of matches:{NC} {result['matches']}\n"
            msg = msg if self.search_query else "\n"
            print(f"{i}.\t{BLUE}{result['filename']}{NC}"
                  # f"\n\t{VIOLET}Folder path:{NC} {result['folder_path']}"
                  f"\n\t{VIOLET}Folder path:{NC} /Users/test/ebooks" + msg)
        # f"\n\t{VIOLET}Number of matches:{NC} {len(result['matches'])}\n")
        return 0


searcher = SearchEbooks()
