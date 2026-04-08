"""Publish a distillary brain as a static website using Quartz.

Quartz (https://quartz.jzhao.xyz) converts Obsidian vaults to static sites
with graph view, wikilinks, backlinks, search, and tags — hosted free on
GitHub Pages.

Usage:
    distillary publish vault-lean-startup-v2/ --repo distillary-vault-lean-startup
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)

QUARTZ_REPO = "https://github.com/jackyzha0/quartz.git"


def publish(
    vault_dir: str | Path,
    repo_name: str | None = None,
    topic: str | None = None,
    dry_run: bool = False,
) -> None:
    """Publish a vault to GitHub Pages via Quartz."""
    vault = Path(vault_dir).resolve()
    if not vault.exists():
        raise FileNotFoundError(f"Vault not found: {vault}")

    repo_name = repo_name or f"distillary-vault-{vault.name}"
    site_dir = vault.parent / f".{vault.name}-site"

    # 1. Check prerequisites
    _check_prereqs()

    # 2. Clone/setup Quartz if needed
    if not (site_dir / "package.json").exists():
        log.info("Setting up Quartz in %s", site_dir)
        subprocess.run(
            ["git", "clone", "--depth=1", QUARTZ_REPO, str(site_dir)],
            check=True,
        )
        subprocess.run(["npm", "i"], cwd=str(site_dir), check=True)

    # 3. Sync vault content to Quartz content dir
    content_dir = site_dir / "content"
    if content_dir.exists():
        shutil.rmtree(content_dir)
    shutil.copytree(vault, content_dir, ignore=shutil.ignore_patterns(".obsidian"))
    log.info("Copied vault to %s", content_dir)

    # 4. Build
    log.info("Building static site...")
    subprocess.run(
        ["npx", "quartz", "build"],
        cwd=str(site_dir),
        check=True,
    )

    if dry_run:
        log.info("Dry run complete. Site built at %s/public", site_dir)
        log.info("Preview: cd %s && npx quartz build --serve", site_dir)
        return

    # 5. Create GitHub repo if needed
    log.info("Creating GitHub repo: %s", repo_name)
    topics = ["distillary-vault"]
    if topic:
        topics.append(topic)

    try:
        subprocess.run(
            ["gh", "repo", "view", repo_name],
            capture_output=True, check=True,
        )
        log.info("Repo %s already exists", repo_name)
    except subprocess.CalledProcessError:
        subprocess.run(
            ["gh", "repo", "create", repo_name, "--public",
             "--description", f"Distillary knowledge vault: {vault.name}"],
            check=True,
        )
        for t in topics:
            subprocess.run(
                ["gh", "repo", "edit", repo_name, "--add-topic", t],
                check=False,
            )

    # 6. Deploy to GitHub Pages
    log.info("Deploying to GitHub Pages...")
    subprocess.run(
        ["npx", "quartz", "sync", "--no-pull"],
        cwd=str(site_dir),
        check=True,
    )

    log.info("Published! Site will be live at: https://<username>.github.io/%s", repo_name)


def preview(vault_dir: str | Path) -> None:
    """Local preview of the vault as a website."""
    vault = Path(vault_dir).resolve()
    site_dir = vault.parent / f".{vault.name}-site"

    if not (site_dir / "package.json").exists():
        # Quick setup
        subprocess.run(
            ["git", "clone", "--depth=1", QUARTZ_REPO, str(site_dir)],
            check=True,
        )
        subprocess.run(["npm", "i"], cwd=str(site_dir), check=True)

    content_dir = site_dir / "content"
    if content_dir.exists():
        shutil.rmtree(content_dir)
    shutil.copytree(vault, content_dir, ignore=shutil.ignore_patterns(".obsidian"))

    log.info("Starting local preview at http://localhost:8080")
    subprocess.run(
        ["npx", "quartz", "build", "--serve"],
        cwd=str(site_dir),
    )


def _check_prereqs() -> None:
    """Check that node, npm, and gh are available."""
    for cmd in ["node", "npm", "gh"]:
        r = subprocess.run(["which", cmd], capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(
                f"{cmd} not found. Install: "
                + {"node": "brew install node", "npm": "brew install node",
                   "gh": "brew install gh"}[cmd]
            )
