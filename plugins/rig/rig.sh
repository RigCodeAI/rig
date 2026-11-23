#!/bin/sh
# Thin pre-Rust bootstrap. Product behavior lives in the pinned Rig executable.
set -eu
launcher=$0
case "$(uname -s)" in MINGW*|MSYS*) launcher=$(cygpath -u "$launcher");; esac
root=$(CDPATH= cd -- "$(dirname -- "$launcher")" && pwd -P)
RIG_PLUGIN_ROOT=$root
export RIG_PLUGIN_ROOT
runtime_version=0.1.45
source_revision=04e862f86ebed23d38c76486c827e7301876500a
agent_contract=1
fail() {
    printf 'Rig runtime setup failed: %s\n' "$1" >&2
    if [ "${1:-}" != '' ] && [ "${hook_call:-0}" = 1 ]; then
        printf '%s\n' '{"systemMessage":"Rig runtime is unavailable; verification did not run. See the hook error and retry setup in a new session."}'
        exit 0
    fi
    exit 2
}
hook_call=0
if [ "${1:-}" = plugin ] && [ "${2:-}" = hook ]; then hook_call=1; fi
version=$(cat "$root/runtime-version") || fail 'missing runtime pin; reinstall the Rig plugin'
case "$version" in ''|*[!0-9.]*|.*) fail 'invalid pinned runtime version';; esac
RIG_PLUGIN_RUNTIME_PIN=$version
export RIG_PLUGIN_RUNTIME_PIN
if [ "$source_revision" != unreleased ] && [ ! -f "$root/runtime-SHA256SUMS" ]; then
    fail 'missing packaged checksums; reinstall the Rig plugin'
fi
case "$(uname -s)/$(uname -m)" in
    MINGW*/x86_64|MSYS*/x86_64)
        # Git for Windows is a declared native-host prerequisite, never WSL.
        exec powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass \
            -File "$(cygpath -w "$root/rig.ps1")" "$@";;
    Darwin/arm64) target=aarch64-apple-darwin;;
    Linux/aarch64|Linux/arm64) target=aarch64-unknown-linux-gnu;;
    Linux/x86_64) target=x86_64-unknown-linux-gnu;;
    *) fail 'native plugin delivery supports Apple Silicon macOS and Linux x64/arm64 only';;
esac
home=${RIG_HOME:-${RIG_CONFIG_HOME:-${HOME:?HOME is required}/.rig}}
case "$home" in '~') home=$HOME;; '~/'*) home=$HOME/${home#\~/};; esac
case "$home" in /*) ;; *) fail 'RIG_HOME must be absolute';; esac
umask 077
parent=$home/runtime/$version
cache=$parent/$target
mkdir -p "$parent" || fail 'cannot create runtime cache'
checksum() {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d ' ' -f 1
    elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d ' ' -f 1
    else return 1; fi
}
install_runtime() {
    [ "${RIG_OFFLINE+x}" != x ] || fail 'Rig is offline and the pinned runtime is not cached'
    lock=$parent/$target.lock
    waited=0
    until mkdir "$lock" 2>/dev/null; do
        # A host can start its SessionStart hook and MCP server concurrently.
        # Only the owner downloads. Each consumer still verifies the cache.
        [ ! -d "$cache" ] || return 0
        [ -d "$lock" ] || [ -w "$parent" ] || fail 'cannot acquire the runtime setup lock'
        [ "$waited" -lt 50 ] || fail "runtime setup did not finish; remove $lock only after confirming setup has stopped"
        sleep 1
        waited=$((waited + 1))
    done
    if [ -d "$cache" ]; then
        rmdir "$lock"
        return 0
    fi
    tmp=$lock/download
    mkdir "$tmp"
    trap 'rm -rf "$lock"' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    asset=rig-$target
    base=https://downloads.rig.ai/releases/04e862f86ebed23d38c76486c827e7301876500a/45286483914001
    printf 'Rig: downloading pinned runtime %s (%s).\n' "$version" "$target" >&2
    if [ -f "$root/runtime-SHA256SUMS" ]; then
        cp "$root/runtime-SHA256SUMS" "$tmp/SHA256SUMS"
    else
        curl --disable --fail --location --silent --show-error --proto '=https' --proto-redir '=https' \
        --connect-timeout 10 --max-time 15 --max-filesize 8192 \
        "$base/SHA256SUMS" --output "$tmp/SHA256SUMS" || fail 'release checksums unavailable; the pinned release must be published first'
    fi
    expected=$(awk -v name="$asset" '$2 == name {print $1}' "$tmp/SHA256SUMS")
    case "$expected" in ''|*[!0-9a-f]*) fail 'invalid release checksum';; esac
    [ "${#expected}" -eq 64 ] || fail 'missing or duplicate release checksum'
    curl --disable --fail --location --silent --show-error --proto '=https' --proto-redir '=https' \
        --connect-timeout 10 --max-time 45 --max-filesize 100000000 \
        "$base/$asset" --output "$tmp/rig" || fail 'runtime download failed'
    actual=$(checksum "$tmp/rig") || fail 'SHA-256 utility unavailable'
    [ "$actual" = "$expected" ] || fail 'runtime checksum mismatch; executable was not run'
    printf '%s\n' "$expected" > "$tmp/rig.sha256"
    rm "$tmp/SHA256SUMS"
    chmod 700 "$tmp/rig"
    mv "$tmp" "$cache" || fail 'cannot install verified runtime atomically'
    rm -rf "$lock"
    trap - EXIT INT TERM
}
[ -d "$cache" ] || install_runtime
[ -f "$cache/rig" ] && [ -f "$cache/rig.sha256" ] || fail 'incomplete runtime cache; remove this version cache and retry'
actual=$(checksum "$cache/rig") || fail 'cannot verify cached runtime'
[ "$actual" = "$(cat "$cache/rig.sha256")" ] || fail 'cached runtime changed; remove this version cache and retry'
if [ -f "$root/runtime-SHA256SUMS" ]; then
    expected=$(awk -v name="rig-$target" '$2 == name {print $1}' "$root/runtime-SHA256SUMS")
    [ "$actual" = "$expected" ] || fail 'cached runtime differs from selected release; reinstall the Rig plugin'
fi
[ -x "$cache/rig" ] || fail 'runtime is not executable; remove this version cache and retry'
if [ "$source_revision" != unreleased ]; then
    [ "$("$cache/rig" --build-revision)" = "$source_revision" ] || fail 'runtime source revision mismatch; reinstall the Rig plugin'
    [ "$("$cache/rig" --version)" = "rig $runtime_version" ] || fail 'runtime version mismatch; reinstall the Rig plugin'
fi
printf 'Rig plugin %s; runtime %s; source %s; executable %s\n' "$version" "$runtime_version" "$source_revision" "$cache/rig" >&2
if [ "$agent_contract" != unreleased ]; then
    exec "$cache/rig" --require-agent-contract "$agent_contract" --require-release "$runtime_version" "$@"
fi
exec "$cache/rig" "$@"
