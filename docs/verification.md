# Verification — 2026-11-02

## Initial 0.1.0 verification

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
After an update, start a new conversation to avoid previously injected skill
instructions. Refresh/re-login behavior, cross-host/desktop pickup,
workspace import and cloud connectivity have not been exercised by this test.
A public repo is a distribution source; it is not proof that cloud clients can
reach an internal service or that every installed host updates automatically.

## Initial 0.1.0 publication and Git-backed installation

Published public repository:
https://github.com/EmoryUniversity/emory-mcp-catalog

A fresh isolated Codex host fetched the GitHub-backed marketplace and tested
source revision `a555428d6f3b6f4e92e69b93ef29a33a89eaf790`:

- `codex plugin marketplace add EmoryUniversity/emory-mcp-catalog` succeeded.
- Both plugin entries were discoverable at 0.1.0.
- Both plugins installed and were listed as enabled.
- Actual app-server plugin/read returned the platform MCP connection and setup
  onboarding skill for both plugins.

The operator's real client configuration was unchanged. Browser OAuth consent
was not performed by this packaging test; complete Authenticate/Connect from
an Emory-connected host to verify the personal authorization flow.

## Version 0.1.1 — setup skill removal

Both portable and compatibility manifests are bumped to 0.1.1. The two setup
SKILL.md files, skill directory declarations and onboardingSkill references
are removed. Starter prompts now request tool discovery rather than setup.
The validator requires both plugins to contain no skill files or onboarding
declarations. Existing endpoint URLs, OAuth discovery, authentication policy
and sharing remain unchanged.

An isolated host with both 0.1.0 plugins installed was upgraded to 0.1.1. Actual
app-server plugin/read returned platform as the MCP connection, an empty skill
list, and no onboarding skill for both plugins. Portable plugin/MCP schemas and
the public-package validator passed. A fresh GitHub-backed install of source
revision `ef7e938b21716c1a0bba5ca4d2707040246e2a25` also passed for
both 0.1.1 plugins: platform connection present, zero skills, no onboarding skill.
