#!/usr/bin/env python

import pwd

def get_uid(username):
    """Get user id for given username"""
    passwd = pwd.getpwnam(username)
    return str(passwd.pw_uid)


def get_gid(groupname):
    """Get group id for given groupname"""
    return str(0) # TODO



def create(templates):
    for name, template in templates.items():
        print name, template
        for var in template['env'].values():
            print var % template['vars']
        print template['run'] % template['vars']


TEMPLATES = {
    'logserver': {
            'vars': {
                'BASEDIR': '/usr/local/huLOG',
            },
            'env': {
                'UID': get_uid('cklein'),
                'GID': get_gid('wheel'),
                'PYTHONPATH': "%(BASEDIR)s",
            },
            'run': """. %(BASEDIR)s/pyenv/bin/activate
python %(BASEDIR)s/bin/bla.py --help
"""
    }
}

if __name__ == "__main__":
    create(TEMPLATES)