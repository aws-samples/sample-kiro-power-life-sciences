"""Unit tests for the credential manager."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from kiro_life_sciences.credentials.manager import (
    ConfiguredCredential,
    CredentialInstructions,
    CredentialManager,
    _env_var_to_secret_key,
    _is_secret_ref,
    _secret_ref,
)
from kiro_life_sciences.models.manifest import (
    BundleComponents,
    BundleManifest,
    CredentialRequirement,
    MCPServerReference,
    ResourceCatalogDefinition,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cred(**overrides) -> CredentialRequirement:
    base = {
        "name": "NCBI API Key",
        "type": "api_key",
        "required": True,
        "description": "Increases NCBI rate limit.",
        "obtainUrl": "https://www.ncbi.nlm.nih.gov/account/settings/",
        "envVar": "NCBI_API_KEY",
    }
    base.update(overrides)
    return CredentialRequirement(**base)


def _server(**overrides) -> MCPServerReference:
    base = {
        "name": "life-sciences-genomics",
        "version": "0.1.0",
        "pypiPackage": "life-sciences-genomics",
        "description": "Genomics MCP server.",
        "domain": "Genomics and Sequencing",
        "databases": [],
        "credentials": [_cred()],
        "dependencies": [],
    }
    base.update(overrides)
    return MCPServerReference(**base)


def _manifest(servers: list[MCPServerReference] | None = None) -> BundleManifest:
    return BundleManifest(
        name="test-bundle",
        version="1.0.0",
        components=BundleComponents(
            mcpServers=servers or [_server()],
        ),
        resourceCatalog=ResourceCatalogDefinition(entries=[]),
    )


def _write_mcp_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _read_mcp_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_env_var_to_secret_key(self):
        assert _env_var_to_secret_key("NCBI_API_KEY") == "ncbi-api-key"

    def test_env_var_to_secret_key_single_word(self):
        assert _env_var_to_secret_key("TOKEN") == "token"

    def test_secret_ref(self):
        assert _secret_ref("NCBI_API_KEY") == "${secret:ncbi-api-key}"

    def test_is_secret_ref_valid(self):
        assert _is_secret_ref("${secret:ncbi-api-key}") is True

    def test_is_secret_ref_invalid(self):
        assert _is_secret_ref("plain-value") is False

    def test_is_secret_ref_partial(self):
        assert _is_secret_ref("${secret:}") is False

    def test_is_secret_ref_empty(self):
        assert _is_secret_ref("") is False


# ---------------------------------------------------------------------------
# CredentialManager.store
# ---------------------------------------------------------------------------


class TestStore:
    def test_store_creates_env_entry(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "command": "uvx",
                    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "my-secret-key")

        data = _read_mcp_json(mcp_path)
        env = data["mcpServers"]["life-sciences-genomics"]["env"]
        assert env["NCBI_API_KEY"] == "${secret:ncbi-api-key}"

    def test_store_does_not_write_actual_value(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "super-secret-123")

        raw = mcp_path.read_text(encoding="utf-8")
        assert "super-secret-123" not in raw

    def test_store_creates_server_entry_if_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-clinical", "OMIM_API_KEY", "key-value")

        data = _read_mcp_json(mcp_path)
        assert "life-sciences-clinical" in data["mcpServers"]
        env = data["mcpServers"]["life-sciences-clinical"]["env"]
        assert env["OMIM_API_KEY"] == "${secret:omim-api-key}"

    def test_store_creates_file_if_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "val")

        assert mcp_path.exists()
        data = _read_mcp_json(mcp_path)
        assert data["mcpServers"]["life-sciences-genomics"]["env"]["NCBI_API_KEY"] == "${secret:ncbi-api-key}"

    def test_store_preserves_existing_env_vars(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "command": "uvx",
                    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
                    "env": {
                        "EXISTING_VAR": "${secret:existing-var}"
                    }
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "val")

        data = _read_mcp_json(mcp_path)
        env = data["mcpServers"]["life-sciences-genomics"]["env"]
        assert env["EXISTING_VAR"] == "${secret:existing-var}"
        assert env["NCBI_API_KEY"] == "${secret:ncbi-api-key}"

    def test_store_overwrites_existing_credential(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:old-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "new-val")

        data = _read_mcp_json(mcp_path)
        assert data["mcpServers"]["life-sciences-genomics"]["env"]["NCBI_API_KEY"] == "${secret:ncbi-api-key}"


# ---------------------------------------------------------------------------
# CredentialManager.retrieve
# ---------------------------------------------------------------------------


class TestRetrieve:
    def test_retrieve_returns_secret_ref(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        result = mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY")
        assert result == "${secret:ncbi-api-key}"

    def test_retrieve_returns_none_when_not_configured(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        assert mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY") is None

    def test_retrieve_returns_none_for_non_secret_value(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "plain-text-value"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        assert mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY") is None

    def test_retrieve_returns_none_when_server_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        assert mgr.retrieve("nonexistent-server", "SOME_KEY") is None

    def test_retrieve_returns_none_when_file_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        mgr = CredentialManager(mcp_path)
        assert mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY") is None


# ---------------------------------------------------------------------------
# CredentialManager.delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_removes_env_entry(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        mgr.delete("life-sciences-genomics", "NCBI_API_KEY")

        data = _read_mcp_json(mcp_path)
        assert "NCBI_API_KEY" not in data["mcpServers"]["life-sciences-genomics"]["env"]

    def test_delete_preserves_other_env_vars(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {
                        "NCBI_API_KEY": "${secret:ncbi-api-key}",
                        "OTHER_KEY": "${secret:other-key}",
                    }
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        mgr.delete("life-sciences-genomics", "NCBI_API_KEY")

        data = _read_mcp_json(mcp_path)
        env = data["mcpServers"]["life-sciences-genomics"]["env"]
        assert "NCBI_API_KEY" not in env
        assert env["OTHER_KEY"] == "${secret:other-key}"

    def test_delete_noop_when_credential_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {"env": {}}
            }
        })
        mgr = CredentialManager(mcp_path)
        # Should not raise
        mgr.delete("life-sciences-genomics", "NONEXISTENT_KEY")

    def test_delete_noop_when_server_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        # Should not raise
        mgr.delete("nonexistent-server", "SOME_KEY")

    def test_delete_noop_when_file_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        mgr = CredentialManager(mcp_path)
        # Should not raise
        mgr.delete("life-sciences-genomics", "NCBI_API_KEY")


# ---------------------------------------------------------------------------
# CredentialManager.list_configured
# ---------------------------------------------------------------------------


class TestListConfigured:
    def test_lists_all_secret_refs(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {
                        "NCBI_API_KEY": "${secret:ncbi-api-key}",
                        "COSMIC_API_KEY": "${secret:cosmic-api-key}",
                    }
                },
                "life-sciences-clinical": {
                    "env": {
                        "OMIM_API_KEY": "${secret:omim-api-key}",
                    }
                },
            }
        })
        mgr = CredentialManager(mcp_path)
        creds = mgr.list_configured()

        assert len(creds) == 3
        names = {(c.connector_name, c.credential_name) for c in creds}
        assert ("life-sciences-genomics", "NCBI_API_KEY") in names
        assert ("life-sciences-genomics", "COSMIC_API_KEY") in names
        assert ("life-sciences-clinical", "OMIM_API_KEY") in names

    def test_skips_non_secret_env_vars(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {
                        "NCBI_API_KEY": "${secret:ncbi-api-key}",
                        "LOG_LEVEL": "DEBUG",
                    }
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        creds = mgr.list_configured()

        assert len(creds) == 1
        assert creds[0].credential_name == "NCBI_API_KEY"

    def test_empty_when_no_servers(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        assert mgr.list_configured() == []

    def test_empty_when_file_missing(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        mgr = CredentialManager(mcp_path)
        assert mgr.list_configured() == []

    def test_enriches_type_from_manifest(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        manifest = _manifest()
        mgr = CredentialManager(mcp_path, manifest=manifest)
        creds = mgr.list_configured()

        assert len(creds) == 1
        assert creds[0].type == "api_key"
        assert creds[0].is_valid is True

    def test_defaults_type_without_manifest(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)  # no manifest
        creds = mgr.list_configured()

        assert len(creds) == 1
        assert creds[0].type == "api_key"  # default


# ---------------------------------------------------------------------------
# CredentialManager.get_instructions
# ---------------------------------------------------------------------------


class TestGetInstructions:
    def test_returns_instructions_from_manifest(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        manifest = _manifest()
        mgr = CredentialManager(mcp_path, manifest=manifest)

        instructions = mgr.get_instructions("life-sciences-genomics", "NCBI_API_KEY")

        assert isinstance(instructions, CredentialInstructions)
        assert instructions.credential_name == "NCBI_API_KEY"
        assert instructions.type == "api_key"
        assert "ncbi.nlm.nih.gov" in instructions.obtain_url
        assert len(instructions.steps) > 0

    def test_returns_generic_instructions_without_manifest(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)  # no manifest

        instructions = mgr.get_instructions("life-sciences-genomics", "NCBI_API_KEY")

        assert isinstance(instructions, CredentialInstructions)
        assert instructions.credential_name == "NCBI_API_KEY"
        assert instructions.type == "api_key"
        assert instructions.obtain_url == ""
        assert len(instructions.steps) > 0

    def test_instructions_reference_env_var(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        manifest = _manifest()
        mgr = CredentialManager(mcp_path, manifest=manifest)

        instructions = mgr.get_instructions("life-sciences-genomics", "NCBI_API_KEY")

        # At least one step should mention the env var
        combined = " ".join(instructions.steps)
        assert "NCBI_API_KEY" in combined

    def test_instructions_for_unknown_credential(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        manifest = _manifest()
        mgr = CredentialManager(mcp_path, manifest=manifest)

        instructions = mgr.get_instructions("life-sciences-genomics", "UNKNOWN_KEY")

        assert instructions.credential_name == "UNKNOWN_KEY"
        assert instructions.obtain_url == ""


# ---------------------------------------------------------------------------
# Credential type support
# ---------------------------------------------------------------------------


class TestCredentialTypes:
    """Verify that all three credential types are supported."""

    def test_api_key_type(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        server = _server(credentials=[_cred(type="api_key", envVar="API_KEY")])
        manifest = _manifest(servers=[server])
        mgr = CredentialManager(mcp_path, manifest=manifest)

        mgr.store("life-sciences-genomics", "API_KEY", "val")
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"API_KEY": "${secret:api-key}"}
                }
            }
        })
        creds = mgr.list_configured()
        assert creds[0].type == "api_key"

    def test_oauth_type(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        server = _server(
            credentials=[_cred(name="OAuth Token", type="oauth", envVar="OAUTH_TOKEN")]
        )
        manifest = _manifest(servers=[server])
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"OAUTH_TOKEN": "${secret:oauth-token}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path, manifest=manifest)
        creds = mgr.list_configured()
        assert creds[0].type == "oauth"

    def test_username_password_type(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        server = _server(
            credentials=[_cred(name="DB Creds", type="username_password", envVar="DB_CREDS")]
        )
        manifest = _manifest(servers=[server])
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"DB_CREDS": "${secret:db-creds}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path, manifest=manifest)
        creds = mgr.list_configured()
        assert creds[0].type == "username_password"


# ---------------------------------------------------------------------------
# Expiry detection
# ---------------------------------------------------------------------------


class TestExpiryDetection:
    def test_valid_credential_not_expired(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        future = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", future)

        assert result is not None
        assert result.is_valid is True
        assert result.expires_at == future

    def test_expired_credential(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", past)

        assert result is not None
        assert result.is_valid is False
        assert result.expires_at == past

    def test_no_expiry_means_valid(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", None)

        assert result is not None
        assert result.is_valid is True
        assert result.expires_at is None

    def test_check_expiry_returns_none_when_not_configured(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", None)
        assert result is None

    def test_invalid_expiry_string_treated_as_valid(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        mgr = CredentialManager(mcp_path)
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", "not-a-date")

        assert result is not None
        assert result.is_valid is True

    def test_expiry_enriches_type_from_manifest(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {
            "mcpServers": {
                "life-sciences-genomics": {
                    "env": {"NCBI_API_KEY": "${secret:ncbi-api-key}"}
                }
            }
        })
        manifest = _manifest()
        mgr = CredentialManager(mcp_path, manifest=manifest)
        result = mgr.check_expiry("life-sciences-genomics", "NCBI_API_KEY", None)

        assert result is not None
        assert result.type == "api_key"


# ---------------------------------------------------------------------------
# Store → Retrieve → Delete lifecycle
# ---------------------------------------------------------------------------


class TestLifecycle:
    def test_store_retrieve_delete_cycle(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)

        # Initially not configured
        assert mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY") is None

        # Store
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "my-key")
        ref = mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY")
        assert ref == "${secret:ncbi-api-key}"

        # Listed
        creds = mgr.list_configured()
        assert len(creds) == 1
        assert creds[0].connector_name == "life-sciences-genomics"
        assert creds[0].credential_name == "NCBI_API_KEY"

        # Delete
        mgr.delete("life-sciences-genomics", "NCBI_API_KEY")
        assert mgr.retrieve("life-sciences-genomics", "NCBI_API_KEY") is None
        assert mgr.list_configured() == []

    def test_multiple_credentials_lifecycle(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)

        mgr.store("life-sciences-genomics", "NCBI_API_KEY", "key1")
        mgr.store("life-sciences-genomics", "COSMIC_API_KEY", "key2")
        mgr.store("life-sciences-clinical", "OMIM_API_KEY", "key3")

        creds = mgr.list_configured()
        assert len(creds) == 3

        # Delete one
        mgr.delete("life-sciences-genomics", "NCBI_API_KEY")
        creds = mgr.list_configured()
        assert len(creds) == 2

        # The other two remain
        names = {(c.connector_name, c.credential_name) for c in creds}
        assert ("life-sciences-genomics", "COSMIC_API_KEY") in names
        assert ("life-sciences-clinical", "OMIM_API_KEY") in names


# ---------------------------------------------------------------------------
# Security: never write credentials to project files
# ---------------------------------------------------------------------------


class TestSecurityInvariants:
    def test_actual_value_never_in_file(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)

        secret_value = "super-secret-credential-value-12345"
        mgr.store("life-sciences-genomics", "NCBI_API_KEY", secret_value)

        raw = mcp_path.read_text(encoding="utf-8")
        assert secret_value not in raw
        assert "${secret:ncbi-api-key}" in raw

    def test_store_multiple_values_never_leak(self, tmp_path: Path):
        mcp_path = tmp_path / "mcp.json"
        _write_mcp_json(mcp_path, {"mcpServers": {}})
        mgr = CredentialManager(mcp_path)

        secrets = ["secret-a-123", "secret-b-456", "secret-c-789"]
        env_vars = ["KEY_A", "KEY_B", "KEY_C"]

        for env_var, secret in zip(env_vars, secrets):
            mgr.store("life-sciences-genomics", env_var, secret)

        raw = mcp_path.read_text(encoding="utf-8")
        for secret in secrets:
            assert secret not in raw
