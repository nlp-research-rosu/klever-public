for path in evidence/*.status; do printf "%s=" "$(basename "$path")"; tr -d "\\n" < "$path"; printf "\\n"; done; find evidence -maxdepth 1 -type f -printf "%f %s bytes\\n" | sort
