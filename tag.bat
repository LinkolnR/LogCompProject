@echo off
setlocal

REM Verifica se foi fornecido exatamente um argumento
if "%~1"=="" (
    echo Uso: %0 ^<versão^>
    exit /b 1
)

REM Define a versão fornecida como variável
set "versao=%~1"

REM Substitui "x.x.x" pela versão fornecida nos comandos git
set "tag=v%versao%"
set "mensagem=Mensagem sobre o release %versao%"
set "comando_tag=git tag -a %tag% -m "%mensagem%""
set "comando_push=git push origin %tag%"

REM Executa os comandos git com a versão substituída
echo Executando: %comando_tag%
%comando_tag%
echo.
echo Executando: %comando_push%
%comando_push%

endlocal
