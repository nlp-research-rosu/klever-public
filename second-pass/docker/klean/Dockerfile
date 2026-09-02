FROM runtimeverificationinc/kframework-k:ubuntu-jammy-7.1.293@sha256:f3f64ab72bd7b560082d50e4c6c23e107025cf217ca62ab73700104fc45de09a

ARG K_COMMIT=ff15baac9e66426612ec45ff912af7f14965b64a
ARG LEAN_TOOLCHAIN=leanprover/lean4:v4.22.0
ARG UV_VERSION=0.8.17
ARG UV_SHA256=920cbcaad514cc185634f6f0dcd71df5e8f4ee4456d440a22e0f8c0f142a8203
ARG ELAN_VERSION=4.1.2
ARG ELAN_SHA256=f81c2e48c1588d4612cd2c8851947898a45ac8d72748a07dff3a5694f1cf589b

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl git \
 && curl -fsSLo /tmp/uv.tar.gz \
      "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" \
 && echo "${UV_SHA256}  /tmp/uv.tar.gz" | sha256sum -c - \
 && tar -xzf /tmp/uv.tar.gz -C /tmp \
 && install -m 0555 /tmp/uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/uv \
 && install -m 0555 /tmp/uv-x86_64-unknown-linux-gnu/uvx /usr/local/bin/uvx \
 && export ELAN_HOME=/opt/elan \
 && curl -fsSLo /tmp/elan.tar.gz \
      "https://github.com/leanprover/elan/releases/download/v${ELAN_VERSION}/elan-x86_64-unknown-linux-gnu.tar.gz" \
 && echo "${ELAN_SHA256}  /tmp/elan.tar.gz" | sha256sum -c - \
 && tar -xzf /tmp/elan.tar.gz -C /tmp \
 && /tmp/elan-init -y --no-modify-path --default-toolchain none \
 && /opt/elan/bin/elan toolchain install "$LEAN_TOOLCHAIN" \
 && /opt/elan/bin/elan default "$LEAN_TOOLCHAIN" \
 && git clone https://github.com/runtimeverification/k.git /opt/runtimeverification-k \
 && git -C /opt/runtimeverification-k checkout "$K_COMMIT" \
 && test "$(git -C /opt/runtimeverification-k rev-parse HEAD)" = "$K_COMMIT" \
 && printf '%s\n' "$K_COMMIT" > /opt/runtimeverification-k/.source-commit \
 && uv sync --frozen --project /opt/runtimeverification-k/pyk \
 && rm -rf /opt/runtimeverification-k/.git /var/lib/apt/lists/* /tmp/uv* /tmp/elan*

ENV ELAN_HOME=/opt/elan
ENV PYTHONHASHSEED=0
ENV PATH="/opt/elan/bin:/opt/runtimeverification-k/pyk/.venv/bin:${PATH}"

COPY docker/klean/patches/k2lean4-ceil.patch /tmp/k2lean4-ceil.patch
RUN patch /opt/runtimeverification-k/pyk/src/pyk/klean/k2lean4.py /tmp/k2lean4-ceil.patch \
 && (patch /opt/pipx/venvs/kframework/lib/python3.10/site-packages/pyk/klean/k2lean4.py /tmp/k2lean4-ceil.patch || true) \
 && rm /tmp/k2lean4-ceil.patch
COPY tools/klean.py tools/klean_export.py tools/klean_preflight.py \
     tools/k_rule_inventory.py tools/lemma_discovery_contract.py \
     /opt/humaneval/tools/
COPY data/klean-toolchain.lock.json /opt/humaneval/data/
COPY docker/frozen-toolchain-check.sh /usr/local/bin/assert-frozen-toolchain
COPY docker/klean/entrypoint.sh /usr/local/bin/klean-entrypoint
RUN chmod 0555 /usr/local/bin/assert-frozen-toolchain \
                    /usr/local/bin/klean-entrypoint \
 && /usr/local/bin/assert-frozen-toolchain klean \
 && chmod -R a-w /opt/humaneval /opt/runtimeverification-k /opt/elan

RUN useradd -m -u 1000 -s /bin/bash agent \
 && mkdir /generations \
 && chown agent:agent /generations
USER agent
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/klean-entrypoint"]
