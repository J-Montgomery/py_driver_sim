import os
import re

class Matcher:
    def __init__(self):
        # This regex captures everything between two non-capturing groups
        # e.g. /* MACRO_BEGIN */ code... /* MACRO_END */
        base_regex = r"(?:\/\*\s*{0}_BEGIN\s*\*\/)([\S\s]*?)(?:\/\*\s*{0}_END\s*\*\/)"
        self.include_matcher = re.compile(base_regex.format("INCLUDE"))
        self.macro_matcher = re.compile(base_regex.format("MACRO"))
        self.struct_matcher = re.compile(base_regex.format("STRUCT"))
        self.enum_matcher = re.compile(base_regex.format("ENUM"))
        self.prototype_matcher = re.compile(base_regex.format("PROTOTYPE"))

    def get_includes(self, text):
        m = self.include_matcher.findall(text)
        return m

    def get_macros(self, text):
        m = self.macro_matcher.findall(text)
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

def get_files(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.join(dirpath, f)

def parse_headers(path):
    print("\n\n\n-------------------------------------------")

    headers = list(get_files(path))
    matcher = Matcher()

    for file in headers:
        print(f"Matching {file}")
        with open(file) as f:
            data = f.read()
            test = matcher.get_includes(data)
            includes = "\n".join(matcher.get_includes(data))
            macros = "\n".join(matcher.get_macros(data))
            structs = "\n".join(matcher.get_structs(data))
            prototypes = "\n".join(matcher.get_prototypes(data))
            print(f"Includes:\n{str(includes)}\nmacros:\n{macros}\nstructs:\n{structs}\nprototypes:\n{prototypes}\n")

    print("-------------------------------------------\n\n\n")
