# Claude Code + K-framework runner for the HumanEval verification benchmark.
#
# The container IS the sandbox: only the mounted /work (one runs/<config>/<id>
# task folder) is visible, git is removed, memory is capped by compose, and the
# entrypoint enforces a wall-clock timeout and records duration + peak memory.
#
# Base: Runtime Verification's official K release image, pinned to the exact K
# version the host/reference proofs use (kompile/krun/kprove, LLVM + Haskell
# backends, Z3, OpenJDK, python3 are all included).
FROM runtimeverificationinc/kframework-k:ubuntu-jammy-7.1.293

# Node.js 22 for the Claude Code CLI (jammy's apt nodejs is far too old).
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
 && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

# No git in the runner: the benchmark forbids git usage. The kframework deb has
# no git dependency (verified against its debian control file), so purging is
# safe; the CLI-level deny rule in the entrypoint is defense in depth.
RUN apt-get purge -y git git-man && apt-get autoremove -y || rm -f /usr/bin/git

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Non-root user with uid 1000 (matches the host user), so files the agent
# writes into the mounted /work are owned by you on the host.
RUN useradd -m -u 1000 -s /bin/bash agent
USER agent
ENV CLAUDE_CONFIG_DIR=/home/agent/.claude \
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
WORKDIR /work
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
