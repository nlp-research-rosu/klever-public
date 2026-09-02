# Supersession note

`02_producer_crosscheck.txt` is retained as raw evidence. Its final
`image_id_cross_match=False` line came from using Python tuple membership
(`value in (path, manifest_text)`) where substring/equality checks were
intended. It is not an observed provenance mismatch.

The corrected exact checks are:

- generator image ID equals source-manifest image ID; and
- the digest portion equals the audit-input producer-path basename.

Both are `true` in `07_reconstructed_inventory_and_hashes.json` and
`39_all_recorded_hashes_bijection_target.json`.
