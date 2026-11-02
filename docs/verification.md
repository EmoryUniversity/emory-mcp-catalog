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

## Version 0.1.2 — explicit-only setup help

Both plugins restore a single namespaced `setup` helper with
`agents/openai.yaml` setting `policy.allow_implicit_invocation: false`.
Neither manifest declares an onboarding skill, and the helper has no tool
dependencies. It addresses the requested connection issue without requiring
credentials for unrelated upstreams. Marketplace authentication is `ON_USE`;
explicit connection/attachment can still request browser authorization.

Portable manifest/MCP schemas, skill YAML/frontmatter and public-package checks
pass. An isolated Codex app-server loads each platform connection and its setup
skill with `onboardingSkill: null`. The packaged policy files were checked for
explicit-only invocation. Browser OAuth and model skill selection were not
performed by the packaging checks.

During investigation of a desktop chat reporting 110 tools, a fresh live
`tools/list` returned 671 tools for the full route (632 AAP, 39 GHES) and 35 for
the read-only route. Both included the exact `emory-aap-jobs_list` tool.
Using the pilot's personal binding, job/template/inventory/host reads passed
on both routes, and the full route's identity read passed. The temporary
user-associated test key was deleted. This validates the server and binding;
it does not establish the tool set loaded by that Windows desktop chat.

Codex supports deferred tool discovery: its tool-search implementation exposes
matching deferred tools on a subsequent model call. A model's current summary
count alone cannot diagnose missing server tools. The affected desktop chat's
exact tool-search/call result remains necessary to resolve its reported count.
The screenshot also showed underscore-normalized names. Codex's MCP name
sanitizer replaces dashes with underscores while retaining raw identities for
protocol calls, so `emory-aap-jobs_list` becomes `emory_aap_jobs_list` in the
model-facing tool name. This explains the exact-name mismatch, independently
of the reported tool count. See the [name sanitizer](https://github.com/openai/codex/blob/d92aae550180544fa2b7f656173c837271de6df3/codex-rs/codex-mcp/src/mcp/mod.rs)
and [raw/callable tool mapping](https://github.com/openai/codex/blob/d92aae550180544fa2b7f656173c837271de6df3/codex-rs/codex-mcp/src/tools.rs).
See the [Codex tool-search implementation](https://github.com/openai/codex/blob/d92aae550180544fa2b7f656173c837271de6df3/codex-rs/core/src/tools/handlers/tool_search_spec.rs)
and [explicit skill invocation policy](https://developers.openai.com/codex/skills.md).
