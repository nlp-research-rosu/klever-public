requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [ground-five-six]:
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
      => 8
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
