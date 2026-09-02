requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  syntax Int  ::= cubeOf(Int)              [function, total]
  syntax Bool ::= cubeSearch(Int, Int)     [function, total]
                | isCubeInt(Int)           [function, total]
  syntax Val  ::= "iscubeClosure"          [function, total]
endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  // The mathematical cube used by the specification predicate.
  rule cubeOf(I) => (I *Int I) *Int I

  // Search nonnegative candidates in increasing order.  The three guards are
  // disjoint and exhaustive for mathematical integers.
  rule cubeSearch(A, I) => true
    requires cubeOf(I) ==Int A
  rule cubeSearch(A, I) => false
    requires cubeOf(I) >Int A
  rule cubeSearch(A, I) => cubeSearch(A, I +Int 1)
    requires cubeOf(I) <Int A

  // At loop exit, the Python equality is exactly the search result: if the
  // cube is not below A, it is either equal (both true) or above (both false).
  rule ((I *Int I) *Int I ==Int A) => cubeSearch(A, I)
    requires notBool ((I *Int I) *Int I <Int A)
    [simplification]

  // The function-frame pop in the fixed semantics deletes scope key 1.
  // Normalize that exact symbolic Map update after proving the key is absent
  // from the preserved remainder.
  rule ((1 |-> S:Scope) REST:Map) [ 1 <- undef ] => REST
    requires notBool 1 in_keys(REST)
    [simplification]

  // Cubeness is invariant under sign, so search the nonnegative magnitude.
  rule isCubeInt(A) => cubeSearch(0 -Int A, 0)
    requires A <Int 0
  rule isCubeInt(A) => cubeSearch(A, 0)
    requires A >=Int 0

  // Exact closure produced when solution.mpy is loaded in module scope 0.
  // This is a definitional abbreviation, not an execution shortcut.
  rule iscubeClosure
    => closureVal(
         "a",
         If(
           Compare(Name("a"), CmpOp("<", Int(0))),
           Assign(Name("a"), UnaryOp("-", Name("a"))),
           .Stmts)
         Assign(Name("candidate"), Int(0))
         While(
           Compare(
             BinOp(
               "*",
               BinOp("*", Name("candidate"), Name("candidate")),
               Name("candidate")),
             CmpOp("<", Name("a"))),
           AugAssign(Name("candidate"), "+", Int(1)))
         Return(
           Compare(
             BinOp(
               "*",
               BinOp("*", Name("candidate"), Name("candidate")),
               Name("candidate")),
             CmpOp("==", Name("a")))),
         0)
endmodule
