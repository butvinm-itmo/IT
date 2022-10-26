from time import time
from regex_yaml_parser import RegexYamlParser
from yaml_parser import YamlParser
import yaml
from xml_builder import XmlBuilder
from markdown_builder import MarkdownBuilder


def test_raw():
    with open('input/schedule.yml', encoding='utf-8') as f:
        yml_text = f.read()

    parser = YamlParser()
    content = parser.parse_text(yml_text)

    return content


def test_regex():
    with open('input/schedule.yml', encoding='utf-8') as f:
        yml_text = f.read()

    parser = RegexYamlParser()
    content = parser.parse_text(yml_text)

    return content


def test_lib():
    with open('input/schedule.yml', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


def test_time():
    test_raw_time = sum([-time() - len(test_raw()) * 0 + time() for _ in range(100)])
    test_regex_time = sum([-time() - len(test_regex()) * 0 + time() for _ in range(100)])
    test_lib_time = sum([-time() - len(test_lib()) * 0 + time() for _ in range(100)])    
    print(f'{test_raw_time=}\n{test_regex_time=}\n{test_lib_time=}\n')


def test_yaml_to_xml():
    with open('output/test_raw.xml', 'w', encoding='utf-8') as f:
        xml = XmlBuilder.build_xml_text(test_raw())
        f.write(xml)
    
    with open('output/test_regex.xml', 'w', encoding='utf-8') as f:
        xml = XmlBuilder.build_xml_text(test_regex())
        f.write(xml)

    with open('output/test_lib.xml', 'w', encoding='utf-8') as f:
        parser = YamlParser()
        xml = XmlBuilder.build_xml_text(parser.parse_yamllib_data(test_lib()))
        f.write(xml)


def test_md():
    with open('output/test_md.md', 'w', encoding='utf-8') as f:
        md = MarkdownBuilder.build_md_text(test_raw())
        f.write(md)


if __name__ == '__main__':
    test_time()
    test_yaml_to_xml()
    test_md()
