requires "verification.k"

// Bridge-free execution for N=5,D=2 increments divisor once before returning.
module BRIDGE-STATE-FIXED-CORRECT
  imports VERIFICATION

  claim <mpy>
          <k>
            While(Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("length"))),
              If(Compare(
                BinOp("%", Name("length"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Str("NO")),
                .Stmts)
              Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
            ~> (Return(Str("YES")) .Stmts)
            => strVal("YES")
          </k>
          <functions> .Map </functions>
          <env>
            "length" |-> intVal(5)
            "divisor" |-> (intVal(2) => intVal(3))
          </env>
        </mpy>
endmodule

// This is a deliberately false state conclusion under bridge-free execution.
module BRIDGE-STATE-FIXED-FALSE
  imports VERIFICATION

  claim <mpy>
          <k>
            While(Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("length"))),
              If(Compare(
                BinOp("%", Name("length"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Str("NO")),
                .Stmts)
              Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
            ~> (Return(Str("YES")) .Stmts)
            => strVal("YES")
          </k>
          <functions> .Map </functions>
          <env>
            "length" |-> intVal(5)
            "divisor" |-> intVal(2)
          </env>
        </mpy>
endmodule

// The candidate bridge proves that same false state conclusion because its rule
// rewrites only <k> and therefore incorrectly preserves divisor=2.
module BRIDGE-STATE-EXTENDED-FALSE
  imports VERIFICATION-WITH-LOOP-LEMMA

  claim <mpy>
          <k>
            While(Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("length"))),
              If(Compare(
                BinOp("%", Name("length"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Str("NO")),
                .Stmts)
              Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
            ~> (Return(Str("YES")) .Stmts)
            => strVal("YES")
          </k>
          <functions> .Map </functions>
          <env>
            "length" |-> intVal(5)
            "divisor" |-> intVal(2)
          </env>
        </mpy>
endmodule

// The same false preservation claim at the loop state reached from the valid
// intended input interval1=(0,5), interval2=(0,5).  Unmentioned cells are
// framed by the cell-fragment completion.
module BRIDGE-ACTUAL-INPUT-FIXED-FALSE
  imports VERIFICATION

  claim <k>
          While(Compare(
            BinOp("*", Name("divisor"), Name("divisor")),
            CmpOp("<=", Name("length"))),
            If(Compare(
              BinOp("%", Name("length"), Name("divisor")),
              CmpOp("==", Int(0))),
              Return(Str("NO")),
              .Stmts)
            Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
          ~> (Return(Str("YES")) .Stmts)
          => strVal("YES")
        </k>
        <env>
          "interval1" |-> tupleVal(intVal(0), intVal(5))
          "interval2" |-> tupleVal(intVal(0), intVal(5))
          "left" |-> intVal(0)
          "right" |-> intVal(5)
          "length" |-> intVal(5)
          "divisor" |-> intVal(2)
        </env>
endmodule

module BRIDGE-ACTUAL-INPUT-EXTENDED-FALSE
  imports VERIFICATION-WITH-LOOP-LEMMA

  claim <k>
          While(Compare(
            BinOp("*", Name("divisor"), Name("divisor")),
            CmpOp("<=", Name("length"))),
            If(Compare(
              BinOp("%", Name("length"), Name("divisor")),
              CmpOp("==", Int(0))),
              Return(Str("NO")),
              .Stmts)
            Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
          ~> (Return(Str("YES")) .Stmts)
          => strVal("YES")
        </k>
        <env>
          "interval1" |-> tupleVal(intVal(0), intVal(5))
          "interval2" |-> tupleVal(intVal(0), intVal(5))
          "left" |-> intVal(0)
          "right" |-> intVal(5)
          "length" |-> intVal(5)
          "divisor" |-> intVal(2)
        </env>
endmodule
