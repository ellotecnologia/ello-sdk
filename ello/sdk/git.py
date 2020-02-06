import os
import subprocess
import logging
import shutil

logger = logging.getLogger()


def git(args):
    cmd = 'git {0}'.format(args)
    with open(os.devnull, 'w') as FNULL:
        exit_code = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    return exit_code


def create_version_tag(tag_name):
    logger.info("Criando tag {}".format(tag_name))
    git("tag {0}".format(tag_name))


def push_tags():
    logger.info("Enviando atualizações para o repositório remoto (commits, tags)...")
    git("push")
    git("push --tags")


def get_latest_tag():
    """ Get last defined tag from git log
    """
    cmd = 'git rev-list --tags --max-count=1'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    last_hash = p.communicate()[0].strip()

    cmd = 'git describe --tags {}'.format(last_hash.decode('latin1'))
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip().decode('latin1')


def get_changes_from(from_tag):
    cmd = ['git', 'changelog', '--reverse', '{}..'.format(from_tag)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    changes = p.communicate()[0].splitlines()
    changes = map(lambda text: text.decode('utf8'), changes)
    return changes


def install_hooks(args):
    """ Instala alguns hooks no repositorio atual """
    if not os.path.exists(".git"):
        print("Repositório git não encontrado")
        return
    hooks_path = os.path.abspath(os.path.dirname(__file__) + "/../../git_hooks")
    for root, dirs, files in os.walk(hooks_path):
        for filename in files:
            shutil.copyfile(os.path.join(hooks_path, filename), ".git/hooks/" + filename)