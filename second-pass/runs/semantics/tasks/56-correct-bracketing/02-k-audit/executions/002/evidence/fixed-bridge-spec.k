requires "fixed-verification.k"

module FIXED-BRIDGE-SPEC
  imports FIXED-VERIFICATION

  claim [return-bool]:
    <k> Return(Bool(B:Bool)) ~> SUFFIX:K => B ~> CONT </k>
    <env> L => CALLER </env>
    <scopes> (L |-> FRAME:Scope SC:Map) => SC </scopes>
    <scopeLoc> CUR:Int => SAVED </scopeLoc>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <ret> noRet </ret>
    requires notBool L in_keys(SC)

  claim [return-depth-equality]:
    <k>
      Return(Compare(Name("depth"), CmpOp("==", Int(0)))) ~> SUFFIX:K
    =>
      (D ==Int 0) ~> CONT
    </k>
    <env> L => CALLER </env>
    <scopes>
      (L |-> scope(
          "brackets" |-> BRACKETS:Val
          "depth" |-> D:Int
          "bracket" |-> BRACKET:Val,
          PARENT:Parent)
       SC:Map)
    =>
      SC
    </scopes>
    <scopeLoc> CUR:Int => SAVED </scopeLoc>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <ret> noRet </ret>
    requires notBool L in_keys(SC)

  claim [if-bracket-open]:
    <k>
      If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
         THEN:Stmts, ELSE:Stmts) ~> CONT:K
    =>
      THEN ~> CONT
    </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> str(iCons(C:Int, .IntSeq)),
        PARENT:Parent) ...
    </scopes>
    requires C ==Int 60

  claim [if-bracket-close]:
    <k>
      If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
         THEN:Stmts, ELSE:Stmts) ~> CONT:K
    =>
      ELSE ~> CONT
    </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> str(iCons(C:Int, .IntSeq)),
        PARENT:Parent) ...
    </scopes>
    requires C =/=Int 60

  claim [augassign-plus]:
    <k> AugAssign(Name("depth"), "+", Int(1)) ~> CONT:K => CONT </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> (D:Int => D +Int 1)
        "bracket" |-> BRACKET:Val,
        PARENT:Parent) ...
    </scopes>

  claim [augassign-minus]:
    <k> AugAssign(Name("depth"), "-", Int(1)) ~> CONT:K => CONT </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> (D:Int => D -Int 1)
        "bracket" |-> BRACKET:Val,
        PARENT:Parent) ...
    </scopes>

  claim [if-depth-negative]:
    <k>
      If(Compare(Name("depth"), CmpOp("<", Int(0))),
         THEN:Stmts, ELSE:Stmts) ~> CONT:K
    =>
      THEN ~> CONT
    </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> BRACKET:Val,
        PARENT:Parent) ...
    </scopes>
    requires D <Int 0

  claim [if-depth-nonnegative]:
    <k>
      If(Compare(Name("depth"), CmpOp("<", Int(0))),
         THEN:Stmts, ELSE:Stmts) ~> CONT:K
    =>
      ELSE ~> CONT
    </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        "brackets" |-> BRACKETS:Val
        "depth" |-> D:Int
        "bracket" |-> BRACKET:Val,
        PARENT:Parent) ...
    </scopes>
    requires D >=Int 0

  claim [pop-normalization]:
    <k> #pop => V ~> CONT </k>
    <ret> retV(V:Val) => noRet </ret>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <env> L:Int => CALLER </env>
    <scopes> (L |-> FRAME:Scope SC:Map) => SC </scopes>
    <scopeLoc> CUR:Int => SAVED </scopeLoc>
    requires notBool L in_keys(SC)
endmodule
