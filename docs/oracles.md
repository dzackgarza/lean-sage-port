# Sage reference oracle

The mathematical implementation runs in Lean. Sage supplies independent expected results and
doctests. The baseline index is the Sage 11.0.beta5 source checkout at
`c00171e47d6e68d8148d7ee10c4dd77b71a97662` (`inventory/sage/baseline.yaml`). Its selectors
identify source doctests; `docs/capability-records.md` defines how records inherit them.

The existing research image is `ghcr.io/dzackgarza/sage` on `linux/amd64`. Pin the platform manifest
when running an oracle:

```text
ghcr.io/dzackgarza/sage@sha256:dadfded3a44fb8314266afb3225855b5ba531b49a53ac70ed844b457435fcfc0
```

The image config label `org.opencontainers.image.revision` is
`5173d4afc9f493e5df5bb060de074f8de53b9e48`. The Sage executable inside is
`/sage/.venv/bin/sage`. These values were read from the OCI manifest and config on 2026-11-17;
the image source revision differs from the indexed baseline. Compare operation semantics and
version-dependent outputs with that distinction in view.

Run an oracle query in the image with Docker:

```sh
docker run --rm ghcr.io/dzackgarza/sage@sha256:dadfded3a44fb8314266afb3225855b5ba531b49a53ac70ed844b457435fcfc0 \
  /sage/.venv/bin/sage -c 'R = PolynomialRing(QQ, "x"); x = R.gen(); f = (x^2 - 1)*(x - 1); print(f.factor()); print(f.gcd(x^2 - 1))'
```

The workstation's installed `sage` launcher was executed with this query on 2026-11-17. It
reported SageMath 10.10.beta8 and returned `(x + 1) * (x - 1)^2` and `x^2 - 1`. That local
execution verifies the query and its expected mathematical result. The pinned image was inspected
but not run on this workstation; its layers total about 13.2 GB before unpacking. To inspect the
current published image and its source revision, use the producer's
`docker/sage-image.py info` after fetching, or `docker buildx imagetools inspect` on the pinned
manifest. The image build and environment checks are owned by
`~/gitclones/sage-dev-allopts-develop/docker/SAGE-ENVIRONMENT.md`.
