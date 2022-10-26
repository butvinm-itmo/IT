from typing import List
from tokens import Token, OpenTag, CloseTag, TagValue
from yaml_parser import YamlParser


class MarkdownBuilder:
    @staticmethod
    def build_md_text(tokens: List[Token]) -> str:
        """Build text in Markdown format from tokens

        Args:
            tokens (List[Token]): Structure in tokens

        Returns:
            str: Builded md text
        """

        md_text = ''
        for token in tokens:
            md_text += '>' * (token.ident // 2)
            if isinstance(token, OpenTag):
                md_text += '### {tag}\n'.format(tag=token.tag)
            elif isinstance(token, CloseTag):
                md_text += '\n'
            elif isinstance(token, TagValue):
                md_text += '**{tag}:** {value} \n\n'.format(
                    tag=token.tag, value=token.value)

        return md_text


if __name__ == '__main__':
    with open('input/schedule.yml', encoding='utf-8') as f:
        yml_text = f.read()

    parser = YamlParser()
    content = parser.parse_text(yml_text)
    md = MarkdownBuilder.build_md_text(content)
