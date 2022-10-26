from typing import Any, Dict, List, Optional
from tokens import Token, OpenTag, CloseTag, TagValue
import yaml


class YamlParser:
    IDENT_OFFSET = 4

    def __init__(self) -> None:
        self.content: List[Token]
        self.wrapping_tags: Dict[int, str]
        self.type_tag: str
        self.list_tag: str
        self._init_values()

    def _init_values(self):
        """Init inner values for parsing"""

        self.content = []
        self.wrapping_tags = {}
        self.type_tag = ''
        self.list_tag = ''

    def close(self, line: str, next_line: str, line_idents: int) -> None:
        """Add closing wrapping tags to content

        Args:
            line (str): Parsed line
            next_line (str): Next line
            line_idents (int): Idents size for next line
        """

        max_ident = max(self.wrapping_tags.keys())
        for i in range(max_ident, line_idents - self.IDENT_OFFSET, -2):
            if i in self.wrapping_tags:
                tag = self.wrapping_tags.pop(i)
                self.content.append(CloseTag(tag, line_idents))

        if self.is_instance_begin(next_line) and (line_idents - self.IDENT_OFFSET in self.wrapping_tags):
            tag = self.wrapping_tags.get(line_idents - self.IDENT_OFFSET, '')
            self.content.append(CloseTag(tag, line_idents - self.IDENT_OFFSET))

    def parse_text(self, yml_text: str) -> List[Token]:
        """Parse yaml

        Args:
            yml_text (str): text in yaml format

        Returns:
            List[Token]: ParsedTokens
        """

        # filter text lines
        lines = [line for line in yml_text.split('\n')]
        lines = [line for line in lines if line.strip()]
        lines += ['']

        for i in range(len(lines) - 1):
            line, line_idents = self.get_line_and_idents(lines[i])
            next_line, next_idents = self.get_line_and_idents(lines[i + 1])

            if self.is_list_tag(line, next_line):
                tag, value = self.get_tag_and_value(line)
                self.list_tag = tag
                self.content.append(OpenTag(tag, line_idents))
                self.wrapping_tags[line_idents] = tag

            elif self.is_type_tag(line, next_line):
                tag, value = self.get_tag_and_value(line)
                self.wrapping_tags[line_idents] = tag

            elif self.is_wrap_tag(line):
                tag, value = self.get_tag_and_value(line)
                self.content.append(OpenTag(tag, line_idents))
                self.wrapping_tags[line_idents] = tag

            elif self.is_list_item(line):
                tag, value = self.get_tag_and_value(line)
                item_tag = self.list_tag[:-1]
                self.content.append(TagValue(item_tag, tag, line_idents))

            elif self.is_instance_begin(line):
                type_tag = self.wrapping_tags[line_idents - self.IDENT_OFFSET]
                self.content.append(
                    OpenTag(type_tag, line_idents - self.IDENT_OFFSET))
                if self.is_attr(line):
                    tag, value = self.get_tag_and_value(line)
                    self.content.append(
                        TagValue(tag, value, line_idents + self.IDENT_OFFSET // 2))

            elif self.is_attr(line):
                tag, value = self.get_tag_and_value(line)
                self.content.append(TagValue(tag, value, line_idents))

            else:
                raise Exception(f'Parsing error at line "{line}"')

            if self.is_wrap_end(line, line_idents, next_idents):
                self.close(line, next_line, next_idents)

        content = self.content.copy()
        self._init_values()
        return content

    def parse_yamllib_data(self, data: Dict[str, Any]) -> List[Token]:
        """Convert output of yaml.load to list of tokens

        Args:
            data (Dict[str, Any]): Output of yaml lib

        Returns:
            List[Token]: Parsed token
        """

        self._parse_node('', data)
        content = self.content.copy()
        return content

    def _parse_node(self, key: str, value: Any):
        """Recursive parse yaml data

        Args:
            key (str): Node key
            value (Any): Node entries
        """

        if isinstance(value, dict):
            if key:
                self.content.append(OpenTag(tag=key))

            for node_key, node_value in value.items():
                self._parse_node(node_key, node_value)

            if key:
                self.content.append(CloseTag(tag=key))

        elif isinstance(value, list):
            if isinstance(value[0], str):
                self.content.append(OpenTag(tag=key))
                for item in value:
                    self._parse_node(key[:-1], item)

                self.content.append(CloseTag(tag=key))
            else:
                for item in value:
                    self._parse_node(key, item)

        elif isinstance(value, str):
            self.content.append(TagValue(tag=key, value=value))

    @classmethod
    def get_tag_and_value(cls, line: str) -> tuple[str, str]:
        """Get tag and value from line

        Args:
            line (str): Parsed line

        Returns:
            tuple[str, str]: Tag and value
        """

        line = line.rstrip('}').rstrip(',')
        if ':' in line:
            tag, *value = line.split(':')
            if tag.startswith('-'):
                tag = tag.lstrip('-').strip()

            value = ':'.join(value).strip().strip('"')
        else:
            tag = line.strip()
            value = ''

        return tag, value

    @classmethod
    def get_line_and_idents(cls, line: str) -> tuple[str, int]:
        """Get size of line ident and cleaned line

        Args:
            line (str): Parsed line

        Returns:
            tuple[str, int]: Line and ident size
        """

        idents = len(line) - len(line.lstrip())
        line = line.strip()
        return line, idents

    @classmethod
    def is_list_item(cls, line: str) -> bool:
        """Chick if line is list item

        Args:
            line (str): Parsed line

        Returns:
            bool: True if list item
        """

        return line.lstrip().startswith('-') and ':' not in line and line.lstrip('-').strip() != ''

    @classmethod
    def is_attr(cls, line: str) -> bool:
        """Check if line is attribute with value

        Args:
            line (str): Parsed line
        Returns:
            bool: True if attr
        """

        items = line.split(':')
        return len(items) > 1 and items[1] != ''

    @classmethod
    def is_instance_begin(cls, line: str) -> bool:
        """Check if line is beginning of type instance

        Args:
            line (str): Parsed line

        Returns:
            bool: True if line is instance begin
        """

        s1 = line.startswith('- {')
        s2 = (line.strip().startswith('-')
              and ((':' in line) or line.lstrip('-').strip() == ''))
        return s1 or s2

    @classmethod
    def is_wrap_tag(cls, line: str) -> bool:
        """Check if tag is wrapping tag

        Args:
            line (str): Parsed line 
            next_line (str): Next line 

        Returns:
            bool: True if wrapping tag
        """

        return line.endswith(':')

    @classmethod
    def is_wrap_end(cls, line: str, line_idents: int, next_idents: int) -> bool:
        """Check if line is end of wrapping tag

        Args:
            line (str): Parsed line
            line_idents (int): Size of line ident
            next_idents (int): Size of next line ident

        Returns:
            bool: True if wrap end
        """

        return (
            (line_idents > next_idents) or
            (line_idents == next_idents and cls.is_instance_begin(line))
        )

    @classmethod
    def is_type_tag(cls, line: str, next_line: str) -> bool:
        """Check if line is type tag

        Args:
            line (str): Parsed line 
            next_line (str): Next line 

        Returns:
            bool: True if type tag
        """

        return cls.is_wrap_tag(line) and cls.is_instance_begin(next_line)

    @classmethod
    def is_list_tag(cls, line: str, next_line: str) -> bool:
        """Check if line is start of list

        Args:
            line (str): Parsed line
            next_line (str): Next line

        Returns:
            bool: True if list tag
        """

        return cls.is_wrap_tag(line) and cls.is_list_item(next_line)


if __name__ == '__main__':
    with open('input/schedule.yml', encoding='utf-8') as f:
        yml_text = f.read()

    parser = YamlParser()
    content = parser.parse_text(yml_text)

    print(content)
