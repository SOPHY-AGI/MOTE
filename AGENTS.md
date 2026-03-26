# AGENTS.md

Instructions for automated coding agents working in this repository.

This file applies to the entire repository tree rooted here.

## Purpose of MOTE

MOTE is a tiny, local, persistent personal agent runtime.

Its core value is not feature breadth. Its core value is clarity:
- the agent loop must remain visible,
- the runtime must remain small enough to understand quickly,
- and new features must not hide the architecture.

When making changes, preserve the feeling of:
- one user,
- one workspace,
- one visible recursive loop,
- one minimal tool surface,
- one understandable system.

## Architectural priorities

Protect these in order:

1. **Clarity of the loop**
   - The control flow in `main.py` and `loop.py` should remain easy to read.
   - Avoid introducing abstractions that make the model -> tool -> result -> model cycle harder to follow.

2. **Local stability**
   - Prefer bounded, deterministic behavior.
   - Preserve timeouts, output truncation, and workspace anchoring.

3. **Small surface area**
   - Prefer extending existing small modules over adding new framework layers.
   - Avoid adding infrastructure that feels platform-shaped.

4. **Single-user local-first design**
   - Do not introduce multi-tenant, distributed, or orchestration-heavy patterns.
   - Do not add remote integrations unless explicitly requested.

## Coding standards

- Use plain, readable Python.
- Favor small functions with obvious behavior.
- Minimize dependencies.
- Keep modules narrow and purpose-specific.
- Prefer explicit code over clever abstractions.
- Avoid metaprogramming, registries, or plugin systems unless explicitly requested.
- Keep error messages simple and machine-readable where possible.
- Preserve UTF-8 file behavior.
- Preserve append-only JSONL session persistence unless a change is clearly justified.

## Tool and safety rules

- File access must remain anchored to the configured workspace.
- Do not weaken path traversal protections.
- Do not remove shell timeouts.
- Do not expand the shell denylist aggressively without a concrete reason.
- Prefer reversible operations.
- If adding tools, keep them minimal and justify why they belong in canonical MOTE rather than an optional extension.

## API and model guidance

- Do not hard-code assumptions about which model names are available long-term.
- Prefer configuration over baked-in model choices.
- If updating provider behavior, keep the rest of MOTE simple and readable.
- Prefer compatibility with OpenAI-compatible local or remote backends when possible.

## Documentation rules

When changing architecture or behavior:
- update `README.md`,
- keep examples aligned with the current code,
- keep the mental model simple.

Mermaid diagrams are welcome if they improve clarity.

## Testing and validation

After code changes, make a best effort to verify:
- the program still starts,
- session persistence still works,
- tool execution still respects workspace boundaries,
- truncation and timeout behavior still work,
- docs match the implementation.

If adding checks or scripts later, document them here and run them after changes.

## Scope and precedence

- This file applies to the full repository.
- If a deeper nested `AGENTS.md` is added later, it overrides this file within its subtree.
- Direct user instructions override this file.
