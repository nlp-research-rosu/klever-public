cwd: /audit-output
command: bash -c find\ /reference/reference-semantics\ -printf\ \"REFERENCE\ %y\ %P\ -\>\ %l\\n\"\ \|\ sort\;\ find\ /candidate/reference-semantics\ -printf\ \"CANDIDATE\ %y\ %P\ -\>\ %l\\n\"\ \|\ sort\;\ find\ /candidate\ -type\ l\ -printf\ \"CANDIDATE_SYMLINK\ %p\ -\>\ %l\\n\"
