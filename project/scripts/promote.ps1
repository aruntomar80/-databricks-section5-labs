param([ValidateSet("dev","test","prod")][string]$Target = "test")
$ErrorActionPreference = "Stop"
Push-Location (Join-Path $PSScriptRoot "..")
try {
    databricks bundle validate -t $Target
    if ($LASTEXITCODE -ne 0) { throw "Validation failed; no deployment attempted." }
    databricks bundle deploy -t $Target
    if ($LASTEXITCODE -ne 0) { throw "Deployment failed; no job run attempted." }
    databricks bundle run -t $Target performance_job
    if ($LASTEXITCODE -ne 0) { throw "Smoke run failed; do not promote further." }
    databricks bundle summary -t $Target
    if ($LASTEXITCODE -ne 0) { throw "Could not obtain deployment summary." }
} finally { Pop-Location }
