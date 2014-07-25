from __future__ import with_statement

from fabric.api import run, prefix, env, cd, task, local

import os.path as op

# -----------------------------------------------------------------------------

CURRENT_DIR = op.dirname(__file__)

# -----------------------------------------------------------------------------

env.base_dir = CURRENT_DIR
env.hosts = ["thomaskliszowski.fr"]
env.user = 'backup'

# -----------------------------------------------------------------------------

def virtualenv():
    return prefix('. %(base_dir)s/venv/bin/activate' % env)

@task
def deploy():
    with cd(env.base_dir):
        run("git pull")

        # with virtualenv():
        #     run("pip install -r requirements.txt")

@task
def pypi_upload():
    with virtualenv():
        local("sudo python setup.py sdist register upload")
