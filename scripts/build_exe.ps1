Param(
    [switch]$Gui,
    [switch]$Cli,
    [string]$Name = "Timerzone",
    [string]$Icon,
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg) { Write-Host "[ OK ] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg) { Write-Host "[ERR ] $msg" -ForegroundColor Red }

try {
    $root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
    Set-Location $root

    if (-not ($Gui -or $Cli)) { $Gui = $true }

    $venvPath = Join-Path $root ".venv"
    $pythonExe = Join-Path $venvPath "Scripts/python.exe"
    $pipExe = Join-Path $venvPath "Scripts/pip.exe"

    if ($Clean) {
        Write-Info "Limpando pastas de build anteriores..."
        if (Test-Path "$root/build") { Remove-Item -Recurse -Force "$root/build" }
        if (Test-Path "$root/dist") { Remove-Item -Recurse -Force "$root/dist" }
        Get-ChildItem $root -Filter "*.spec" | ForEach-Object { Remove-Item -Force $_.FullName }
    }

    if (-not (Test-Path $venvPath)) {
        Write-Info "Criando ambiente virtual (.venv)..."
        $pyLauncher = (Get-Command py -ErrorAction SilentlyContinue)
        if ($pyLauncher) {
            & $pyLauncher.Source -3 -m venv "$venvPath"
        } else {
            & python -m venv "$venvPath"
        }
    } else {
        Write-Info ".venv já existe."
    }

    if (-not (Test-Path $pythonExe)) {
        throw "Python do venv não encontrado em $pythonExe"
    }

    Write-Info "Instalando dependências..."
    if (Test-Path "$root/requirements.txt") {
        & $pythonExe -m pip install --upgrade pip
        & $pipExe install -r "$root/requirements.txt"
    } else {
        Write-Warn "requirements.txt não encontrado; seguindo em frente."
    }

    Write-Info "Instalando PyInstaller..."
    & $pipExe install pyinstaller

    $addData = @()
    if (Test-Path "$root/config.json") {
        $addData += "--add-data", "config.json;."
    }

    $iconArgs = @()
    if ($Icon) {
        if (-not (Test-Path $Icon)) {
            Write-Warn "Ícone não encontrado: $Icon. Ignorando."
        } else {
            $iconArgs += "--icon", (Resolve-Path $Icon).Path
        }
    }

    $builtAny = $false

    if ($Gui) {
        Write-Info "Verificando suporte ao tkinter..."
        & $pythonExe -c "import tkinter, tkinter.ttk; print('tkinter OK')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Err "tkinter não está disponível nesta instalação do Python."
            Write-Host "Sugestões:" -ForegroundColor Yellow
            Write-Host " - Instale o Python oficial de python.org (inclui Tcl/Tk)" -ForegroundColor Yellow
            Write-Host " - Ou reinstale o Python garantindo a opção 'tcl/tk and IDLE'" -ForegroundColor Yellow
            throw "Dependência ausente: tkinter"
        }
        Write-Info "Gerando EXE GUI a partir de ui.py..."
        $hiddenTk = @("--hidden-import","tkinter","--hidden-import","tkinter.ttk")
        & $pythonExe -m PyInstaller --noconfirm --onefile --windowed `
            --name $Name @iconArgs @addData @hiddenTk `
            "$root/ui.py"
        $builtAny = $true
    }

    if ($Cli) {
        $cliName = if ($Gui) { "${Name}CLI" } else { $Name }
        Write-Info "Gerando EXE CLI a partir de main.py..."
        & $pythonExe -m PyInstaller --noconfirm --onefile --console `
            --name $cliName @iconArgs @addData `
            "$root/main.py"
        $builtAny = $true
    }

    if (-not $builtAny) {
        throw "Nenhuma saída selecionada. Use -Gui e/ou -Cli."
    }

    $dist = Join-Path $root "dist"
    if (Test-Path $dist) {
        Write-Ok "Build concluído. Arquivos em: $dist"
        Get-ChildItem $dist -Filter "*.exe" | ForEach-Object { Write-Host " - " $_.FullName }
    } else {
        Write-Err "Falha: pasta dist não encontrada. Verifique mensagens do PyInstaller acima."
        exit 1
    }

    Write-Host "\nDica: Para executar, abra o arquivo .exe dentro de 'dist'." -ForegroundColor Gray
}
catch {
    Write-Err $_
    exit 1
}


