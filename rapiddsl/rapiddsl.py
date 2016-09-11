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

import cli
import filters
import loaders

import shutil
import jinja2
import datetime
import os

def set_system_globals(definition):
    definition['now'] = datetime.datetime.now()

def merge_definitions(definitions):
    merged_definition = {}
    for definition in definitions:
        merged_definition.update(definition)
    return merged_definition

def create_jinja2_environment(directory):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('rapiddsl', directory),
        trim_blocks=True
    )
    filters.register_filters(env)
    return env

def rename(filepath, definition):
    filedir, filename = os.path.split(filepath)
    new_filename = definition['name'] + filename
    new_filepath = os.path.join(filedir, new_filename)
    new_filepath = new_filepath.replace('.tmpl', '')
    os.rename(filepath, new_filepath)

def fill(filepath, definition):
    dirpath, filename = os.path.split(filepath)
    env = create_jinja2_environment(dirpath)
    filled = env.get_template(filename).render(definition)
    f = open(filepath, "w")
    f.write(filled)
    f.close()

def for_each_file(folder,arguments,functions):
    folder_abs = os.path.abspath(folder)
    for dir_path, dirs, filenames in os.walk(folder_abs):
        for filename in filenames:
            filepath = os.path.join(dir_path,filename)
            for function in functions:
                function(filepath,arguments)

def prepare_build(templates_dir,build_dir):
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(templates_dir,build_dir)

def build(build_dir,definition):
    for_each_file(build_dir, definition, [fill, rename])

def main():   
    parser = cli.create_parser()
    args = parser.parse_args()
    definitions = loaders.load(args.d)
    definition = merge_definitions(definitions)
    set_system_globals(definition)
    prepare_build(args.t,args.b)
    build(args.b,definition)

if __name__ == "__main__":
    main()
