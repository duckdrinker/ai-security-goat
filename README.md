# ai-security-goat

A deliberately vulnerable AI/LLM codebase, built to validate Xygeni's **AI Security** risk detectors. Originally scoped to the OWASP LLM Top 10:2025 (categories LLM01–LLM10); since 2026-08-31 it also covers detectors that map to the OWASP Agentic Security Initiative (ASI) taxonomy instead — non-human-identity and agent-runtime risks that don't fit a single LLM Top 10 category (`ASI0N-*` top-level folders, same structure/conventions as the LLM0N ones).

This project follows the same spirit as [xygeni-goat](https://github.com/xygeni/xygeni-goat) (Xygeni's existing "goat" project for supply-chain issues — SCA, IaC, Secrets), but focused on AI/LLM-specific risks instead. It is currently developed inside the `DepsDoctor-Test` repo for convenience, but is designed to be extracted into its own standalone repository later with no changes required — it has no dependency on anything else in `DepsDoctor-Test` (no references to `TestCases/`, `Karate/`, or any other sibling folder).

> **Warning**
> This repository is for educational and internal-testing purposes only. Do NOT deploy any code from this repository in any real environment, and do NOT use the techniques shown here for unauthorized purposes.

## Structure

```
ai-security-goat/
├── LLM01-prompt-injection/
│   ├── <detector-id>/
│   │   ├── bad_<variant>.<ext> (one or more — each triggers the detector a different way)
│   │   ├── good[_<variant>].<ext> (mitigated equivalent — shared reference, not paired 1:1 with each bad file)
│   │   └── expected.yaml      (what a scan of this folder is expected to find)
│   └── ...
├── LLM02-sensitive-information-disclosure/
├── LLM03-supply-chain/
├── LLM04-data-and-model-poisoning/
├── LLM05-improper-output-handling/
├── LLM06-excessive-agency/
├── LLM07-system-prompt-leakage/
├── LLM08-vector-and-embedding-weaknesses/
├── LLM09-misinformation/
├── LLM10-unbounded-consumption/
├── ASI03-identity-abuse/
└── ASI05-unexpected-code-execution/
```

Each top-level folder is one OWASP LLM Top 10:2025 category, or (for the `ASI0N-*` folders) one OWASP Agentic Security Initiative category (its own `README.md` lists the specific detectors it covers). Each detector subfolder is self-contained: it can be scanned on its own, or the whole tree can be scanned at once.

**Note on detector coverage:** as of 2026-07-21, only some of these detectors are confirmed implemented in the Xygeni AI Security scanner (LLM01 and at least part of LLM10 have been observed producing real findings). The rest document the *intended* behavior per the product specs — scanning them today may produce no finding, which is itself useful signal about what's not implemented yet, not a fixture bug. Each `expected.yaml` for an unconfirmed detector says so explicitly.

## Languages

Fixtures are Python by default. Since 2026-10-20 (xygeni-product-backlog#2244, AI Security for Java, Kotlin and Go) some detector folders also hold `.java`, `.kt` and `.go` fixtures, named `bad_<lang>_<framework>_<case>.<ext>` / `good_<lang>_<framework>_<case>.<ext>` (for example `bad_java_langchain4j_while_true_loop.java`, `good_go_model_json_unmarshal.go`). They are scanned, not compiled, so class and package names do not need to match the file name. Most are single self-contained files; the tool-using agent in `LLM01-prompt-injection/agent-tool-without-input-guardrail` also exists as multi-file projects (`bad_java_multifile_*/`, `good_java_multifile_*/`: `Assistant.java`, `EmailTool.java`, `AgentApp.java`) and as `*_agentapp_*` Kotlin variants, so the same case is covered in two shapes. `bad_java_multifile_tools_text_only_model/` uses a text-only model (`gpt-3.5-turbo`): it keeps the tool-invoking finding but loses `multi-modal-input-without-sanitization`, which that detector derives from the model capability and not from the code.

Where each family lives:

| Condition | Folder |
|---|---|
| Agent loop with no iteration cap (Java, Kotlin, Go) | `LLM10-unbounded-consumption/agent-loop-without-iteration-cap` |
| Model call with no timeout or token cap (Java) | `LLM10-unbounded-consumption/inference-call-without-timeout-or-token-cap` |
| Provider trains on prompts by default (Java, Kotlin) | `LLM02-sensitive-information-disclosure/provider-trains-on-prompts-by-default` |
| User content in the system prompt (Java) | `LLM01-prompt-injection/unbounded-user-content-in-system-prompt` |
| Tool-using agent without input guardrail (Java, Kotlin, Go), and non-AI controls | `LLM01-prompt-injection/agent-tool-without-input-guardrail` |
| Public agent without prompt-extraction guardrail (Go) | `LLM07-system-prompt-leakage/public-agent-missing-prompt-extraction-guardrail` |
| Autonomous agent with side-effecting tool, no approval (Java, Kotlin, Go) | `LLM06-excessive-agency/autorun-agent-without-human-in-the-loop` |
| Model output reaching a shell or SQL sink, and model JSON parsed as data (Java, Kotlin, Go) | `ASI05-unexpected-code-execution/untrusted-data-reaches-code-sink` |

As with the Python fixtures, a `bad_*` file that the scanner does not flag documents the intended behaviour; its `expected.yaml` entry says whether it was detected and with which scanner version. Observed with Scanner 6.21.0 on 2026-10-20, the Java/Kotlin/Go `bad_*` files that were **not** detected are: the Go tool-invoking agent, the Go public handler, the Java model call without bounds, the Java CV-in-system-prompt, the Kotlin model-output-to-shell, and all three `autorun-agent-without-human-in-the-loop` fixtures (that detector reported nothing in any language, Python included).
## How to scan

Using the Xygeni CLI (see this repo's own `TestCases/CLAUDE.md` for the full invocation convention when run from inside `DepsDoctor-Test`):

```powershell
# Scan a single detector's fixtures
xygeni.ps1 ai --dir ai-security-goat/LLM10-unbounded-consumption/inference-call-without-timeout-or-token-cap

# Scan an entire category
xygeni.ps1 ai --dir ai-security-goat/LLM01-prompt-injection

# Scan everything
xygeni.ps1 ai --dir ai-security-goat
```

Compare the resulting `ai-xygeni.json` report against the `expected.yaml` files under the folders you scanned.
