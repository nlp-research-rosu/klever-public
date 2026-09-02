requires "verification.k"

module XOR-GROUND-WITNESS
  imports XOR-VERIFICATION

  claim [ground-recursive]:
    <k> exec(solutionBody,
             env(str(segment(3, seed(2))), str(segment(3, seed(3)))),
             solutionBody)
      => returned(str(cons(true, cons(false, cons(false, empty))))) ... </k>
    <args> Args(str(empty), str(empty)) </args>

  claim [ground-entry]:
    <k> solutionProgram
      => returned(str(cons(true, cons(false, cons(false, empty))))) ... </k>
    <args>
      Args(str(segment(3, seed(2))), str(segment(3, seed(3))))
    </args>
endmodule
