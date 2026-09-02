# Operational-bridge assessment for the generated target parameter

There is one `target.parameters` entry:

- Lean name: `«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool»`
- Lean type: `SortIntSeq → SortBool → SortBool`
- KORE symbol:
  `LblfirstAfter'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'IntSeq'Unds'Bool`
- bound source rule:
  `rule-49d35612d63bf56fdd624a16c30b97a62ddbf196c0acb5a07976bc8b31be1a41`

The candidate defines that exact Lean name once:

```lean
def «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» :
    SortIntSeq → SortBool → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», flag => flag
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _, _ => false
```

This is the frozen operational meaning, not merely a definition convenient for
the exported equation:

- Frozen line 66 says `firstAfter(.IntSeq,F) => F`, matching the empty branch.
- Frozen line 67 says `firstAfter(iCons(I,R),F) => false`, matching the
  nonempty branch.
- Frozen line 65, the bound domain lemma, says
  `firstAfter(IS,false) => false`; both candidate branches satisfy it.
- The source program initializes `first = true`, changes it to `false` during
  the first loop iteration, and never changes it back. Thus empty input
  preserves the incoming flag and every nonempty input ends with `false`.
- `SortIntSeq` has exactly the empty and `iCons` constructors, and `SortBool`
  is Lean `Bool`; the candidate covers the complete operational domain.

`BridgeAudit.lean` machine-checks a stronger universal comparison against the
generated Option-valued K function:

```lean
∀ input flag,
  _root_.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» input flag =
    some (Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» input flag)
```

It closes by cases on both constructors and both Boolean values. Ground
witnesses also cover empty/true, empty/false, singleton/true,
singleton/false, and a two-element sequence.

The exported theorem alone deliberately does not determine the parameter's
complete meaning. The adversarial file demonstrates two counterfactuals:

- a constant-false definition proves the target but disagrees on empty/true;
- an identity-on-flag definition proves the target but disagrees on
  nonempty/true.

Both counterfactual target proofs compile, and both disagreement witnesses
compile. This shows why the operational-bridge check is material. The actual
candidate is neither counterfactual: it distinguishes both constructors and
matches the frozen behavior on the adversarial cases and universally.

Conclusion: the sole target parameter passes the operational bridge audit.
