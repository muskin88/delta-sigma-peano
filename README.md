# Δ-Σ Reconstruction of Peano Arithmetic

**Experimental proof** that natural numbers emerge from two operators: **Δ (distinction)** and **Σ (connection)**.

## Core Idea
- **Δ**: Branching, choice (`Z` vs `S`)  
- **Σ**: Composition, succession (`S(n) = succ(n)`)

From these two primitives, we reconstruct:
- Natural numbers: `Z`, `S(Z)`, `S(S(Z))`, ...
- Addition: `add(a, b) = Δ(b) ? a : succ(add(a, b.pred))`
- Multiplication: as iterated addition

## Quick Run
```bash
python delta_sigma.py