# Controllo privilegi in PowerShell
If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
    ).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
  Write-Warning "Lo script deve essere eseguito come amministratore."
  exit 1
}

$svc = New-Object -ComObject Microsoft.Update.ServiceManager
$svc.AddService2('7971f918-a847-4430-9279-4a52d1efe18d',7,'')

Write-Host "Cerco aggiornamenti driver..."
$sess = New-Object -ComObject Microsoft.Update.Session
$searcher = $sess.CreateUpdateSearcher()
$res = $searcher.Search("IsInstalled=0 and Type='Driver' and IsHidden=0")

If ($res.Updates.Count -eq 0) {
  Write-Host "Nessun aggiornamento driver trovato."
  exit 0
}

$col = New-Object -ComObject Microsoft.Update.UpdateColl
For ($i = 0; $i -lt $res.Updates.Count; $i++) {
  $u = $res.Updates.Item($i)
  If (-not $u.EulaAccepted) { $u.AcceptEula() }
  $col.Add($u) | Out-Null
}

Write-Host "Scarico e installo $($col.Count) aggiornamenti..."

# Barra di progresso per il download
$dl = $sess.CreateUpdateDownloader()
$dl.Updates = $col
$dl.Download()
For ($i = 0; $i -lt $col.Count; $i++) {
    $percent = ($i / $col.Count) * 100
    Write-Progress -Activity "Download aggiornamenti" -Status "Scaricamento $($i+1) di $($col.Count)" -PercentComplete $percent
}
Write-Progress -Activity "Download completato" -Status "Tutti gli aggiornamenti sono stati scaricati." -PercentComplete 100

# Barra di progresso per l'installazione
$inst = $sess.CreateUpdateInstaller()
$inst.Updates = $col
$r = $inst.Install()
For ($i = 0; $i -lt $col.Count; $i++) {
    $percent = ($i / $col.Count) * 100
    Write-Progress -Activity "Installazione aggiornamenti" -Status "Installazione $($i+1) di $($col.Count)" -PercentComplete $percent
}
Write-Progress -Activity "Installazione completata" -Status "Tutti gli aggiornamenti sono stati installati." -PercentComplete 100

If ($r.RebootRequired) {
  Write-Warning "Riavvio richiesto."
  exit 2
}

Write-Host "Installazione completata."
exit 0
