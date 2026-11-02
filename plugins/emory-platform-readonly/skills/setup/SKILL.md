---
name: setup
description: Optional Emory MCPHub connection and personal credential help, only when explicitly selected. Do not use for ordinary GHES or AAP tasks.
---

Help with the connection issue the user describes. This helper is optional;
using platform tools does not require completing a setup workflow.

- If the requested tools already work, continue the user's task. Do not start
  authentication, replace credentials, or require another upstream to be set up.
- For network failures, check that the Codex host has approved Emory network/VPN
  access. The public catalog does not make the internal MCPHub endpoint public.
- For MCPHub authorization failures, direct the user to the plugin's
  Authenticate/Connect action and its browser sign-in/consent. Group access
  depends on the exact MCPHub username and an administrator's sharing settings.
- For a missing/expired upstream credential, open https://mcphub.int.emory.edu
  and choose Credentials. For emory-ghes, save the complete `Bearer <PAT>` value.
  For emory-aap, save only the AAP token; the service adds the Bearer prefix.
  Ask the user to enter secrets there, never in chat or a command.
- Keep unrelated tools usable when one upstream is unavailable. After a fix,
  retry the requested discovery or an authorized read. Do not replay writes.
- If a tool seems absent, search the connected platform's tools by operation
  and exact name before concluding that the server lacks it. The full route
  advertises `emory-aap-jobs_list`; Codex exposes `emory_aap_jobs_list` after
  normalizing dashes to underscores. Use the name available in that client
  and its namespace. Do not use a language model's summary count
  as a complete MCP inventory. Report discovery errors precisely.
