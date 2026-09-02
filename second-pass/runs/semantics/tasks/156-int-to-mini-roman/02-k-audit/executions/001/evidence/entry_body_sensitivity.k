requires "/tmp/audit-work/candidate/verification.k"

// The actual `_roman_ones` closure body bound in the entry configuration is
// mutated from the submitted tuple lookup to `return "z"`.  At N=1, fixed
// semantics therefore returns "z", whereas the original postcondition is "i".

module ENTRY-BODY-MUTATION-BRIDGED
  imports ROMAN-VERIFICATION

  claim [mutatedEntryStillProves]:
    <k>
      Call(Name("int_to_mini_roman"), Int(1))
      => str(romanSpec(1))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", romanThousandsBody, 0)
        "_roman_hundreds"
          |-> closureVal("digit", romanHundredsBody, 0)
        "_roman_tens"
          |-> closureVal("digit", romanTensBody, 0)
        "_roman_ones"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "int_to_mini_roman"
          |-> closureVal("number", romanSolutionBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module ENTRY-BODY-MUTATION-FIXED
  imports ROMAN-BASE

  claim [mutatedEntryMustFailOriginalResult]:
    <k>
      Call(Name("int_to_mini_roman"), Int(1))
      => str(romanSpec(1))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", romanThousandsBody, 0)
        "_roman_hundreds"
          |-> closureVal("digit", romanHundredsBody, 0)
        "_roman_tens"
          |-> closureVal("digit", romanTensBody, 0)
        "_roman_ones"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "int_to_mini_roman"
          |-> closureVal("number", romanSolutionBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
