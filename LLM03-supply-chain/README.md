# LLM03: Supply Chain

This category covers weaknesses in the AI/LLM software supply chain: outdated frameworks with known CVEs, models and skills pulled from unverified or unknown sources, unsafe deserialization of remotely-fetched artifacts, MCP server containers that float on a mutable tag, and package/skill names that typosquat a legitimate, trusted dependency. Each subfolder below is one detector; see the top-level `ai-security-goat/README.md` for how to scan and how to read `expected.yaml`.

| Detector | What it flags |
|---|---|
| [`vulnerable-ai-framework-version`](./vulnerable-ai-framework-version/) | An AI/LLM framework or library pinned to a version with a known public CVE (e.g. an old `langchain`, `transformers`, or `langchain4j` release). |
| [`unverified-model-source`](./unverified-model-source/) | A model loaded from a URL, raw IP, or unofficial mirror instead of a verified source (HuggingFace Hub repo_id, known registry). |
| [`unsafe-deserializer-on-remote-artifact`](./unsafe-deserializer-on-remote-artifact/) | `torch.load()`/`pickle.load()`/`joblib.load()` (or equivalent) applied to a remotely-fetched artifact without `weights_only=True`, integrity verification, or a safe format. |
| [`unpinned-mcp-server-image`](./unpinned-mcp-server-image/) | An MCP server container image referenced by the mutable `:latest` tag or with no tag at all, instead of a pinned version or digest. |
| [`unknown-skill-registry`](./unknown-skill-registry/) | An agent skill installed from a source URL outside an allowlist of known registries (PyPI, npm, first-party registries), e.g. random domains, raw IPs, paste sites, gists, or curl-pipe-to-bash installers. |
| [`skill-name-typosquatting`](./skill-name-typosquatting/) | A package/skill/import name that closely mimics a legitimate, trusted one (character substitution, transposition, leetspeak), a common technique for tricking developers into installing a malicious lookalike. |
