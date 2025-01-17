import http.server
import socket
import socketserver
import threading
import urllib.parse
from pathlib import Path

import pypub


def find_available_port():
    """Find an available port on the system."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(("", 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """A custom HTTP request handler that serves files from a specified directory."""

    def translate_path(self, path):
        """Translate a URL path to a local file path."""
        # Get the base path from the server instance
        root_path = self.server.base_path
        # Decode the URL path
        path = urllib.parse.unquote(path)
        # Join the root path with the requested path
        full_path = root_path / path.lstrip("/")  # Ensure no leading slash
        return str(full_path)


def run_server(path: Path, port: int):
    """Run a simple HTTP server."""
    Handler = MyHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    httpd.base_path = path
    return httpd


def generate_epub(tree, destination_path: Path, build_path: Path, title="HiPEAC Vision") -> bytes:
    """Generate an epub from a tree of sections and items."""
    epub = pypub.Epub(
        title=title,
        creator="HiPEAC",
        language="en",
        publisher="HiPEAC",
        cover=str(destination_path / "cover.jpg"),
    )

    port = find_available_port()
    httpd = run_server(destination_path, port)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://localhost:{port}"

    print(f"Server running on http://localhost:{port}")

    try:
        for section in tree:
            for item in section["items"]:
                html = item.export(format="html", v=4).decode("utf-8")
                html = html.replace("./images/", f"{base_url}/images/")
                chapter = pypub.create_chapter_from_html(html.encode("utf-8"))
                chapter.title = item.title
                epub.add_chapter(chapter)

        epub.create(build_path)

        return build_path

    finally:
        print("Shutting down server...")
        httpd.shutdown()
        server_thread.join()  # Wait for the thread to finish
        print("Server stopped.")
