param(
    [switch]$RunTests
)

Write-Host "Starting build-all script (PowerShell)"

# Detect JDK21 installation (Adoptium common path)
$jdk = Get-ChildItem 'C:\Program Files\Eclipse Adoptium' -Directory -Filter 'jdk-21*' -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $jdk) {
    $jdk = Get-ChildItem 'C:\Program Files' -Directory -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'jdk-21*' } | Select-Object -First 1
}
if ($jdk) {
    $env:JAVA_HOME = $jdk.FullName
    Write-Host "Using JAVA_HOME:" $env:JAVA_HOME
    $env:Path = "$env:JAVA_HOME\bin;" + $env:Path
} else {
    Write-Host "No JDK21 detected; using existing JAVA_HOME or system java." -ForegroundColor Yellow
}

# Detect Maven (M2_HOME) in common download location
$m2 = 'C:\Users\bueno\Downloads\apache-maven-3.9.11-bin\apache-maven-3.9.11'
if (Test-Path $m2) {
    $env:M2_HOME = $m2
    $env:Path = "$env:M2_HOME\bin;" + $env:Path
    Write-Host "Using M2_HOME:" $env:M2_HOME
}

$skipTests = $true -and -not $RunTests
if ($RunTests) { $buildArg = '' } else { $buildArg = '-DskipTests' }

function Run-BuildModule($modulePath) {
    Write-Host "\nBuilding module: $modulePath"
    if (Test-Path (Join-Path $modulePath 'mvnw')) {
        Write-Host "Found mvnw — using wrapper"
        & "$modulePath\mvnw" $buildArg clean package
    } else {
        Write-Host "Using system mvn"
        Push-Location $modulePath
        mvn $buildArg clean package
        Pop-Location
    }
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
# Adjust if script invoked from scripts/
$repoRoot = Resolve-Path (Join-Path $root '..')

Run-BuildModule (Join-Path $repoRoot 'backend\microservicio-dispositivos')
Run-BuildModule (Join-Path $repoRoot 'backend\microservicio-usuarios')

Write-Host "\nBuild-all finished"
