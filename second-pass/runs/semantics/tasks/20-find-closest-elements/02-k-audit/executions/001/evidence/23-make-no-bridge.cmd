cwd=/tmp/audit-work/reconstruction
command=bash -o pipefail -c \{\ sed\ -n\ \"1\,200p\"\ /candidate/verification.k\;\ sed\ -n\ \"224p\"\ /candidate/verification.k\;\ \}\ \|\ tee\ /audit-output/evidence/verification-no-bridge.k\ \>/tmp/audit-work/reconstruction/verification-no-bridge.k 
