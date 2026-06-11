# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a DevOps learning and practice repository covering multiple technologies: Kubernetes, GitHub Actions CI/CD, Jenkins, Python scripting, and AWS AgentCore agent deployment.

## Areas of the Repository

### Kubernetes (`kubernetes/`)
- `tutorial/` — YAML manifests for learning: pods, deployments, services, namespaces, configmaps
- `practices/` — Hands-on exercises including a MySQL deployment with persistent storage, secrets, and configmaps
- Reference commands are documented in `Readme-Kubernetes.md`

### GitHub Actions (`.github/workflows/`)
- `test_1.yml` — Multi-job workflow (hola → other, test-build) triggered on push to `main`
- `script.sh` — Shell script executed within the workflow

### Python Scraper (`precios_cuidados/`)
- SQLAlchemy-backed scraper using BeautifulSoup + requests
- Models in `models.py`, DB setup in `db.py`, scraping logic in `scrapping.py`
- Dependencies: `pip install -r precios_cuidados/requirements.txt`

### AWS AgentCore (`clase_surfeando_nube/AgenteCurso2026/`)
- Agent defined in `agentcore/agentcore.json` — Container build, Python 3.14, HTTP protocol
- App code lives in `app/AgenteCurso2026/main.py` (entrypoint)
- CDK infrastructure in `agentcore/cdk/`
- Secrets go in `agentcore/.env.local` (gitignored)

## Key Commands

### Kubernetes (minikube)
```bash
minikube start -p <profile>
kubectl apply -f <file.yaml>
kubectl get pods -A
kubectl describe pod <name>
kubectl scale deployment <name> --replicas=<n>
kubectl rollout history deployment <name>
kubectl rollout undo deployment <name> --to-revision=<n>
```

### AWS AgentCore
```bash
agentcore dev          # Run agent locally with hot-reload
agentcore deploy       # Deploy to AWS via CDK
agentcore invoke       # Invoke agent (local or deployed)
agentcore validate     # Validate agentcore.json configuration
agentcore logs         # View agent logs
agentcore status       # Show deployment status
```

### Python scraper
```bash
pip install -r precios_cuidados/requirements.txt
python precios_cuidados/scrapping.py
```

## AgentCore Architecture

The AgentCore agent uses a flat resource model defined in `agentcore/agentcore.json`:
- **Runtime**: Container build deployed to AgentCore Runtime (PUBLIC network, HTTP protocol)
- **Memory**: `AgenteCurso2026Memory` with 30-day event expiry
- **Credentials**: OpenAI API key via `ApiKeyCredentialProvider`
- Infrastructure is managed by CDK (`managedBy: "CDK"`) — edit `agentcore/cdk/lib/cdk-stack.ts` for infra changes, not the JSON directly when CDK-managed resources are involved.
