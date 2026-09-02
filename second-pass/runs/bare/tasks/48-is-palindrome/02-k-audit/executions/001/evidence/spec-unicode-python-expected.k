requires "../source/verification.k"

module SPEC-UNICODE-PYTHON-EXPECTED
  imports VERIFICATION

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
        ~> #invoke(
             "is_palindrome",
             PyString("🙂a🙂"))
      => PyBool(true)
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
