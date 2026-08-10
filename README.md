# GlacierEQ Excellence Core

**Layer 1 foundation** for the GlacierEQ Tower of Babel — shared primitives, base classes, serialization helpers, schema validators, and protocol versioning consumed by all 37 excellence pack modules.

[![CI](https://github.com/GlacierEQ/glaciereq-excellence-core/actions/workflows/ci.yml/badge.svg)](https://github.com/GlacierEQ/glaciereq-excellence-core/actions/workflows/ci.yml)

---

## Install

```bash
pip install git+https://github.com/GlacierEQ/glaciereq-excellence-core.git
```

---

## Core abstractions

| Class | Purpose |
|---|---|
| `EvidencePacket` | A single piece of evidence: source, hash, metadata |
| `ClaimReceipt` | A verifiable claim with status and attached evidence |
| `EnvelopeContract` | Producer/consumer contract with schema version constraints |
| `AuthorityMatrix` | Role-based action permission table |
| `QuorumVote` | Threshold-based multi-approver decision |
| `BaseModule` | Abstract base every pack module must subclass |

---

## Serialization

All packs exchange artifacts as JSON. Use `serialize()` / `deserialize()` — never call `.model_dump()` directly. The helpers embed the current protocol version into every artifact so receivers can reject stale or future payloads.

```python
from glaciereq_excellence_core import serialize, deserialize, ClaimReceipt

receipt = ClaimReceipt(claim_id="c1", subject="demo", status="open")
raw = serialize(receipt)          # JSON string with _protocol_version embedded
back = deserialize(raw, ClaimReceipt)  # fails fast if versions incompatible
```

---

## Schema validation

Call `validate_payload()` on any untrusted input before deserializing. Built-in schemas: `CLAIM_SCHEMA`, `ENVELOPE_SCHEMA`.

```python
from glaciereq_excellence_core import validate_payload, CLAIM_SCHEMA

validate_payload(incoming_dict, CLAIM_SCHEMA)  # raises jsonschema.ValidationError if invalid
```

---

## Protocol versioning

Version is `major.minor.patch`. Compatibility rule: major must match, artifact minor ≤ current minor.

```python
from glaciereq_excellence_core import CURRENT_VERSION  # ProtocolVersion(1, 0, 0)
```

Bump `CURRENT_VERSION` in `versioning.py` on any breaking schema change and update downstream pack dependencies.

---

## How to build a downstream excellence pack

Every downstream repo follows this exact pattern:

### 1. Depend on this core

In your pack's `pyproject.toml`:

```toml
[project]
dependencies = [
  "glaciereq-excellence-core @ git+https://github.com/GlacierEQ/glaciereq-excellence-core.git"
]
```

### 2. Subclass `BaseModule`

```python
from glaciereq_excellence_core import BaseModule, ClaimReceipt, EvidencePacket
from glaciereq_excellence_core import validate_payload, serialize

INPUT_SCHEMA = {
    "type": "object",
    "required": ["claim_id", "subject"],
    "properties": {
        "claim_id": {"type": "string"},
        "subject": {"type": "string"}
    }
}

class MyPackModule(BaseModule):
    name = "my-pack-module"
    version = "0.1.0"

    def run(self, payload):
        validate_payload(payload, INPUT_SCHEMA)
        evidence = EvidencePacket(source=self.name, content_hash="sha256:...", metadata={})
        receipt = ClaimReceipt(
            claim_id=payload["claim_id"],
            subject=payload["subject"],
            status="pending",
            evidence=[evidence]
        )
        return {"status": "ok", "result": serialize(receipt)}
```

### 3. Return a typed result

`run()` must always return `{"status": "ok" | "error", "result": ...}`. Errors surface as `{"status": "error", "detail": str}`.

### 4. Add CI

Copy `.github/workflows/ci.yml` from this repo into your pack repo and replace the repo name. Tests in `tests/` run on every push.

---

## Worked example

See [`src/glaciereq_excellence_core/example_module.py`](src/glaciereq_excellence_core/example_module.py) for `NullGateModule` — the canonical template every downstream pack should start from.

---

## Repository layout

```
glaciereq-excellence-core/
├── .github/workflows/ci.yml      # CI: test on Python 3.10, 3.11, 3.12
├── src/
│   └── glaciereq_excellence_core/
│       ├── __init__.py
│       ├── base.py               # BaseModule ABC
│       ├── models.py             # Pydantic data models
│       ├── serialization.py      # serialize() / deserialize()
│       ├── schema.py             # validate_payload(), CLAIM_SCHEMA, ENVELOPE_SCHEMA
│       ├── versioning.py         # ProtocolVersion, CURRENT_VERSION
│       └── example_module.py     # NullGateModule worked example
├── tests/
│   └── test_core.py
├── pyproject.toml
├── LICENSE
└── README.md
```
