# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

[CmdletBinding()]
param(
    [ValidateSet('Core', 'Loaders', 'Checks', 'GameTests', 'Focused')]
    [string]$Stage = 'Core',
    [string]$Workspace = 'C:\Sandbox\Codex\Workspaces\CCLuau',
    [string]$JavaHome,
    [ValidatePattern('^[A-Za-z0-9-]+$')]
    [string]$RunId = 'M1-20261015',
    [ValidateRange(1, 4)]
    [int]$Workers = 2,
    [ValidateRange(1, 60)]
    [int]$TimeoutMinutes = 30
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$Workspace = (Resolve-Path -LiteralPath $Workspace).Path
if (-not $Workspace.StartsWith('C:\Sandbox\Codex\Workspaces\', [StringComparison]::OrdinalIgnoreCase)) {
    throw '[Baseline:Runner] Workspace must be inside the remote Codex workspace root'
}
if (-not (Test-Path -LiteralPath (Join-Path $Workspace 'gradlew.bat'))) {
    throw '[Baseline:Runner] Gradle wrapper not found'
}
if ($JavaHome) {
    if (-not (Test-Path -LiteralPath (Join-Path $JavaHome 'bin\java.exe'))) {
        throw '[Baseline:Runner] JavaHome does not contain bin\java.exe'
    }
    $env:JAVA_HOME = $JavaHome
}

$LogRoot = "C:\Sandbox\Codex\Logs\CCLuau\$RunId"
$env:GRADLE_USER_HOME = 'C:\Sandbox\Codex\Cache\CCLuau\Gradle'
New-Item -ItemType Directory -Force -Path $LogRoot,$env:GRADLE_USER_HOME | Out-Null
$env:JAVA_TOOL_OPTIONS = "-Djava.awt.headless=true -XX:ActiveProcessorCount=$Workers -XX:ErrorFile=$LogRoot\hs_err_pid%p.log"
$Tasks = switch ($Stage) {
    'Core' { '--configure-on-demand :core:assemble :core:test' }
    'Loaders' { ':fabric:assemble :forge:assemble' }
    'Checks' { 'check -x runGametest' }
    'GameTests' { ':fabric:runGametest :forge:runGametest' }
    'Focused' { '--configure-on-demand :core:test --tests dan200.computercraft.core.computer.BaselineTest' }
}

$Stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$Prefix = Join-Path $LogRoot "$Stamp-$Stage"
$Arguments = "--no-daemon --max-workers=$Workers --console=plain $Tasks"
$StartInfo = New-Object Diagnostics.ProcessStartInfo
$StartInfo.FileName = $env:ComSpec
$StartInfo.Arguments = '/d /c ""' + (Join-Path $Workspace 'gradlew.bat') + '" ' + $Arguments + '"'
$StartInfo.WorkingDirectory = $Workspace
$StartInfo.UseShellExecute = $false
$StartInfo.CreateNoWindow = $true
$StartInfo.RedirectStandardOutput = $true
$StartInfo.RedirectStandardError = $true
$Process = New-Object Diagnostics.Process
$Process.StartInfo = $StartInfo
$Timer = [Diagnostics.Stopwatch]::StartNew()
[void]$Process.Start()
$OutputFile = [IO.File]::Open("$Prefix.stdout.log", [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
$ErrorFile = [IO.File]::Open("$Prefix.stderr.log", [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
$Output = $Process.StandardOutput.BaseStream.CopyToAsync($OutputFile)
$Errors = $Process.StandardError.BaseStream.CopyToAsync($ErrorFile)
$TimedOut = -not $Process.WaitForExit($TimeoutMinutes * 60000)
if ($TimedOut) {
    # Terminate only the tree rooted at this runner's directly created process.
    $StopInfo = New-Object Diagnostics.ProcessStartInfo
    $StopInfo.FileName = 'taskkill.exe'
    $StopInfo.Arguments = "/PID $($Process.Id) /T /F"
    $StopInfo.UseShellExecute = $false
    $StopInfo.CreateNoWindow = $true
    $StopInfo.RedirectStandardOutput = $true
    $StopInfo.RedirectStandardError = $true
    $StopProcess = [Diagnostics.Process]::Start($StopInfo)
    $StopOutput = $StopProcess.StandardOutput.ReadToEndAsync()
    $StopErrors = $StopProcess.StandardError.ReadToEndAsync()
    $StopProcess.WaitForExit()
    $StopOutput.Result | Set-Content -LiteralPath "$Prefix.stop.log" -Encoding UTF8
    $StopErrors.Result | Add-Content -LiteralPath "$Prefix.stop.log" -Encoding UTF8
    $StopProcess.Dispose()
}
$Process.WaitForExit()
$Timer.Stop()
[void]$Output.GetAwaiter().GetResult()
[void]$Errors.GetAwaiter().GetResult()
$OutputFile.Dispose()
$ErrorFile.Dispose()
$ExitCode = if ($TimedOut) { 124 } else { $Process.ExitCode }
$Process.Dispose()

$ArtifactRoot = "C:\Sandbox\Codex\Artifacts\CCLuau\$RunId\$Stamp-$Stage"
New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null
foreach ($Project in Get-ChildItem -LiteralPath (Join-Path $Workspace 'projects') -Directory) {
    $Results = Join-Path $Project.FullName 'build\test-results'
    if (Test-Path -LiteralPath $Results) {
        Copy-Item -LiteralPath $Results -Destination (Join-Path $ArtifactRoot $Project.Name) -Recurse
    }
    if ($Stage -in @('Core', 'Loaders')) {
        $Libraries = Join-Path $Project.FullName 'build\libs'
        if (Test-Path -LiteralPath $Libraries) {
            $JarOutput = Join-Path $ArtifactRoot "$($Project.Name)-jars"
            New-Item -ItemType Directory -Force -Path $JarOutput | Out-Null
            Get-ChildItem -LiteralPath $Libraries -Filter '*.jar' | Copy-Item -Destination $JarOutput
        }
    }
}
$Inventory = Join-Path $Workspace 'projects\core\build\tmp\testFiles\baseline\CoreRuntimeInventory.json'
if (Test-Path -LiteralPath $Inventory) { Copy-Item -LiteralPath $Inventory -Destination $ArtifactRoot }

Push-Location -LiteralPath $Workspace
try {
    $Source = git rev-parse HEAD
    $Dirty = @(git status --porcelain)
} finally {
    Pop-Location
}
[ordered]@{
    Stage = $Stage
    Command = "gradlew.bat $Arguments"
    Source = $Source
    Dirty = $Dirty
    Workspace = $Workspace
    GradleUserHome = $env:GRADLE_USER_HOME
    JavaHome = $env:JAVA_HOME
    JavaToolOptions = $env:JAVA_TOOL_OPTIONS
    HostName = $env:COMPUTERNAME
    Workers = $Workers
    ExitCode = $ExitCode
    TimedOut = $TimedOut
    ElapsedSeconds = $Timer.Elapsed.TotalSeconds
    Stdout = "$Prefix.stdout.log"
    Stderr = "$Prefix.stderr.log"
    ArtifactRoot = $ArtifactRoot
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath "$Prefix.json" -Encoding UTF8
Write-Output "[Baseline:Runner] $Stage exit=$ExitCode seconds=$($Timer.Elapsed.TotalSeconds) metadata=$Prefix.json"
Get-Content -LiteralPath "$Prefix.stdout.log" -Tail 20
Get-Content -LiteralPath "$Prefix.stderr.log" -Tail 30
exit $ExitCode
