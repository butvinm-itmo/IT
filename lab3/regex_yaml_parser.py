from xml_builder import XmlBuilder
import re

from yaml_parser import YamlParser


class RegexYamlParser(YamlParser):
    TAG = re.compile(r'([\w-]+):')
    VALUE = re.compile(r': *"*([^\n"]+)')
    LIST_ITEM = re.compile(r'- (\w+)')
    ATTR = re.compile(r'([\w-]+): (.+)$')
    INSTANCE_BEGIN = re.compile(f'- ({ATTR.pattern}|$)')
    WRAP_TAG = re.compile('.+:$')

    @classmethod
    def get_tag_and_value(cls, line: str) -> tuple[str, str]:
        """Get tag and value from line

        Args:
            line (str): Parsed line

        Returns:
            tuple[str, str]: Tag and value
        """

        line = line.lstrip('-').rstrip('}').rstrip(',')
        if ':' in line:
            tag = re.search(cls.TAG, line)
            tag = tag.group(1) if tag is not None else ''
            value = re.search(cls.VALUE, line)
            value = value.group(1).strip() if value is not None else ''
        else:
            tag = line.strip()
            value = ''

        return tag, value

    @classmethod
    def is_list_item(cls, line: str) -> bool:
        """Chick if line is list item

        Args:
            line (str): Parsed line

        Returns:
            bool: True if list item
        """

        return re.fullmatch(cls.LIST_ITEM, line) is not None

    @classmethod
    def is_attr(cls, line: str) -> bool:
        """Check if line is attribute with value

        Args:
            line (str): Parsed line
        Returns:
            bool: True if attr
        """

        return re.search(cls.ATTR, line) is not None

    @classmethod
    def is_instance_begin(cls, line: str) -> bool:
        """Check if line is beginning of type instance

        Args:
            line (str): Parsed line

        Returns:
            bool: True if line is instance begin
        """

        return re.fullmatch(cls.INSTANCE_BEGIN, line) is not None

    @classmethod
    def is_wrap_tag(cls, line: str) -> bool:
        """Check if tag is wrapping tag

        Args:
            line (str): Parsed line 
            next_line (str): Next line 

        Returns:
            bool: True if wrapping tag
        """

        return re.fullmatch(cls.WRAP_TAG, line) is not None

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

    parser = RegexYamlParser()
    content = parser.parse_text(yml_text)

    xml_text = XmlBuilder.build_xml_text(content)
    with open('output/schedule.xml', 'w', encoding='utf-8') as f:
        f.write(xml_text)
