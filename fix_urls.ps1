# Script para corrigir todas as referências de URL antigas
$projectPath = "c:\Users\Rafae\Desktop\ENG.Software [2025]\(05.01) NAES\AdoptM3"

# Lista de substituições a fazer
$replacements = @{
    "{% url 'records-CreateState' %}" = "{% url 'records:StateCreate' %}"
    "{% url 'records-UpdateState'" = "{% url 'records:StateUpdate'"
    "{% url 'records-DeleteState'" = "{% url 'records:StateDelete'"
    "{% url 'records-ListState' %}" = "{% url 'records:StateList' %}"
    
    "{% url 'records-CreateCity' %}" = "{% url 'records:CityCreate' %}"
    "{% url 'records-UpdateCity'" = "{% url 'records:CityUpdate'"
    "{% url 'records-DeleteCity'" = "{% url 'records:CityDelete'"
    "{% url 'records-ListCity' %}" = "{% url 'records:CityList' %}"
    
    "{% url 'records-CreateAddress' %}" = "{% url 'records:AddressCreate' %}"
    "{% url 'records-UpdateAddress'" = "{% url 'records:AddressUpdate'"
    "{% url 'records-DeleteAddress'" = "{% url 'records:AddressDelete'"
    "{% url 'records-ListAddress' %}" = "{% url 'records:AddressList' %}"
    
    "{% url 'records-CreateAdoption' %}" = "{% url 'records:AdoptionCreate' %}"
    "{% url 'records-UpdateAdoption'" = "{% url 'records:AdoptionUpdate'"
    "{% url 'records-DeleteAdoption'" = "{% url 'records:AdoptionDelete'"
    "{% url 'records-ListAdoption' %}" = "{% url 'records:AdoptionList' %}"
    
    "{% url 'records-CreateAdoptionRelic' %}" = "{% url 'records:AdoptionRelicCreate' %}"
    "{% url 'records-UpdateAdoptionRelic'" = "{% url 'records:AdoptionRelicUpdate'"
    "{% url 'records-DeleteAdoptionRelic'" = "{% url 'records:AdoptionRelicDelete'"
    "{% url 'records-ListAdoptionRelic' %}" = "{% url 'records:AdoptionRelicList' %}"
}

# Buscar todos os arquivos .html no diretório de templates
$templateFiles = Get-ChildItem -Path "$projectPath\records\templates" -Recurse -Filter "*.html"

Write-Host "Processando $($templateFiles.Count) arquivos de template..."

foreach ($file in $templateFiles) {
    $content = Get-Content $file.FullName -Raw
    $changed = $false
    
    foreach ($old in $replacements.Keys) {
        $new = $replacements[$old]
        if ($content.Contains($old)) {
            $content = $content.Replace($old, $new)
            $changed = $true
            Write-Host "Substituindo '$old' por '$new' em $($file.Name)"
        }
    }
    
    if ($changed) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "Arquivo $($file.Name) atualizado!"
    }
}

Write-Host "Processo concluído!"
