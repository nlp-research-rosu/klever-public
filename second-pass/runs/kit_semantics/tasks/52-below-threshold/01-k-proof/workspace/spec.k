requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [below-threshold-empty]:
    <k>
      #loadAll(
        Module(
          FuncDef("below_threshold", Params("l", "t"),
            Expr(Str("Return True if all numbers in the list l are below threshold t."))
            Assign(Name("e"), Int(0))
            For(Name("e"), Name("l"),
              If(Compare(Name("e"), CmpOp("<", Name("t"))),
                Continue, .Stmts)
              Return(Bool(false)))
            Return(Bool(true)))))
      ~> Call(Name("below_threshold"), list(.ValSeq), T:Int)
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [below-threshold-int]:
    <k>
      #loadAll(
        Module(
          FuncDef("below_threshold", Params("l", "t"),
            Expr(Str("Return True if all numbers in the list l are below threshold t."))
            Assign(Name("e"), Int(0))
            For(Name("e"), Name("l"),
              If(Compare(Name("e"), CmpOp("<", Name("t"))),
                Continue, .Stmts)
              Return(Bool(false)))
            Return(Bool(true)))))
      ~> Call(
        Name("below_threshold"),
        list(vCons(I:Int, REST:ValSeq)),
        T:Int)
      => allBelow(vCons(I, REST), T)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericSeq(REST)

  claim [below-threshold-bool]:
    <k>
      #loadAll(
        Module(
          FuncDef("below_threshold", Params("l", "t"),
            Expr(Str("Return True if all numbers in the list l are below threshold t."))
            Assign(Name("e"), Int(0))
            For(Name("e"), Name("l"),
              If(Compare(Name("e"), CmpOp("<", Name("t"))),
                Continue, .Stmts)
              Return(Bool(false)))
            Return(Bool(true)))))
      ~> Call(
        Name("below_threshold"),
        list(vCons(B:Bool, REST:ValSeq)),
        T:Int)
      => allBelow(vCons(B, REST), T)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericSeq(REST)

  claim [below-threshold-float]:
    <k>
      #loadAll(
        Module(
          FuncDef("below_threshold", Params("l", "t"),
            Expr(Str("Return True if all numbers in the list l are below threshold t."))
            Assign(Name("e"), Int(0))
            For(Name("e"), Name("l"),
              If(Compare(Name("e"), CmpOp("<", Name("t"))),
                Continue, .Stmts)
              Return(Bool(false)))
            Return(Bool(true)))))
      ~> Call(
        Name("below_threshold"),
        list(vCons(F:Float, REST:ValSeq)),
        T:Int)
      => allBelow(vCons(F, REST), T)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericSeq(REST)
endmodule
