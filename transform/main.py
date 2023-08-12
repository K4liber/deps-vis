import argparse
from collections import defaultdict
import json
import logging
from pprint import pformat

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s [%(asctime)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True)
parser.add_argument('-o', '--output', required=True)


def input_dict_to_output(input_dict: dict) -> dict:
    module_names = list(input_dict.keys())
    nodes = []
    edges = []
    node_to_imports = defaultdict(int)
    
    for module_name in module_names:
        module_dict = input_dict[module_name]

        for imported_module_name in module_dict.get('imports', []):
            node_to_imports[module_name] += 1
            edges.append(
                {
                    "data": { 
                        "id": f'{imported_module_name}_{module_name}',
                        "source": imported_module_name,
                        "target": module_name
                    }
                }
            )

    for module_name in module_names:
        module_dict = input_dict[module_name]
        nodes.append(
            {
                "data": { 
                    "id": module_name,
                    "label": f'{module_name} ({node_to_imports.get(module_name, 0)})'
                }
            }
        )

    return {
        "nodes": nodes,
        "edges": edges
    }


if __name__ == '__main__':
    args = parser.parse_args()
    logger.info(f'Running transform from {args.input} to {args.output}.')

    with open(args.input) as input_file:
        input_dict = json.load(input_file)

    logger.info(f'Input dict: \n{pformat(input_dict)}')
    output_dict = input_dict_to_output(input_dict=input_dict)
    logger.info(f'Output dict: \n{pformat(output_dict)}')

    with open(args.output, 'w') as output_file:
        json.dump(output_dict, output_file, indent=4)
