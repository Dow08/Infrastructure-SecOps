# Déploiement AD - Provisioning OUs, Groupes et Utilisateurs
# A exécuter sur le DC cible avec les droits d'administration

Import-Module ActiveDirectory

$CurrentDomain = (Get-ADDomain).DNSRoot
$DomainDN = (Get-ADDomain).DistinguishedName
$CSVPath = "$PSScriptRoot\utilisateurs.csv"
$BaseOUName = "ENTREPRISE"
$DefaultPassword = ConvertTo-SecureString "CyberSec_2026!" -AsPlainText -Force

Write-Host "[*] Démarrage du provisioning sur : $CurrentDomain" -ForegroundColor Cyan

if (-not (Test-Path $CSVPath)) {
    Write-Host "[!] CSV introuvable : $CSVPath" -ForegroundColor Red
    Exit
}

$AllUsers = Import-Csv $CSVPath -Delimiter ","
$DomainUsers = $AllUsers | Where-Object { $_.Domaine -eq $CurrentDomain }

if ($DomainUsers.Count -eq 0) {
    Write-Host "[*] Aucun compte à créer sur ce domaine." -ForegroundColor Yellow
    Exit
}

# 1. OU Racine
$BaseOUPath = "OU=$BaseOUName,$DomainDN"
if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$BaseOUName'" -SearchBase $DomainDN -ErrorAction SilentlyContinue)) {
    New-ADOrganizationalUnit -Name $BaseOUName -Path $DomainDN -ProtectedFromAccidentalDeletion $true
    Write-Host "[+] OU Racine créée : $BaseOUName"
}

# 2. Provisioning
foreach ($User in $DomainUsers) {
    
    $OUName = $User.OU
    $OUPath = "OU=$OUName,$BaseOUPath"
    
    # OUs métiers
    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$OUName'" -SearchBase $BaseOUPath -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $OUName -Path $BaseOUPath -ProtectedFromAccidentalDeletion $true
    }

    # Groupes globaux (AGDLP)
    $GroupName = "GG-$OUName"
    if (-not (Get-ADGroup -Filter "Name -eq '$GroupName'" -SearchBase $OUPath -ErrorAction SilentlyContinue)) {
        New-ADGroup -Name $GroupName -GroupCategory Security -GroupScope Global -Path $OUPath
    }

    # Utilisateurs
    $SamAccountName = ($User.Prenom[0] + "." + $User.Nom).ToLower()
    $UPN = "$SamAccountName@$CurrentDomain"
    $DisplayName = "$($User.Prenom) $($User.Nom)"

    if (-not (Get-ADUser -Filter "SamAccountName -eq '$SamAccountName'" -ErrorAction SilentlyContinue)) {
        New-ADUser -Name $DisplayName `
                   -SamAccountName $SamAccountName `
                   -UserPrincipalName $UPN `
                   -Path $OUPath `
                   -AccountPassword $DefaultPassword `
                   -Enabled $true `
                   -PasswordNeverExpires $true `
                   -GivenName $User.Prenom `
                   -Surname $User.Nom `
                   -Description "Auto-provisioned"

        Add-ADGroupMember -Identity $GroupName -Members $SamAccountName
        Write-Host "  -> Utilisateur créé : $SamAccountName (Groupe: $GroupName)" -ForegroundColor Green
    }
}

Write-Host "[*] Provisioning terminé." -ForegroundColor Cyan