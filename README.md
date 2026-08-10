# GlacierEQ Excellence Core

Shared primitives, base classes, and protocols for the GlacierEQ excellence pack ecosystem.

## Purpose

This repository provides the common contracts used across the excellence packages so each package can expose a consistent interface while remaining domain-specific.

## Core abstractions

- `ClaimReceipt`
- `EnvelopeContract`
- `AuthorityMatrix`
- `QuorumVote`
- `EvidencePacket`
- `BaseModule`

## Design goals

- Deterministic outputs.
- Explicit evidence handling.
- Typed interfaces.
- Reusable orchestration contracts.
- Lightweight Python packaging.

## Initial layout

- `src/glaciereq_excellence_core/models.py`
- `src/glaciereq_excellence_core/base.py`
- `tests/test_core.py`
