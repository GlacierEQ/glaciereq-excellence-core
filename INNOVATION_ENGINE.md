# GlacierEQ Innovation Engine Foundation

This repository is a protocol substrate, not a language monoculture and not a gate factory.

## Prime directive

Every active GlacierEQ system must continuously move toward greater capability, reliability, intelligence, efficiency, and architectural fitness. Governance preserves truth, provenance, rollback, and safety. It must not freeze a system merely because the current state is known.

The default loop is:

```text
OBSERVE FRONTIER → MAP PRESSURE → DESIGN CANDIDATE → BOUNDED EXPERIMENT
→ MEASURE → ADVERSARIAL TEST → OPERATE → PROMOTE OR ROLLBACK → REPEAT
```

## Tower of Babel law

Languages are assigned by engineering boundary, not organizational convenience.

A repository MAY contain many languages. Each language MUST own a clearly named architecture lane with:

- one concern;
- one primary language/runtime;
- a measurable reason that language fits the boundary;
- a versioned interface to adjacent lanes;
- repository-native proof;
- an explicit replacement path when a better technology wins.

No language receives estate-wide privilege. Python and TypeScript are tools, not constitutional monarchs.

Examples of legitimate lanes include kernel/runtime, durable memory, analytical query, accelerator kernels, control plane, browser/UI, distributed coordination, formal verification, numerical kernels, embedded logic, and high-assurance boundary code.

## Innovation versus admission

Experimentation is intentionally easier than promotion.

A bounded, reversible experiment may run when it has a baseline, candidate, expected advantage, measurement plan, and rollback. It does not need to pretend the candidate is already proven.

Promotion requires evidence. The stronger the operational claim, the stronger the proof: deterministic tests, adversarial tests, runtime observation, observability, rollback proof, benchmarks, hardware receipts, or formal verification as appropriate.

## Reliability definition

Reliability is not immobility. A reliable system can change quickly because it can detect failure, isolate it, recover, measure the result, and roll back without corrupting truth.

An operational capability should therefore converge on:

1. deterministic behavior proof;
2. adversarial/failure-path proof;
3. runtime observation;
4. observability sufficient to diagnose drift;
5. proven rollback or recovery.

## Daily frontier metabolism

Every day, the estate should ingest primary-source signals from major AI/model/toolchain/research ecosystems, deduplicate them, classify them by capability and maturity, map them against active GlacierEQ bottlenecks, and create bounded experiments only where the signal could materially improve a system.

Primary-source classes include vendor release notes, model/API changelogs, official repositories/releases, standards bodies, and original research. Secondary reporting may discover a signal but may not be the sole basis for technical admission.

A news item is not an upgrade. The metabolism pipeline must produce one of: ignore with reason, watch, experiment, admit, migrate, or retire.

## Anti-stagnation rules

The foundation must reject these failure modes:

- exact-template cloning across unrelated systems;
- one-language-for-everything doctrine;
- governance gates with no capability-development path;
- proof systems that only prove the system remained unchanged;
- frozen dependencies justified only by age or familiarity;
- novelty theater without measurable advantage;
- architecture diversification without lane ownership;
- current-tech claims without a fresh primary-source observation.

## Core machine primitives

`LanguageLane`, `FrontierSignal`, `InnovationProposal`, `ReliabilityContract`, and `InnovationEngineState` are exported from `glaciereq_excellence_core` so downstream systems can express the innovation loop without inheriting an implementation language.
