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

Review your agent's hook trust requirements, then start a new session in your
project. The plugin downloads and verifies its matching Rig program automatically.
Supported systems: macOS and Linux, on Intel/AMD or Arm processors.

## Install the standalone CLI

```sh
curl -fsSL https://downloads.rig.ai/install.sh | sh
```

Then run `rig setup` and `rig scan /path/to/project`.

The CLI installer selects the current release. Each plugin publication pins its
own tested release. You do not need to install the standalone CLI for the plugin.

## Bugs and feature requests

[Report a bug or suggest a feature](https://github.com/RigCodeAI/rig/issues/new/choose).
Search existing issues first, and remove private code, secrets and personal
information from anything you share.

## About this repository

This repository contains the public agent plugin and issue tracker. Rig's program
source is private. Learn more at [rig.ai](https://rig.ai).
