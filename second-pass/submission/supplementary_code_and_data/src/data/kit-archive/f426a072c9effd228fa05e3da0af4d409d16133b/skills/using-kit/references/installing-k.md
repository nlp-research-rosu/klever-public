# Installing K

How to install the K toolchain via `kup` and make it visible to agent and
non-interactive shells.

## Official install path

K is installed via `kup`, which itself is bootstrapped by a one-line script.
Run it as your regular user, not as root — running the installer as root
produces a broken installation. If you don't have the ability to run it, ask
the user to.

```bash
# installs Nix + kup, requires sudo password during the Nix step
# you may need to ask the user to do it
bash <(curl https://kframework.org/install)

# installs the K toolchain (~1.4GB)
kup install k
```

After installation completes, open a fresh shell and run:

```bash
kompile --version && kprove --version          # sanity check
```

## The PATH gotcha — critical for agent/non-interactive shells

After install, the K tools live at `~/.nix-profile/bin`, which may not be on
`PATH` in a non-interactive or agent shell. See
[running-k.md](../../shared/running-k.md#shell-setup) for the shared shell
setup.

**Fix: prepend the PATH preamble to every shell session that runs K:**

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
```

Place this before any `kompile`, `krun`, or `kprove` call. In scripts, put it at the top. In agent tasks, include it in every shell command that calls a K tool.

## Version management

List available K versions:

```bash
kup list k
```

Install a specific version:

```bash
kup install k --version <version>
```
