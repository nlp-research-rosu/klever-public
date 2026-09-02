requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  // The three constructor cases exhaust ISeq and validate the len<2 bridge
  // for the exact Name("lst") expression used by the submitted program.
  claim [short-nil]:
    <k> eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(true) ... </k>
    <env> "lst" |-> pyList(nil) </env>

  claim [short-singleton]:
    <k> eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(true) ... </k>
    <env> "lst" |-> pyList(cons(A, nil)) </env>

  claim [short-long]:
    <k> eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(false) ... </k>
    <env> "lst" |-> pyList(cons(A, cons(B, REST))) </env>
    requires size(REST) >=Int 0

  // The two parity guards exhaust Int and validate the result-bearing
  // keepIfEven bridge for the exact pure subscript used by the program.
  claim [even-item]:
    <k> eval(IfExp(
          Compare(
            BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
            CmpOp("==", Int(0))),
          Subscript(Name("lst"), Int(1)),
          Int(0)))
      => pyInt(evenPart(I)) ... </k>
    <env> "lst" |-> pyList(cons(A, cons(I, REST))) </env>
    requires I %Int 2 ==Int 0

  claim [odd-item]:
    <k> eval(IfExp(
          Compare(
            BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
            CmpOp("==", Int(0))),
          Subscript(Name("lst"), Int(1)),
          Int(0)))
      => pyInt(evenPart(I)) ... </k>
    <env> "lst" |-> pyList(cons(A, cons(I, REST))) </env>
    requires I %Int 2 =/=Int 0
endmodule
