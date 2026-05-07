[![Deploy to AWS](https://img.shields.io/badge/Deploy-AWS-orange?logo=amazon-aws)](https://github.com/kdeath83/aws-gcm-prototype/actions/workflows/deploy.yml)

# Governable Capability Monitor (GCM)

**Exploring the next frontier of AI governance: structural boundaries for productive capability.**

This prototype is inspired by the thinking of [Gregor Wegener](https://www.linkedin.com/pulse/next-frontier-governable-capability-gregor-wegener-mdt0f/) on *Governable Capability* — the recognition that AI systems need runtime control coherence, not just capability benchmarks, to remain productive in deployment.

## 🚀 One-Click Deploy to AWS

### Option 1: GitHub Actions (Recommended)
Fork this repo, add AWS credentials as GitHub secrets, and push to `main`:

```yaml
AWS_ACCESS_KEY_ID: your-access-key
AWS_SECRET_ACCESS_KEY: your-secret-key
AWS_REGION: us-east-1
```

### Option 2: Local One-Click
```bash
chmod +x scripts/one-click-deploy.sh
./scripts/one-click-deploy.sh
```

### Option 3: Manual SAM
```bash
cd backend
sam build
sam deploy --guided --parameter-overrides Environment=prod
```

## The Core Insight

> "The gap between model capability and system productivity is structural, not algorithmic."

Raw capability without governance decays into latency, waste, and audit failure. GCM surfaces the structural dynamics that make capable agents unproductive — and provides the observability layer to fix them.

**[Read the full philosophy →](docs/PHILOSOPHY.md)**

## Four Principles of Governable Capability

1. **Runtime Control Coherence** — When schedulers, policy layers, and circuit breakers conflict, the system becomes unpredictable. GCM detects these control loop collisions in real-time.

2. **Tool-Call Graph Monitoring** — Agents can expand their tool invocation graphs without making progress. GCM visualizes these expansion-without-progress patterns before they become infinite loops.

3. **Structural Waste Detection** — The gap between benchmarked capability and realized productivity is measurable. GCM quantifies activation degradation — where capability exists but doesn't translate to output.

4. **Execution Reconstruction** — Multi-step planning requires auditability. GCM captures full execution traces with decision rationale, enabling compliance-ready reconstruction of any agent decision.

## Architecture: AWS-Native by Design

GCM is built entirely on AWS managed services — no external dependencies, no infrastructure to maintain.

```
┌────────────────────────────────────────────────────────────┐
│  AGENT (Bedrock AgentCore)                               │
│  • Loan approval demo with 4 failure scenarios          │
└────────────────┬───────────────────────────────────────────┘
                 │ EventBridge (real-time events)
┌────────────────▼───────────────────────────────────────────┐
│  GCM CONTROL PLANE (Serverless)                          │
│  ┌──────────────┬──────────────┬──────────────┐           │
│  │ Coherence    │ Tool-Call    │ Waste        │           │
│  │ Detector     │ Tracer       │ Meter        │           │
│  │ (Lambda)     │ (Lambda)     │ (Lambda)     │           │
│  └──────────────┴──────────────┴──────────────┘           │
│  ┌──────────────────────────────────────────┐             │
│  │ Reconstructor (DynamoDB Streams + S3)      │             │
│  └──────────────────────────────────────────┘             │
└────────────────────────────────────────────────────────────┘
                 │ WebSocket API
┌────────────────▼───────────────────────────────────────────┐
│  DASHBOARD (React + CloudFront)                          │
│  • Live principle tabs with drill-down                   │
│  • Execution replay with pause/inspect                   │
│  • Before/after comparison mode                          │
└────────────────────────────────────────────────────────────┘
```

## Post-Deployment

Get your WebSocket URL for the dashboard:
```bash
aws cloudformation describe-stacks \
  --stack-name gcm-prototype-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`WebSocketEndpoint`].OutputValue' \
  --output text
```

## Why This Matters

As organizations deploy more autonomous AI agents, they hit a wall: the agents work in development but fail in production. Not because the models are wrong, but because the governance structure around them is incoherent.

GCM makes those structural failures visible — and fixable.

## 🚀 Deploy to AWS

### Option 1: GitHub Actions (Recommended)
Fork this repo, add AWS credentials as GitHub secrets, and push to `main`:

```yaml
AWS_ACCESS_KEY_ID: your-access-key
AWS_SECRET_ACCESS_KEY: your-secret-key
AWS_REGION: us-east-1
```

### Option 2: Local One-Click
```bash
chmod +x scripts/one-click-deploy.sh
./scripts/one-click-deploy.sh
```

### Option 3: Manual SAM
```bash
cd backend
sam build
sam deploy --guided --parameter-overrides Environment=prod
```

### Post-Deployment
Get your WebSocket URL:
```bash
aws cloudformation describe-stacks \
  --stack-name gcm-prototype-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`WebSocketEndpoint`].OutputValue' \
  --output text
```

## Acknowledgments

This work is inspired by conversations with **Gregor Wegener** on the [next frontier of governable capability](https://www.linkedin.com/pulse/next-frontier-governable-capability-gregor-wegener-mdt0f/). His framing of runtime control coherence, structural waste, and execution reconstructability shaped the principles implemented here.

## License

MIT
