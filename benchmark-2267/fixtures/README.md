# #2267 fixtures (synthetic)

Scan: `xygeni --skip-update ai -d fixtures -f json -o ../results/ai --never-fail`

| Dir | What | Expected |
|---|---|---|
| `A-payloads/{skill,prompt,code,mcp}/<family>` | agentdojo, injecagent_enhanced, injecagent_base, garak_dan, garak_inthewild | Dev claims 100% (agentdojo, injecagent_enhanced), 93% (dan), 50% (inthewild); injecagent_base stays 0% (known) |
| `A-payloads/*/benign_*` | benign + prose explaining injection | 0 findings of content detectors |
| `B-mcp-code/*/poisoned_*` | poisoned tool description in py/ts/go/java | `mcp-tool-description-poisoning` |
| `B-mcp-code/*/clean_*` | clean description | none |
| `C-json-tools/poisoned_tools.json` | tool list in JSON | reported; `clean_tools.json` and `not_tool_shaped.json` not |
| `D-obfuscation/{skill,prompt,code}/{base64,homoglyph,zerowidth}` | obfuscated override | reported (dev: 90/90/100%); `benign/*` not |
| `E-model-source/unpinned_unknown_org.py` | HF repo, unknown org, no revision | reported, low; `pinned_unknown_org.py` and `official_org.py` not |
| `F-prose/**` | docs/prose with crontab, "avoid ignore previous", provider trains, medical, exposed vector store | no high/critical from prose; persistence only low; `real-persistence/install.py` still reported |
| `G-benign/**` | benign prompt, skill, non-AI Flask | 0 findings |
