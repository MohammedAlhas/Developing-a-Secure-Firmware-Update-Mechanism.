# secure_https_server.py

from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to prevent logging each request
        return

def run(server_class=HTTPServer, handler_class=SecureHTTPRequestHandler, port=4443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older, insecure protocols
    context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')  # Use strong ciphers
    context.load_cert_chain(certfile='certs/cert.pem', keyfile='certs/key.pem')

    # Wrap the socket with the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f'Serving HTTPS on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
