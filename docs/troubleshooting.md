# DevLaunch Troubleshooting Notes

## 1. Helm ownership conflicts

**Problem:** Helm failed to adopt Kubernetes resources originally created with kubectl.

**Cause:** Existing Deployment selectors and Service fields conflicted with the Helm chart.

**Resolution:** Use a separate Helm release or carefully remove conflicting resources after verifying they are safe to delete.

**Lesson:** Give each Kubernetes resource one clear owner.

## 2. Port-forward port already in use

**Problem:** kubectl port-forward could not bind to local port 8001.

**Cause:** Another process was already using that port.

**Resolution:** Use another local port, such as 8003:

```powershell
kubectl port-forward svc/sample-api-gitops -n devlaunch-dev 8003:80
```

## 3. Verifying GitOps deployment

**Problem:** The image shown by an earlier command did not match the latest Git commit.

**Resolution:** Check Argo CD sync and health, the Deployment image, and rollout status:

```powershell
kubectl get application sample-api -n argocd
kubectl get deployment sample-api-gitops -n devlaunch-dev
kubectl get deployment sample-api-gitops -n devlaunch-dev -o jsonpath="{.spec.template.spec.containers[0].image}"
kubectl rollout status deployment/sample-api-gitops -n devlaunch-dev
```

**Lesson:** A successful Git push alone does not prove deployment succeeded. Verify reconciliation and pod readiness.
