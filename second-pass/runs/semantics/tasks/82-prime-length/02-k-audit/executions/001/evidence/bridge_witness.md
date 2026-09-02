# Operational-bridge witness

The first bridge in `verification.k` matches every `While(C, B)` at the head of
the `<k>` cell with any continuation. The last bridge replaces the captured
integer plus `_REST:K` with `#primeLoopEntry(N,D)`, clears all scopes and the
stack, resets the environment/scope location/return cell, and thereby discards
`_REST`.

Concrete intended-domain witness: invoke the submitted function with `"abcd"`
(length 4). Just before the loop, fixed semantics has `n = 4`, `divisor = 2`,
and:

```text
While(divisor < n, primeLoopBody) ~> Return(Bool(true)) ~> #endcall
```

Fixed supplied semantics evaluates the loop body, observes `4 % 2 == 0`, and
returns Boolean `false`. The bridge-enabled execution instead produces
`#primeLoopEntry(4,2)`, discards the return/end-call continuation, and clears
the callee frame. Thus it does not preserve the result or control/state
footprint.

Continuation-sensitivity witness independent of the task body:

```text
While(Bool(false), .Stmts)
~> Assign(Name("x"), Int(7))
~> Return(Bool(true))
~> #endcall
```

With a frame containing integer bindings `n = 4` and `divisor = 2`, fixed
semantics skips the body, writes `x = 7`, and returns `true`. The bridge instead
returns `#primeLoopEntry(4,2)` and discards the assignment and return. No
bridge-free universal connection theorem is submitted for either context.
