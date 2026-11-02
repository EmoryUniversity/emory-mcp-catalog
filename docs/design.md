# Catalog decisions

The requested PoC uses a public GitHub.com repository under EmoryUniversity to
make existing MCPHub endpoint definitions discoverable and versioned. It avoids
per-user GitHub Enterprise clone credentials and keeps user secrets in MCPHub.

The earlier discussion is design context, not an execution checklist. Verified
corrections for the pinned MCPHub 1.1.8 deployment:

- Dashboard OIDC and incoming MCP OAuth are separate settings. Live inspection
  confirmed OAuth and public dynamic client registration enabled. Both group
  resource metadata documents and the authorization-server document return 200;
  unauthenticated MCP requests return 401 with the correct metadata challenge.
- The Git seed still said OAuth disabled when first inspected. Live PostgreSQL
  settings were enabled. Startup upsert manages server/group declarations and
  preserves existing system settings; the seed is a bootstrap default, not
  proof that live OAuth is disabled.
- Existing encrypted bindings already work in database mode with the original
  sibling key file. A new encryption key is unnecessary and would endanger them.
- Native sync and help-label edits were tested without deleting bindings. A
  blanket claim that every server-definition edit wipes bindings is incorrect.
- The pinned credential slots support headers for HTTP and env/args for stdio;
  a URL credential slot and prefix transform are not supported by this version.
  The Emory AAP patch supplies token-only input explicitly.
- Group sharing can prelist exact usernames before first login. LDAP group
  mapping is not supplied by this catalog.
- The two existing group URLs retain their different tool selections. Replacing
  them with the global `/mcp` route would change the access surface. OAuth scope
  names alone are not a demonstrated substitute for group tool filtering.
- A CLI marketplace, ChatGPT desktop host, workspace-imported plugin and the
  universal public directory are different distribution surfaces. Matching
  host/config and actual connectivity need verification; no universal CLI-to-web
  propagation or one-login-for-all-endpoints behavior is promised.

The initial catalog has two plugins, one per existing workflow/access route.
The catalog requests authentication on install and the URL-only MCP definitions
use OAuth discovery; the server enforces authentication and sharing. This catalog does not disable existing keys, alter group visibility,
create users, register upstream OAuth applications, or change token lifetimes.
New MCPHub keys/PATs are not copied into the package.

Current-client compatibility was verified against Codex 0.164.0-alpha.11.1.
Although OpenAI packaging docs describe per-server OAuth vendor extensions,
the published Agent Plugins 1.0 MCP schema and inspected Codex parser reject
that `extensions` key. The working package therefore uses schema-valid URL-only
MCP entries and ON_INSTALL authentication, letting the client discover the live
OAuth server and DCR endpoint from the challenge. No API-key input or static
header is configured. This does not disable keys already accepted by MCPHub;
server-side OAuth-only enforcement would be a separate change.
