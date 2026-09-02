requires "../source/verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real program returns true for S = "" and S = "aba".
  claim
    <py>
      <k>
        Module(
          FuncDef("is_palindrome", Params("text"),
            Return(
              Compare(
                Name("text"),
                CmpOp(
                  "==",
                  Subscript(
                    Name("text"),
                    Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))))
        ~> #invoke("is_palindrome", PyString(S:String))
      => PyBool(false)
      </k>
      <functions>
        .Map
      => "is_palindrome" |-> #function(
           "text",
           Return(
             Compare(
               Name("text"),
               CmpOp(
                 "==",
                 Subscript(
                   Name("text"),
                   Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
      </functions>
      <env> .Map </env>
    </py>
endmodule
