# GlacierEQ APEX Innovation Engine

This repository is a protocol substrate for **maximum coherent advance**. It is not a language monoculture, not a gate factory, and not a mechanism for shrinking an ambitious system until it becomes easy to govern.

## Human authority

Casey Barton is the sole human authority over GlacierEQ project direction, intent, and development target. System-generated policy, assistants, CI, projections, registries, merge state, receipts, or automation may verify facts and constrain false claims, but they do not acquire authority to redefine the intended system into a smaller one.

APEX is the controlling engineering mode.

## APEX objective

APEX optimizes the reachable system frontier, not minimum scope.

For a candidate architecture vector `x`:

```text
APEX(x) =
  capability
+ intelligence
+ reliability
+ leverage
+ composability
+ reach
+ frontier_fitness
- fragility
- coordination_cost
- unverifiability
- duplication
```

The exact weights may be specialized by domain, but the direction is invariant: maximize coherent useful power. A smaller system wins only when it actually produces the stronger APEX vector, not merely because it is smaller.

The preferred design set is the **non-dominated frontier**. When two designs represent real tradeoffs, preserve both as candidates and measure them. Do not manufacture a single answer by policy fiat.

`ApexVector` and `InnovationEngineState.apex_frontier()` make that objective executable.

## Prime directive

Every active GlacierEQ system must continuously move toward greater capability, reliability, intelligence, efficiency, leverage, composition, reach, and architectural fitness.

Truth, provenance, observability, and rollback exist to let the system move harder without losing reality. They are support structures for advance, not a substitute for advance.

The default loop is:

```text
OBSERVE FRONTIER
→ MAP PRESSURE AND OPPORTUNITY
→ GENERATE MULTIPLE STRONG CANDIDATES
→ COMPOSE THE BEST AVAILABLE TECHNOLOGIES
→ BUILD THE STRONGEST JUSTIFIED EXPERIMENT
→ MEASURE
→ ADVERSARIALLY BREAK IT
→ OPERATE IT
→ COMPARE APEX VECTORS
→ PRESERVE THE WINNER AND ALL UNIQUE GAINS
→ EXPAND THE FRONTIER AGAIN
```

A tiny vertical slice is permitted when it accelerates this loop. It is never the governing target.

## Tower of Babel law

Languages are assigned by engineering boundary, not organizational convenience.

A repository MAY contain many languages. Each language MUST own a clearly named architecture lane with:

- one concern;
- one primary language/runtime;
- a measurable reason that technology fits the boundary;
- a versioned interface to adjacent lanes;
- repository-native proof;
- an explicit replacement path when a better technology wins.

No language receives estate-wide privilege. Python and TypeScript are tools, not constitutional monarchs.

Examples of legitimate lanes include kernel/runtime, durable memory, analytical query, accelerator kernels, control plane, browser/UI, distributed coordination, formal verification, numerical kernels, embedded logic, graph reasoning, declarative policy, and high-assurance boundary code.

A component dedicated to memory should be allowed to specialize aggressively around memory semantics. A kernel should be allowed to use kernel-grade technology. A proof boundary should use proof-oriented technology. Uniformity is not an engineering virtue when specialization produces a stronger system.

## Innovation versus proof

Experimentation is intentionally easier than production claims.

A bounded reversible experiment may run when it has a baseline, candidate, expected advantage, measurement plan, and rollback. Experiments may be ambitious. They do not need to pretend the candidate is already proven.

Operational claims require evidence appropriate to the claim: deterministic tests, adversarial tests, runtime observation, observability, rollback proof, benchmarks, hardware receipts, or formal verification.

Evidence limits what may be **claimed**. It does not limit what may be **attempted** when the attempt is controlled and reversible.

## Reliability definition

Reliability is not immobility. A reliable system can change quickly because it can detect failure, isolate it, recover, measure the result, and preserve prior gains.

An operational capability should converge on:

1. deterministic behavior proof;
2. adversarial/failure-path proof;
3. runtime observation;
4. observability sufficient to diagnose drift;
5. proven rollback or recovery;
6. preservation of unique capability through replacement or migration.

## Daily frontier metabolism

Every day, the estate ingests primary-source signals from major AI, model, runtime, compiler, database, hardware, standards, and research ecosystems, deduplicates them, classifies them by capability and maturity, maps them against active GlacierEQ systems, and opens ambitious but testable paths where the signal could materially extend the frontier.

Primary-source classes include vendor release notes, model/API changelogs, official repositories/releases, standards bodies, and original research. Secondary reporting may discover a signal but may not be the sole basis for technical adoption.

Every material signal resolves to one of:

```text
IGNORE_WITH_REASON | WATCH | EXPERIMENT | ADMIT | MIGRATE | RETIRE
```

`ADMIT` means the technology won its declared boundary under evidence. It does not grant authority over unrelated boundaries.

## Anti-collapse rules

APEX rejects these failure modes:

- reducing architecture merely to minimize the number of moving parts;
- exact-template cloning across unrelated systems;
- one-language-for-everything doctrine;
- policy gates with no capability-development path;
- proof systems that only prove the system remained unchanged;
- freezing dependencies merely because they are familiar;
- rewriting an ambitious source design into a smaller projection and then treating the projection as source truth;
- novelty theater without measurable advantage;
- architecture diversification without lane ownership;
- deleting prior gains during refactors or migrations;
- current-tech claims without a fresh primary-source observation;
- selecting the smallest candidate when a larger candidate is demonstrably more coherent and capable.

## Core machine primitives

`LanguageLane`, `FrontierSignal`, `InnovationProposal`, `ReliabilityContract`, `ApexVector`, and `InnovationEngineState` are exported so downstream systems can express APEX without inheriting an implementation language.
