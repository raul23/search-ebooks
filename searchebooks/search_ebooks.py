import time

from pyebooktools.configs import default_config


class SearchEbooks:
    def __init__(self):
        self.input_data = None
        self.cache_size_limit = default_config.cache_size_limit

    def _search_file(self, file_path):
        num_matches = 0
        window_length = 200
        ext = file_path.suffix.split('.')[-1]
        if ext not in args.ebook_formats:
            return 1
        flags = re.MULTILINE | re.IGNORECASE if args.ignore_case else re.MULTILINE
        search_result = {'filename': file_path.name, 'folder_path': file_path.parent,
                         'file_path': file_path, 'matches': []}
        if ext == 'epub' and args.epub_search_method == 'zipgrep':
            zipgrep = 'zipgrep -i' if args.ignore_case else 'zipgrep'
            cmd = f'find "{file_path}" -exec {zipgrep} {args.search_query} {{}} \\;'
            cmd_args = shlex.split(cmd)
            result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                return 1
            else:
                text = result.stdout.decode()
                # TODO: important, explain remove lines with content.opf
                lines = [l for l in text.splitlines() if not l.count('content.opf')]
                text = '\n'.join(lines)
                matches = re.findall(args.search_query, text, flags)
                # TODO: important, uncomment for interactive
                # text = re.sub(f"({args.search_query})", f"{GREEN}{BOLD}\\1{NC}", text, flags=flags)
                search_result['matches'] = len(matches)
                return search_result
        text = convert(file_path, **args.__dict__)
        if text == 1:
            return 1
        matches = re.findall(args.search_query, text, flags)
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
        # TODO: add debug message about update attributes
        self.__dict__.update(kwargs)
        self.input_data = input_data
        if self.input_data.is_file():
            start_time = time.time()
            search_result = process_file(input_data, args)
            num_results, total_seconds = process_result(start_time, num_results,
                                                        total_seconds)
        else:
            for fp in input_data.rglob('*'):
                print(fp)
                start_time = time.time()
                search_result = process_file(fp, args)
                num_results, total_seconds = process_result(start_time, num_results,
                                                            total_seconds)
            # search_results = sorted(search_results, key=lambda k: len(k['matches']),
            #                         reverse=True)
            search_results = sorted(search_results, key=lambda k: k['matches'],
                                    reverse=True)


searcher = SearchEbooks()
