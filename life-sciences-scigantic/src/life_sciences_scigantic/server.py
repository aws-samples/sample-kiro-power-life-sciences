"""Scigantic MCP server entry point.

Creates a ``ScigateServer`` that extends :class:`BaseLifeSciencesServer` and
registers the Scigantic catalog tools. The server is started via stdio
transport when run as ``uvx life-sciences-scigantic``.

Scigantic is a cross-domain catalog of public scientific datasets. For each
dataset it pre-computes a compact *schema card* (format, layout, sample file
headers, sidecar docs, access snippets, and a starter cell), so an agent can
understand a dataset without listing buckets or opening files.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

from life_sciences_common import BaseLifeSciencesServer

from .clients import scigantic_client

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS: list[Tool] = [
    Tool(
        name="scigantic_search",
        description=(
            "Search the Scigantic catalog of public scientific datasets by "
            "natural-language query. Returns ranked matches across every domain "
            "with their id, title, category, and a short summary."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural-language search, e.g. 'single-cell RNA-seq of human cortex'.",
                },
                "category": {
                    "type": "string",
                    "description": "Optional category filter, e.g. 'Genomics & Bioinformatics'.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum results to return.",
                    "default": 10,
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="scigantic_get_archive",
        description="Fetch full metadata for one dataset by its Scigantic archive id.",
        inputSchema={
            "type": "object",
            "properties": {
                "archive_id": {
                    "type": "string",
                    "description": "Archive id from scigantic_search.",
                },
            },
            "required": ["archive_id"],
        },
    ),
    Tool(
        name="scigantic_get_schema_card",
        description=(
            "Get the schema card for a dataset: file format, directory layout, "
            "sample object keys, sample file headers, sidecar docs, access "
            "snippets, and a starter cell. The fastest way to understand a "
            "dataset's structure without listing buckets or opening files."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "archive_id": {
                    "type": "string",
                    "description": "Archive id from scigantic_search.",
                },
            },
            "required": ["archive_id"],
        },
    ),
    Tool(
        name="scigantic_get_data_access",
        description=(
            "Get how to load a dataset in your own environment: its storage "
            "location plus copy-paste code snippets from the schema card."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "archive_id": {
                    "type": "string",
                    "description": "Archive id from scigantic_search.",
                },
                "language": {
                    "type": "string",
                    "description": "Optional snippet-language filter, e.g. 'datasets', 's3fs', 'gcsfs'.",
                },
            },
            "required": ["archive_id"],
        },
    ),
    Tool(
        name="scigantic_list_files",
        description="List a sample of the files/objects in a dataset's storage.",
        inputSchema={
            "type": "object",
            "properties": {
                "archive_id": {
                    "type": "string",
                    "description": "Archive id from scigantic_search.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum entries to return.",
                    "default": 50,
                },
            },
            "required": ["archive_id"],
        },
    ),
    Tool(
        name="scigantic_lookup_paper",
        description=(
            "Resolve a research paper (arXiv id, DOI, URL, or title) and return "
            "its metadata plus any Scigantic datasets linked to or suggested by it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "arXiv id, DOI, paper URL, or title.",
                },
            },
            "required": ["query"],
        },
    ),
]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


def _build_dispatch(base: "ScigateServer") -> dict[str, Any]:
    """Build a name → coroutine-function mapping for all tools."""
    return {
        "scigantic_search": lambda args: scigantic_client.search(
            base, args["query"], args.get("category"), args.get("max_results", 10),
        ),
        "scigantic_get_archive": lambda args: scigantic_client.get_archive(
            base, args["archive_id"],
        ),
        "scigantic_get_schema_card": lambda args: scigantic_client.get_schema_card(
            base, args["archive_id"],
        ),
        "scigantic_get_data_access": lambda args: scigantic_client.get_data_access(
            base, args["archive_id"], args.get("language"),
        ),
        "scigantic_list_files": lambda args: scigantic_client.list_files(
            base, args["archive_id"], args.get("max_results", 50),
        ),
        "scigantic_lookup_paper": lambda args: scigantic_client.lookup_paper(
            base, args["query"],
        ),
    }


# ---------------------------------------------------------------------------
# ScigateServer
# ---------------------------------------------------------------------------


class ScigateServer(BaseLifeSciencesServer):
    """MCP server for the Scigantic cross-domain dataset catalog.

    Tools: search, archive metadata, schema cards, data-access snippets, file
    listings, and paper-to-dataset lookup.
    """

    def __init__(self) -> None:
        super().__init__("life-sciences-scigantic")
        self._dispatch = _build_dispatch(self)
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register list_tools and call_tool handlers on the MCP server."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return TOOLS

        dispatch = self._dispatch

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None = None,
        ) -> list[TextContent]:
            if name not in dispatch:
                raise ValueError(f"Unknown tool: {name}")
            result = await dispatch[name](arguments or {})
            return [TextContent(type="text", text=json.dumps(result, default=str))]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def _run() -> None:
    """Start the Scigantic MCP server over stdio."""
    from mcp.server.stdio import stdio_server

    scigantic = ScigateServer()
    try:
        async with stdio_server() as (read_stream, write_stream):
            await scigantic.server.run(
                read_stream,
                write_stream,
                scigantic.server.create_initialization_options(),
            )
    finally:
        await scigantic.cleanup()


def main() -> None:
    """CLI entry point for ``life-sciences-scigantic``."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()
