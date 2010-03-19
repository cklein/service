#!/usr/bin/env python
'''
config.py

Created by Christian Klein on 2010-03-10.
Copyright (c) 2010 Christian Klein. All rights reserved.
'''

import sys
import os
import pwd
from optparse import OptionParser


def get_ids(username):
    '''Get user id for given username'''
    passwd = pwd.getpwnam(username)
    return passwd.pw_uid, passwd.pw_gid


def makelog(directory, loguser):
    '''Create log directory'''
    
    uid, gid = get_ids(loguser)
    
    fname = os.path.join(directory, 'main')
    os.makedirs(fname)
    os.chown(fname, uid, gid)
    os.chmod(fname, 02755)
    
    fname = os.path.join(directory, 'status')
    open(fname, 'w')
    os.chown(fname, uid, gid)
    os.chmod(fname, 0644);
    
    fname = os.path.join(directory, 'run')
    open(fname, 'w').write('#!/bin/sh\nexec\nsetuidgid %s\nmultilog t ./main\n' % loguser)
    os.chown(fname, uid, gid)
    os.chmod(fname, 0755)


def create(templates):
    '''Create directory structures'''
    
    # create directory structure:
    for name, template in templates.items():
        vars = template.get('vars', {})
        try:
            directory = template['directory']
            for subdir in 'env', 'log':
                os.makedirs(os.path.join(directory, subdir), 02755)
        
            makelog(os.path.join(directory, 'log'), template.get('loguser', template.get('user')))
        
            # environment variables:
            uid, gid = get_ids(template['user'])
            template['env'].update({'UID': str(uid), 'GID': str(gid)})
        
            for variable, value in template['env'].items():
                filename = os.path.join(directory, 'env', variable % vars)
                open(filename, 'w').write(value)
                os.chmod(filename, 0644)
        
            # create run script:
            fname = os.path.join(directory, 'run')
            run = open(fname, 'w')
            run.write('#!/bin/sh\n')
            if 'run_prologue' in template:
                run.write(template['run_prologue'] % vars)
            run.write('exec 2>&1\nexec envdir %s/env \\\n' % directory)
            run.write(template['run'] % vars)
            os.chmod(fname, 0755)
        except (KeyError, OSError), exception:
            sys.stderr.write("Could not create service directories: %s\n" % exception)
            # tear down
            #print "tearing down", directory
            pass


def load_yaml(filename):
    from yaml import load
    from yaml import Loader as Loader
    return load(open(filename), Loader=Loader)


def load_json(filename):
    import simplejson as json
    return json.load(open(filename))


def load_python(filename):
    lvars = {}
    execfile(filename, lvars)
    return lvars['TEMPLATES']


def main():
    parser = OptionParser()
    parser.add_option('-f', '--format', type='choice', choices=['python', 'yaml', 'json'],
                       default='python', help='Format of template file [default: %default]')
    parser.add_option('-s', '--service', action="store_true", help="Create service directories")
    
    options, args = parser.parse_args(sys.argv)
    
    if len(args) != 2:
       parser.error('No template file given')
    templates = globals().get('load_%s' % options.format)(args[1])
    
    if options.service:
        create(templates)
    

if __name__ == '__main__':
    main()
