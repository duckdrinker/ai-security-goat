# ai-security-goat

A deliberately vulnerable AI/LLM codebase, built to validate Xygeni's **AI Security** risk detectors (OWASP LLM Top 10:2025, categories LLM01–LLM10).

This project follows the same spirit as [xygeni-goat](https://github.com/xygeni/xygeni-goat) (Xygeni's existing "goat" project for supply-chain issues — SCA, IaC, Secrets), but focused on AI/LLM-specific risks instead. It is currently developed inside the `DepsDoctor-Test` repo for convenience, but is designed to be extracted into its own standalone repository later with no changes required — it has no dependency on anything else in `DepsDoctor-Test` (no references to `TestCases/`, `Karate/`, or any other sibling folder).

> **Warning**
> This repository is for educational and internal-testing purposes only. Do NOT deploy any code from this repository in any real environment, and do NOT use the techniques shown here for unauthorized purposes.

## Structure

```
ai-security-goat/
├── LLM01-prompt-injection/
│   ├── <detector-id>/
│   │   ├── bad_<variant>.py   (one or more — each triggers the detector a different way)
│   │   ├── good.py            (mitigated equivalent — shared reference, not paired 1:1 with each bad file)
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
└── LLM10-unbounded-consumption/
```

Each top-level folder is one OWASP LLM Top 10:2025 category (its own `README.md` lists the specific detectors it covers). Each detector subfolder is self-contained: it can be scanned on its own, or the whole tree can be scanned at once.

**Note on detector coverage:** as of 2026-07-21, only some of these detectors are confirmed implemented in the Xygeni AI Security scanner (LLM01 and at least part of LLM10 have been observed producing real findings). The rest document the *intended* behavior per the product specs — scanning them today may produce no finding, which is itself useful signal about what's not implemented yet, not a fixture bug. Each `expected.yaml` for an unconfirmed detector says so explicitly.

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
