# Documentacao: Usando WSL Ubuntu com PuTTY

Este guia registra o procedimento feito para abrir o Ubuntu no WSL, instalar o servidor SSH e conectar nele usando o PuTTY.

## 1. Verificar as distribuicoes WSL instaladas

No PowerShell, rode:

```powershell
wsl -l -v
```

Exemplo que apareceu:

```text
NAME              STATE    VERSION
* docker-desktop  Stopped  2
  Ubuntu          Stopped  2
```

Se o `docker-desktop` estiver com `*`, o comando `wsl` abre o ambiente do Docker, nao o Ubuntu. Esse ambiente pode nao ter `sudo` nem `apt`.

## 2. Definir Ubuntu como padrao

No PowerShell, rode:

```powershell
wsl --shutdown
wsl --update
wsl --set-default Ubuntu
```

Depois abra o Ubuntu:

```powershell
wsl -d Ubuntu
```

Se quiser, depois disso o comando abaixo tambem passa a abrir o Ubuntu:

```powershell
wsl
```

## 3. Se aparecer erro E_UNEXPECTED

Se o comando abaixo falhar:

```powershell
wsl -d Ubuntu
```

com erro parecido com:

```text
Falha catastrofica
Codigo de erro: Wsl/Service/E_UNEXPECTED
```

tente no PowerShell como Administrador:

```powershell
wsl --shutdown
wsl --update
wsl --set-default Ubuntu
```

Se ainda falhar:

```powershell
Restart-Service LxssManager
wsl -d Ubuntu
```

## 4. Criar o usuario Linux

Na primeira abertura do Ubuntu, ele pede:

```text
Create a default Unix user account:
```

Foi criado o usuario:

```text
ronaldo
```

Depois ele pede senha:

```text
New password:
Retype new password:
```

Importante: no Linux, ao digitar senha, nada aparece na tela. Nao aparecem letras, bolinhas nem asteriscos. Mesmo assim o teclado esta funcionando.

Se aparecer:

```text
Sorry, passwords do not match.
Try again? [y/N]
```

digite:

```text
y
```

e repita a senha com calma.

## 5. Pergunta sobre metricas do Ubuntu

O Ubuntu pode perguntar:

```text
Would you like to opt-in to platform metrics collection? [Y/n/e]:
```

Voce pode responder:

```text
n
```

para nao enviar metricas, ou:

```text
y
```

para enviar.

## 6. Atualizar pacotes do Ubuntu

Dentro do Ubuntu, rode:

```bash
sudo apt update
```

Quando pedir senha, digite a senha criada para o usuario `ronaldo`. A senha nao aparece na tela enquanto voce digita.

## 7. Instalar o servidor SSH

Dentro do Ubuntu:

```bash
sudo apt install openssh-server
```

Se perguntar:

```text
Continue? [Y/n]
```

digite:

```text
y
```

## 8. Iniciar o SSH

Depois da instalacao:

```bash
sudo service ssh start
```

Verifique o status:

```bash
sudo service ssh status
```

O resultado correto deve mostrar:

```text
Active: active (running)
Server listening on 0.0.0.0 port 22
Server listening on :: port 22
```

## 9. Abrir o PuTTY

No PuTTY, preencha:

```text
Host Name: 127.0.0.1
Port: 22
Connection type: SSH
```

Clique em `Open`.

Na primeira conexao, o PuTTY mostra um alerta de seguranca dizendo que a chave do servidor ainda nao esta salva. Como a conexao e com o proprio computador (`127.0.0.1`), clique em:

```text
Accept
```

## 10. Fazer login pelo PuTTY

Quando aparecer:

```text
login as:
```

digite:

```text
ronaldo
```

Depois digite a senha criada no Ubuntu. Novamente, a senha nao aparece na tela.

Se tudo der certo, aparecera algo parecido com:

```bash
ronaldo@DESKTOP-Q4TOCMV:~$
```

## 11. Comandos basicos para testar

Mostrar a pasta atual:

```bash
pwd
```

Listar arquivos:

```bash
ls
```

Listar em detalhes:

```bash
ls -l
```

Se aparecer:

```text
total 0
```

isso so significa que a pasta esta vazia.

Criar uma pasta de teste:

```bash
mkdir teste
ls -l
```

Entrar na pasta do Windows:

```bash
cd /mnt/c/Users/Felipe
```

Sair do PuTTY:

```bash
exit
```

## 12. Observacoes importantes

- Para usar o Ubuntu diretamente, use `wsl` ou `wsl -d Ubuntu` no PowerShell.
- O PuTTY nao abre o WSL diretamente; ele conecta no SSH que esta rodando dentro do Ubuntu.
- Se reiniciar o Windows ou desligar o WSL, talvez seja necessario iniciar o SSH novamente:

```bash
sudo service ssh start
```

- Se `sudo` ou `apt` nao existir, provavelmente voce esta no `docker-desktop`, nao no Ubuntu. Confira com:

```powershell
wsl -l -v
```

e abra o Ubuntu com:

```powershell
wsl -d Ubuntu
```

