import argparse
import yaml
import os
import shutil
import jinja2
    
def load(filepath):    
    f = open(filepath)
    document = yaml.load(f)
    f.close();
    return document;
 
def clear_dir(dirpath):
    if(os.path.exists(dirpath)):
        shutil.rmtree(dirpath,ignore_errors=True)
    os.mkdir(dirpath)    
 
def for_each_file(folder,arguments,functions):
    for dir_path, dirs, filenames in os.walk(folder):
        for filename in filenames: 
            filepath = os.path.join(dir_path,filename)
            for function in functions:
                function(filepath,arguments)

def copy(filepath,arguments):
    shutil.copy(filepath,arguments['destination_dir'])
 
def rename(filepath,arguments):
    filedir, filename = os.path.split(filepath)
    new_filename = arguments['domain']['name'] + filename
    new_filepath = os.path.join(filedir,new_filename)
    os.rename(filepath,new_filepath)
    
def fill(filepath,arguments):
    dirpath, filename = os.path.split(filepath)
    env = build_jinja2_environment(dirpath)
    filled = env.get_template(filename).render(arguments['domain'])
    f=open(filepath,"w")
    f.write(filled)
    f.close()
    
def build_jinja2_environment(directory):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('rapiddsl', directory),
        trim_blocks=True
    )
    return env
                      
def prepare_templates(templates_dir,destination_dir):
    arguments = {}
    arguments['destination_dir'] = destination_dir
    for_each_file(templates_dir,arguments,[copy])

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-source',required=True,help='Source folder containing templates and domain.yaml.',metavar='FOLDER')
    return parser

def standard_paths(source_dir):
    domain_file = os.path.join(source_dir,'domain.yaml')
    templates_dir = os.path.join(source_dir,'templates')
    results_dir = os.path.join(source_dir,'results')
    return domain_file, templates_dir, results_dir
    
def main():
    parser = build_parser()
    args = parser.parse_args()
    domain_file, templates_dir, results_dir = standard_paths(args.source)
    domain = load(domain_file)
    clear_dir(results_dir)
    prepare_templates(templates_dir,results_dir)
    arguments = {}
    arguments['domain'] = domain
    for_each_file(results_dir,arguments,[fill,rename])

if __name__ == "__main__":
    main()
