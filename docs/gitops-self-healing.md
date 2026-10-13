# GitOps Self-Healing Test

## Objective
Verify that Argo CD reconciles manual changes to a Kubernetes deployment
back to the desired state defined by the Helm chart in Git.

## Configuration
- Argo CD automated sync: enabled
- Self-healing: enabled
- Helm chart: `charts/sample-api`
- Desired replica count: 2
- Kubernetes namespace: `devlaunch-dev`

## Test procedure
1. Confirmed the GitOps deployment had 2 ready replicas.
2. Manually scaled `sample-api-gitops` to 1 replica.
3. Watched the deployment with `kubectl get deployment --watch`.
4. Observed readiness change to 1/2 and then return to 2/2.

## Result
PASS — Argo CD restored the deployment to the desired replica count of 2.

## Commands used
```powershell
kubectl scale deployment sample-api-gitops --replicas=1 -n devlaunch-dev
kubectl get deployment sample-api-gitops -n devlaunch-dev --watch
