# Surrogate Server

A simple proxy server built with `aiohttp`, designed to route incoming requests to different local services based on the path prefix. The server uses `argparse` to configure the ports for various routes and provides flexibility for deployment.

## Features

- **Dynamic Routing**: Routes requests based on path prefixes (`/download`, `/script`, `/cmd`).
- **Configurable Ports**: Use command-line arguments to set custom ports for each route.
- **Proxying**: Proxies requests to the corresponding service running on the specified ports.
- **CORS Support**: Configures Cross-Origin Resource Sharing (CORS) to allow cross-origin requests.
- **Logging**: Built-in logging for better tracking and debugging.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ghostnet2000/surrogate-server.git
   cd surrogate-server
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run the surrogate server by specifying the desired ports and host using command-line arguments.

### Command-Line Arguments

- `-d`, `--download-port`: Port for `/download` requests (default: `1949`)
- `-s`, `--script-port`: Port for `/script` requests (default: `7385`)
- `-c`, `--cmd-port`: Port for `/cmd` requests (default: `7385`)
- `-H`, `--host`: Host address to bind the server to (default: `0.0.0.0`)
- `-p`, `--port`: Port for the web server (default: `80`)

### Example Command

Run the server with custom ports:

```bash
python surrogate_server.py --download-port 1950 --script-port 7390 --cmd-port 7390 --host 0.0.0.0 --port 8080
```
