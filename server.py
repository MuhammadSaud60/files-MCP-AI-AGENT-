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


if __name__ == "__main__":
    mcp.run()

