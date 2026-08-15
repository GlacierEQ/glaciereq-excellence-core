# GlacierEQ Excellence Core

**Foundation protocol for the GlacierEQ innovation engine.**

This repository provides implementation-neutral contracts for evidence, interfaces, authority, frontier signals, language-lane ownership, bounded experimentation, and operational reliability. It is not a mandate that every downstream system be Python, inherit one base class, or copy one repository shape.

See [`INNOVATION_ENGINE.md`](INNOVATION_ENGINE.md) for the governing engineering model.

## What the core owns

- evidence and claim receipts;
- versioned producer/consumer envelopes;
- authority primitives;
- protocol compatibility;
- language-lane ownership contracts;
- daily frontier-signal representation;
- bounded innovation proposals;
- reliability promotion state.

## What the core does **not** own

- the implementation language of downstream systems;
- the number of languages in a repository;
- one universal application framework;
- a requirement to subclass `BaseModule` when a different runtime boundary is better;
- technology selection that belongs to the Tower of Babel.

`BaseModule` remains available for Python components that actually benefit from it. It is no longer the canonical shape of every GlacierEQ system.

## Polyglot architecture

A repository may use Rust for a kernel/runtime lane, SQL for durable memory, Triton for accelerator kernels, TypeScript for a control plane, or any other justified technology combination. The requirement is not language uniformity. The requirement is **clear lane ownership, explicit interfaces, measurable advantage, and proof**.

```python
from glaciereq_excellence_core import InnovationEngineState, LanguageLane

state = InnovationEngineState(
    system_id="example",
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
```

## Innovation loop

```text
OBSERVE FRONTIER
→ MAP TO A REAL BOTTLENECK
→ DESIGN A REVERSIBLE CANDIDATE
→ EXPERIMENT
→ MEASURE
→ ADVERSARIAL TEST
→ OPERATE
→ PROMOTE OR ROLLBACK
→ REPEAT
```

Experimentation is deliberately easier than promotion. New technology should be tried quickly in bounded form. Operational claims still require evidence.

## Reliability

`ReliabilityContract.operational()` requires deterministic tests, adversarial tests, runtime observation, observability, and rollback proof. Reliability therefore means the system can evolve aggressively **without losing the ability to detect, diagnose, recover, and prove what happened**.

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

The new innovation primitives are:

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

The foundation should make stronger systems easier to build. If a rule preserves a known state by preventing justified improvement, the rule is defective.
