"""Scigantic catalog API client.

Base URL: https://api.scigantic.com (override with the ``SCIGANTIC_API_URL``
environment variable). All endpoints used here are public and read-only, so no
credentials are required.
"""

from __future__ import annotations

import os
from typing import Any

from life_sciences_common import BaseLifeSciencesServer

SERVICE_NAME = "Scigantic"
BASE_URL = os.environ.get("SCIGANTIC_API_URL", "https://api.scigantic.com").rstrip("/")


def _archive_summary(archive: dict[str, Any]) -> dict[str, Any]:
    """Reduce a catalog record to the fields useful for ranking and follow-up."""
    return {
        "id": archive.get("id"),
        "title": archive.get("title"),
        "category": archive.get("category"),
        "cloudProvider": archive.get("cloudProvider"),
        "summary": archive.get("summary") or archive.get("description"),
        "source": archive.get("sourceUrl")
        or archive.get("websiteUrl")
        or archive.get("huggingFaceUrl"),
    }


async def search(
    server: BaseLifeSciencesServer,
    query: str,
    category: str | None = None,
    max_results: int = 10,
) -> dict[str, Any]:
    """Search the Scigantic catalog of public scientific datasets by query."""
    url = f"{BASE_URL}/api/archives"
    params: dict[str, Any] = {"search": query, "limit": max_results}
    if category:
        params["category"] = category
    response = await server._request_with_retry("GET", url, params=params)
    await server._handle_api_error(response, SERVICE_NAME, query=query)
    data = response.json()
    archives = [_archive_summary(a) for a in (data.get("data") or [])[:max_results]]
    return {"query": query, "count": len(archives), "archives": archives}


async def get_archive(
    server: BaseLifeSciencesServer,
    archive_id: str,
) -> dict[str, Any]:
    """Fetch full metadata for one dataset by its Scigantic archive id."""
    url = f"{BASE_URL}/api/archives/{archive_id}"
    response = await server._request_with_retry("GET", url)
    await server._handle_api_error(response, SERVICE_NAME, query=archive_id)
    return response.json().get("data", {})


async def get_schema_card(
    server: BaseLifeSciencesServer,
    archive_id: str,
) -> dict[str, Any]:
    """Get the schema card for a dataset: format, layout, sample objects, sample
    file headers, sidecar docs, access snippets, and a starter cell.
    """
    url = f"{BASE_URL}/api/archives/{archive_id}"
    response = await server._request_with_retry("GET", url)
    await server._handle_api_error(response, SERVICE_NAME, query=archive_id)
    archive = response.json().get("data", {})
    return {
        "id": archive.get("id"),
        "title": archive.get("title"),
        "schemaCard": archive.get("schemaCard"),
    }


async def get_data_access(
    server: BaseLifeSciencesServer,
    archive_id: str,
    language: str | None = None,
) -> dict[str, Any]:
    """Return how to load a dataset in your own environment: its storage
    location plus copy-paste code snippets from the schema card.
    """
    url = f"{BASE_URL}/api/archives/{archive_id}"
    response = await server._request_with_retry("GET", url)
    await server._handle_api_error(response, SERVICE_NAME, query=archive_id)
    archive = response.json().get("data", {})
    card = archive.get("schemaCard") or {}
    hints = card.get("accessHints") or []
    if language:
        matched = [h for h in hints if language.lower() in (h.get("language") or "").lower()]
        hints = matched or hints
    return {
        "id": archive.get("id"),
        "title": archive.get("title"),
        "storage": {
            "cloudProvider": archive.get("cloudProvider"),
            "bucket": archive.get("bucketName"),
            "prefix": archive.get("bucketPrefix"),
            "region": archive.get("region"),
            "access": archive.get("bucketAccessType"),
        },
        "accessHints": hints,
        "starterCell": card.get("starterCell"),
        "mountPath": card.get("mountPath"),
    }


async def list_files(
    server: BaseLifeSciencesServer,
    archive_id: str,
    max_results: int = 50,
) -> dict[str, Any]:
    """List a sample of the files/objects in a dataset's storage."""
    url = f"{BASE_URL}/api/archives/{archive_id}/files"
    response = await server._request_with_retry("GET", url)
    await server._handle_api_error(response, SERVICE_NAME, query=archive_id)
    data = response.json().get("data") or {}
    files = data.get("files") if isinstance(data, dict) else data
    files = files or []
    return {
        "id": archive_id,
        "count": min(len(files), max_results),
        "files": files[:max_results],
        "truncated": bool(isinstance(data, dict) and data.get("truncated")) or len(files) > max_results,
    }


async def lookup_paper(
    server: BaseLifeSciencesServer,
    query: str,
) -> dict[str, Any]:
    """Resolve a paper (arXiv id, DOI, URL, or title) and return its metadata
    plus any Scigantic datasets linked to or suggested by it.
    """
    url = f"{BASE_URL}/api/papers/lookup"
    response = await server._request_with_retry("POST", url, json={"query": query})
    await server._handle_api_error(response, SERVICE_NAME, query=query)
    body = response.json()
    return {
        "paper": body.get("data"),
        "suggestedArchives": body.get("suggestedArchives") or [],
    }
