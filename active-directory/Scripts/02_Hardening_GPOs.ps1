# Déploiement automatisé des Stratégies de Groupe (Hardening)
# Ce script crée la GPO de restriction CMD et la lie à l'OU ENTREPRISE

Import-Module GroupPolicy

$GPOName = "SEC-Restreindre-CMD"
$TargetOU = "OU=ENTREPRISE," + (Get-ADDomain).DistinguishedName

Write-Host "[*] Début de la configuration des GPOs de sécurité..." -ForegroundColor Cyan

# 1. Création de la GPO si elle n'existe pas
if (-not (Get-GPO -Name $GPOName -ErrorAction SilentlyContinue)) {
    New-GPO -Name $GPOName -Comment "Désactivation de l'invite de commande et des scripts batch pour les utilisateurs" | Out-Null
    Write-Host "  [+] GPO '$GPOName' créée." -ForegroundColor Green
} else {
    Write-Host "  [i] La GPO '$GPOName' existe déjà." -ForegroundColor Yellow
}

# 2. Configuration de la clé de registre (Modèles d'administration -> Système -> Empêcher l'accès à l'invite de commande)
# La valeur '2' désactive CMD ET le traitement silencieux des scripts .bat/.cmd
Set-GPRegistryValue -Name $GPOName `
                    -Key "HKCU\Software\Policies\Microsoft\Windows\System" `
                    -ValueName "DisableCMD" `
                    -Type DWord `
                    -Value 2 | Out-Null

Write-Host "  [+] Paramètres de restriction appliqués au registre de la GPO." -ForegroundColor Green

# 3. Liaison de la GPO à l'OU cible
New-GPLink -Name $GPOName -Target $TargetOU -LinkEnabled Yes | Out-Null
Write-Host "  [+] GPO liée avec succès à l'OU : $TargetOU" -ForegroundColor Green

Write-Host "[*] Durcissement terminé. Les stratégies s'appliqueront au prochain redémarrage des postes." -ForegroundColor Cyan