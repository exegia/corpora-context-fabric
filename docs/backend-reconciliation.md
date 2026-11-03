# Backend RC reconciliation

This candidate integrates `cf-rust` at
`76f657781638a3d0876fc716d4523f7c631f720f` with the fork master/dev base
`2e58fccadc6440c906243f3c4c7d5b5ff83563bb`. The merge is conflict-free and retains
both master-only documentation commits. No browser/explorer frontend is introduced.
`master` remains the upstream tracking branch; `dev` is the backend integration target.

The new Backend integration workflow tests PRs to dev on the current hosted macOS ARM image with Python
3.13/3.14. Existing upstream workflows remain unchanged. This workflow does not
publish packages or execute Windows/Linux qualification.

## Local validation, November 3, 2026

On macOS 27.0.1 ARM64, CPython 3.13.15:

- Rust formatting and Clippy pass; 129 Rust tests pass.
- Built and installed engine: 341 Python tests pass, 21 skip because optional
  corpus fixtures are unavailable. Tests run outside the source package to ensure
  the installed compiled extension is loaded.
- Standalone MCP tests: 168 pass, including local stdio/SSE/HTTP transport tests.
- Benchmark contract tests: 56 pass. No new performance claim is made.
- Current Corpora Python dev plus its rebuilt native conversion wheel: 24 native
  CLI/converter acceptance tests pass; 113 API/runtime/converter contracts pass
  after a consumer-test correction for the sectionFeatures representation.

Standalone cfabric-mcp requires MCP 1.x; Corpora's separate FastMCP stack resolves
MCP 2.x. Validate them in separate environments. Incremental installation of one
stack into the other does not establish a compatible combined environment.

## Remaining gates

Hosted checks on the published candidate are separate from local results. Full
corpus parity/performance, Python 3.14 runtime validation, public package
installation and release authorization remain separate gates. Historical baseline
results retain their failures/skips and are not replaced by these bounded checks.
Windows qualification is on hold and Linux qualification is deferred. Default
Corpora conversion remains Python; native TEI stays opt-in. No UI integration or
production deployment is part of this candidate.

## Revised macOS acceptance, November 3, 2026

The user withdrew minimum macOS 15 qualification. The workflow now uses
`macos-latest` while preserving ARM and Python 3.13/3.14 coverage and all test
steps. Local macOS 27.0.1 ARM64 results remain explicitly local: 129 Rust,
347 installed-engine (21 optional-corpus skips), 168 MCP and 56 benchmark
tests passed after the six regression cases were added. The Python backend
suite against the fixed engine passed 1103 tests with 39 skips. Earlier
hosted capacity failures are not passes and do not certify any OS version.
