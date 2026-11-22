# Rig

Catch security problems while your agent codes.

Rig gives your coding agent security checks tailored to your project. It works
with Claude Code and Codex.

## Install with your coding agent

Claude Code:

```sh
claude plugin marketplace add RigCodeAI/rig
claude plugin install rig@rig
```

Codex CLI:

```sh
codex plugin marketplace add RigCodeAI/rig
codex plugin add rig@rig
```

For native Codex on Windows, use the Windows marketplace ref instead:

```powershell
codex plugin marketplace add RigCodeAI/rig --ref windows-codex
codex plugin add rig@rig
```

If you already installed the public Rig marketplace on Windows without that
ref, run `codex plugin marketplace remove rig` once before the two commands
above. Later upgrades use the normal marketplace upgrade command.

Review your agent's hook trust requirements, then start a new session in your
project. Hook or MCP startup downloads and verifies the pinned Rig executable
when its versioned cache is empty. Installing the plugin alone installs its
agent resources. A standalone installation is how you get a `rig` command on PATH.
Supported systems are Apple Silicon macOS and GNU/Linux x64 or arm64.

To update, run `codex plugin marketplace upgrade rig` for Codex, or run
`claude plugin marketplace update rig` followed by `claude plugin update rig@rig`
for Claude Code. Start a new session to use the new package.

## Install the standalone CLI

```sh
curl -fsSL https://downloads.rig.ai/install.sh | sh
```

If needed, add the install directory to PATH. For the default directory, run
`export PATH="$HOME/.local/bin:$PATH"`. Then run `rig setup` and `rig scan /path/to/project`.

The CLI installer selects the current release. Each plugin publication pins its
own tested release. You do not need to install the standalone CLI for the plugin.

## Bugs and feature requests

[Report a bug or suggest a feature](https://github.com/RigCodeAI/rig/issues/new/choose).
Search existing issues first, and remove private code, secrets and personal
information from anything you share.

## About this repository

This repository contains the public agent plugin and issue tracker. Rig's program
source is private. Learn more at [rig.ai](https://rig.ai).
