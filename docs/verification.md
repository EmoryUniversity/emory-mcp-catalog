# Verification — 2026-11-02

## Local package

- Both portable plugin manifests validate against the published Agent Plugins
  1.0 plugin schema. Both portable MCP definitions validate against its MCP
  schema. Skill frontmatter parses as YAML.
- `scripts/validate.py` passes: endpoint/membership consistency, contained
  source paths, synchronized portable/legacy identity and metadata, setup
  skill references, no static authentication material or user roster.
- Codex **0.164.0-alpha.11.1** in an isolated temporary config/cache successfully
  adds the local marketplace, lists both plugins at **0.1.0**, installs them,
  and lists both as enabled. The operator's real Codex configuration was not
  modified.
- An actual Codex app-server `plugin/read` call loads the **platform** MCP
  connection, namespaced setup skill and onboarding skill for each plugin.
  This caught and corrected a documented OAuth vendor-extension format that
  the current parser rejects; see design.md. A successful install alone was
  insufficient to prove that the connection was loaded.
- The compatibility `.mcp.json` uses HTTP transport; portable `mcp.json` uses
  streamable-http. Both contain exactly the same existing group URL, without
  a credential. The catalog requests authentication on installation.

## Live MCPHub inspection

Read-only inspection confirmed:

- Incoming MCP OAuth enabled in PostgreSQL. Public dynamic registration enabled,
  allowing authorization_code and refresh_token without initial registration
  authentication. Dashboard OIDC is separately configured and already working.
- Authorization-server discovery returns **200**, with the expected HTTPS issuer,
  authorize/token/register URLs and **S256** support.
- Both group protected-resource metadata URLs return **200** with their own
  canonical resource and the same authorization server.
- Unauthenticated initialize against each group returns **401** with the
  correct group-specific `resource_metadata` challenge.
- The existing seven-user sharing lists remain unchanged. No user, bearer key,
  token lifetime, LDAP mapping, group visibility or upstream permission was
  changed for this catalog.

Existing live tool evidence before catalog work: one pilot's GHES and AAP reads
passed through both groups; read-only had 35 total tools and full had 671.
Those checks used the existing personal bindings; they do not establish a new
browser OAuth grant for this plugin.

## Remaining user verification

On an Emory-connected Codex host, install from GitHub, Authenticate through
MCPHub/SSO, complete consent, and verify group discovery and an authorized read.
Test the setup action in a fresh conversation and installation during an
existing conversation. Refresh/re-login behavior, cross-host/desktop pickup,
workspace import and cloud connectivity have not been exercised by this test.
A public repo is a distribution source; it is not proof that cloud clients can
reach an internal service or that every installed host updates automatically.

## Publication status

Repository created publicly under the requested organization:
https://github.com/EmoryUniversity/emory-mcp-catalog

Local source and client loading checks passed. The initial catalog upload and
a fresh installation from the GitHub-backed marketplace are being verified.
