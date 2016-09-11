# rapiddsl

rapiddsl is a tool that can turn any definition into code using templates.
It can read json or yaml definitions and uses jinja2 templates.

## Features

- definition files are automatically merged into one definition, this allows global definitions
- template files directory structure is kept for the generated code
- extra filters: first_upper, first_lower, const_case
- now: current moment in time: {{now.strftime('%Y-%m-%d')}}

## Dependencies

- python2
- pyyaml: pip install pyyaml
- jinja2: pip install jinja2
    
