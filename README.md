# rapiddsl

rapiddsl is a generic code generator that can turn any json/yaml definition into code using jinja2 templates.

## Features

- Several definitions are automatically merged. This allows global definitions.
- First level elements (in definitions) can be used in file names.
- Templates directory structure is kept for the generated code.
- Current time. Usage: {{now.strftime('%Y-%m-%d')}}.
- Text transformation functions: first_upper, first_lower, const_case. Implemented as Jinja2 filters.

## Example

A simple example making use of all the features.

	cd examples/person
	python3 ../../rapiddsl.py -d person.yaml globals.json -t templates -b build

## Dependencies

- python3
- pip3 install jinja2 pyyaml
    
