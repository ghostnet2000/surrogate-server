import aiohttp
import aiohttp_cors
import asyncio
from aiohttp import web
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping of path prefixes to their corresponding ports
PATH_TO_PORT = {}

def get_remote_url(request):
    """
    Generates the appropriate remote URL based on the request path.
    
    Args:
        request: The incoming HTTP request.
    
    Returns:
        str: The generated remote URL.
    """
    # Check if the path matches any of the keys in the dictionary
    for path_prefix, port in PATH_TO_PORT.items():
        if request.path.startswith(path_prefix):
            path = request.path.replace(path_prefix, "")
            return f"http://localhost:{port}{path}"
    
    # Default fallback if no matching path is found
    return "http://localhost:8080"

async def create_app(download_port, script_port, cmd_port):
    """
    Creates and configures the aiohttp application.
    
    Args:
        download_port: Port for /download requests.
        script_port: Port for /script requests.
        cmd_port: Port for /cmd requests.
    
    Returns:
        web.Application: The configured aiohttp application.
    """
    global PATH_TO_PORT  # Access the global dictionary to set it here
    # Assign the port values to the dictionary in the main
    PATH_TO_PORT = {
        "/download": download_port,
        "/script": script_port,
        "/cmd": cmd_port
    }

    app = web.Application()

    # Create an HTTP connector for making proxy requests
    connector = aiohttp.TCPConnector()
    proxy_pool = aiohttp.ClientSession(connector=connector)

    # Store the session in the app for later use
    app["proxy_pool"] = proxy_pool

    # Set up CORS
    aiohttp_cors.setup(app)

    # Define routes
    app.router.add_route("*", "/{tail:.*}", lambda request: handle_request(request))

    return app

async def handle_request(request):
    """
    Handles the incoming request and proxies it to the appropriate remote server.
    
    Args:
        request: The incoming HTTP request.
    
    Returns:
        web.Response: The response returned to the client.
    """
    remote_url = get_remote_url(request)

    logger.info(f"Processing request: {request.method} {request.path} with query {request.query}")

    async with request.app["proxy_pool"].request(
        request.method, remote_url, headers=request.headers, params=request.query
    ) as resp:
        body = await resp.read()
        return web.Response(
            status=resp.status,
            body=body,
            headers=resp.headers
        )

if __name__ == "__main__":
    # Setup argparse to accept command-line arguments for ports
    parser = argparse.ArgumentParser(description="Create a surrogate server")
    parser.add_argument('-d', '--download-port', help='Port for download requests', type=int, default=1949)
    parser.add_argument('-s', '--script-port', help='Port for script requests', type=int, default=7385)
    parser.add_argument('-c', '--cmd-port', help='Port for cmd requests', type=int, default=7385)
    parser.add_argument('-H', '--host', help='Host address', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', help='Port for the web server', type=int, default=80)
    
    args = parser.parse_args()

    # Run the web application
    logger.info(f"Starting server on {args.host}:{args.port}")
    web.run_app(create_app(args.download_port, args.script_port, args.cmd_port), host=args.host, port=args.port)
