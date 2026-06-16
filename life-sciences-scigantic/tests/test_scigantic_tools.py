"""Unit tests for life-sciences-scigantic MCP server tools.

Uses ``respx`` to mock httpx responses, following the same pattern as
``life-sciences-common/tests/test_server.py``.
"""

from __future__ import annotations

import pytest
import respx

from life_sciences_common import BaseLifeSciencesServer

BASE = "https://api.scigantic.com"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def server():
    srv = BaseLifeSciencesServer("test-scigantic")
    yield srv
    await srv.cleanup()


ARCHIVE = {
    "id": "abc123",
    "title": "OpenFold3 Training Data",
    "category": "Life Sciences",
    "cloudProvider": "aws",
    "bucketName": "openfold3-data",
    "region": "us-west-2",
    "bucketAccessType": "public",
    "summary": "MSAs and predicted structures used to train OpenFold3.",
    "websiteUrl": "https://portal.openfold.omsf.io/datasets",
    "schemaCard": {
        "format": "binary",
        "layout": {"pattern": "{prefix}/{seg1}/{seg2}/{object}"},
        "accessHints": [
            {"language": "python-anonymous", "snippet": "import boto3 ..."},
            {"language": "python-local", "snippet": "open('/mnt/archive/...', 'rb')"},
        ],
        "starterCell": "with open('/mnt/archive/...', 'rb') as fh: ...",
        "mountPath": "/mnt/archive",
    },
}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


class TestScigateSearch:
    @respx.mock
    async def test_search(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives").respond(
            200,
            json={"success": True, "count": 1, "data": [ARCHIVE]},
        )
        result = await scigantic_client.search(server, "openfold3", max_results=5)
        assert result["count"] == 1
        assert result["archives"][0]["id"] == "abc123"
        # source falls back to websiteUrl when sourceUrl is absent
        assert result["archives"][0]["source"] == "https://portal.openfold.omsf.io/datasets"


# ---------------------------------------------------------------------------
# Archive metadata
# ---------------------------------------------------------------------------


class TestScigateArchive:
    @respx.mock
    async def test_get_archive(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives/abc123").respond(
            200, json={"success": True, "data": ARCHIVE},
        )
        result = await scigantic_client.get_archive(server, "abc123")
        assert result["id"] == "abc123"
        assert result["title"] == "OpenFold3 Training Data"


# ---------------------------------------------------------------------------
# Schema card
# ---------------------------------------------------------------------------


class TestScigateSchemaCard:
    @respx.mock
    async def test_get_schema_card(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives/abc123").respond(
            200, json={"success": True, "data": ARCHIVE},
        )
        result = await scigantic_client.get_schema_card(server, "abc123")
        assert result["id"] == "abc123"
        assert result["schemaCard"]["format"] == "binary"


# ---------------------------------------------------------------------------
# Data access
# ---------------------------------------------------------------------------


class TestScigateDataAccess:
    @respx.mock
    async def test_get_data_access(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives/abc123").respond(
            200, json={"success": True, "data": ARCHIVE},
        )
        result = await scigantic_client.get_data_access(server, "abc123")
        assert result["storage"]["bucket"] == "openfold3-data"
        assert result["storage"]["region"] == "us-west-2"
        assert len(result["accessHints"]) == 2
        assert result["mountPath"] == "/mnt/archive"

    @respx.mock
    async def test_get_data_access_language_filter(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives/abc123").respond(
            200, json={"success": True, "data": ARCHIVE},
        )
        result = await scigantic_client.get_data_access(server, "abc123", language="local")
        assert len(result["accessHints"]) == 1
        assert result["accessHints"][0]["language"] == "python-local"


# ---------------------------------------------------------------------------
# File listing
# ---------------------------------------------------------------------------


class TestScigateListFiles:
    @respx.mock
    async def test_list_files(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.get(f"{BASE}/api/archives/abc123/files").respond(
            200,
            json={
                "success": True,
                "data": {
                    "files": [
                        {"name": "data.parquet", "size": 1024},
                        {"name": "README.md", "size": 50},
                    ]
                },
            },
        )
        result = await scigantic_client.list_files(server, "abc123")
        assert result["count"] == 2
        assert result["files"][0]["name"] == "data.parquet"


# ---------------------------------------------------------------------------
# Paper lookup
# ---------------------------------------------------------------------------


class TestScigateLookupPaper:
    @respx.mock
    async def test_lookup_paper(self, server: BaseLifeSciencesServer):
        from life_sciences_scigantic.clients import scigantic_client

        respx.post(f"{BASE}/api/papers/lookup").respond(
            200,
            json={
                "success": True,
                "data": {"title": "A Great Paper", "authors": ["Ada L."]},
                "suggestedArchives": [{"id": "abc123", "title": "OpenFold3 Training Data"}],
            },
        )
        result = await scigantic_client.lookup_paper(server, "A Great Paper")
        assert result["paper"]["title"] == "A Great Paper"
        assert result["suggestedArchives"][0]["id"] == "abc123"
