import os
import os.path
import subprocess

from argparse import ArgumentParser, Namespace

from ello.project import ProjectMetadata
from ello.sdk.version import bump_version
from ello.sdk.changelog import make_changelog


def init_args(parser: ArgumentParser) -> None:
    cmd = parser.add_parser("deploy", help="Realiza o deploy do projeto atual")
    cmd.add_argument("--release", help="Realiza o upload da revisão", action='store_false')
    cmd.set_defaults(func=deploy)


def deploy(args: Namespace) -> None:
    project = ProjectMetadata()

    args.project = project.project_name
    args.commit = True
    args.push = True
    args.create_tag = True
    args.fecha_chamados = True

    bump_version(args)
    make_changelog(args)

    if args.release:
        run_deploy_target(project)


def run_deploy_target(project: ProjectMetadata) -> None:
    if not os.path.exists(project.makefile):
        return

    cur_dir = os.getcwd()
    os.chdir(project.path)
    subprocess.call("make deploy")
    os.chdir(cur_dir)

    for p in project.dependent_projects:
        run_deploy_target(ProjectMetadata(p))
