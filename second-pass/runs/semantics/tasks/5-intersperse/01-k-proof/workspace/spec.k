requires "verification.k"

module INTERSPERSE-SPEC
  imports INTERSPERSE-VERIFICATION

  // Empty loop at function entry: no target has yet been bound.
  claim
    <k>
      #loop(
        list(.ValSeq), Name("number"),
        If(Name("result"),
          Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
          .Stmts)
        Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
      ~> CONT
      => CONT
    </k>
    <env> L </env>
    <scopes>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap> HEAP H |-> list(.ValSeq) </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))

  // Nonempty loop at function entry. One execution establishes the invariant
  // in the following claim.
  claim
    <k>
      #loop(
        list(vCons(V, REST)), Name("number"),
        If(Name("result"),
          Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
          .Stmts)
        Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
      ~> CONT
      => CONT
    </k>
    <env> L </env>
    <scopes>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
      =>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "number" |-> lastNumber(V, REST)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap>
      HEAP H |-> list(.ValSeq)
      => HEAP H |-> list(intersperseAcc(.ValSeq, vCons(V, REST), D))
    </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))

  // Once the first item has been appended, the accumulator is nonempty and
  // every later iteration appends the delimiter followed by the next item.
  claim
    <k>
      #loop(
        list(REST), Name("number"),
        If(Name("result"),
          Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
          .Stmts)
        Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
      ~> CONT
      => CONT
    </k>
    <env> L </env>
    <scopes>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "number" |-> OLD
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
      =>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "number" |-> lastNumber(OLD, REST)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap>
      HEAP H |-> list(vCons(A, AS))
      => HEAP H |-> list(intersperseAcc(vCons(A, AS), REST, D))
    </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))

  claim
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("intersperse", Params("numbers", "delimeter"),
          Assign(Name("result"), ListExpr(.Exprs))
          For(Name("number"), Name("numbers"),
            If(Name("result"),
              Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
              .Stmts)
            Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
          Return(Name("result")))))
      ~> Call(Name("intersperse"), list(NUMBERS), D)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "intersperse" |-> closureVal(
          ("numbers", "delimeter"),
          Assign(Name("result"), ListExpr(.Exprs))
          For(Name("number"), Name("numbers"),
            If(Name("result"),
              Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
              .Stmts)
            Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
          Return(Name("result")),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(intersperseVS(NUMBERS, D)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
