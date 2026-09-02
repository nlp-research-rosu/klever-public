requires "semantic-no-specializations.k"

module BRIDGE-CONNECTION
  imports MPY

  claim [len-nil]:
    <k> (eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(true)) ... </k>
    <env> "lst" |-> pyList(nil) </env>

  claim [len-singleton]:
    <k> (eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(true)) ... </k>
    <env> "lst" |-> pyList(cons(HEAD, nil)) </env>

  claim [len-two-plus]:
    <k> (eval(Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))))
      => pyBool(false)) ... </k>
    <env> "lst" |-> pyList(cons(HEAD, cons(SECOND, REST))) </env>

  claim [parity-conditional]:
    <k> (eval(IfExp(
          Compare(
            BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
            CmpOp("==", Int(0))),
          Subscript(Name("lst"), Int(1)),
          Int(0)))
      => pyInt(evenPart(SECOND))) ... </k>
    <env> "lst" |-> pyList(cons(HEAD, cons(SECOND, REST))) </env>

  claim [parity-even]:
    <k> (eval(IfExp(
          Compare(
            BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
            CmpOp("==", Int(0))),
          Subscript(Name("lst"), Int(1)),
          Int(0)))
      => pyInt(SECOND)) ... </k>
    <env> "lst" |-> pyList(cons(HEAD, cons(SECOND, REST))) </env>
    requires SECOND %Int 2 ==Int 0

  claim [parity-odd]:
    <k> (eval(IfExp(
          Compare(
            BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
            CmpOp("==", Int(0))),
          Subscript(Name("lst"), Int(1)),
          Int(0)))
      => pyInt(0)) ... </k>
    <env> "lst" |-> pyList(cons(HEAD, cons(SECOND, REST))) </env>
    requires SECOND %Int 2 =/=Int 0

  claim [size-nonnegative]:
    (size(VALUES:ISeq) >=Int 0 => true)

  claim [size-nonnegative-config]:
    <k> (size(VALUES:ISeq) >=Int 0 => true) ... </k>
endmodule
