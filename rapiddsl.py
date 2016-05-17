'''
Copyright (c) 2015, Eduard Beutel
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by the copyright holder.
4. Neither the name of the copyright holder nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY EDUARD BEUTEL ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import argparse
import yaml
import os
import shutil
import jinja2
import datetime

def first_lower(x):
    return x[0].lower() + x[1:]
    
def first_upper(x):
    return x[0].upper() + x[1:]
    
def load_yaml(filepath):    
    f = open(filepath)
    document = yaml.load(f)
    f.close();
    return document;
    
def load_product(filepath,product_name):    
    document = load_yaml(filepath)
    for product in document['products']:
        if product['name'] == product_name:
            return product
    raise Exception('Product ' + product_name + ' not found in ' + filepath + '.')

def copy_tmpl(filepath,destination):
    if filepath.endswith('.tmpl'):
        shutil.copy(filepath,destination)
     
def rename(filepath,domain):
    filedir, filename = os.path.split(filepath)
    new_filename = domain['name'] + filename
    new_filepath = os.path.join(filedir,new_filename)
    new_filepath = new_filepath.replace(".tmpl","")
    os.rename(filepath,new_filepath)
    
def fill(filepath,domain):
    dirpath, filename = os.path.split(filepath)
    env = create_jinja2_environment(dirpath)
    filled = env.get_template(filename).render(domain)
    f=open(filepath,"w")
    f.write(filled)
    f.close()
    
def create_jinja2_environment(directory):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('rapiddsl', directory),
        trim_blocks=True
    )
    register_filters(env)
    return env

def register_filters(env):
    env.filters['first_upper'] = first_upper
    env.filters['first_lower'] = first_lower
    
def for_each_file(folder,arguments,functions):
    for dir_path, dirs, filenames in os.walk(folder):
        for filename in filenames: 
            filepath = os.path.join(dir_path,filename)
            for function in functions:
                function(filepath,arguments)
                
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config','-c',required=False,help='The path to the config file.',metavar='config')
    parser.add_argument('-product','-p',required=True,help='The name of the product to create.',metavar='product')
    parser.add_argument('-domain-object','-d',required=True,help='Yaml file containing domain object definition.',metavar='domain.yaml')
    return parser
    
def create_destination_dir(products_dir,product_name):
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    destination_dir = products_dir + '/' + product_name + '_' + now
    if not os.path.isdir(products_dir):
        os.mkdir(products_dir)       
    os.mkdir(destination_dir)   
    return destination_dir  
    
def main():   
    config_path = 'config.yaml'
    parser = create_parser()
    args = parser.parse_args()
    if args.config:
        config_path = args.config
    config = load_yaml(config_path)
    domain = load_yaml(args.domain_object)
    global_objects = load_yaml(config['globals'])
    domain.update(global_objects)
    domain['now'] = datetime.datetime.now()
    product = load_product(config['products'],args.product)
    destination = create_destination_dir(config['output'],product['name'])
    for_each_file(config['templates'],destination,[copy_tmpl])
    for_each_file(destination,domain,[fill,rename])

if __name__ == "__main__":
    main()
