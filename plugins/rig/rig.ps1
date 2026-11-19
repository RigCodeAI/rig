# Thin native Windows bootstrap for the host-owned pinned plugin runtime.
# The public plugin package supplies the immutable checksum; PATH Rig is unused.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = New-Object Text.UTF8Encoding($false)
[Console]::OutputEncoding = New-Object Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$runtimeVersion = 'unreleased'
$sourceRevision = 'unreleased'
$runtimeBase = 'unreleased'
$pluginArguments = $args
$env:RIG_PLUGIN_ROOT = $PSScriptRoot
try {
    $pluginVersion = ([IO.File]::ReadAllText((Join-Path $PSScriptRoot 'runtime-version'))).Trim()
    if ($pluginVersion -cnotmatch '^\d+\.\d+\.\d+$' -or $runtimeVersion -eq 'unreleased') {
        throw 'Reinstall a published Windows-capable Rig plugin'
    }
    if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64' -or $env:PROCESSOR_ARCHITEW6432 -eq 'ARM64') {
        throw 'Rig plugin supports Windows x64'
    }
    $asset = 'rig-x86_64-pc-windows-msvc.exe'
    $checksums = [IO.File]::ReadAllLines((Join-Path $PSScriptRoot 'runtime-SHA256SUMS'))
    $matches = @($checksums | Where-Object { $_ -cmatch ('^[a-f0-9]{64}  ' + [Regex]::Escape($asset) + '$') })
    if ($matches.Count -ne 1) { throw 'Windows runtime is absent from this plugin release' }
    $expected = $matches[0].Substring(0,64)
    $homeRoot = if ($env:RIG_HOME) { $env:RIG_HOME } elseif ($env:RIG_CONFIG_HOME) { $env:RIG_CONFIG_HOME } else { Join-Path $env:USERPROFILE '.rig' }
    if (-not [IO.Path]::IsPathRooted($homeRoot)) { throw 'RIG_HOME must be absolute' }
    $parent = Join-Path $homeRoot ('runtime\' + $pluginVersion)
    $cache = Join-Path $parent 'x86_64-pc-windows-msvc'
    $binary = Join-Path $cache 'rig.exe'
    function Assert-Regular([string] $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Unexpected runtime file type' }
    }
    function Get-Digest([string] $Path) {
        Assert-Regular $Path
        # Use the .NET baseline even when a PowerShell 7 parent supplies a
        # PSModulePath that hides Windows PowerShell 5.1's Get-FileHash function.
        $stream = [IO.File]::OpenRead($Path)
        $sha = [Security.Cryptography.SHA256]::Create()
        try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
        finally { $sha.Dispose(); $stream.Dispose() }
    }
    if (-not (Test-Path -LiteralPath $cache)) {
        if (Test-Path Env:RIG_OFFLINE) { throw 'Rig is offline and its pinned runtime is not cached' }
        [IO.Directory]::CreateDirectory($parent) | Out-Null
        $lock = $null
        $deadline = [DateTime]::UtcNow.AddSeconds(120)
        while ($null -eq $lock) {
            try { $lock = [IO.File]::Open((Join-Path $parent 'windows-runtime.lock'), 'OpenOrCreate', 'ReadWrite', 'None') }
            catch [IO.IOException] {
                if ([DateTime]::UtcNow -gt $deadline) { throw 'Pinned runtime setup is busy; retry in a new session' }
                Start-Sleep -Milliseconds 100
            }
        }
        $stage = Join-Path $parent ('windows-stage-' + [Guid]::NewGuid().ToString('N'))
        try {
            if (-not (Test-Path -LiteralPath $cache)) {
                [IO.Directory]::CreateDirectory($stage) | Out-Null
                $next = Join-Path $stage 'rig.exe'
                $curl = Join-Path $env:SystemRoot 'System32\curl.exe'
                & $curl --disable --fail --location --silent --show-error --proto '=https' --proto-redir '=https' --connect-timeout 10 --max-time 90 --max-filesize 100000000 --output $next ($runtimeBase + '/' + $asset)
                if ($LASTEXITCODE -ne 0 -or (Get-Digest $next) -cne $expected) { throw 'Pinned runtime download failed verification' }
                [IO.Directory]::Move($stage, $cache)
            }
        } finally {
            $lock.Dispose()
            if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
        }
    }
    if ((Get-Digest $binary) -cne $expected) { throw 'Pinned runtime changed; remove this version cache and retry' }
    if ((& $binary --build-revision) -cne $sourceRevision -or (& $binary --version) -cne ('rig ' + $runtimeVersion)) { throw 'Pinned runtime identity differs from this plugin' }
    & $binary --require-agent-contract 1 --require-release $runtimeVersion @pluginArguments
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine('Rig runtime setup failed: ' + $_.Exception.Message)
    if ($pluginArguments.Count -ge 2 -and $pluginArguments[0] -eq 'plugin' -and $pluginArguments[1] -eq 'hook') {
        [Console]::WriteLine('{"systemMessage":"Rig runtime is unavailable; verification did not run. Retry setup in a new session."}')
        exit 0
    }
    exit 2
}
