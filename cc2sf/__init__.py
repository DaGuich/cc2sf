import re
import struct


class CStruct:
    types = {'char': 'c',
             'byte': 'c',
             'signed char': 'b',
             'unsigned char': 'B',
             '_Bool': '?',
             'short': 'h',
             'unsigned short': 'H',
             'int': 'i',
             'unsigned int': 'I',
             'long': 'l',
             'unsigned long': 'L',
             'long long': 'q',
             'unsigned long long': 'Q',
             'ssize_t': 'n',
             'size_t': 'N',
             'float': 'f',
             'double': 'd',
             'char[]': 's',
             'void *': 'P'}

    def __init__(self, file):
        self.__file_content = None
        self.__definitions = dict()
        self.__structs = dict()

        with open(file, 'r') as f:
            self.__file_content = f.readlines()
        self.__file_content = self.__parse(self.__file_content)
        del self.__file_content

        for def_name in self.__definitions:
            self.__structs[def_name] = None

        for name, definitions in self.__definitions.items():
            self.__structs[name] = list()
            for definition in definitions:
                self.__structs[name].append(definition[0])
                if definition[0] in self.types:
                    self.__structs[name][-1] = self.types[definition[0]]
                elif definition[0] in self.__definitions:
                    pass
                self.__structs[name][-1] = (int(definition[2]),
                                            self.__structs[name][-1])

        for name, definitions in self.__structs.items():
            all_good = True
            for count, definition in definitions:
                if definition not in self.types.values():
                    all_good = False
                    break
            if all_good:
                format_str = ''.join([c * s for c, s in definitions])
                self.__structs[name] = struct.Struct(format_str)

        for name, definitions in self.__structs.items():
            if isinstance(definitions, struct.Struct):
                continue

            format_str = ''
            for count, definition in definitions:
                if definition in self.__structs and \
                   isinstance(self.__structs[definition], struct.Struct):
                    format_str += count * '{}s'.format(self.__structs[definition].size)
                elif definition in self.types.values():
                    format_str += count * definition
            self.__structs[name] = struct.Struct(format_str)

    def unpack(self, buffer):
        pass

    def pack(self, *vals):
        pass

    @staticmethod
    def __remove_comments(content):
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*\*/', '', content)
        return content

    def __parse(self, content):
        parse_struct_r = r'(?P<typedef>typedef)?\s?(?P<s_name>(?:struct)\s' \
                         r'\S+)\s*\{\s*(?P<content>.+?)\s*\}\s*(?P<name>\S+?)?;'
        parse_data = re.compile(r'(?P<type>\S+)\s*(?P<name>\S+?)(?:\[(?P<count>\d+)\])?;')

        for i, line in enumerate(content):
            content[i] = self.__remove_comments(line)
            content[i] = content[i].strip()

        content = ' '.join(content)

        for x in re.finditer(parse_struct_r, content):
            name = x.group('name')
            if name is None:
                name = x.group('s_name')
            self.__definitions[name] = list()
            groupdict = x.groupdict()

            for c in parse_data.finditer(groupdict['content']):
                count = 1
                if c['count'] is not None:
                    count = c['count']
                self.__definitions[name].append((c['type'],
                                                 c['name'],
                                                 count))
        return content
