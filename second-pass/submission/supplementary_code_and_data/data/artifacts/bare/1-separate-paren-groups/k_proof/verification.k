requires "semantic.k"

module MPY-VERIFICATION
  imports MPY

  // A direct contract model. It consumes input characters into a mathematical
  // scanner state: depth, unfinished group, completed groups, and last loop
  // character. Spaces change only the last-character component.
  syntax ScanState ::= "scanState" "(" PInt "," Chars "," Outputs "," Chars ")"
  syntax ScanState ::= "runSpec" "(" Chars "," PInt "," Chars "," Outputs "," Chars ")" [function]
  syntax PInt ::= "stateDepth" "(" ScanState ")" [function]
  syntax Chars ::= "stateCurrent" "(" ScanState ")" [function]
                 | "stateLast" "(" ScanState ")" [function]
  syntax Outputs ::= "stateOutput" "(" ScanState ")" [function]
                   | "separateSpec" "(" Chars ")" [function]

  rule runSpec(.Chars, D, CURRENT, OUT, LAST) => scanState(D, CURRENT, OUT, LAST)
  rule runSpec(SP CS, D, CURRENT, OUT, _LAST) => runSpec(CS, D, CURRENT, OUT, SP)
  rule runSpec(LP CS, D, CURRENT, OUT, _LAST) => runSpec(CS, succ(D), #concat(CURRENT, LP), OUT, LP)
  rule runSpec(RP CS, zero, CURRENT, OUT, _LAST) => runSpec(CS, zero, .Chars, #snocOut(OUT, #concat(CURRENT, RP)), RP)
  rule runSpec(RP CS, succ(zero), CURRENT, OUT, _LAST) => runSpec(CS, zero, .Chars, #snocOut(OUT, #concat(CURRENT, RP)), RP)
  rule runSpec(RP CS, succ(succ(D)), CURRENT, OUT, _LAST) => runSpec(CS, succ(D), #concat(CURRENT, RP), OUT, RP)

  rule stateDepth(scanState(D, _, _, _)) => D
  rule stateCurrent(scanState(_, CURRENT, _, _)) => CURRENT
  rule stateOutput(scanState(_, _, OUT, _)) => OUT
  rule stateLast(scanState(_, _, _, LAST)) => LAST
  rule separateSpec(CS) => stateOutput(runSpec(CS, zero, .Chars, .Outputs, .Chars))

endmodule
