# DevLaunch — Kubernetes Platform Engineering Project

DevLaunch is a hands-on platform engineering project demonstrating containerization, Kubernetes deployments, Helm packaging, CI security scanning, container image publishing, and GitOps-based delivery with Argo CD.

## Architecture

```text
Developer pushes code to GitHub
             |
             v
      GitHub Actions CI
      - Build Docker image
      - Lint Helm chart
      - Render Kubernetes manifests
      - Scan image with Trivy
             |
             v
       GitHub Container Registry
       (GHCR, commit-SHA tags)
             |
             v
       GitHub repository
       (Helm chart and values)
             |
             v
           Argo CD
       (automated sync and
        self-healing enabled)
             |
             v
       Kubernetes (kind)
             |
             v
        DevLaunch Sample API
```

## Technology stack

- **Application:** Python HTTP API
- **Containerization:** Docker
- **Orchestration:** Kubernetes using kind
- **Packaging:** Helm
- **CI:** GitHub Actions
- **Image security:** Trivy vulnerability scanning
- **Image registry:** GitHub Container Registry (GHCR)
- **GitOps:** Argo CD
- **Development environment:** Windows, PowerShell, Docker Desktop

## Current capabilities

- Builds the API container image in GitHub Actions.
- Validates the Helm chart and renders its Kubernetes manifests.
- Scans the built image for fixable and unfixed critical/high vulnerabilities.
- Publishes commit-SHA-tagged images to GHCR after successful checks on pushes to `master`.
- Deploys the Helm chart from Git through Argo CD.
- Enables automated synchronization and self-healing.
- Configures readiness and liveness probes and CPU/memory requests and limits.
- Documents a tested self-healing scenario in `docs/gitops-self-healing.md`.

## Repository layout

```text
.
├── .github/
│   └── workflows/
│       └── ci.yaml
├── apps/
│   └── sample-api/
│       ├── app.py
│       └── Dockerfile
├── charts/
│   └── sample-api/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           └── service.yaml
├── docs/
│   └── gitops-self-healing.md
└── README.md
```

## Run locally

### Prerequisites

Install and configure:

- Docker Desktop
- kubectl
- kind
- Helm
- Git

### 1. Build the API image

From the repository root:

```powershell
docker build -t devlaunch/sample-api:1.0.0 .\apps\sample-api
```

### 2. Load the image into kind

```powershell
kind load docker-image devlaunch/sample-api:1.0.0 --name devlaunch
```

### 3. Deploy with Helm

```powershell
helm lint .\charts\sample-api
helm upgrade --install sample-api-platform .\charts\sample-api `
  --namespace devlaunch-dev --create-namespace --wait
```

The default chart values currently reference the GHCR image. To use the locally built image instead, pass an explicit image override:

```powershell
helm upgrade --install sample-api-platform .\charts\sample-api `
  --namespace devlaunch-dev `
  --set image.repository=devlaunch/sample-api `
  --set image.tag=1.0.0 `
  --set image.pullPolicy=IfNotPresent `
  --wait
```

### 4. Access the API

For a Helm deployment named `sample-api-platform`:

```powershell
kubectl port-forward svc/sample-api-platform -n devlaunch-dev 8001:80
```

In another PowerShell window:

```powershell
Invoke-RestMethod http://localhost:8001/health
Invoke-RestMethod http://localhost:8001/
```

Stop port forwarding with `Ctrl+C`.

## GitOps deployment

Argo CD watches the `master` branch and reads the Helm chart at `charts/sample-api`. Its Application is named `sample-api` in the `argocd` namespace, and it deploys into `devlaunch-dev`.

Useful checks:

```powershell
kubectl get application sample-api -n argocd
kubectl get deployments -n devlaunch-dev
kubectl get pods -n devlaunch-dev
```

## Self-healing test

The self-healing experiment is documented in [`docs/gitops-self-healing.md`](docs/gitops-self-healing.md).

The test manually reduced the GitOps-managed deployment from two replicas to one. Argo CD restored the desired replica count of two.

## Security and design notes

- Images are tagged with the source commit SHA for traceability.
- CI scans the built image before publishing.
- The sample API runs as a non-root user inside the container.
- Kubernetes health probes help detect unhealthy containers.
- CPU and memory requests and limits are configured in Helm.
- Argo CD manages the GitOps deployment separately from manual Helm releases.

## Current scope and future improvements

This is a local learning and portfolio environment, not a production-ready platform. Potential next steps include:

- Automated tests for the API.
- Image digest pinning and dependency/action version pinning.
- Automated updates of Helm values when new images are published.
- Pull-request-based promotion between environments.
- Metrics and dashboards with Prometheus and Grafana.
- Additional policies and runtime security checks.

## License

No license has been added yet. Add one before explicitly permitting others to reuse or redistribute this project.


