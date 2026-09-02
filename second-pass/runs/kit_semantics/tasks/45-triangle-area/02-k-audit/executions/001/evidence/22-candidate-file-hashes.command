find -P /candidate -type f -print0 | sort -z | xargs -0 sha256sum && find -P /candidate -type f | wc -l && find -P /candidate -type l -print
