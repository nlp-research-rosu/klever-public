requires "verification.k"

module FALSE-RESULT
  imports VERIFICATION

  // Fresh false result obligation: correct execution returns 8, not 9.
  claim [false-ground-result]:
    <k>
      Call(
        closureVal(
          ("s", "n"),
          Return(
            BinOp(
              "-",
              BinOp(
                "-",
                Name("n"),
                Call(
                  Name("int"),
                  Subscript(
                    Call(Attribute(Name("s"), "split"), .Exprs),
                    Int(0)),
                  .Exprs)),
              Call(
                Name("int"),
                Subscript(
                  Call(Attribute(Name("s"), "split"), .Exprs),
                  Int(3)),
                .Exprs)))
          .Stmts,
          0),
        str(strToCodes("5 apples and 6 oranges")),
        19)
      => 9
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
