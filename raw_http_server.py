import socket

HOST = "127.0.0.1"
PORT = 8080

def parse_http_request(raw_data: str):
    """Splits raw text into Method, Path, Protocol, Headers, and Body."""
    lines = raw_data.split("\r\n")
    if not lines or not lines[0]:
        return None, None, None, {}, ""

    # Request Line: "GET /hello HTTP/1.1"
    request_line = lines[0].split(" ")
    method = request_line[0]
    path = request_line[1] if len(request_line) > 1 else "/"
    version = request_line[2] if len(request_line) > 2 else "HTTP/1.1"

    # Headers
    headers = {}
    idx = 1
    while idx < len(lines) and lines[idx] != "":
        header_line = lines[idx]
        if ": " in header_line:
            key, val = header_line.split(": ", 1)
            headers[key] = val
        idx += 1

    # Body (everything after the blank line delimiter)
    body = "\r\n".join(lines[idx + 1 :])
    return method, path, version, headers, body

def run_server():
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] Raw TCP Server listening on http://{HOST}:{PORT}")

    while True:
        client_conn, client_addr = server_socket.accept()
        raw_request = client_conn.recv(4096).decode("utf-8")
        if not raw_request:
            client_conn.close()
            continue

        method, path, version, headers, body = parse_http_request(raw_request)

        # Basic routing
        if path == "/health":
            response_body = '{"status": "ok", "engine": "raw_socket"}'
            status_line = "HTTP/1.1 200 OK\r\n"
        else:
            response_body = f"<h1>SyncEngine Raw Gateway</h1><p>Method: {method}</p><p>Path: {path}</p>"
            status_line = "HTTP/1.1 200 OK\r\n"

        # Construct raw HTTP/1.1 wire response
        response_headers = (
            f"Content-Type: {'application/json' if path == '/health' else 'text/html'}\r\n"
            f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
            "Connection: close\r\n\r\n"
        )

        full_response = status_line + response_headers + response_body
        client_conn.sendall(full_response.encode("utf-8"))
        client_conn.close()

if __name__ == "__main__":
    run_server()