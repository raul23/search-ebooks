import re
import shlex
import subprocess
import time
from pathlib import Path

from pyebooktools.convert_to_txt import convert
from searchebooks.configs import default_config as default_cfg
from pyebooktools.lib import (BLUE, NC, VIOLET, YELLOW)


class SearchEbooks:
    def __init__(self):
        self.input_data = None
        self.cache_size_limit = default_cfg.cache_size_limit
        self.ebook_formats = default_cfg.ebook_formats
        self.epub_search_method = default_cfg.epub_search_method
        self.ignore_case = default_cfg.ignore_case
        self.search_query = default_cfg.search_query
        # TODO: urgent, add ocr options

    def _search_file(self, file_path):
        # num_matches = 0
        # window_length = 200
        ext = file_path.suffix.split('.')[-1]
        if ext not in self.ebook_formats:
            return 1
        flags = re.MULTILINE | re.IGNORECASE if self.ignore_case else re.MULTILINE
        search_result = {'filename': file_path.name,
                         'folder_path': file_path.parent, 'file_path': file_path,
                         'matches': []}
        if ext == 'epub' and self.epub_search_method == 'zipgrep':
            zipgrep = 'zipgrep -i' if self.ignore_case else 'zipgrep'
            cmd = f'find "{file_path}" -exec {zipgrep} {self.search_query} {{}} \\;'
            cmd_args = shlex.split(cmd)
            result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        text = convert(file_path, **self.__dict__)
        if text == 1:
            return 1
        matches = re.findall(self.search_query, text, flags)
        search_result['matches'] = len(matches)
        # TODO: important, uncomment for interactive
        """
        matches = re.finditer(args.search_query, text, flags)
        for match in matches:
            num_matches += 1
            start, end = match.span()
            length = end - start
            if start < window_length / 2:
                subtext = text[start - 0:int(start + length + window_length / 2)]
            else:
                subtext = text[int(start - window_length / 2):int(start + length + window_length / 2)]
            subtext = re.sub(f"({args.search_query})", f"{GREEN}{BOLD}\\1{NC}",
                             subtext, flags=flags)
            # TODO: important, use trans
            subtext = subtext.replace('\n', ' ').replace('\x0cix', '').strip()
            search_result['matches'].append(subtext)
        search_result['matches'] = num_matches
        """
        return search_result

    def search(self, input_data, **kwargs):

        def process_result(start_t, num_res, total_secs):
            if search_result != 1:
                search_results.append(search_result)
                # num_res += len(search_result['matches'])
                num_res += search_result['matches']
            total_secs += time.time() - start_t
            return num_res, total_secs

        # TODO: add debug message about update attributes
        self.__dict__.update(kwargs)
        input_data = Path(input_data)
        self.input_data = input_data
        search_results = []
        num_results = 0
        total_seconds = 0

        if self.input_data.is_file():
            start_time = time.time()
            search_result = self._search_file(input_data)
            num_results, total_seconds = process_result(start_time, num_results,
                                                        total_seconds)
        else:
            for fp in input_data.rglob('*'):
                print(fp)
                start_time = time.time()
                search_result = self._search_file(fp)
                num_results, total_seconds = process_result(start_time, num_results,
                                                            total_seconds)
            # search_results = sorted(search_results, key=lambda k: len(k['matches']),
            #                         reverse=True)
            search_results = sorted(search_results, key=lambda k: k['matches'],
                                    reverse=True)

        print(f'{YELLOW}Total of {num_results} matches ({round(total_seconds, 3)} '
              f'seconds){NC}\n')
        for i, result in enumerate(search_results, start=1):
            print(f"{i}.\t{BLUE}{result['filename']}{NC}"
                  f"\n\t{VIOLET}Folder path:{NC} {result['folder_path']}"
                  f"\n\t{VIOLET}Number of matches:{NC} {result['matches']}\n")
        # f"\n\t{VIOLET}Number of matches:{NC} {len(result['matches'])}\n")
        return 0


searcher = SearchEbooks()
