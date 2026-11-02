---
name: setup
description: Set up this Emory platform plugin, complete MCPHub sign-in, bind personal GHES/AAP credentials, or troubleshoot missing tools and authentication challenges.
---

Help the user connect this plugin to the existing Emory MCPHub group endpoint.

1. Confirm that the user's Codex host can reach https://mcphub.int.emory.edu
   through its approved Emory network/VPN route. Installing the public catalog
   does not supply that network access.
2. Use the host's supported Authenticate/Connect action for this plugin. It
   discovers MCPHub OAuth and uses a browser sign-in/consent flow. Have the user
   complete Emory SSO, MFA, and consent themselves. Never ask for passwords,
   MFA codes, callback codes, access tokens, or refresh tokens in chat.
3. If access is denied, verify the user's existing MCPHub group sharing with an
   administrator. This plugin neither changes visibility nor maps LDAP groups.
   Never suggest switching to the global /mcp route to evade a group restriction.
4. If tools are missing or personal credentials are required, ask the user to
   open https://mcphub.int.emory.edu and select Credentials. For emory-ghes,
   enter the complete header value Bearer <personal GHES PAT>. For emory-aap,
   paste only the personal AAP token: the Emory AAP service adds Bearer itself.
   Existing Bearer-prefixed AAP bindings also work. All secret entry happens
   in the dashboard, never this conversation or a public file.
5. Retry discovery and a permitted read, such as listing job templates or
   repository branches. Use only actual discovered names/arguments. A valid
   empty result is possible under the user's upstream permissions. Do not
   launch jobs, change inventories, or perform other writes for onboarding.

OAuth connects the client to MCPHub. GHES and AAP personal bindings are separate
credentials with independent expiration and revocation; a hub refresh token
cannot refresh either manually bound upstream token. On an expired/revoked
upstream token, guide the user to replace their own binding in Credentials.
On expired hub authorization, use the supported Authenticate action again.
Do not promise an exact re-login interval or that separate endpoint connections
share stored tokens. Ask the user to retry a failed operation after sign-in;
do not automatically replay a write.

This plugin includes writes and Controller administration. Require a concrete
user request for changes and respect the user's permissions and approval policy.
