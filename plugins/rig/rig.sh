#!/bin/sh
# Thin pre-Rust bootstrap. Product behavior lives in the pinned Rig executable.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
RIG_PLUGIN_ROOT=$root
export RIG_PLUGIN_ROOT
version=$(cat "$root/runtime-version")
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
case "$version" in ''|*[!0-9.]*|.*) fail 'invalid pinned runtime version';; esac
case "$(uname -s)/$(uname -m)" in
    Darwin/arm64) target=aarch64-apple-darwin;;
    Darwin/x86_64) target=x86_64-apple-darwin;;
    Linux/aarch64|Linux/arm64) target=aarch64-unknown-linux-gnu;;
    Linux/x86_64) target=x86_64-unknown-linux-gnu;;
    *) fail 'native plugin delivery supports Linux/macOS x64/arm64 only';;
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
if [ ! -d "$cache" ]; then
    lock=$parent/$target.lock
    mkdir "$lock" 2>/dev/null || fail 'runtime setup is already running; retry after it finishes'
    tmp=$lock/download
    mkdir "$tmp"
    trap 'rm -rf "$lock"' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    asset=rig-$target
    base=https://downloads.rig.ai/releases/67df8e187716ebed85cee517d3f7da846ed3ca1c/42028424211001
    printf 'Rig: downloading pinned runtime %s (%s).\n' "$version" "$target" >&2
    if [ -f "$root/runtime-SHA256SUMS" ]; then
        cp "$root/runtime-SHA256SUMS" "$tmp/SHA256SUMS"
    else
        curl --fail --location --silent --show-error --proto '=https' --proto-redir '=https' \
            --connect-timeout 10 --max-time 15 --max-filesize 8192 \
            "$base/SHA256SUMS" --output "$tmp/SHA256SUMS" || fail 'release checksums unavailable; the pinned release must be published first'
    fi
    expected=$(awk -v name="$asset" '$2 == name {print $1}' "$tmp/SHA256SUMS")
    case "$expected" in ''|*[!0-9a-f]*) fail 'invalid release checksum';; esac
    [ "${#expected}" -eq 64 ] || fail 'missing or duplicate release checksum'
    curl --fail --location --silent --show-error --proto '=https' --proto-redir '=https' \
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
fi
[ -f "$cache/rig" ] && [ -f "$cache/rig.sha256" ] || fail 'incomplete runtime cache; remove this version cache and retry'
actual=$(checksum "$cache/rig") || fail 'cannot verify cached runtime'
[ "$actual" = "$(cat "$cache/rig.sha256")" ] || fail 'cached runtime changed; remove this version cache and retry'
exec "$cache/rig" "$@"
