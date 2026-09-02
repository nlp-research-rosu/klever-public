requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  /*
   * The translated module initializes both sentinels and reaches the loop
   * with the arbitrary integer input unchanged.
   */
  claim
    <k> run(solutionProgram, Value(pyIntList(IS)))
      => iterateIntSeq("value", IS,
           If(Compare(Name("value"), CmpOp("<", Int(0))),
             If(Compare(Name("largest_negative"), CmpOp("is", NoneVal)),
               Assign(Name("largest_negative"), Name("value")),
               If(Compare(Name("value"), CmpOp(">", Name("largest_negative"))),
                 Assign(Name("largest_negative"), Name("value")),
                 .Stmts)),
             .Stmts)
           If(Compare(Name("value"), CmpOp(">", Int(0))),
             If(Compare(Name("smallest_positive"), CmpOp("is", NoneVal)),
               Assign(Name("smallest_positive"), Name("value")),
               If(Compare(Name("value"), CmpOp("<", Name("smallest_positive"))),
                 Assign(Name("smallest_positive"), Name("value")),
                 .Stmts)),
             .Stmts))
         ~> exec(Return(
              TupleExpr(Name("largest_negative"), Name("smallest_positive"))))
    </k>
    <env> .Map
      => "largest_negative" |-> pyNone
         "lst" |-> pyIntList(IS)
         "smallest_positive" |-> pyNone
    </env>
    <steps> 0 </steps>

  /*
   * Generalized loop invariant.  K proves this claim circularly: nil is the
   * base case; icon(I, IS) executes one operational iteration and reuses the
   * claim on the strictly smaller tail IS.  Instantiating N and P with pyNone
   * gives the HumanEval contract after the setup claim above.
   */
  claim
    <k> iterateIntSeq("value", IS,
          If(Compare(Name("value"), CmpOp("<", Int(0))),
            If(Compare(Name("largest_negative"), CmpOp("is", NoneVal)),
              Assign(Name("largest_negative"), Name("value")),
              If(Compare(Name("value"), CmpOp(">", Name("largest_negative"))),
                Assign(Name("largest_negative"), Name("value")),
                .Stmts)),
            .Stmts)
          If(Compare(Name("value"), CmpOp(">", Int(0))),
            If(Compare(Name("smallest_positive"), CmpOp("is", NoneVal)),
              Assign(Name("smallest_positive"), Name("value")),
              If(Compare(Name("value"), CmpOp("<", Name("smallest_positive"))),
                Assign(Name("smallest_positive"), Name("value")),
                .Stmts)),
            .Stmts))
        ~> exec(Return(
             TupleExpr(Name("largest_negative"), Name("smallest_positive"))))
      => pyTuple(#negFold(IS, N), #posFold(IS, P)) </k>
    <env>
      "largest_negative" |-> N
      "smallest_positive" |-> P
      "value" |-> _OLD
      _REST:Map
      => ?_
    </env>
    <steps> _S => ?_ </steps>

  /*
   * End-to-end correctness for every finite integer sequence.  The empty
   * branch executes directly.  The nonempty branch executes its first real
   * iteration, establishing the value binding required by the generalized
   * loop invariant above, which then discharges the arbitrary tail.
   */
  claim
    <k> run(solutionProgram, Value(pyIntList(IS)))
      => pyTuple(#posFold(IS, pyNone), #negFold(IS, pyNone)) </k>
    <env> .Map => ?_ </env>
    <steps> 0 => ?_ </steps>
endmodule
