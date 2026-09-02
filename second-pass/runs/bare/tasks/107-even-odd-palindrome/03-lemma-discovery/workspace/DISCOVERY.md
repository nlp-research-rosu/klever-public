# Trust-boundary discovery

The canonical inventory has 12 rules, in module `VERIFICATION`. The
classification follows the inventory order exactly.

## Definitions

Nine rules are `DEFINITION`:

- `rule-32cad05a64c44632298853378940192d3c804447dd83229d8a824e0240a74279`
  expands the named `solutionProgram` proof term to the program's constructor
  tree.
- `rule-5639e2c99eb51b9725048d8a94cdf17a251b925207b44ccabd13f83e7d2989cc`,
  `rule-b420efe5a5d6b559894e9b2dcf3682f704a96a1296cd27ced3b38a7f164769c4`,
  `rule-ced743b34ecc9e2fe8be6dea91017f7c31493bb880c77ee89ec60542e20559c9`,
  and
  `rule-46f9bffa7142e559d9ea0e12584aca7bddf0d8ffd70f0d7a9c84d1f49d98995d`
  are the exhaustive piecewise equations defining `reverseDigits` on the
  verification domain.
- `rule-a15a3a912c8e5c59021bb7fa638e70dfc2e8e94ef58268ba78f0d8e7c85cf412`,
  `rule-4ab06aa9264329b8f86f4b1278a7b6f2fc4c0598789e6036a18bc4f74cc54a25`,
  `rule-ae19ad0ec4c2e52545ee9fa09bb59be8495250e94c52031263a6713b68ae5b45`,
  and
  `rule-1f4247cac142a5865c2739c28105473e4bb5886abefb7d9c847efebb364a8047`
  define the zero-or-one even- and odd-palindrome indicator functions.

These rules introduce named proof terms or mathematical summaries by
equation. They do not assert extra facts about previously defined functions.

## Operational verification rules

Three rules are `OPERATIONAL_RULE`:

- `rule-c04a2da71e61cfe5735da1913fe21a0382c45abe95efcffaa922508643b25486`
  schedules one program execution and expected-result check, then advances
  the exhaustive range state.
- `rule-aa77e71298d42c8f794cd88933ca94928bae20ee5ef7011a7829f77675e34632`
  terminates the range traversal after the maximum input.
- `rule-87b7d51b1061db4e639ee5ccd629e4d9cbf9fd3622d5019c90ad1dca2fbcdf47`
  observes and consumes a matching returned tuple and clears the environment.

These are execution and observation behavior in the verification harness,
not additional mathematical facts.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1's `prove.sh` first compiles
`verification.k` as module `VERIFICATION`, with all 12 inventoried rules
already present, and then runs one `kprove` command for `spec.k` against that
compiled definition. It contains no earlier proof against a module lacking
any candidate rule, no subsequent recompilation that adds a proved rule, and
therefore no evidence satisfying the required proof-before-use ordering or
exact-statement correspondence.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional trusted
mathematical fact, and the inventory reports no rule carrying the
`simplification` attribute.
