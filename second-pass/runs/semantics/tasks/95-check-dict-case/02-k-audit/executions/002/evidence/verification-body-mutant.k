requires "reference-semantics/semantics.k"

module CHECK-DICT-CASE-VERIFICATION
  imports MPY

  // These constructors are the exact AST emitted in solution.mpy, factored
  // into named terms so that the reachability claims remain readable.
  syntax Stmts ::= checkDictLoopBody() [function, total]
  rule checkDictLoopBody()
    => Assign(Name("has_key"), Bool(true))
       If(UnaryOp("not", Call(Name("isinstance"), (Name("key"), Name("str"), .Exprs))),
          Assign(Name("all_lower"), Bool(false))
          Assign(Name("all_upper"), Bool(false)),
          If(UnaryOp("not", Call(Attribute(Name("key"), "islower"), .Exprs)),
             Assign(Name("all_lower"), Bool(false)),
             .Stmts)
          If(UnaryOp("not", Call(Attribute(Name("key"), "isupper"), .Exprs)),
             Assign(Name("all_upper"), Bool(false)),
             .Stmts))

  syntax Expr ::= checkDictResultExpr() [function, total]
  rule checkDictResultExpr()
    => BoolOp("or",
         (Name("has_key"),
          BoolOp("or", (Name("all_lower"), Name("all_upper"), .Exprs)),
          .Exprs))

  syntax Stmts ::= checkDictBody() [function, total]
  rule checkDictBody()
    => Assign(Name("has_key"), Bool(false))
       Assign(Name("all_lower"), Bool(true))
       Assign(Name("all_upper"), Bool(true))
       Assign(Name("key"), NoneVal)
       For(Name("key"),
           Call(Attribute(Name("dict"), "keys"), .Exprs),
           checkDictLoopBody())
       Return(checkDictResultExpr())

  syntax Module ::= checkDictCaseModule() [function, total]
  rule checkDictCaseModule()
    => Module(
         FuncDef("check_dict_case", Params("dict"), checkDictBody()))

  // Mathematical specification. A key counts as lower/upper exactly when it
  // is a string and Python's corresponding case predicate is true.
  syntax Bool ::= stringCaseKey(Val) [function, total]
                | lowerCaseKey(Val) [function, total]
                | upperCaseKey(Val) [function, total]
  rule stringCaseKey(str(_:IntSeq)) => true
  rule stringCaseKey(_:Val) => false [owise]
  rule lowerCaseKey(str(CS:IntSeq))
    => hasLower(CS) andBool notBool hasUpper(CS)
  rule lowerCaseKey(_:Val) => false [owise]
  rule upperCaseKey(str(CS:IntSeq))
    => hasUpper(CS) andBool notBool hasLower(CS)
  rule upperCaseKey(_:Val) => false [owise]

  // Proof-only observation splitters. The reference functions intentionally
  // leave an abstract Val opaque; these guarded rules expose the two exhaustive
  // Boolean outcomes without choosing either one. On concrete values their
  // guards reduce to exactly the reference isinstance/string-method results.
  rule <k> #applyK(toCall(builtinV("isinstance")),
                   (V:Val, typeV("str"), .Vals))
        => true ... </k>
       requires stringCaseKey(V)
       [priority(30)]
  rule <k> #applyK(toCall(builtinV("isinstance")),
                   (V:Val, typeV("str"), .Vals))
        => false ... </k>
       requires notBool stringCaseKey(V)
       [priority(30)]

  rule <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
        => true ... </k>
       requires stringCaseKey(V) andBool lowerCaseKey(V)
       [priority(30)]
  rule <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
        => false ... </k>
       requires stringCaseKey(V) andBool notBool lowerCaseKey(V)
       [priority(30)]

  rule <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
        => true ... </k>
       requires stringCaseKey(V) andBool upperCaseKey(V)
       [priority(30)]
  rule <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
        => false ... </k>
       requires stringCaseKey(V) andBool notBool upperCaseKey(V)
       [priority(30)]

  syntax Bool ::= allLowerKeys(ValSeq) [function, total]
                | allUpperKeys(ValSeq) [function, total]
  rule allLowerKeys(.ValSeq) => true
  rule allLowerKeys(vCons(K:Val, KS:ValSeq))
    => stringCaseKey(K)
       andBool lowerCaseKey(K)
       andBool allLowerKeys(KS)
  rule allUpperKeys(.ValSeq) => true
  rule allUpperKeys(vCons(K:Val, KS:ValSeq))
    => stringCaseKey(K)
       andBool upperCaseKey(K)
       andBool allUpperKeys(KS)

  syntax Bool ::= keySeenAfter(ValSeq, Bool) [function, total]
  rule keySeenAfter(_:ValSeq, true) => true
  rule keySeenAfter(.ValSeq, false) => false
  rule keySeenAfter(vCons(_:Val, _:ValSeq), _:Bool) => true

  // The generalized postcondition used as the loop invariant: prior state is
  // conjoined with the classification of every remaining dictionary key.
  syntax Bool ::= checkDictCaseResult(ValSeq, Bool, Bool, Bool)
                  [function, total]
  rule checkDictCaseResult(KS:ValSeq, SEEN:Bool, LOWER:Bool, UPPER:Bool)
    => keySeenAfter(KS, SEEN)
       andBool ((LOWER andBool allLowerKeys(KS))
                orBool (UPPER andBool allUpperKeys(KS)))
endmodule
