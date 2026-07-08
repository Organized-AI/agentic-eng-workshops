# Removed

The **Local AI** workshop was folded out of the Vol 2 lineup. Edge deployment and local
model material now live as cross-cutting infra (`modules/09-deployment`) and inside the
**Harness Eng** and **Observability** tracks where relevant.

This folder can be safely deleted:

```bash
git rm -r workshops/04-local-ai && git commit -m "Remove dropped 04-local-ai" && git push
```
