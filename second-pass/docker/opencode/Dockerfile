# OpenCode + K-framework runner for the HumanEval verification benchmark.
# Mirror of ../claude-code and ../codex, with the OpenCode CLI as the agent
# (used to drive OpenRouter models, e.g. moonshotai/kimi-k3).
#
# Same guarantees: only the mounted /work task folder is visible, git is
# removed, memory capped by compose, entrypoint enforces the wall-clock timeout
# and records duration + peak memory, full session trace preserved.
FROM runtimeverificationinc/kframework-k:ubuntu-jammy-7.1.293

# Node.js 22 for the OpenCode CLI.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
 && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && rm -rf /var/lib/apt/lists/*

RUN npm install -g opencode-ai

# No git in the runner (benchmark rule; kframework has no git dependency).
RUN apt-get purge -y git git-man && apt-get autoremove -y || rm -f /usr/bin/git

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Non-root user with uid 1000 (matches the host user).
RUN useradd -m -u 1000 -s /bin/bash agent
USER agent

# Non-interactive permission profile: the container is the sandbox, so tool use
# is auto-allowed; session sharing is off.
RUN mkdir -p /home/agent/.config/opencode && cat > /home/agent/.config/opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "share": "disabled",
  "permission": {
    "edit": "allow",
    "bash": "allow",
    "webfetch": "allow",
    "external_directory": "allow"
  },
  "provider": {
    "openrouter": {
      "models": {
        "moonshotai/kimi-k3": {
          "limit": { "context": 1048576, "output": 262144 },
          "options": { "reasoning": { "effort": "high" } }
        }
      }
    },
    "zai-coding-plan": {
      "models": {
        "glm-5.2": {
          "limit": { "context": 200000, "output": 131072 }
        }
      }
    }
  }
}
EOF

WORKDIR /work
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
