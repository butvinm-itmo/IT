from typing import List
from tokens import Token, OpenTag, CloseTag, TagValue
from yaml_parser import YamlParser


class XmlBuilder:
    @staticmethod
    def build_xml_text(tokens: List[Token]) -> str:
        """Build text in XML format from tokens

        Args:
            tokens (List[Token]): Xml structure in tokens

        Returns:
            str: Builded xml text
        """

        xml_text = ''
        for token in tokens:
            xml_text += ' ' * token.ident
            if isinstance(token, OpenTag):
                xml_text += f'<{token.tag}>\n'
            elif isinstance(token, CloseTag):
                xml_text += f'</{token.tag}>\n'
            elif isinstance(token, TagValue):
                xml_text += f'<{token.tag}>{token.value}</{token.tag}>\n'

        return xml_text


if __name__ == '__main__':
    with open('input/schedule.yml', encoding='utf-8') as f:
        yml_text = f.read()

    parser = YamlParser()
    content = parser.parse_text(yml_text)
    xml_text = XmlBuilder.build_xml_text(content)
    with open('output/schedule.xml', 'w', encoding='utf-8') as f:
        f.write(xml_text)