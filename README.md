# Example

A web-based Python code execution environment with a modern UI.

## Features

- Interactive Python code execution
- Modern web interface built with React and Vite
- Support for pandas DataFrames and Series
- API documentation with Scalar

## Installation

```bash
pip install example
```

## Usage

To start the server:

```bash
python -m example run
```

Optional arguments:
- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to bind to (default: 8000)

Then open your browser to http://localhost:8000

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/example.git
cd example
```

2. Install dependencies:
```bash
# Backend
pip install -e .

# Frontend
cd ui
npm install
```

3. Run the development servers:
```bash
# Backend (in one terminal)
python -m example run

# Frontend (in another terminal)
cd ui
npm run dev
```

## License

MIT 