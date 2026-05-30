# Minimal static file server (raw sockets) for previewing the quiz app.
import sys, os, socket, threading

ROOT = r'C:\Users\Fajam\MyClaude\PMP-Quiz'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8731

TYPES = {'.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
         '.css':'text/css; charset=utf-8', '.json':'application/json'}

def handle(conn):
    try:
        data = b''
        while b'\r\n\r\n' not in data:
            chunk = conn.recv(4096)
            if not chunk: return
            data += chunk
        line = data.split(b'\r\n', 1)[0].decode('latin1')
        parts = line.split(' ')
        path = parts[1] if len(parts) > 1 else '/'
        path = path.split('?', 1)[0]
        if path == '/' or path == '':
            path = '/index.html'
        fp = os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
        if not fp.startswith(ROOT):
            conn.sendall(b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n'); return
        if not os.path.isfile(fp):
            conn.sendall(b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'); return
        with open(fp, 'rb') as f:
            body = f.read()
        ext = os.path.splitext(fp)[1].lower()
        ct = TYPES.get(ext, 'application/octet-stream')
        hdr = ('HTTP/1.1 200 OK\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n'
               % (ct, len(body))).encode('latin1')
        conn.sendall(hdr + body)
    except Exception:
        pass
    finally:
        try: conn.close()
        except Exception: pass

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('127.0.0.1', PORT))
srv.listen(50)
print('serving %s on http://127.0.0.1:%d' % (ROOT, PORT), flush=True)
while True:
    conn, _ = srv.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
