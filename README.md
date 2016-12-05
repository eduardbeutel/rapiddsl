# rapiddsl

rapiddsl is a tool that can turn any json/yaml definition into code using jinja2 templates.

## Features

- Definition files are automatically merged into one definition. This allows global definitions.
- Template files directory structure is kept for the generated code.
- First level elements from definition files can be used in file names.
- Now: current time template constant. Usage: {{now.strftime('%Y-%m-%d')}}.
- Extra jinja2 filters: first_upper, first_lower, const_case.

## Running the example

	cd examples/person
	python ../../rapiddsl.py -d person.yaml globals.json -t templates -b build

## Dependencies

- python2
- pyyaml: pip install pyyaml
- jinja2: pip install jinja2
    
