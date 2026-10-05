from mcp.server.fastmcp import FastMCP
from pathlib  import Path

mcp = FastMCP('File Server')

WORKSPACE = Path('workspace').resolve()


def safe_path(filename: str) -> Path:
    """Make sure the file stays inside workspace."""
    path = (WORKSPACE / filename).resolve()

    if not path.is_relative_to(WORKSPACE):
        raise ValueError("Access outside workspace is not allowed")

    return path



@mcp.tool()
def list_files() -> list[str]:
    """List all files inside the workspace."""
    return [
        str(path.relative_to(WORKSPACE))
        for path in WORKSPACE.rglob("*")
        if path.is_file()
    ]



@mcp.tool()
def read_file(filename: str) -> str:
    """Read a text file from the workspace."""
    path = safe_path(filename)

    if not path.exists():
        return f"File not found: {filename}"

    return path.read_text(encoding="utf-8")


@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """Create or overwrite a text file inside the workspace."""
    path = safe_path(filename)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return f"File written successfully: {filename}"


@mcp.tool()
def search_files(query: str) -> list[dict]:
    """Search for a text query inside all text files in the workspace."""

    results = []

    for path in WORKSPACE.rglob("*"):
        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        lines = content.splitlines()

        for line_number, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                results.append({
                    "file": str(path.relative_to(WORKSPACE)),
                    "line": line_number,
                    "text": line.strip()
                })

    return results


@mcp.tool()
def create_directory(dirname: str) -> str:
    """Create a directory inside the workspace."""

    path = safe_path(dirname)

    path.mkdir(parents=True, exist_ok=True)

    return f"Directory created successfully: {dirname}"


@mcp.tool()
def delete_file(filename: str) -> str:
    """Delete a file inside the workspace."""

    path = safe_path(filename)

    if not path.exists():
        return f"File not found: {filename}"

    if not path.is_file():
        return f"Not a file: {filename}"

    path.unlink()

    return f"File deleted successfully: {filename}"


if __name__ == "__main__":
    mcp.run()

