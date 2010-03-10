TEMPLATES = {
    'logserver': {
            'directory': '/Users/cklein/Desktop/huLOG/service/camserver',
            'user': 'cklein',
            'loguser': 'cklein',
            'vars': {
                'BASEDIR': '/Users/cklein/Desktop/huLOG/service/camserver',
            },
            'env': {
                'PYTHONPATH': "%(BASEDIR)s",
            },
            'run_prologue': '. %(BASEDIR)s/pyenv/bin/activate\n',
            'run': "python %(BASEDIR)s/camserver/server/camserver\n"
    }
}
