# Governable Capability Monitor (GCM) Prototype

**AWS-native AI governance demonstration showcasing the four principles of Governable Capability.**

> ⚠️ **Security Remediation Complete**: All 13 critical security/logic/performance issues identified in code review have been fixed. See [REMEDIATION.md](REMEDIATION.md) for details.

## Principles

1. **Runtime Control Coherence** — Detect conflicting control loops between schedulers, policy layers, and circuit breakers
2. **Tool-Call Graph Monitoring** — Visualize expanding tool chains and detect expansion without progress  
3. **Structural Waste Detection** — Measure the gap between model capability and system productivity
4. **Execution Reconstruction** — Full audit trail with replay capability for multi-step planning

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│  DEMO AGENT (Bedrock AgentCore)                          │
│  • Simulated loan approval agent with 4 failure modes     │
└────────────────┬───────────────────────────────────────────┘
                 │ EventBridge
┌────────────────▼───────────────────────────────────────────┐
│  GCM CONTROL PLANE (Serverless)                          │
│  ┌──────────────┬──────────────┬──────────────┐           │
│  │ Coherence    │ Tool-Call    │ Waste        │           │
│  │ Detector     │ Tracer       │ Meter        │           │
│  │ (Lambda)     │ (Lambda)     │ (Lambda)     │           │
│  └──────────────┴──────────────┴──────────────┘           │
│  ┌──────────────────────────────────────────┐             │
│  │ Reconstructor (DynamoDB + S3)            │             │
│  └──────────────────────────────────────────┘             │
└────────────────────────────────────────────────────────────┘
                 │
┌────────────────▼───────────────────────────────────────────┐
│  DASHBOARD (React + CloudFront)                          │
│  • 4 Principle tabs (live updates)                        │
│  • Demo playback controls                                 │
│  • Before/after comparison                                │
└────────────────────────────────────────────────────────────┘
```

## Quick Deploy

```bash
cd backend
sam build
sam deploy --guided --parameter-overrides Environment=dev
```

## Security Features

- ✅ KMS encryption at rest (DynamoDB, S3, EventBridge, SQS)
- ✅ Input validation with JSON Schema
- ✅ Least-privilege IAM policies
- ✅ Dead Letter Queue (DLQ) for failed processing
- ✅ Idempotency keys for stream processing
- ✅ No hardcoded credentials
- ✅ S3 public access blocked

## Demo Script

See `docs/demo-script.md` for the full walkthrough.

## Documentation

- [REMEDIATION.md](REMEDIATION.md) - Security & performance fixes applied
- [SAM Template](backend/template.yaml) - Infrastructure as Code
- [Lambda Functions](backend/src/) - GCM principle implementations

## License

MIT
