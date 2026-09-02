requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [max-int-numeric-acc]:
    <k>
      #maxAcc(list(VS:ValSeq), M:Int)
      =>
      maxIntNumericVS(M, VS)
      ...
    </k>
    requires allNumericVS(VS)

  claim [max-float-numeric-acc]:
    <k>
      #maxAccF(list(VS:ValSeq), M:Float)
      =>
      maxFloatNumericVS(M, VS)
      ...
    </k>
    requires allNumericVS(VS)

  claim [max-general-numeric-acc]:
    <k>
      #maxAccV(list(VS:ValSeq), M:Val)
      =>
      maxNumericGeneralVS(M, VS)
      ...
    </k>
    requires isNumericV(M) andBool allNumericVS(VS)

  claim [max-element-int-head]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(Name("max_element"), list(vCons(I:Int, REST:ValSeq)))
      => maxIntNumericVS(I, REST)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumericVS(REST)

  claim [max-element-float-head]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(Name("max_element"), list(vCons(F:Float, REST:ValSeq)))
      => maxFloatNumericVS(F, REST)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumericVS(REST)

  claim [max-element-bool-head]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(Name("max_element"), list(vCons(B:Bool, REST:ValSeq)))
      => maxNumericGeneralVS(B, REST)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumericVS(REST)

endmodule

module SPEC-STR
  imports VERIFICATION

  claim [max-general-str-acc]:
    <k>
      #maxAccV(list(VS:ValSeq), M:Val)
      =>
      maxStrGeneralVS(M, VS)
      ...
    </k>
    requires isStr(M) andBool allStrVS(VS)

  claim [max-element-str-head]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(Name("max_element"), list(vCons(S:Str, REST:ValSeq)))
      => maxStrGeneralVS(S, REST)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrVS(REST)
endmodule
