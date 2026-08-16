# GlacierEQ Excellence Core

**Foundation protocol for the GlacierEQ APEX innovation engine.**

This repository provides implementation-neutral contracts for evidence, interfaces, frontier signals, language-lane ownership, experimentation, operational reliability, and maximum coherent advance. It is not a mandate that downstream systems be Python, inherit one base class, copy one repository shape, or collapse toward the smallest governable implementation.

See [`INNOVATION_ENGINE.md`](INNOVATION_ENGINE.md) for the APEX engineering model.

## APEX

APEX is the controlling engineering mode: maximize coherent capability, intelligence, reliability, efficiency, leverage, composability, reach, and frontier fitness while minimizing fragility, coordination cost, unverifiability, and duplication.

Casey Barton is the sole human authority over GlacierEQ project direction and intended system scope. Automation, assistants, tests, receipts, merge state, and generated projections may verify facts. They may not redefine the target into a smaller system merely because the smaller system is easier to govern.

`ApexVector` makes the optimization target machine-readable. `InnovationEngineState.apex_frontier(vectors, weights=...)` preserves every non-dominated candidate and uses optional `ApexWeights` only to order real tradeoffs. All objective values and weights are finite and non-negative.

## What the core owns

- evidence and claim receipts;
- versioned producer/consumer envelopes;
- protocol compatibility;
- language-lane ownership contracts;
- frontier-signal representation;
- innovation proposals and experiments;
- reliability state;
- APEX objective vectors, domain weights, and Pareto-frontier selection.

## What the core does **not** own

- the implementation language of downstream systems;
- the number of languages in a repository;
- one universal application framework;
- a requirement to subclass `BaseModule` when a different runtime boundary is better;
- authority to reduce user intent;
- technology selection that belongs to the Tower of Babel boundary analysis.

`BaseModule` remains available for Python components that actually benefit from it. It is not the universal shape of GlacierEQ systems.

## Polyglot architecture

A repository may use Rust for a kernel/runtime lane, SQL for durable memory, Triton for accelerator kernels, TypeScript for a control plane, Julia for numerical kernels, Lean for proof, or any other justified combination. The requirement is not language uniformity. The requirement is **clear lane ownership, explicit interfaces, measurable advantage, and proof**.

```python
from glaciereq_excellence_core import (
    ApexVector,
    ApexWeights,
    InnovationEngineState,
    LanguageLane,
)

state = InnovationEngineState(
    system_id="example",
    apex=ApexVector(
        capability=9,
        intelligence=9,
        reliability=9,
        efficiency=9,
        leverage=8,
        composability=9,
        reach=8,
        frontier_fitness=9,
        fragility=1,
        coordination_cost=2,
    ),
    lanes=[
        LanguageLane(
            lane_id="kernel",
            concern="kernel_runtime",
            language="Rust",
            rationale="memory safety and predictable native execution",
            interface="versioned C ABI",
            proof="native tests + runtime receipt",
        ),
        LanguageLane(
            lane_id="memory",
            concern="durable_memory",
            language="SQL",
            rationale="transactional persistence and declarative query semantics",
            interface="versioned schema",
            proof="migration + transaction + recovery tests",
        ),
    ],
)

frontier = InnovationEngineState.apex_frontier(
    [state.apex, ApexVector(capability=10, efficiency=7, reach=10, reliability=8)],
    weights=ApexWeights(reliability=3, efficiency=2, reach=1),
)
```

## APEX loop

```text
OBSERVE FRONTIER
→ MAP PRESSURE AND OPPORTUNITY
→ GENERATE STRONG CANDIDATES
→ COMPOSE BEST-FIT TECHNOLOGIES
→ BUILD
→ MEASURE
→ ADVERSARIALLY TEST
→ OPERATE
→ COMPARE APEX VECTORS
→ PRESERVE WINNER + UNIQUE PRIOR GAINS
→ EXPAND AGAIN
```

Experimentation is deliberately easier than operational promotion. New technology should be tried rapidly when it has a credible path to a stronger boundary.

A narrow experiment is a tactic, not the objective. The objective is the strongest coherent system we can actually make work.

## Reliability

`ReliabilityContract.operational()` requires deterministic tests, adversarial tests, runtime observation, observability, and rollback proof. Reliability means the system can evolve aggressively **without losing the ability to detect, diagnose, recover, preserve gains, and prove what happened**.

## Existing protocol primitives

The original primitives remain available:

- `EvidencePacket`
- `ClaimReceipt`
- `EnvelopeContract`
- `AuthorityMatrix`
- `QuorumVote`
- `BaseModule`
- `serialize()` / `deserialize()`
- schema validation and protocol versioning

The APEX innovation primitives are:

- `ApexVector`
- `ApexWeights`
- `LanguageLane`
- `FrontierSignal`
- `InnovationProposal`
- `ReliabilityContract`
- `InnovationEngineState`

## Installation

```bash
pip install git+https://github.com/GlacierEQ/glaciereq-excellence-core.git
```

## Verification

```bash
python -m pytest -q
```

The foundation exists to make stronger systems easier to build. Any rule that preserves a known state by preventing justified coherent advance is defective.
