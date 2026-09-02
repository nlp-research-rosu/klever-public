requires "verification.k"

module SPEC
  imports VERIFICATION

  // Exact-output proofs.  These execute the constructor tree reproduced from
  // solution.mpy through the semantic machine.
  claim Run(SolutionMachine(1))
    => Run(Halted(.Map, SolutionFunctions(), .List, ListVal(.List)))

  claim Run(SolutionMachine(2))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)))))

  claim Run(SolutionMachine(3))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)))))

  claim Run(SolutionMachine(4))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2)))))

  claim Run(SolutionMachine(8))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(2)))))

  claim Run(SolutionMachine(9))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)) ListItem(IntVal(3)))))

  claim Run(SolutionMachine(13))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(13)))))

  claim Run(SolutionMachine(25))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(5)) ListItem(IntVal(5)))))

  claim Run(SolutionMachine(31))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(31)))))

  claim Run(SolutionMachine(70))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(5))
                 ListItem(IntVal(7)))))

  claim Run(SolutionMachine(100))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(5)) ListItem(IntVal(5)))))

  claim Run(SolutionMachine(360))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(2)) ListItem(IntVal(3))
                 ListItem(IntVal(3)) ListItem(IntVal(5)))))

  claim Run(SolutionMachine(999))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)) ListItem(IntVal(3))
                 ListItem(IntVal(3)) ListItem(IntVal(37)))))

  // Contract proofs for the same representative partition.  The verifier
  // checks product equality, nondecreasing order, and primality of every item.
  claim Observe(ValidFactorization(1, MachineValue(SolutionMachine(1))))
    => Observe(true)
  claim Observe(ValidFactorization(2, MachineValue(SolutionMachine(2))))
    => Observe(true)
  claim Observe(ValidFactorization(3, MachineValue(SolutionMachine(3))))
    => Observe(true)
  claim Observe(ValidFactorization(4, MachineValue(SolutionMachine(4))))
    => Observe(true)
  claim Observe(ValidFactorization(8, MachineValue(SolutionMachine(8))))
    => Observe(true)
  claim Observe(ValidFactorization(9, MachineValue(SolutionMachine(9))))
    => Observe(true)
  claim Observe(ValidFactorization(13, MachineValue(SolutionMachine(13))))
    => Observe(true)
  claim Observe(ValidFactorization(25, MachineValue(SolutionMachine(25))))
    => Observe(true)
  claim Observe(ValidFactorization(31, MachineValue(SolutionMachine(31))))
    => Observe(true)
  claim Observe(ValidFactorization(70, MachineValue(SolutionMachine(70))))
    => Observe(true)
  claim Observe(ValidFactorization(100, MachineValue(SolutionMachine(100))))
    => Observe(true)
  claim Observe(ValidFactorization(360, MachineValue(SolutionMachine(360))))
    => Observe(true)
  claim Observe(ValidFactorization(999, MachineValue(SolutionMachine(999))))
    => Observe(true)
endmodule
