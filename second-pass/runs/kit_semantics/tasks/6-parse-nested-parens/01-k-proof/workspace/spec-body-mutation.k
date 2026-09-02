requires "spec.k"

module SPEC-BODY-MUTATION
  imports SPEC

  // Deliberately mutated implementation: initial depth is 1 instead of 0.
  // The unchanged expected result [1] for "()" must therefore be rejected.
  claim [mutated-body]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("parse_nested_parens", Params("paren_string"),
          Assign(Name("depths"), ListExpr(.Exprs))
          Assign(Name("depth"), Int(1))
          Assign(Name("deepest"), Int(0))
          Assign(Name("char"), Str(""))
          For(Name("char"), Name("paren_string"), loopBody)
          afterLoop)))
      ~> Call(Name("parse_nested_parens"),
              str(iCons(40, iCons(41, .IntSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
          "parse_nested_parens"
            |-> closureVal(
              "paren_string",
              Assign(Name("depths"), ListExpr(.Exprs))
              Assign(Name("depth"), Int(1))
              Assign(Name("deepest"), Int(0))
              Assign(Name("char"), Str(""))
              For(Name("char"), Name("paren_string"), loopBody)
              afterLoop,
              0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
