from http.server import (
    HTTPServer,
    ThreadingHTTPServer,
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
    CGIHTTPRequestHandler,
)
from sys import exit
from threading import Thread
import traceback


def run_threaded(httpd: HTTPServer):
    try:
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        print(f"Thread: {thread}")
        print(f"PID: {thread.native_id}")
        thread.join()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down server.")
        httpd.shutdown()
        thread.join()
        exit(0)
    except:
        print("\nException detected, shutting down server.")
        httpd.shutdown()
        thread.join()
        print(traceback.format_exc())
        exit(1)
    print("done")


def run(httpd: HTTPServer):
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        exit(0)


if __name__ == "__main__":
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass = ThreadingHTTPServer
    # protocol = "HTTP/1.0"
    port = 8000
    bind = None
    # ServerClass.address_family, addr = _get_best_family(bind, port)
    # HandlerClass.protocol_version = protocol
    with ServerClass(("", port), HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f"[{host}]" if ":" in host else host
        print(f"Serving HTTP on {host} port {port} (http://{url_host}:{port}/) ...")
        run_threaded(httpd)
