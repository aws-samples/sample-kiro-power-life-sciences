"""Credential manager for the Kiro for Life Sciences bundle.

Credentials are stored as environment variable entries in ``mcp.json`` using
the ``${secret:<key-name>}`` syntax.  Kiro's built-in secret management
resolves these placeholders at runtime so that actual credential values never
appear in project files or version control.

Example ``mcp.json`` snippet after storing a credential::

    {
      "mcpServers": {
        "life-sciences-genomics": {
          "command": "uvx",
          "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
          "env": {
            "NCBI_API_KEY": "${secret:ncbi-api-key}"
          }
        }
      }
    }
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kiro_life_sciences.models.manifest import BundleManifest, CredentialRequirement


# ---------------------------------------------------------------------------
# Public data classes
# ---------------------------------------------------------------------------


@dataclass
class ConfiguredCredential:
    """Represents a credential that has been configured in ``mcp.json``."""

    connector_name: str
    credential_name: str
    type: str  # "api_key" | "oauth" | "username_password"
    is_valid: bool
    expires_at: str | None = None


@dataclass
class CredentialInstructions:
    """Step-by-step instructions for obtaining a credential."""

    credential_name: str
    type: str
    obtain_url: str
    steps: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Pattern that matches ``${secret:<name>}`` values in mcp.json env entries.
_SECRET_PATTERN = re.compile(r"^\$\{secret:([^}]+)\}$")


def _env_var_to_secret_key(env_var: str) -> str:
    """Derive a secret key name from an environment variable name.

    ``NCBI_API_KEY`` → ``ncbi-api-key``
    """
    return env_var.lower().replace("_", "-")


def _secret_ref(env_var: str) -> str:
    """Build the ``${secret:…}`` reference string for *env_var*."""
    return f"${{secret:{_env_var_to_secret_key(env_var)}}}"


def _is_secret_ref(value: str) -> bool:
    """Return ``True`` if *value* matches the ``${secret:…}`` pattern."""
    return _SECRET_PATTERN.match(value) is not None


# ---------------------------------------------------------------------------
# CredentialManager
# ---------------------------------------------------------------------------


class CredentialManager:
    """Manage credentials stored in ``mcp.json``.

    The manager reads and writes the ``env`` section of MCP server entries in
    ``mcp.json``.  Actual credential values are **never** persisted — only
    ``${secret:<key>}`` placeholders are written.

    Parameters
    ----------
    mcp_json_path:
        Path to the ``mcp.json`` file.
    manifest:
        Optional :class:`BundleManifest` used to look up credential metadata
        (type, obtain URL, instructions) when calling
        :meth:`get_instructions` or :meth:`list_configured`.
    """

    def __init__(
        self,
        mcp_json_path: Path,
        manifest: BundleManifest | None = None,
    ) -> None:
        self._mcp_json_path = mcp_json_path
        self._manifest = manifest

    # -- internal I/O -------------------------------------------------------

    def _read_mcp_json(self) -> dict[str, Any]:
        """Read and parse ``mcp.json``, returning an empty structure if the
        file does not exist or is empty."""
        if not self._mcp_json_path.exists():
            return {"mcpServers": {}}
        text = self._mcp_json_path.read_text(encoding="utf-8").strip()
        if not text:
            return {"mcpServers": {}}
        data = json.loads(text)
        if "mcpServers" not in data:
            data["mcpServers"] = {}
        return data

    def _write_mcp_json(self, data: dict[str, Any]) -> None:
        """Atomically write *data* back to ``mcp.json``."""
        self._mcp_json_path.parent.mkdir(parents=True, exist_ok=True)
        self._mcp_json_path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
        )

    # -- manifest helpers ---------------------------------------------------

    def _find_credential_requirement(
        self,
        connector_name: str,
        credential_name: str,
    ) -> CredentialRequirement | None:
        """Look up a :class:`CredentialRequirement` from the manifest."""
        if self._manifest is None:
            return None
        for server in self._manifest.components.mcpServers:
            if server.name == connector_name:
                for cred in server.credentials:
                    if cred.envVar == credential_name or cred.name == credential_name:
                        return cred
        return None

    def _find_credential_by_env_var(
        self,
        env_var: str,
    ) -> tuple[str, CredentialRequirement] | None:
        """Return ``(server_name, cred_req)`` for a given env var."""
        if self._manifest is None:
            return None
        for server in self._manifest.components.mcpServers:
            for cred in server.credentials:
                if cred.envVar == env_var:
                    return server.name, cred
        return None

    # -- public API ---------------------------------------------------------

    def store(
        self,
        connector_name: str,
        credential_name: str,
        value: str,  # noqa: ARG002 — value is intentionally unused
    ) -> None:
        """Store a credential reference in ``mcp.json``.

        The actual *value* is **not** written to the file.  Instead, a
        ``${secret:<key>}`` placeholder is added to the ``env`` section of the
        MCP server entry identified by *connector_name*.  The *credential_name*
        should be the environment variable name (e.g. ``NCBI_API_KEY``).

        Parameters
        ----------
        connector_name:
            MCP server name (e.g. ``"life-sciences-genomics"``).
        credential_name:
            Environment variable name for the credential.
        value:
            The credential value.  This is accepted for API compatibility but
            is **never** persisted to disk.
        """
        data = self._read_mcp_json()
        servers: dict[str, Any] = data.setdefault("mcpServers", {})

        server_entry = servers.setdefault(connector_name, {})
        env: dict[str, str] = server_entry.setdefault("env", {})
        env[credential_name] = _secret_ref(credential_name)

        self._write_mcp_json(data)

    def retrieve(
        self,
        connector_name: str,
        credential_name: str,
    ) -> str | None:
        """Check whether a credential is configured for *connector_name*.

        Returns the ``${secret:…}`` placeholder string if the credential is
        present, or ``None`` if it is not configured.

        .. note::

           The actual secret value is resolved by Kiro at runtime and is
           **never** available to this manager.
        """
        data = self._read_mcp_json()
        servers: dict[str, Any] = data.get("mcpServers", {})
        server_entry = servers.get(connector_name, {})
        env: dict[str, str] = server_entry.get("env", {})
        value = env.get(credential_name)
        if value is not None and _is_secret_ref(value):
            return value
        return None

    def delete(
        self,
        connector_name: str,
        credential_name: str,
    ) -> None:
        """Remove a credential entry from ``mcp.json``.

        If the credential or server entry does not exist, this is a no-op.
        """
        data = self._read_mcp_json()
        servers: dict[str, Any] = data.get("mcpServers", {})
        server_entry = servers.get(connector_name)
        if server_entry is None:
            return
        env: dict[str, str] = server_entry.get("env", {})
        if credential_name in env:
            del env[credential_name]
            self._write_mcp_json(data)

    def list_configured(self) -> list[ConfiguredCredential]:
        """Return all credentials currently configured across all MCP servers.

        Each entry in the returned list corresponds to an ``env`` variable
        whose value matches the ``${secret:…}`` pattern.
        """
        data = self._read_mcp_json()
        servers: dict[str, Any] = data.get("mcpServers", {})
        result: list[ConfiguredCredential] = []

        for server_name, server_entry in servers.items():
            if not isinstance(server_entry, dict):
                continue
            env: dict[str, str] = server_entry.get("env", {})
            for env_var, env_value in env.items():
                if not _is_secret_ref(env_value):
                    continue

                # Try to enrich from manifest metadata
                cred_type = "api_key"  # default
                cred_req = self._find_credential_requirement(server_name, env_var)
                if cred_req is not None:
                    cred_type = cred_req.type

                result.append(
                    ConfiguredCredential(
                        connector_name=server_name,
                        credential_name=env_var,
                        type=cred_type,
                        is_valid=True,  # assumed valid; expiry checked below
                        expires_at=None,
                    )
                )

        return result

    def get_instructions(
        self,
        connector_name: str,
        credential_name: str,
    ) -> CredentialInstructions:
        """Return step-by-step instructions for obtaining a credential.

        If the manifest is available, the instructions are derived from the
        :class:`CredentialRequirement` metadata.  Otherwise, generic
        instructions are returned.
        """
        cred_req = self._find_credential_requirement(connector_name, credential_name)

        if cred_req is not None:
            return CredentialInstructions(
                credential_name=cred_req.envVar,
                type=cred_req.type,
                obtain_url=cred_req.obtainUrl,
                steps=[
                    f"Visit {cred_req.obtainUrl} to obtain your {cred_req.name}.",
                    f"Copy the credential value.",
                    f"Run the credential store command for {connector_name} with env var {cred_req.envVar}.",
                    f"The credential will be stored as ${{secret:{_env_var_to_secret_key(cred_req.envVar)}}} in mcp.json.",
                ],
            )

        # Fallback: generic instructions
        return CredentialInstructions(
            credential_name=credential_name,
            type="api_key",
            obtain_url="",
            steps=[
                f"Obtain the credential for {credential_name} from the service provider.",
                f"Run the credential store command for {connector_name} with env var {credential_name}.",
                f"The credential will be stored as ${{secret:{_env_var_to_secret_key(credential_name)}}} in mcp.json.",
            ],
        )

    # -- expiry detection ---------------------------------------------------

    def check_expiry(
        self,
        connector_name: str,
        credential_name: str,
        expires_at: str | None,
    ) -> ConfiguredCredential | None:
        """Check whether a configured credential has expired.

        Parameters
        ----------
        connector_name:
            MCP server name.
        credential_name:
            Environment variable name.
        expires_at:
            ISO-8601 expiry timestamp, or ``None`` if the credential does not
            expire.

        Returns
        -------
        A :class:`ConfiguredCredential` with ``is_valid`` set to ``False`` and
        ``expires_at`` populated if the credential has expired, or ``None`` if
        the credential is not configured.
        """
        ref = self.retrieve(connector_name, credential_name)
        if ref is None:
            return None

        cred_type = "api_key"
        cred_req = self._find_credential_requirement(connector_name, credential_name)
        if cred_req is not None:
            cred_type = cred_req.type

        is_valid = True
        if expires_at is not None:
            try:
                expiry_dt = datetime.fromisoformat(expires_at)
                if expiry_dt.tzinfo is None:
                    expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
                is_valid = datetime.now(timezone.utc) < expiry_dt
            except (ValueError, TypeError):
                # Unparseable expiry → treat as valid (don't block the user)
                is_valid = True

        return ConfiguredCredential(
            connector_name=connector_name,
            credential_name=credential_name,
            type=cred_type,
            is_valid=is_valid,
            expires_at=expires_at,
        )
