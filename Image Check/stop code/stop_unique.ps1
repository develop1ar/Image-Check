Write-Output "Stopping unique_screen.py..."
Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -match "unique_screen\.py"
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force
    Write-Output "Stopped: unique_screen.py (PID: $($_.ProcessId))"
}
