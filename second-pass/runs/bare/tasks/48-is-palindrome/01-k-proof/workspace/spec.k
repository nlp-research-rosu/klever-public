requires "verification.k"

module SPEC
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
        ~> #invoke("is_palindrome", PyString(S:String))
      => PyBool(isPalindrome(S))
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
