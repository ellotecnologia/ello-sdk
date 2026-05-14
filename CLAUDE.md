# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install for development:**
```
pip install -e .
```

**Run tests:**
```
python -m pytest tests/
```

**Run a single test file:**
```
python -m unittest tests.text_manipulation_tests
```

**Build standalone executables** (Windows, requires pyinstaller):
```
make configure
```
This produces `configure.exe` and `ell.exe` via PyInstaller with `--onefile --noupx`.

## Architecture

The repo is a Python CLI toolkit called **Ello SDK**, built for internal use at Ello to automate development workflows around Delphi projects — versioning, deployment, changelog generation, and cross-system notifications.

### Package layout

- **`ello/cli/`** — Console entry points. Each file maps to a registered `console_scripts` command (e.g. `ell`, `ordena-uses`, `configure`, `crystal`).
- **`ello/sdk/`** — Reusable library code consumed by CLI modules. No direct entry points.
- **`ello/project/`** — Reads project metadata from `package.json` (JS-style) or `.dof` files (Delphi).
- **`ello/notifications/`** — Sends deployment notifications via Telegram, WhatsApp (ZapZap bridge), or Facebook.
- **`ello/chamados/`** — Integration with Ello's internal issue tracking system.
- **`ello/windows/`** — Windows-specific helpers.
- **`delphi/`** — Delphi compiler invocation, `.dof` / `.rc` (resource) file parsing and version-stamping.
- **`tests/`** — unittest-based tests; currently covers `ello/sdk/text_manipulation.py`.

### Key CLI commands

| Command | Module | Purpose |
|---|---|---|
| `ell` | `ello/cli/ell.py` | Main orchestrator: `init`, `install`, `generate`, `deploy`, `notify-team`, etc. |
| `configure` | `ello/cli/configure.py` | Installs project dependencies defined in `package.json` |
| `ordena-uses` | `ello/cli/ordena_uses.py` | Sorts Delphi `uses` clause entries alphabetically |
| `crystal` | `ello/cli/crystal.py` | Analyses Crystal Reports `.rpt` files and validates embedded SQL |
| `dfmgrep` / `dbgrep` / `crgrep` | cli/ | Grep-style search inside Delphi forms, DB tables, and Crystal Reports |
| `dof` | `ello/cli/dof.py` | Reads/writes Delphi `.dof` project options |
| `fbtrace` | `ello/cli/fbtrace.py` | Firebird trace log utilities |

### Core SDK modules

- **`sdk/config.py`** — Reads `~/ell.ini` (INI format) for all external credentials and server paths (sections: `servidor`, `ftp`, `wiki`, `telegram`, `whatsapp`, `firebird`).
- **`sdk/git.py`** — Git helpers: list tags, read commit logs between refs, manage hooks.
- **`sdk/changelog.py`** — Generates changelogs from git commit history between version tags.
- **`sdk/text_manipulation.py`** — Normalises Portuguese commit messages for changelog output: capitalises, maps verbs to impersonal form, strips technical noise, enforces 140-char limit.
- **`sdk/version.py`** — Bumps versions (calendar-based `YYYY.M.N` or semantic `MAJOR.MINOR.PATCH`), writes back to `package.json` and Delphi files.
- **`sdk/wiki.py`** — Pushes changelog pages to DokuWiki via its XML-RPC API.
- **`sdk/database.py`** — Generates SQL patch scripts for Firebird.
- **`sdk/shell.py`** — Cross-platform subprocess wrapper.

### Configuration (`~/ell.ini`)

All runtime configuration lives in `~/ell.ini`. The SDK reads it at startup via `sdk/config.py`. Required sections vary by command, but the typical structure is:

```ini
[servidor]
host = ...
usuario = ...
senha = ...

[ftp]
caminho = ...

[wiki]
url = ...
usuario = ...
senha = ...

[telegram]
token = ...
chat_id = ...

[firebird]
host = ...
banco = ...
usuario = ...
senha = ...
```

### Commit message conventions

Commit messages are in **Portuguese**. `sdk/text_manipulation.py` applies normalisation rules when generating changelogs — messages containing certain words (`revisão`, `frame`, `metadado`, `revert`, etc.) are excluded from changelogs entirely. Verbs like `ajustado` are mapped to impersonal forms and technical terms like `form` are replaced with user-facing synonyms (`tela`).
