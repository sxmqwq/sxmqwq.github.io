#!/usr/bin/env python3
"""Run upstream Gmeek in a disposable workspace, then import its output."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def main():
    if not os.environ.get("GH_TOKEN"):
        raise SystemExit("GH_TOKEN is required to read the blog Issues")
    repository = os.environ.get("GITHUB_REPOSITORY", "sxmqwq/sxmqwq.github.io")
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    if config.get("homeUrl") != "https://sxmqwq.github.io/blog":
        raise SystemExit("config.json homeUrl must point to /blog")
    with tempfile.TemporaryDirectory(prefix="gmeek-", dir=os.environ.get("RUNNER_TEMP")) as directory:
        work = Path(directory)
        generator = work / "source"
        run(["git", "clone", "https://github.com/Meekdai/Gmeek.git", str(generator)])
        version = config.get("GMEEK_VERSION", "last")
        if version == "last":
            latest = subprocess.check_output(["git", "rev-list", "--tags", "--max-count=1"], cwd=generator, text=True).strip()
            version = subprocess.check_output(["git", "describe", "--tags", latest], cwd=generator, text=True).strip()
        if not version or version.startswith("-"):
            raise ValueError("Invalid GMEEK_VERSION")
        run(["git", "checkout", "--detach", version], cwd=generator)

        environment = work / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = str(environment / "bin" / "python")
        run([python, "-m", "pip", "install", "--disable-pip-version-check", "-r", str(generator / "requirements.txt")])
        shutil.copy2(ROOT / "config.json", generator / "config.json")
        if (ROOT / "static").is_dir():
            shutil.copytree(ROOT / "static", generator / "static", dirs_exist_ok=True)
        # Force a complete rebuild; no saved htmlDir or old homeUrl can leak in.
        (generator / "blogBase.json").unlink(missing_ok=True)
        env = os.environ.copy()
        env["GITHUB_WORKSPACE"] = str(generator)
        env["GITHUB_REPOSITORY"] = repository
        env["PYTHONUNBUFFERED"] = "1"
        # Gmeek expects argv. Keep its token in process memory, off shell arguments.
        wrapper = "import os,runpy,sys;sys.argv=['Gmeek.py',os.environ.pop('GH_TOKEN'),os.environ['GITHUB_REPOSITORY'],'--issue_number','0'];runpy.run_path('Gmeek.py',run_name='__main__')"
        run([python, "-c", wrapper], cwd=generator, env=env)
        run([sys.executable, str(ROOT / "scripts/assemble_site.py"), "--blog-source", str(generator / "docs"), "--metadata", str(generator / "blogBase.json"), "--backup", str(generator / "backup")], cwd=ROOT)


if __name__ == "__main__":
    main()
