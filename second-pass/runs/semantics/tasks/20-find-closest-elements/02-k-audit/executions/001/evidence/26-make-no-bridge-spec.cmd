cwd=/tmp/audit-work/reconstruction
command=bash -o pipefail -c sed\ \"s/requires\ \\\"verification.k\\\"/requires\ \\\"verification-no-bridge.k\\\"/\"\ /candidate/spec.k\ \|\ tee\ /audit-output/evidence/spec-no-bridge.k\ \>/tmp/audit-work/reconstruction/spec-no-bridge.k 
