# coding: utf8
import sys
import subprocess
import shutil
import os
from datetime import datetime

def get_latest_tag():
    cmd = 'git describe --abbrev=0 --tags' 
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip()

def generate_temp_changelog(latest_tag, changes):
    major = ".".join(latest_tag.split('.')[:-1])
    next_release = int(latest_tag.split('.')[-1], 10)+1
    next_tag = major + ".{}".format(next_release)

    data_atual = datetime.now().strftime("%d/%m/%Y")

    headline = u"{} - Revisão {}\n".format(data_atual, next_tag)

    f = open('temp.txt', 'w')
    print >>f, headline.encode('latin1')
    for line in changes:
        print >>f, line.decode('utf8').encode('latin1')
    print >>f, ""
    f.close()

def merge_temp_with_changelog():
    filenames = ['temp.txt', 'CHANGELOG.txt']
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', 'CHANGELOG.txt')
    #os.remove('temp.txt')
    os.remove('result.txt')

def update():
    print "Atualizando arquivo CHANGELOG.txt"
    latest_tag = get_latest_tag()
    changes = get_change_list(latest_tag)

    generate_temp_changelog(latest_tag, changes)

    notepad = subprocess.Popen(['notepad', 'temp.txt'])
    notepad.wait()

    merge_temp_with_changelog()

def get_change_list(from_tag):
    cmd = ['git', 'changelog', '--reverse', '{}..'.format(from_tag)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p.communicate()[0].splitlines()

def commit():
    print u"Commitando atualização do changelog..."
    subprocess.call(u'git ci -am "Atualização do changelog"'.encode('latin1'))

def push():
    print u"Fazendo push do changelog..."
    exit_code = subprocess.call('git push')
    if exit_code>0:
        print 'Falha ao fazer o push do changelog...'
        sys.exit(1)


if __name__=='__main__':
    update()

