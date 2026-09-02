requires "/tmp/audit-work/104-unique-digits-audit-002/source/verification.k"

module AUDIT-PINNING-TERM
  imports VERIFICATION

  claim <k> solutionProgram
        => Module(
             FuncDef("no_even_digit", Params("n"),
               If(Compare(Name("n"), CmpOp("==", Int(0))),
                 Return(Bool(true)),
                 .Stmts)
               If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
                 Return(Bool(false)),
                 .Stmts)
               Return(Call(Name("no_even_digit"), BinOp("//", Name("n"), Int(10)))))
             FuncDef("unique_digits", Params("x"),
               Return(
                 Call(
                   Name("sorted"),
                   ListComp(Name("n"),
                     CompFor(
                       Name("n"),
                       Name("x"),
                       Call(Name("no_even_digit"), Name("n")))))))) ... </k>
endmodule

module AUDIT-PRECONDITION-WITNESS
  imports VERIFICATION

  claim <k> positiveInts(cons(15, cons(2, .Ints))) => true ... </k>
endmodule

module AUDIT-ENTRY-WITNESS
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(15, cons(2, .Ints))))
        => pyList(cons(15, .Ints)) ... </k>
endmodule
