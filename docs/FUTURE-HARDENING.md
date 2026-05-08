# Future Hardening Path — GCM Prototype

This document outlines the staged maturation path for the Governable Capability Monitor, based on feedback from [Gregor Wegener](https://independent-research-systems-modeling.com/catalog.html) on SORT-AI alignment.

## Three-Stage Hardening Model

### Stage 1: Conceptual Alignment ✅ CURRENT

**Status:** Implemented May 2026

**Objective:** Precise terminology and diagnostic references without claiming full framework implementation.

**Deliverables:**
- AI.04.S1-aligned documentation for Coherence Detector (explicit runtime control conflict)
- AI.30-aligned documentation for Reconstructor (structural stability evidence pack)
- AI.47 documentation-level alignment for Waste Meter (capability-productivity divergence)
- AI.52 documented as future hardening candidate (weak-signal aggregation)
- Attribution hygiene: explicit framing as diagnostic references, not full SORT-AI implementation

### Stage 2: Semantic Hardening ⚠️ LIMITED SCOPE

**Status:** Partial exploration; full implementation not current priority

**Objective:** Move from monitored signals toward diagnostic interpretation.

**Potential Enhancements:**
- **Evidence-completeness scoring:** Quantify reconstruction quality (AI.30 Stage 2)
- **Source vs. derived evidence distinction:** Separate raw runtime events from interpreted diagnostic states
- **Minimal event schema:** Formalize event taxonomy for cross-module consistency
- **SOV.03 auditability surface:** Dashboard outputs explicitly supporting audit defense
- **SOV.05 decision-translation:** Executive-facing outputs (proceed, monitor, constrain, defer, revisit)

**Boundary:** Stage 2 enhancements should not expand prototype beyond four-module demo scope.

### Stage 3: Formal Structural Diagnosis ❌ NOT CURRENT SCOPE

**Status:** Documented for future reference only

**Objective:** Full SORT-AI implementation with formal state representation.

**Would Require:**
- Explicit state representation and projection logic
- Structural deviation measures
- Kernel-modulated coherence evaluation
- Complete AI.04, AI.30, AI.52, AI.47 implementations
- SOV-layer translation as first-class modules

**Recommendation:** Do not pursue Stage 3 until GCM evolves beyond demonstration scope into production governance platform.

---

## Three Regimes of Runtime Control Coherence

The Coherence Detector currently implements **AI.04.S1 (Explicit Conflict)**. Two additional regimes are documented as future hardening:

### S1: Multi-Layer Runtime Control Stack ✅ IMPLEMENTED

**Detection Surface:**
- Scheduler conflicts (equal priorities, resource contention)
- Policy contradictions (ALLOW vs. BLOCK decisions)
- Circuit-breaker abuse (frequency, pattern, recovery)

**Visibility:** High — explicit conflict events

**Implementation:** Real-time detection in Coherence Detector Lambda

### S2: Hidden Retry Amplification 🔮 FUTURE HARDENING

**Detection Surface:**
- Success metrics remain high while actual attempt multipliers increase
- Cost per successful completion inflates
- Capacity-planning error grows

**Visibility:** Low — incoherence not visible at KPI surface; appears as cost-incoherent execution behind nominally healthy success rates

**Minimal Entry Point (Optional):**
- Retry cost tracking
- Success-rate-versus-attempt-count divergence
- Actual attempt multiplier logging

**Caution:** Do not present minimal S2 signals as full S2 detection. Document clearly as exploratory.

### S3: SLA-Adjacent Runtime Operation 🔮 FUTURE HARDENING

**Detection Surface:**
- Reactive control loops near service-level boundaries
- SLA compliance preserved while stability margins consumed
- Diminishing returns on capacity additions

**Visibility:** Very low — presents as oscillation rather than explicit conflict; detectable only over time via temporal analysis

**Requirements for Detection:**
- Margin erosion tracking
- Control-loop interaction analysis
- Time-series coherence evaluation

**Recommendation:** Remains future hardening for current demo scope. Requires Stage 2 semantic hardening as prerequisite.

---

## Module-Specific Hardening Roadmap

### Coherence Detector

**Current (Stage 1):**
- AI.04.S1-aligned: Explicit conflict detection (scheduler, policy, circuit-breaker)

**Stage 2 (Limited):**
- Minimal S2 signal: Retry cost anomaly flagging
- Source vs. derived evidence tagging

**Future (Not Current Scope):**
- Full S2: Hidden retry amplification detection
- Full S3: SLA-adjacent oscillation detection
- Kernel-modulated coherence evaluation (Stage 3)

### Reconstructor

**Current (Stage 1):**
- AI.30-aligned: Evidence-complete reconstruction
- Output labeling: "AI.30-aligned Evidence Pack"

**Stage 2 (Limited):**
- Evidence-completeness scoring (0-100% reconstruction quality)
- Auditability surface (SOV.03): Reconstruction defensibility metrics
- Decision-translation layer (SOV.05): Summary recommendations

**Future (Not Current Scope):**
- Real-time reconstruction streaming
- Cross-execution pattern mining
- Predictive reconstruction (pre-incident capture)

### Waste Meter

**Current (Stage 1):**
- AI.47 documentation-level: Capability-productivity divergence
- Operational labels: Neutral ("evaluation_deployment_divergence")

**Stage 2 (Limited):**
- Evaluation-context projection instability scoring
- Benchmark-to-production drift quantification

**Future (Not Current Scope):**
- Full AI.47: Evaluation baseline versioning and comparison
- Predictive waste forecasting

### Tool-Call Tracer

**Current (Stage 1):**
- Tool-call graph monitoring
- Cycle detection (DFS algorithm)
- Expansion-without-progress identification

**Stage 2 (Limited):**
- Tool semantic categorization (read/write/transform)
- Progress-velocity scoring

**Future (Not Current Scope):**
- AI.52 integration: Weak-signal aggregation across tool chains
- Predictive tool-call optimization

### Cross-Module: AI.52 Weak-Signal Aggregator

**Status:** Documented as fifth-module candidate; not current scope

**Concept:** Aggregate low-amplitude indicators across Coherence, Tool-Call, Waste, and Reconstruction modules to surface distributed early degradation that no single module can classify independently.

**Prerequisites:**
- Stage 2 semantic hardening across existing modules
- Common event schema formalization
- Normalized signal taxonomy

**Implementation Path:**
1. Document as natural extension in README
2. Develop event schema (Stage 2)
3. Implement as optional fifth Lambda (future hardening)

---

## Attribution and Scope Hygiene

All SORT-AI references in this prototype are:
- **Diagnostic alignments:** Conceptual references strengthening semantic precision
- **Explicitly scoped:** Stage 1 (current), Stage 2 (limited), or Future (not current)
- **Non-claiming:** Not asserting full SORT-AI framework implementation
- **Attributed:** Derived from public SORT-AI material (https://independent-researchs-systems-modeling.com/catalog.html)

**Code-Level Labels:**
- Docstrings reference SORT-AI IDs (AI.04.S1, AI.30, etc.)
- Operational logs remain implementation-neutral
- Dashboard outputs may reference alignment for transparency

**README Presentation:**
- SORT-AI alignment table for conceptual clarity
- Clear boundary between current implementation and future hardening
- Link to public application catalog for reference

---

## Decision Log

**May 2026:** Implemented Stage 1 conceptual alignment per Gregor Wegener feedback. Documented S2/S3 as future hardening. Positioned AI.52 as fifth-module candidate. Committed to limited Stage 2 semantic hardening without expanding demo scope.

**Next Review:** Upon GCM prototype evolution from demo to production candidate, reassess Stage 2 completion and Stage 3 feasibility.
