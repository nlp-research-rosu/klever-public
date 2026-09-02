requires "verification.k"

module AUDIT-SPEC-FALSE
  imports VERIFICATION

  claim [reviewer-off-by-one]:
    <k>
      Call(Name("get_max_triples"), Int(N))
      => expectedTriples(N) -Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |->
          closureVal(
            "n",
            Assign(
              Name("divisible_by_three"),
              BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3)))
            Assign(
              Name("not_divisible_by_three"),
              BinOp("-", Name("n"), Name("divisible_by_three")))
            Assign(
              Name("triples_of_divisible"),
              BinOp(
                "//",
                BinOp(
                  "*",
                  BinOp(
                    "*",
                    Name("divisible_by_three"),
                    BinOp("-", Name("divisible_by_three"), Int(1))),
                  BinOp("-", Name("divisible_by_three"), Int(2))),
                Int(6)))
            Assign(
              Name("triples_of_non_divisible"),
              BinOp(
                "//",
                BinOp(
                  "*",
                  BinOp(
                    "*",
                    Name("not_divisible_by_three"),
                    BinOp("-", Name("not_divisible_by_three"), Int(1))),
                  BinOp("-", Name("not_divisible_by_three"), Int(2))),
                Int(6)))
            Return(
              BinOp(
                "+",
                Name("triples_of_divisible"),
                Name("triples_of_non_divisible"))),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N ==Int 4
endmodule
