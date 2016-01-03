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

def load_domain_object(filepath):    
    f = open(filepath)
    document = yaml.load(f)
    f.close();
    return document;

def duplicate_template(filepath,destination):
    if filepath.endswith(".tmpl"):
        filedir, filename = os.path.split(filepath)
        filename = filename + ".fill"
        destination = os.path.join(destination,filename)
        shutil.copy2(filepath,destination)
  
def rename(filepath,new_filename):
    filedir, filename = os.path.split(filepath)
    new_filepath = os.path.join(filedir,new_filename)
    os.rename(filepath,new_filepath)
    
def rename_final(filepath,domain):
    if filepath.endswith(".fill"):
        filedir, filename = os.path.split(filepath)
        new_filename = domain['name'] + filename
        new_filename = new_filename.replace(".fill","")
        new_filename = new_filename.replace(".tmpl","")
        rename(filepath,new_filename)
    
def fill(filepath,domain):
    if filepath.endswith(".fill"):
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
    return env

def for_each_file(folder,arguments,functions):
    for dir_path, dirs, filenames in os.walk(folder):
        for filename in filenames: 
            filepath = os.path.join(dir_path,filename)
            for function in functions:
                function(filepath,arguments)
                
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-do',required=True,help='Yaml file containing domain object (do).',metavar='do.yaml')
    return parser
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    domain_object = load_domain_object(args.do)
    destination_dir, filename = os.path.split(args.do)
    for_each_file(destination_dir,destination_dir,[duplicate_template])
    for_each_file(destination_dir,domain_object,[fill,rename_final])

if __name__ == "__main__":
    main()
