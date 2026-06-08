<#
PowerShell helper: cleans secret from history or creates a clean branch and pushes.
Run in repository root with your venv activated.
Usage examples:
  .\scripts\cleanup_and_push.ps1         -> interactive
  .\scripts\cleanup_and_push.ps1 -Mode rewrite -Secret "<EXACT_SECRET>" -RemoteUrl "https://github.com/venky0112/Antarman-AI.git" -Branch main
#>
param(
    [ValidateSet('rewrite','clean-branch')]
    [string]$Mode = 'rewrite',
    [string]$Secret = '',
    [string]$RemoteUrl = '',
    [string]$Branch = 'main'
)
function Run-Command($cmd) {
    Write-Host "==> $cmd" -ForegroundColor Cyan
    & cmd /c $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Command failed: $cmd" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}
if (-not $RemoteUrl) {
    $RemoteUrl = Read-Host 'Remote URL (e.g. https://github.com/you/repo.git)'
}
if ($Mode -eq 'rewrite') {
    if (-not $Secret) { $Secret = Read-Host 'Exact secret string to remove (paste full token)'}
    if (-not $Secret) { Write-Host 'Secret required for rewrite mode.' -ForegroundColor Red; exit 1 }
    Write-Host "Creating backup branch 'backup-before-clean'..."
    git branch -M backup-before-clean 2>$null || Write-Host 'backup branch renamed/exists' -ForegroundColor Yellow
    Write-Host "Writing replacements.txt (temporary)..."
    "$Secret==>REDACTED_GEMINI_KEY" | Out-File -Encoding utf8 replacements.txt
    Write-Host 'Ensure python and git-filter-repo are available (will attempt to install)...'
    python -m pip install --user git-filter-repo
    Write-Host 'Running git-filter-repo (this will rewrite history)...'
    git filter-repo --replace-text replacements.txt --force
    Write-Host 'Verifying no occurrences remain...'
    git log -S "$($Secret.Substring(0,[Math]::Min(20,$Secret.Length)))" --all --oneline
    if ($LASTEXITCODE -eq 0) {
        Write-Host 'Search returned hits. Examine results and retry after fixing.' -ForegroundColor Red
        exit 2
    } else {
        Write-Host 'No hits. Cleaning up replacements file.' -ForegroundColor Green
        Remove-Item replacements.txt -ErrorAction Ignore
    }
    Write-Host 'Compressing repository...'
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    $confirm = Read-Host "Ready to force-push rewritten $Branch to $RemoteUrl? Type 'YES' to continue"
    if ($confirm -ne 'YES') { Write-Host 'Aborting push.'; exit 0 }
    git remote remove origin 2>$null
    git remote add origin $RemoteUrl
    git push --force origin $Branch
    Write-Host 'Force-push complete. Rotate the compromised key NOW.' -ForegroundColor Yellow
} else {
    Write-Host 'Creating a clean snapshot repo and pushing as cleaned-main...'
    $tmp = Join-Path $env:TEMP ('Antarman-AI-clean-'+[System.Guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path $tmp | Out-Null
    Write-Host "Copying files to $tmp (excluding .git)..."
    robocopy . $tmp /E /XD .git | Out-Null
    Push-Location $tmp
    git init
    git add .
    git commit -m "Clean snapshot without history (sanitized)"
    git branch -M cleaned-main
    git remote add origin $RemoteUrl
    git push -u origin cleaned-main
    Pop-Location
    Write-Host "Clean branch pushed as 'cleaned-main'." -ForegroundColor Green
    Write-Host 'If push blocked, search files in the copy for secrets and remove them then repeat.'
}
