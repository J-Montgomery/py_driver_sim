from dis import pretty_flags
import os
import re
import networkx as nx

class Matcher:
    def __init__(self):
        # This regex captures everything between two non-capturing groups
        # e.g. /* MACRO_BEGIN */ code... /* MACRO_END */
        base_regex = r"(?:\/\*\s*{0}_BEGIN\s*\*\/)([\S\s]*?)(?:\/\*\s*{0}_END\s*\*\/)"
        self.include_matcher = re.compile(base_regex.format("INCLUDE"))
        self.macro_value_matcher = re.compile(base_regex.format("MACRO_VALUE"))
        self.macro_func_matcher = re.compile(base_regex.format("MACRO_FUNC"))
        self.struct_matcher = re.compile(base_regex.format("STRUCT"))
        self.enum_matcher = re.compile(base_regex.format("ENUM"))
        self.prototype_matcher = re.compile(base_regex.format("PROTOTYPE"))
        self.code_matcher = re.compile(base_regex.format("CODE"))

    def get_includes(self, text):
        m = self.include_matcher.findall(text)
        return m

    def get_macro_vals(self, text):
        m = self.macro_value_matcher.findall(text)
        return m

    def get_macro_funcs(self, text):
        m = self.macro_func_matcher.findall(text)
        return m

    def get_structs(self, text):
        m = self.struct_matcher.findall(text)
        return m

    def get_enums(self, text):
        m = self.enum_matcher.findall(text)
        if not len(m):
            return None
        else:
            return m

    def get_prototypes(self, text):
        m = self.prototype_matcher.findall(text)
        return m

    def get_code(self, text):
        m = self.code_matcher.findall(text)
        return m


def get_files(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.join(dirpath, f)

def get_referred_path(is_local, path, filepath, rootpath):
    search_paths = []

    if is_local:
        dir = os.path.dirname(filepath)
        search_paths.append(os.path.join(dir, path))
    search_paths.append(os.path.join(rootpath, path))

    for potential_path in search_paths:
        fullpath = os.path.abspath(potential_path)
        if os.path.exists(fullpath):
            return fullpath
    return None


def parse_includes(inc_list, filepath, rootpath):
    # Takes a list of lines containing includes
    re_include = re.compile(r"(?:#\s*include\s*)([<|\"])(.+)([>|\"])")
    found_headers = []
    for line in inc_list:
        referred = None
        m = re_include.search(line)
        if m:
            if m.group(1) == "\"":
                referred = get_referred_path(True, m.group(2), filepath, rootpath)
            else:
                referred = get_referred_path(False, m.group(2), filepath, rootpath)
        if referred is not None:
            found_headers.append(referred)

    return found_headers

def parse(root):
    print("\n-------------------------------------------")

    headers = [os.path.abspath(x) for x in get_files(root)]

    matcher = Matcher()
    file_graph = nx.DiGraph()

    for file in headers:
        print(f"Searching {file}")
        with open(file) as f:
            data = f.read()
            includes = "\n".join(matcher.get_includes(data))
            edges = parse_includes(includes.splitlines(), file, root)
            if edges == []:
                file_graph.add_node(file)
            for edge in edges:
                file_graph.add_edge(edge, file)
                if edge not in headers:
                    headers.append(edge)

    headers = list(nx.topological_sort(file_graph))
    macro_vals = []
    macro_funcs = []
    structs = []
    prototypes = []
    code = []
    for file in headers:
        with open(file) as f:
            data = f.read()
            macro_vals.append("\n".join(matcher.get_macro_vals(data)))
            macro_funcs.append("\n".join(matcher.get_macro_funcs(data)))
            structs.append("\n".join(matcher.get_structs(data)))
            prototypes.append("\n".join(matcher.get_prototypes(data)))
            code.append("\n".join(matcher.get_code(data)))
    print("-------------------------------------------\n")
    return (macro_vals, macro_funcs, structs, prototypes, code)
