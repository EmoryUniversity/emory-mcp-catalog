# Emory MCP Catalog

A public GitHub.com marketplace maintained under **EmoryUniversity**. It contains
versioned connection definitions and manual setup instructions for existing Emory
MCPHub groups. Service access remains controlled by MCPHub and each person's
upstream permissions.

| Plugin | MCP endpoint | Surface |
| --- | --- | --- |
| `emory-platform-readonly` | `https://mcphub.int.emory.edu/mcp/platform-official-readonly` | Reviewed GHES and AAP Controller reads |
| `emory-platform-full` | `https://mcphub.int.emory.edu/mcp/platform-official-full` | Enabled GHES tools and all pinned Controller tools, including writes |

Choose the read-only plugin for read workflows. Install the full plugin when
you need its operations and already have the corresponding MCPHub/upstream
permissions. Installing both exposes overlapping tools; they are separate client
connections and can require separate authorization. Both reuse the same
per-user GHES/AAP bindings in MCPHub.

## Install in Codex

Run these commands on the Codex host that has approved Emory network/VPN access:

```sh
codex plugin marketplace add EmoryUniversity/emory-mcp-catalog
codex plugin list --marketplace emory-mcp
codex plugin add emory-platform-readonly@emory-mcp
```

Or install the full variant:

```sh
codex plugin add emory-platform-full@emory-mcp
```

Open the plugin's Authenticate/Connect action when prompted, then complete the
browser flow. The client discovers OAuth and dynamic registration from MCPHub's challenge
and metadata; no client secret or bearer key is included. The marketplace requests
connection authentication on use rather than installation. Explicitly connecting
or attaching a server can still open the browser. Exact prompts depend on client
version; installation does not prove browser consent or service access.

This is a Git-backed local-client marketplace, separate from the universal
OpenAI plugin directory. A CLI install does not publish or install a plugin
into the ChatGPT web workspace. Workspace import is a separate admin workflow.
The internal endpoint resolves privately; the host executing MCP requests must
have network access. A public catalog alone does not make it reachable from a
cloud client. See [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins)
and [workspace marketplace import](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Personal setup

1. Complete the plugin's MCPHub OAuth sign-in and consent. MCPHub uses the
   existing Emory SSO-backed dashboard identity; a first login can create a
   local user, but this does not grant access to restricted groups. An admin
   must share the selected group with the exact local username. Already
   prelisted usernames can gain the intended access when they first sign in.
2. Open https://mcphub.int.emory.edu and select **Credentials**.
3. For **emory-ghes**, save `Bearer <your personal GHES PAT>` as the complete
   header value. For **emory-aap**, paste **only your personal AAP token**;
   the Emory AAP service adds the fixed Bearer prefix. Existing prefixed AAP
   bindings still work.
4. Retry discovery and a read you are allowed to perform. The optional setup
   helper runs only when you explicitly select it; there is no automatic
   onboarding action or setup prerequisite. Tokens are entered only in the dashboard, never chat,
   this repository, screenshots, issues, or command-line examples.

MCPHub OAuth and upstream tokens have independent lifecycles. MCPHub access
tokens can be refreshed by an OAuth-capable client while its refresh grant is
valid. Expired/revoked manually bound GHES/AAP tokens must be replaced in
Credentials. Do not assume one endpoint's authorization automatically signs
in another, an exact re-login interval, or automatic replay of a rejected write.
The read-only filter applies to its group route; other permitted routes may
expose writes. Token scope and upstream resource RBAC remain authoritative.
Neither installation nor a `read` OAuth scope substitutes for those controls.

For connection help, explicitly select the plugin's **setup** skill in the skill
picker, or invoke `$emory-platform-full:setup` (read-only variant:
`$emory-platform-readonly:setup`). Both set
`policy.allow_implicit_invocation: false` in `agents/openai.yaml` and declare no
tool dependencies. Ordinary GHES/AAP requests do not activate the helper.

## Finding tools in Codex

Codex can discover tools on demand, but its current source also imposes a
**64,000-byte combined budget for plugin MCP tool definitions** and an
8,000-byte individual definition limit. Tools excluded by this budget are
hidden even from tool search. This is a likely explanation for a Windows
desktop client (26.1027.30824) exposing 110 tools while MCPHub returns 671;
the exact client-side byte calculation has not been reproduced.
See [Codex's plugin tool budget](https://github.com/openai/codex/blob/d92aae550180544fa2b7f656173c837271de6df3/codex-rs/core/src/mcp_tool_exposure.rs).

A **direct MCP connection**, configured outside the plugin, bypasses that
plugin-specific budget in current Codex source. Its ordinary MCP catalog
guard is 2,048 tools, which accommodates this full endpoint. Use this option
when you need the complete full catalog:

```sh
codex mcp add emory-platform-full --url https://mcphub.int.emory.edu/mcp/platform-official-full
codex mcp login emory-platform-full
```

Disable the full plugin's connection in the client to avoid duplicate tools,
then start a new chat. This uses the same server and permissions; no upstream
token needs to be copied into Codex. Browser consent may be needed for the
new direct connection. These commands were syntax-checked locally; the
operator must complete browser login and verify this on the Windows host.

To verify, ask the chat to discover `emory_aap_jobs_list` and list one job with
`page_size: 1`. This is a read operation; it should not launch a job.
MCPHub advertises `emory-aap-jobs_list`; Codex normalizes
dashes to underscores in model-visible names and routes calls back to the
original server name. Search using the name exposed by your client; its
namespace can add a further prefix. Report the actual discovery/call error
if it fails.

Live MCPHub verification on 2026-11-02 returned **671** tools from the full
route (632 AAP, 39 GHES), including `emory-aap-jobs_list`, which passed using
the pilot's personal binding. The read-only route returned 35 tools. These
counts describe the server response, not a guarantee of what every client
loads. An analytics call returning HTTP 403 is a separate upstream AAP access
failure, not evidence that job listing is absent from the server.

## Update

Bump the changed plugin's semantic version, validate, and publish the change.
Consumers refresh their Git marketplace and update/reinstall the desired plugin
as supported by their client; updates are not a guaranteed push to every host:

```sh
codex plugin marketplace upgrade emory-mcp
codex plugin add emory-platform-readonly@emory-mcp
```

Restart/reload the client if required and verify the installed version. Existing
OAuth authorization or new consent may be needed after connection changes.
Workspace-imported marketplaces have a separate daily/manual sync mechanism;
local CLI refresh and workspace sync are different operations.

## Maintain and verify

```sh
python3 scripts/validate.py
```

- `.agents/plugins/marketplace.json` is the Codex marketplace entry point.
- `plugins/*/plugin.json` and `mcp.json` are portable plugin definitions.
- `.codex-plugin/plugin.json` and `.mcp.json` supply the synchronized legacy
  compatibility format. Legacy MCP configuration uses OAuth discovery from
  the server challenge, as does the schema-valid portable declaration.
- Version **0.1.2** bundles explicit-only setup help, without automatic onboarding,
  and requests authentication on use.
- `catalog.json` is a simple inventory for humans and other consumers; it is not
  an additional Codex configuration mechanism.

The public package contains endpoint URLs and instructions. Deployment JSON,
user rosters, passwords, credentials, OAuth tokens, private keys and production
exports remain outside this repository. See [verification](docs/verification.md)
for what was actually tested and [design decisions](docs/design.md) for the
relationship to the earlier distribution discussion.

## Update from 0.1.0 or 0.1.1

Version 0.1.1 removed setup skills. Version 0.1.2 restores them as optional,
explicit-only helpers with no onboarding declaration. Follow the refresh/reinstall
commands above, then start a new chat so old automatic setup instructions are
no longer part of the conversation context. For the full plugin use
`codex plugin add emory-platform-full@emory-mcp` after the marketplace upgrade.
If you registered a manually cloned local marketplace, update that clone first
with `git pull --ff-only` in its directory, then reinstall the plugin.
