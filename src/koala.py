import argparse
from parser import Parser
import yaml
from jsonparser.json_parser import JSONParser

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='koala: template language parser')
    args_parser.add_argument('template_file', nargs=1, type=str, metavar='template_file', help='template file path')
    args_parser.add_argument('-dt', '--dictionary_type', nargs=1, type=str, choices=['yaml', 'json'], help='dictionary type')
    args_parser.add_argument('dictionary', nargs=1, type=str, metavar='dictionary', help='yaml or json dictionary file path')
    args_parser.add_argument('output_file', nargs=1, type=str, metavar='output_file', help='output file path')

    args = args_parser.parse_args()

    dic_content = open(args.dictionary[0], 'r')

    dic = {}
    if (args.dictionary_type[0] == 'yaml'):
        dic = yaml.load(dic_content, Loader=yaml.FullLoader)
    else:
        jsonparser = JSONParser()
        dic = jsonparser.load(dic_content.read())

    p = Parser(dic)
    p.load_template(args.template_file[0])
    result = p.parse()

    output = open(args.output_file[0], 'w')
    output.write(result)
