requires "fixed-verification.k"

module BRIDGE-CHECK
  imports FIXED-VERIFICATION

  claim [return-bool]:
    <k> Return(Bool(B:Bool)) ~> _KREST:K => #pop </k>
    <ret> noRet => retV(B) </ret>

  claim [return-depth-equality]:
    <k>
      Return(Compare(Name("depth"), CmpOp("==", Int(0)))) ~> _KREST:K
      =>
      #pop
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> _BRACKET:Val,
        _PARENT:Parent) ...
    </scopes>
    <ret> noRet => retV(D ==Int 0) </ret>

  claim [if-bracket-open]:
    <k>
      If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
         THEN:Stmts, ELSE:Stmts)
      =>
      #branch(true, THEN, ELSE)
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> _D:Int
        "bracket" |-> str(iCons(C:Int, .IntSeq)),
        _PARENT:Parent) ...
    </scopes>
    requires C ==Int 60

  claim [if-bracket-close]:
    <k>
      If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
         THEN:Stmts, ELSE:Stmts)
      =>
      #branch(false, THEN, ELSE)
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> _D:Int
        "bracket" |-> str(iCons(C:Int, .IntSeq)),
        _PARENT:Parent) ...
    </scopes>
    requires C =/=Int 60

  claim [augassign-plus]:
    <k> AugAssign(Name("depth"), "+", Int(1)) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> (D:Int => D +Int 1)
        "bracket" |-> _BRACKET:Val,
        _PARENT:Parent) ...
    </scopes>

  claim [augassign-minus]:
    <k> AugAssign(Name("depth"), "-", Int(1)) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> (D:Int => D -Int 1)
        "bracket" |-> _BRACKET:Val,
        _PARENT:Parent) ...
    </scopes>

  claim [if-depth-negative]:
    <k>
      If(Compare(Name("depth"), CmpOp("<", Int(0))),
         THEN:Stmts, ELSE:Stmts)
      =>
      #branch(true, THEN, ELSE)
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> _BRACKET:Val,
        _PARENT:Parent) ...
    </scopes>
    requires D <Int 0

  claim [if-depth-nonnegative]:
    <k>
      If(Compare(Name("depth"), CmpOp("<", Int(0))),
         THEN:Stmts, ELSE:Stmts)
      =>
      #branch(false, THEN, ELSE)
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> _BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> _BRACKET:Val,
        _PARENT:Parent) ...
    </scopes>
    requires D >=Int 0

  claim [pop-normalization]:
    <k> #pop => V ~> CONT </k>
    <ret> retV(V:Val) => noRet </ret>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <env> L:Int => CALLER </env>
    <scopes> (L |-> _FRAME:Scope SC:Map) => SC </scopes>
    <scopeLoc> _ => SAVED </scopeLoc>
    requires notBool L in_keys(SC)
endmodule
