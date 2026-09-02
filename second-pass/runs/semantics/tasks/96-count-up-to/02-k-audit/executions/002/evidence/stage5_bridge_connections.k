requires "/tmp/audit-work/audit96/verification.k"

// Bridge-free theorem over the complete match domain of the inner summary
// rule. It intentionally omits exactly the same generated configuration cells
// as the rule and leaves the builtins map arbitrary.
module AUDIT-FULL-INNER-BRIDGE-SPEC
  imports COUNT-UP-TO-BASE

  claim <k>
          #while(
            Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
            If(
              Compare(
                BinOp("%", Name("candidate"), Name("divisor")),
                CmpOp("==", Int(0))),
              Assign(Name("is_prime"), Bool(false)),
              .Stmts)
            AugAssign(Name("divisor"), "+", Int(1)))
          => .K
          ...
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope(MOD:Map, parent(-1))
          -1 |-> scope(BI:Map, root)
          1 |-> scope(
            ("candidate" |-> C:Int
             "divisor" |-> (D:Int => C)
             "is_prime" |-> (B:Bool => B andBool noDivisor(C, D, C))
             "n" |-> N:Int
             "result" |-> ref(0)),
            parent(0))
        </scopes>
        <heap> 0 |-> list(VS:ValSeq) </heap>
        requires 2 <=Int D andBool D <=Int C
endmodule

// Bridge-free with respect to the outer summary: the only proof extension
// imported here is the separately checked complete-domain inner theorem.
module AUDIT-FULL-OUTER-BRIDGE-SPEC
  imports COUNT-UP-TO-WITH-INNER

  claim <k>
          #while(
            Compare(Name("candidate"), CmpOp("<", Name("n"))),
            While(
              Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
              If(
                Compare(
                  BinOp("%", Name("candidate"), Name("divisor")),
                  CmpOp("==", Int(0))),
                Assign(Name("is_prime"), Bool(false)),
                .Stmts)
              AugAssign(Name("divisor"), "+", Int(1)))
            If(
              Name("is_prime"),
              Expr(Call(
                Attribute(Name("result"), "append"),
                Name("candidate"))),
              .Stmts)
            AugAssign(Name("candidate"), "+", Int(1))
            Assign(Name("is_prime"), Bool(true))
            Assign(Name("divisor"), Int(2)))
          => .K
          ...
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope(MOD:Map, parent(-1))
          -1 |-> scope(BI:Map, root)
          1 |-> scope(
            ("n" |-> N:Int
             "candidate" |-> (I:Int => N)
             "is_prime" |-> true
             "divisor" |-> 2
             "result" |-> ref(0)),
            parent(0))
        </scopes>
        <heap>
          0 |-> (list(VS:ValSeq) => list(primesAcc(VS, I, N)))
        </heap>
        requires 2 <=Int I andBool I <=Int N
endmodule
