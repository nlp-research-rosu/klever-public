requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal loop invariant.  Symbolic execution narrows CODES one
  // constructor at a time and uses this claim circularly on the remaining
  // suffix.  It covers every contract-valid input, not just the examples.
  claim [all-balanced-inputs]:
    <k>
      #loop(
        str(CODES:IntSeq),
        Name("character"),
        If(Compare(Name("character"), CmpOp("==", Str(" "))),
          Continue .Stmts,
          .Stmts)
        AugAssign(Name("current"), "+", Name("character"))
        If(Compare(Name("character"), CmpOp("==", Str("("))),
          AugAssign(Name("depth"), "+", Int(1)) .Stmts,
          AugAssign(Name("depth"), "-", Int(1)) .Stmts)
        If(Compare(Name("depth"), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("groups"), "append"),
                    (Name("current"), .Exprs)))
          Assign(Name("current"), Str(""))
          .Stmts,
          .Stmts)
        .Stmts)
      ~> KONT:K
      => KONT
    </k>
    <env> 1 </env>
    <scopes>
      RESTSCOPES:Map
      1 |-> scope(
             "character" |-> (OLD:Val => ?FINAL:Val)
             "current"   |-> (str(CUR:IntSeq) => str(.IntSeq))
             "depth"     |-> (DEPTH:Int => 0)
             "groups"    |-> ref(H:Int)
             "paren_string" |-> INPUT:Val,
             parent(0))
    </scopes>
    <heap>
      H |-> list(ACC:ValSeq)
      => H |-> list(scanGroups(CODES, CUR, DEPTH, ACC))
    </heap>
    requires balancedTail(CODES, DEPTH)
     andBool parenSpaceOnly(CODES)
     andBool DEPTH >=Int 0
     andBool (DEPTH >Int 0 orBool CUR ==K .IntSeq)

  // End-to-end public-entry proof.  The universal loop claim discharges the
  // recursive phase after the ordinary call/allocation prefix has executed.
  claim [all-balanced-calls]:
    <k> Call(Name("separate_paren_groups"),
             (str(CODES:IntSeq), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(scanGroups(CODES, .IntSeq, 0, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires balancedTail(CODES, 0)
     andBool parenSpaceOnly(CODES)

  claim [empty]:
    <k> Call(Name("separate_paren_groups"),
             (str(.IntSeq), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [prompt-example]:
    <k> Call(Name("separate_paren_groups"),
             (str(strToCodes("( ) (( )) (( )( ))")), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(str(strToCodes("()")),
           vCons(str(strToCodes("(())")),
           vCons(str(strToCodes("(()())")), .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [adjacent-and-spaced]:
    <k> Call(Name("separate_paren_groups"),
             (str(strToCodes("  (()())() ")), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(str(strToCodes("(()())")),
           vCons(str(strToCodes("()")), .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [deep-nesting]:
    <k> Call(Name("separate_paren_groups"),
             (str(strToCodes("(((())))")), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(str(strToCodes("(((())))")), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

endmodule
