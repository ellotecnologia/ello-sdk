import os
import os.path
import json
import collections
import configparser
import glob
import re

from delphi.dof import DOFFile
from ello.sdk.git import get_sorted_tags

class ProjectMetadata:
    def __init__(self, _filename=None):
        self._metadata = {}
        self._filename = _filename or 'package.json'
        self._type = os.path.splitext(self._filename)[1]
        self._previous_version = None
        self._load_metadata()

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, self._filename)

    def get_current_project_name(self):
        dof_files = glob.glob('*.dof') 
        if dof_files:
           return os.path.splitext(dof_files[0])[0]
        return ''

    def _load_metadata(self):
        # If metadata is json but the metadata file doesn't exists, try to open dof metadata
        if (self._type == '.json') and (not os.path.isfile(self._filename)):
            self._filename = self.get_current_project_name() + '.dof'
            self._type = os.path.splitext(self._filename)[1]

        # No metadata found, let's get some info from the current folder.
        if not os.path.isfile(self._filename):
            self._metadata['name'] = os.path.basename(os.getcwd())
            self._metadata['project_name'] = self._metadata['name']
            return

        if self._type == '.json':
            self._load_json_metadata()
        elif self._type == '.dof':
            self._load_dof_metadata()

    def _load_json_metadata(self):
        with open(self._filename, 'r') as f:
            self._metadata = json.load(
                f,
                object_pairs_hook=collections.OrderedDict
            )

    def _load_dof_metadata(self):
        dof = configparser.ConfigParser()
        dof.read(self._filename)
        major = dof.get('Version Info', 'MajorVer')
        minor = dof.get('Version Info', 'MinorVer')
        release = dof.get('Version Info', 'Release')
        self._metadata['name'] = os.path.splitext(self._filename)[0]
        self._metadata['version'] = '{}.{}.{}'.format(major, minor, release)

    def update_version(self, version):
        """ Updates package.json version info and Project.dof version info """
        self._metadata['version'] = version

        if self._type == '.json':
            with open(self._filename, 'w') as f:
                f.write(json.dumps(self._metadata, indent=2))

        dof_filename = os.path.join(self.path, self.name + '.dof')
        if os.path.isfile(dof_filename):
            dof_file = DOFFile(dof_filename)
            dof_file.update_version(version)

    @property
    def project_name(self):
        if self._metadata.has_key("project_name"):
            return self._metadata["project_name"]
        else:
            return self.name + ".dpr"

    @property
    def resource_file(self):
        if self._metadata.has_key("resource_file"):
            return self._metadata["resource_file"]
        else:
            return self.name + ".rc"

    @property
    def resources(self):
        return self._metadata['resources']

    @property
    def conditionals(self):
        return self._metadata['conditionals']

    @property
    def tag_prefix(self):
        return self._metadata.get('tag-prefix', None)

    @property
    def makefile(self):
        return os.path.join(self.path, 'Makefile')
        
    def __getattr__(self, name):
        return self._metadata.get(name, None)
        
    def dependencies(self):
        for dep in self._metadata['dependencies'].keys():
            hash = self._metadata['dependencies'][dep]
            repo = self._metadata['repos'].get(dep, '')
            yield dep, repo, hash

    @property
    def dependent_projects(self):
        """Retorna uma lista com os projetos dependentes do projeto atual"""
        projects = self._metadata.get('dependent_projects', [])
        projects = map(lambda p: os.path.join(self.path, p) if not os.path.isabs(p) else p, projects)
        return list(projects)

    @property
    def path(self):
        """Caminho completo do projeto atual"""
        return os.path.dirname(os.path.abspath(self._filename))

    @property
    def previous_version(self):
        """ Obtém a última versão 'taggeada' do projeto.
            Leva em consideração se a versão no projeto utiliza 
            prefixo (ex: nome_projeto/1.2.3.4) ou não (ex: 1.2.3.4).
        """
        if self._previous_version:
            return self._previous_version
        tags = get_sorted_tags()
        if self.tag_prefix:
            tags = filter(lambda t: t.startswith(self.tag_prefix), tags)
        else:
            tags = filter(lambda t: '/' not in t, tags)
        return list(tags)[-1]

    def texto_ultima_revisao(self):
        """Retorna o texto da última modificação do changelog"""
        changelog_header = re.compile('\d{2}/\d{2}/\d{4} - ')
        lines = []
        with open(os.path.join(self.path, 'CHANGELOG.txt')) as changelog:
            lines.append(changelog.readline())
            for line in changelog:
                match = changelog_header.search(line)
                if match:
                    break
                lines.append(line)
        return ''.join(lines)


if __name__ == "__main__":
    metadata = ProjectMetadata()
    print(metadata.version)
