# Body-sensitivity mutation

The scratch-only `verification.k` changes the submitted body's `chr` argument
from `48 + x % base` to `49 + x % base`, while leaving `baseDigits` and both
claims unchanged. For witness `(x, base) = (1, 2)`, the mutated body returns
`"2"` but the claim requires `"1"`. A sound proof tied to the body must reject
the unchanged claim.
