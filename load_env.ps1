# Load-Env.ps1
$envFilePath = ".env"

if (-Not (Test-Path $envFilePath)) {
    Write-Error ".env file not found at path: $envFilePath"
    exit 1
}

Get-Content $envFilePath | ForEach-Object {
    $line = $_.Trim()
    
    # Skip empty lines and comments
    if ($line -eq "" -or $line.StartsWith("#")) {
        return
    }

    # Match KEY=VALUE (value may be quoted or unquoted)
    if ($line -match '^\s*([^=]+?)\s*=\s*(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()

        # Remove surrounding quotes if present
        if ($value.StartsWith('"') -and $value.EndsWith('"')) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        # Set environment variable
        [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
    }
}
