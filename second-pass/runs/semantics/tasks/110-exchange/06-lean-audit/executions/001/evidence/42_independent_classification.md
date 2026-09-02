# Independent Stage 3 classification

Frozen source: `/reference/k-proof/verification.k`

The trusted inventory reconstructs 13 local rules in source order. None has a
`simplification` attribute.

## Operational rules

1. `rule-75a15fce623355109a5f77b20ab8dc774ce6373d461e0bab9106cc7f3a2a03ef`
   (line 10) is the empty `#iterNext` transition. It observes the empty
   `intVals(.IntSeq)` representation, produces `#iterDone`, preserves the
   continuation through the framed `<k> ... </k>` context, and touches no
   other cell. It is an `OPERATIONAL_RULE`.
2. `rule-f7c0ae8e417be936aba1c698bac7dda83b700472308f44b0c678405dec4e0e8a`
   (lines 11–12) is the nonempty `#iterNext` transition. It yields the integer
   head and retains the tail as the remaining iterator, preserving the
   continuation and all other cells. It is an `OPERATIONAL_RULE`.

These transitions are constructor-for-constructor copies of the supplied
`MPY-LIST` rules for `.ValSeq` and `vCons` in
`reference-semantics/semantics/list.k`: empty maps to done; a head/tail maps
to yield(head, tail). They define ordinary execution of the typed symbolic
integer-list view and neither assert mathematics nor replace execution of the
source `exchange` body.

## Definitions

3. `rule-d1771b6abc8204d10d0120ab9b6b82ea1aa475841bdb01cc6b36409fa4f30adf`
   is the empty base equation for `oddAcc`.
4. `rule-956626e98bfb99ece5009b0a0de44a05aed5c98965e41f8907088eca7c79eb07`
   is the even-head recurrence for `oddAcc`.
5. `rule-b97491015955141ffb565afee8ad9db67c952400a203da41bfead9e783dbbe5c`
   is the odd-head recurrence for `oddAcc`.
6. `rule-a65280efad851be437f6ad12f7522d3722e54d021e833141bb0b685910b9b5d9`
   is the empty base equation for `evenAcc`.
7. `rule-7a598edc12d29e890d747e7bf34354f9a62ab000d10ed71e5b04eff1f0d54bb8`
   is the even-head recurrence for `evenAcc`.
8. `rule-8b1fd6b7158f31c41fa1892e0da635222d23ac6a005e88a5c5fc16635f401014`
   is the odd-head recurrence for `evenAcc`.

Rules 3–8 are `DEFINITION`s. On divisor 2, supplied `pyMod` implements Python
modulo and its result is either zero or nonzero, so each recurrence pair has
complementary guards. Each call strictly descends from `iCons(I,R)` to `R`.
The equations compute exactly the accumulators changed by the two source
loops.

9. `rule-e061eb1646489564aec80b5a19922a8d529ff803655bcc2ef290bf74cab5c395`
   and
10. `rule-bdf4ad4c5dcad7fbe88b530d009288ef75cab58185bb6804bb0043fd6c1f0d19`
    are the complementary equations defining the named `exchangeResult`
    summary. They encode `YES` exactly when the first list's odd count is no
    larger than the second list's even count, otherwise `NO`. Both are
    `DEFINITION`s.

11. `rule-210e460d0378731e202dc889851fbcbf7db0bc462024103483a45b5b4deeed62`
    defines the `ODD-BODY` macro.
12. `rule-3bd64abc229ddcd421f537aad4487a05bb6728292227449c48adf182fe462354`
    defines the `EVEN-BODY` macro.
13. `rule-89bf73b1f8f0830d193829a61a9abb882a35305459a0fc8c0a542ce37355307d`
    defines the `exchangeDef` macro.

Rules 11–13 are `DEFINITION`s. Expanding the two body macros in
`exchangeDef` gives the exact constructor sequence in frozen `solution.mpy`:
the same three initial assignments, the odd-count loop over `lst1`, the
even-count loop over `lst2`, the `odd <= even` branch returning `YES`, and the
final `NO` return.

## Domain and derived-lemma judgment

No rule is a `PROVED_DERIVED_LEMMA`: no rule is presented as a separately
proved theorem later imported for use.

No rule is a `DOMAIN_LEMMA`: every non-operational rule directly defines a
summary, recurrence, or macro. There is consequently no mathematical fact to
export as a Stage 4 obligation. The true domain set is empty.

