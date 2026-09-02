requires "semantic.k"

module SPEC
  imports SEMANTIC

  // Each upper endpoint is exclusive.  Together these claims cover exactly
  // every integer in the prompt domain 0 <= N <= 10000.
  claim [inputs-00000-00999]:
    <k> checkRange(0, 1000) => true </k>

  claim [inputs-01000-01999]:
    <k> checkRange(1000, 2000) => true </k>

  claim [inputs-02000-02999]:
    <k> checkRange(2000, 3000) => true </k>

  claim [inputs-03000-03999]:
    <k> checkRange(3000, 4000) => true </k>

  claim [inputs-04000-04999]:
    <k> checkRange(4000, 5000) => true </k>

  claim [inputs-05000-05999]:
    <k> checkRange(5000, 6000) => true </k>

  claim [inputs-06000-06999]:
    <k> checkRange(6000, 7000) => true </k>

  claim [inputs-07000-07999]:
    <k> checkRange(7000, 8000) => true </k>

  claim [inputs-08000-08999]:
    <k> checkRange(8000, 9000) => true </k>

  claim [inputs-09000-09999]:
    <k> checkRange(9000, 10000) => true </k>

  claim [input-10000]:
    <k> checkRange(10000, 10001) => true </k>
endmodule
