# rapiddsl

rapiddsl is a tool that helps you to quickly create domain specific languages (DSL).
It imposes some restrictions on the DSL.
The DSL can only have two types of concepts: domain objects and products.

## Domain Objects

Domain objects define the domain model. 
They can have any structure build out of strings, lists and hashmaps.

## Products

A product is one generated output based on the domain model.
For the code generation templates are used.
A product can use one or more templates.

## Program structure

    products.yaml    Holds the templates to product mapping.
    \products        Holds generated code sorted by product and generation timestamp.
    
## Example

    python rapiddsl -domain=examples/person/person.yaml -product=bean


    
