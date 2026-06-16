$path = "C:\Users\paulo.arruda\.gemini\antigravity\brain\d41c0b71-b79c-424d-90ae-cd0d303d798e\.system_generated\logs\transcript.jsonl"
$content = Get-Content $path -Raw
$lines = $content -split "`n"
$jsonLines = @()
$inJson = $false

foreach ($line in $lines) {
  if ($line -match '```json') {
     $jsonStart = $line.IndexOf('```json') + 7
     $inJson = $true
     $line = $line.Substring($jsonStart)
  }
  
  if ($inJson) {
     if ($line -match '```') {
        $jsonEnd = $line.IndexOf('```')
        if ($jsonEnd -gt 0) {
           $jsonLines += $line.Substring(0, $jsonEnd)
        }
        $inJson = $false
        break
     } else {
        $jsonLines += $line
     }
  }
}

$jsonText = $jsonLines -join "`n"
Set-Content -Path "C:\Users\paulo.arruda\Desktop\econometria\questions_full.json" -Value $jsonText
Write-Host "Extraido"
