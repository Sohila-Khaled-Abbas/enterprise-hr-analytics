<#
.SYNOPSIS
    Enterprise HR Analytics Platform Developer Automation Script
.DESCRIPTION
    One-click runner for environment setup, tests, migrations, pipeline execution, and container orchestration.
.EXAMPLE
    .\run.ps1 healthcheck
    .\run.ps1 migrate
    .\run.ps1 pipeline
    .\run.ps1 test
    .\run.ps1 docker-up
#>

param (
    [Parameter(Position = 0)]
    [ValidateSet("help", "healthcheck", "migrate", "pipeline", "summary", "test", "docker-up", "docker-down")]
    [string]$Command = "help"
)

$env:PYTHONPATH = "src"

function Show-Help {
    Write-Host "══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "💎 Nexora Tech Solutions · Enterprise HR Analytics Automation CLI" -ForegroundColor White
    Write-Host "══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "Usage: .\run.ps1 <command>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available Commands:" -ForegroundColor White
    Write-Host "  healthcheck   - Verify SQL Server connection and raw dataset files"
    Write-Host "  migrate       - Run idempotent T-SQL DDL schema migrations (00..04)"
    Write-Host "  pipeline      - Execute complete end-to-end data pipeline"
    Write-Host "  summary       - Print live production database table inventory"
    Write-Host "  test          - Run full automated pytest suite (29 tests)"
    Write-Host "  docker-up     - Spin up SQL Server 2022 and pipeline worker via Docker"
    Write-Host "  docker-down   - Stop and tear down Docker containers and volumes"
    Write-Host "══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
}

switch ($Command) {
    "healthcheck" {
        Write-Host "▶ Running healthcheck..." -ForegroundColor Green
        python -m enterprise_hr.cli healthcheck
    }
    "migrate" {
        Write-Host "▶ Applying database migrations..." -ForegroundColor Green
        python -m enterprise_hr.cli migrate
    }
    "pipeline" {
        Write-Host "▶ Executing end-to-end pipeline..." -ForegroundColor Green
        python -m enterprise_hr.cli run
    }
    "summary" {
        Write-Host "▶ Querying production DWH table inventory..." -ForegroundColor Green
        python -m enterprise_hr.cli summary
    }
    "test" {
        Write-Host "▶ Running automated quality assurance test suite..." -ForegroundColor Green
        python -m pytest tests/ -v
    }
    "docker-up" {
        Write-Host "▶ Spinning up Docker Compose stack..." -ForegroundColor Green
        docker compose up --build
    }
    "docker-down" {
        Write-Host "▶ Stopping Docker Compose stack..." -ForegroundColor Yellow
        docker compose down -v
    }
    default {
        Show-Help
    }
}
