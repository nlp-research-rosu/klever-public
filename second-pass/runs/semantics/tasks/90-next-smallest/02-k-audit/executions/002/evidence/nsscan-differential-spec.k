requires "verification.k"

module NSSCAN-DIFFERENTIAL-SPEC
  imports NEXT-SMALLEST-VERIFICATION
  // Ground inputs checked against trusted canonical.py: 341
  // case 0: []
  claim <k> nsScan(nilInts, 0, 0, 0) => noneV </k>
  // case 1: [1]
  claim <k> nsScan(consInts(1, nilInts), 0, 0, 0) => noneV </k>
  // case 2: [1, 1]
  claim <k> nsScan(consInts(1, consInts(1, nilInts)), 0, 0, 0) => noneV </k>
  // case 3: [1, 2]
  claim <k> nsScan(consInts(1, consInts(2, nilInts)), 0, 0, 0) => 2 </k>
  // case 4: [2, 1]
  claim <k> nsScan(consInts(2, consInts(1, nilInts)), 0, 0, 0) => 2 </k>
  // case 5: [3, 1, 2, 1]
  claim <k> nsScan(consInts(3, consInts(1, consInts(2, consInts(1, nilInts)))), 0, 0, 0) => 2 </k>
  // case 6: [0, -1, 0]
  claim <k> nsScan(consInts(0, consInts(-1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 7: [100000000000000000000000000000000000000000000000000000000000000000000000000000000, 10000000000000000000000000000000000000000000000000000000000000000000000000000000, 1000000000000000000000000000000000000000000000000000000000000000000000000000000000]
  claim <k> nsScan(consInts(100000000000000000000000000000000000000000000000000000000000000000000000000000000, consInts(10000000000000000000000000000000000000000000000000000000000000000000000000000000, consInts(1000000000000000000000000000000000000000000000000000000000000000000000000000000000, nilInts))), 0, 0, 0) => 100000000000000000000000000000000000000000000000000000000000000000000000000000000 </k>
  // case 8: [-100000000000000000000000000000000000000000000000000000000000000000000000000000000, -10000000000000000000000000000000000000000000000000000000000000000000000000000000, -1000000000000000000000000000000000000000000000000000000000000000000000000000000000]
  claim <k> nsScan(consInts(-100000000000000000000000000000000000000000000000000000000000000000000000000000000, consInts(-10000000000000000000000000000000000000000000000000000000000000000000000000000000, consInts(-1000000000000000000000000000000000000000000000000000000000000000000000000000000000, nilInts))), 0, 0, 0) => -100000000000000000000000000000000000000000000000000000000000000000000000000000000 </k>
  // case 9: [-2]
  claim <k> nsScan(consInts(-2, nilInts), 0, 0, 0) => noneV </k>
  // case 10: [-1]
  claim <k> nsScan(consInts(-1, nilInts), 0, 0, 0) => noneV </k>
  // case 11: [0]
  claim <k> nsScan(consInts(0, nilInts), 0, 0, 0) => noneV </k>
  // case 12: [2]
  claim <k> nsScan(consInts(2, nilInts), 0, 0, 0) => noneV </k>
  // case 13: [-2, -2]
  claim <k> nsScan(consInts(-2, consInts(-2, nilInts)), 0, 0, 0) => noneV </k>
  // case 14: [-2, -1]
  claim <k> nsScan(consInts(-2, consInts(-1, nilInts)), 0, 0, 0) => -1 </k>
  // case 15: [-2, 0]
  claim <k> nsScan(consInts(-2, consInts(0, nilInts)), 0, 0, 0) => 0 </k>
  // case 16: [-2, 1]
  claim <k> nsScan(consInts(-2, consInts(1, nilInts)), 0, 0, 0) => 1 </k>
  // case 17: [-2, 2]
  claim <k> nsScan(consInts(-2, consInts(2, nilInts)), 0, 0, 0) => 2 </k>
  // case 18: [-1, -2]
  claim <k> nsScan(consInts(-1, consInts(-2, nilInts)), 0, 0, 0) => -1 </k>
  // case 19: [-1, -1]
  claim <k> nsScan(consInts(-1, consInts(-1, nilInts)), 0, 0, 0) => noneV </k>
  // case 20: [-1, 0]
  claim <k> nsScan(consInts(-1, consInts(0, nilInts)), 0, 0, 0) => 0 </k>
  // case 21: [-1, 1]
  claim <k> nsScan(consInts(-1, consInts(1, nilInts)), 0, 0, 0) => 1 </k>
  // case 22: [-1, 2]
  claim <k> nsScan(consInts(-1, consInts(2, nilInts)), 0, 0, 0) => 2 </k>
  // case 23: [0, -2]
  claim <k> nsScan(consInts(0, consInts(-2, nilInts)), 0, 0, 0) => 0 </k>
  // case 24: [0, -1]
  claim <k> nsScan(consInts(0, consInts(-1, nilInts)), 0, 0, 0) => 0 </k>
  // case 25: [0, 0]
  claim <k> nsScan(consInts(0, consInts(0, nilInts)), 0, 0, 0) => noneV </k>
  // case 26: [0, 1]
  claim <k> nsScan(consInts(0, consInts(1, nilInts)), 0, 0, 0) => 1 </k>
  // case 27: [0, 2]
  claim <k> nsScan(consInts(0, consInts(2, nilInts)), 0, 0, 0) => 2 </k>
  // case 28: [1, -2]
  claim <k> nsScan(consInts(1, consInts(-2, nilInts)), 0, 0, 0) => 1 </k>
  // case 29: [1, -1]
  claim <k> nsScan(consInts(1, consInts(-1, nilInts)), 0, 0, 0) => 1 </k>
  // case 30: [1, 0]
  claim <k> nsScan(consInts(1, consInts(0, nilInts)), 0, 0, 0) => 1 </k>
  // case 31: [2, -2]
  claim <k> nsScan(consInts(2, consInts(-2, nilInts)), 0, 0, 0) => 2 </k>
  // case 32: [2, -1]
  claim <k> nsScan(consInts(2, consInts(-1, nilInts)), 0, 0, 0) => 2 </k>
  // case 33: [2, 0]
  claim <k> nsScan(consInts(2, consInts(0, nilInts)), 0, 0, 0) => 2 </k>
  // case 34: [2, 2]
  claim <k> nsScan(consInts(2, consInts(2, nilInts)), 0, 0, 0) => noneV </k>
  // case 35: [-2, -2, -2]
  claim <k> nsScan(consInts(-2, consInts(-2, consInts(-2, nilInts))), 0, 0, 0) => noneV </k>
  // case 36: [-2, -2, -1]
  claim <k> nsScan(consInts(-2, consInts(-2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 37: [-2, -2, 0]
  claim <k> nsScan(consInts(-2, consInts(-2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 38: [-2, -2, 1]
  claim <k> nsScan(consInts(-2, consInts(-2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 39: [-2, -2, 2]
  claim <k> nsScan(consInts(-2, consInts(-2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 40: [-2, -1, -2]
  claim <k> nsScan(consInts(-2, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 41: [-2, -1, -1]
  claim <k> nsScan(consInts(-2, consInts(-1, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 42: [-2, -1, 0]
  claim <k> nsScan(consInts(-2, consInts(-1, consInts(0, nilInts))), 0, 0, 0) => -1 </k>
  // case 43: [-2, -1, 1]
  claim <k> nsScan(consInts(-2, consInts(-1, consInts(1, nilInts))), 0, 0, 0) => -1 </k>
  // case 44: [-2, -1, 2]
  claim <k> nsScan(consInts(-2, consInts(-1, consInts(2, nilInts))), 0, 0, 0) => -1 </k>
  // case 45: [-2, 0, -2]
  claim <k> nsScan(consInts(-2, consInts(0, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 46: [-2, 0, -1]
  claim <k> nsScan(consInts(-2, consInts(0, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 47: [-2, 0, 0]
  claim <k> nsScan(consInts(-2, consInts(0, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 48: [-2, 0, 1]
  claim <k> nsScan(consInts(-2, consInts(0, consInts(1, nilInts))), 0, 0, 0) => 0 </k>
  // case 49: [-2, 0, 2]
  claim <k> nsScan(consInts(-2, consInts(0, consInts(2, nilInts))), 0, 0, 0) => 0 </k>
  // case 50: [-2, 1, -2]
  claim <k> nsScan(consInts(-2, consInts(1, consInts(-2, nilInts))), 0, 0, 0) => 1 </k>
  // case 51: [-2, 1, -1]
  claim <k> nsScan(consInts(-2, consInts(1, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 52: [-2, 1, 0]
  claim <k> nsScan(consInts(-2, consInts(1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 53: [-2, 1, 1]
  claim <k> nsScan(consInts(-2, consInts(1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 54: [-2, 1, 2]
  claim <k> nsScan(consInts(-2, consInts(1, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 55: [-2, 2, -2]
  claim <k> nsScan(consInts(-2, consInts(2, consInts(-2, nilInts))), 0, 0, 0) => 2 </k>
  // case 56: [-2, 2, -1]
  claim <k> nsScan(consInts(-2, consInts(2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 57: [-2, 2, 0]
  claim <k> nsScan(consInts(-2, consInts(2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 58: [-2, 2, 1]
  claim <k> nsScan(consInts(-2, consInts(2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 59: [-2, 2, 2]
  claim <k> nsScan(consInts(-2, consInts(2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 60: [-1, -2, -2]
  claim <k> nsScan(consInts(-1, consInts(-2, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 61: [-1, -2, -1]
  claim <k> nsScan(consInts(-1, consInts(-2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 62: [-1, -2, 0]
  claim <k> nsScan(consInts(-1, consInts(-2, consInts(0, nilInts))), 0, 0, 0) => -1 </k>
  // case 63: [-1, -2, 1]
  claim <k> nsScan(consInts(-1, consInts(-2, consInts(1, nilInts))), 0, 0, 0) => -1 </k>
  // case 64: [-1, -2, 2]
  claim <k> nsScan(consInts(-1, consInts(-2, consInts(2, nilInts))), 0, 0, 0) => -1 </k>
  // case 65: [-1, -1, -2]
  claim <k> nsScan(consInts(-1, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 66: [-1, -1, -1]
  claim <k> nsScan(consInts(-1, consInts(-1, consInts(-1, nilInts))), 0, 0, 0) => noneV </k>
  // case 67: [-1, -1, 0]
  claim <k> nsScan(consInts(-1, consInts(-1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 68: [-1, -1, 1]
  claim <k> nsScan(consInts(-1, consInts(-1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 69: [-1, -1, 2]
  claim <k> nsScan(consInts(-1, consInts(-1, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 70: [-1, 0, -2]
  claim <k> nsScan(consInts(-1, consInts(0, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 71: [-1, 0, -1]
  claim <k> nsScan(consInts(-1, consInts(0, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 72: [-1, 0, 0]
  claim <k> nsScan(consInts(-1, consInts(0, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 73: [-1, 0, 1]
  claim <k> nsScan(consInts(-1, consInts(0, consInts(1, nilInts))), 0, 0, 0) => 0 </k>
  // case 74: [-1, 0, 2]
  claim <k> nsScan(consInts(-1, consInts(0, consInts(2, nilInts))), 0, 0, 0) => 0 </k>
  // case 75: [-1, 1, -2]
  claim <k> nsScan(consInts(-1, consInts(1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 76: [-1, 1, -1]
  claim <k> nsScan(consInts(-1, consInts(1, consInts(-1, nilInts))), 0, 0, 0) => 1 </k>
  // case 77: [-1, 1, 0]
  claim <k> nsScan(consInts(-1, consInts(1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 78: [-1, 1, 1]
  claim <k> nsScan(consInts(-1, consInts(1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 79: [-1, 1, 2]
  claim <k> nsScan(consInts(-1, consInts(1, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 80: [-1, 2, -2]
  claim <k> nsScan(consInts(-1, consInts(2, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 81: [-1, 2, -1]
  claim <k> nsScan(consInts(-1, consInts(2, consInts(-1, nilInts))), 0, 0, 0) => 2 </k>
  // case 82: [-1, 2, 0]
  claim <k> nsScan(consInts(-1, consInts(2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 83: [-1, 2, 1]
  claim <k> nsScan(consInts(-1, consInts(2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 84: [-1, 2, 2]
  claim <k> nsScan(consInts(-1, consInts(2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 85: [0, -2, -2]
  claim <k> nsScan(consInts(0, consInts(-2, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 86: [0, -2, -1]
  claim <k> nsScan(consInts(0, consInts(-2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 87: [0, -2, 0]
  claim <k> nsScan(consInts(0, consInts(-2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 88: [0, -2, 1]
  claim <k> nsScan(consInts(0, consInts(-2, consInts(1, nilInts))), 0, 0, 0) => 0 </k>
  // case 89: [0, -2, 2]
  claim <k> nsScan(consInts(0, consInts(-2, consInts(2, nilInts))), 0, 0, 0) => 0 </k>
  // case 90: [0, -1, -2]
  claim <k> nsScan(consInts(0, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 91: [0, -1, -1]
  claim <k> nsScan(consInts(0, consInts(-1, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 92: [0, -1, 1]
  claim <k> nsScan(consInts(0, consInts(-1, consInts(1, nilInts))), 0, 0, 0) => 0 </k>
  // case 93: [0, -1, 2]
  claim <k> nsScan(consInts(0, consInts(-1, consInts(2, nilInts))), 0, 0, 0) => 0 </k>
  // case 94: [0, 0, -2]
  claim <k> nsScan(consInts(0, consInts(0, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 95: [0, 0, -1]
  claim <k> nsScan(consInts(0, consInts(0, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 96: [0, 0, 0]
  claim <k> nsScan(consInts(0, consInts(0, consInts(0, nilInts))), 0, 0, 0) => noneV </k>
  // case 97: [0, 0, 1]
  claim <k> nsScan(consInts(0, consInts(0, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 98: [0, 0, 2]
  claim <k> nsScan(consInts(0, consInts(0, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 99: [0, 1, -2]
  claim <k> nsScan(consInts(0, consInts(1, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 100: [0, 1, -1]
  claim <k> nsScan(consInts(0, consInts(1, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 101: [0, 1, 0]
  claim <k> nsScan(consInts(0, consInts(1, consInts(0, nilInts))), 0, 0, 0) => 1 </k>
  // case 102: [0, 1, 1]
  claim <k> nsScan(consInts(0, consInts(1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 103: [0, 1, 2]
  claim <k> nsScan(consInts(0, consInts(1, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 104: [0, 2, -2]
  claim <k> nsScan(consInts(0, consInts(2, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 105: [0, 2, -1]
  claim <k> nsScan(consInts(0, consInts(2, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 106: [0, 2, 0]
  claim <k> nsScan(consInts(0, consInts(2, consInts(0, nilInts))), 0, 0, 0) => 2 </k>
  // case 107: [0, 2, 1]
  claim <k> nsScan(consInts(0, consInts(2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 108: [0, 2, 2]
  claim <k> nsScan(consInts(0, consInts(2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 109: [1, -2, -2]
  claim <k> nsScan(consInts(1, consInts(-2, consInts(-2, nilInts))), 0, 0, 0) => 1 </k>
  // case 110: [1, -2, -1]
  claim <k> nsScan(consInts(1, consInts(-2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 111: [1, -2, 0]
  claim <k> nsScan(consInts(1, consInts(-2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 112: [1, -2, 1]
  claim <k> nsScan(consInts(1, consInts(-2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 113: [1, -2, 2]
  claim <k> nsScan(consInts(1, consInts(-2, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 114: [1, -1, -2]
  claim <k> nsScan(consInts(1, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 115: [1, -1, -1]
  claim <k> nsScan(consInts(1, consInts(-1, consInts(-1, nilInts))), 0, 0, 0) => 1 </k>
  // case 116: [1, -1, 0]
  claim <k> nsScan(consInts(1, consInts(-1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 117: [1, -1, 1]
  claim <k> nsScan(consInts(1, consInts(-1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 118: [1, -1, 2]
  claim <k> nsScan(consInts(1, consInts(-1, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 119: [1, 0, -2]
  claim <k> nsScan(consInts(1, consInts(0, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 120: [1, 0, -1]
  claim <k> nsScan(consInts(1, consInts(0, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 121: [1, 0, 0]
  claim <k> nsScan(consInts(1, consInts(0, consInts(0, nilInts))), 0, 0, 0) => 1 </k>
  // case 122: [1, 0, 1]
  claim <k> nsScan(consInts(1, consInts(0, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 123: [1, 0, 2]
  claim <k> nsScan(consInts(1, consInts(0, consInts(2, nilInts))), 0, 0, 0) => 1 </k>
  // case 124: [1, 1, -2]
  claim <k> nsScan(consInts(1, consInts(1, consInts(-2, nilInts))), 0, 0, 0) => 1 </k>
  // case 125: [1, 1, -1]
  claim <k> nsScan(consInts(1, consInts(1, consInts(-1, nilInts))), 0, 0, 0) => 1 </k>
  // case 126: [1, 1, 0]
  claim <k> nsScan(consInts(1, consInts(1, consInts(0, nilInts))), 0, 0, 0) => 1 </k>
  // case 127: [1, 1, 1]
  claim <k> nsScan(consInts(1, consInts(1, consInts(1, nilInts))), 0, 0, 0) => noneV </k>
  // case 128: [1, 1, 2]
  claim <k> nsScan(consInts(1, consInts(1, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 129: [1, 2, -2]
  claim <k> nsScan(consInts(1, consInts(2, consInts(-2, nilInts))), 0, 0, 0) => 1 </k>
  // case 130: [1, 2, -1]
  claim <k> nsScan(consInts(1, consInts(2, consInts(-1, nilInts))), 0, 0, 0) => 1 </k>
  // case 131: [1, 2, 0]
  claim <k> nsScan(consInts(1, consInts(2, consInts(0, nilInts))), 0, 0, 0) => 1 </k>
  // case 132: [1, 2, 1]
  claim <k> nsScan(consInts(1, consInts(2, consInts(1, nilInts))), 0, 0, 0) => 2 </k>
  // case 133: [1, 2, 2]
  claim <k> nsScan(consInts(1, consInts(2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 134: [2, -2, -2]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(-2, nilInts))), 0, 0, 0) => 2 </k>
  // case 135: [2, -2, -1]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(-1, nilInts))), 0, 0, 0) => -1 </k>
  // case 136: [2, -2, 0]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 137: [2, -2, 1]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 138: [2, -2, 2]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 139: [2, -1, -2]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 140: [2, -1, -1]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(-1, nilInts))), 0, 0, 0) => 2 </k>
  // case 141: [2, -1, 0]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(0, nilInts))), 0, 0, 0) => 0 </k>
  // case 142: [2, -1, 1]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 143: [2, -1, 2]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 144: [2, 0, -2]
  claim <k> nsScan(consInts(2, consInts(0, consInts(-2, nilInts))), 0, 0, 0) => 0 </k>
  // case 145: [2, 0, -1]
  claim <k> nsScan(consInts(2, consInts(0, consInts(-1, nilInts))), 0, 0, 0) => 0 </k>
  // case 146: [2, 0, 0]
  claim <k> nsScan(consInts(2, consInts(0, consInts(0, nilInts))), 0, 0, 0) => 2 </k>
  // case 147: [2, 0, 1]
  claim <k> nsScan(consInts(2, consInts(0, consInts(1, nilInts))), 0, 0, 0) => 1 </k>
  // case 148: [2, 0, 2]
  claim <k> nsScan(consInts(2, consInts(0, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 149: [2, 1, -2]
  claim <k> nsScan(consInts(2, consInts(1, consInts(-2, nilInts))), 0, 0, 0) => 1 </k>
  // case 150: [2, 1, -1]
  claim <k> nsScan(consInts(2, consInts(1, consInts(-1, nilInts))), 0, 0, 0) => 1 </k>
  // case 151: [2, 1, 0]
  claim <k> nsScan(consInts(2, consInts(1, consInts(0, nilInts))), 0, 0, 0) => 1 </k>
  // case 152: [2, 1, 1]
  claim <k> nsScan(consInts(2, consInts(1, consInts(1, nilInts))), 0, 0, 0) => 2 </k>
  // case 153: [2, 1, 2]
  claim <k> nsScan(consInts(2, consInts(1, consInts(2, nilInts))), 0, 0, 0) => 2 </k>
  // case 154: [2, 2, -2]
  claim <k> nsScan(consInts(2, consInts(2, consInts(-2, nilInts))), 0, 0, 0) => 2 </k>
  // case 155: [2, 2, -1]
  claim <k> nsScan(consInts(2, consInts(2, consInts(-1, nilInts))), 0, 0, 0) => 2 </k>
  // case 156: [2, 2, 0]
  claim <k> nsScan(consInts(2, consInts(2, consInts(0, nilInts))), 0, 0, 0) => 2 </k>
  // case 157: [2, 2, 1]
  claim <k> nsScan(consInts(2, consInts(2, consInts(1, nilInts))), 0, 0, 0) => 2 </k>
  // case 158: [2, 2, 2]
  claim <k> nsScan(consInts(2, consInts(2, consInts(2, nilInts))), 0, 0, 0) => noneV </k>
  // case 159: [17, -2, -4, 10, 19, 2, 9, -9, -17]
  claim <k> nsScan(consInts(17, consInts(-2, consInts(-4, consInts(10, consInts(19, consInts(2, consInts(9, consInts(-9, consInts(-17, nilInts))))))))), 0, 0, 0) => -9 </k>
  // case 160: [-12]
  claim <k> nsScan(consInts(-12, nilInts), 0, 0, 0) => noneV </k>
  // case 161: [15, 13, -19]
  claim <k> nsScan(consInts(15, consInts(13, consInts(-19, nilInts))), 0, 0, 0) => 13 </k>
  // case 162: [14, 15, -2]
  claim <k> nsScan(consInts(14, consInts(15, consInts(-2, nilInts))), 0, 0, 0) => 14 </k>
  // case 163: [-9, 11, 9, 20, -11, -6, 5, 18, 7]
  claim <k> nsScan(consInts(-9, consInts(11, consInts(9, consInts(20, consInts(-11, consInts(-6, consInts(5, consInts(18, consInts(7, nilInts))))))))), 0, 0, 0) => -9 </k>
  // case 164: [13, -6, 14, 11, -9, -4, -7]
  claim <k> nsScan(consInts(13, consInts(-6, consInts(14, consInts(11, consInts(-9, consInts(-4, consInts(-7, nilInts))))))), 0, 0, 0) => -7 </k>
  // case 165: [-18, 4]
  claim <k> nsScan(consInts(-18, consInts(4, nilInts)), 0, 0, 0) => 4 </k>
  // case 166: [16, -15, 2, 9, 5, -18, -13]
  claim <k> nsScan(consInts(16, consInts(-15, consInts(2, consInts(9, consInts(5, consInts(-18, consInts(-13, nilInts))))))), 0, 0, 0) => -15 </k>
  // case 167: [13, -8]
  claim <k> nsScan(consInts(13, consInts(-8, nilInts)), 0, 0, 0) => 13 </k>
  // case 168: [-12, 11, -17, -11, -19, -16]
  claim <k> nsScan(consInts(-12, consInts(11, consInts(-17, consInts(-11, consInts(-19, consInts(-16, nilInts)))))), 0, 0, 0) => -17 </k>
  // case 169: [20, 9, 5, -4, 9, 13, -20, -9, -13, 0]
  claim <k> nsScan(consInts(20, consInts(9, consInts(5, consInts(-4, consInts(9, consInts(13, consInts(-20, consInts(-9, consInts(-13, consInts(0, nilInts)))))))))), 0, 0, 0) => -13 </k>
  // case 170: [16, -8, 8, -2, 5, -16, 7, 17, 16, 11]
  claim <k> nsScan(consInts(16, consInts(-8, consInts(8, consInts(-2, consInts(5, consInts(-16, consInts(7, consInts(17, consInts(16, consInts(11, nilInts)))))))))), 0, 0, 0) => -8 </k>
  // case 171: [-18, -14, -10, -9, 17, 1, 0, 18]
  claim <k> nsScan(consInts(-18, consInts(-14, consInts(-10, consInts(-9, consInts(17, consInts(1, consInts(0, consInts(18, nilInts)))))))), 0, 0, 0) => -14 </k>
  // case 172: [5, -3, -6, 6, -1, -10, 18]
  claim <k> nsScan(consInts(5, consInts(-3, consInts(-6, consInts(6, consInts(-1, consInts(-10, consInts(18, nilInts))))))), 0, 0, 0) => -6 </k>
  // case 173: [18]
  claim <k> nsScan(consInts(18, nilInts), 0, 0, 0) => noneV </k>
  // case 174: [-3, 8, -10, -9, -4, 1, -4, 19]
  claim <k> nsScan(consInts(-3, consInts(8, consInts(-10, consInts(-9, consInts(-4, consInts(1, consInts(-4, consInts(19, nilInts)))))))), 0, 0, 0) => -9 </k>
  // case 175: [20, -7, 6, -4]
  claim <k> nsScan(consInts(20, consInts(-7, consInts(6, consInts(-4, nilInts)))), 0, 0, 0) => -4 </k>
  // case 176: [-4, 12]
  claim <k> nsScan(consInts(-4, consInts(12, nilInts)), 0, 0, 0) => 12 </k>
  // case 177: [18, -7, 6, 14, -16, -19, 14, -2, 8]
  claim <k> nsScan(consInts(18, consInts(-7, consInts(6, consInts(14, consInts(-16, consInts(-19, consInts(14, consInts(-2, consInts(8, nilInts))))))))), 0, 0, 0) => -16 </k>
  // case 178: [-3, 3, -4, 12]
  claim <k> nsScan(consInts(-3, consInts(3, consInts(-4, consInts(12, nilInts)))), 0, 0, 0) => -3 </k>
  // case 179: [-3, -18, -14]
  claim <k> nsScan(consInts(-3, consInts(-18, consInts(-14, nilInts))), 0, 0, 0) => -14 </k>
  // case 180: [-3, -11, -17, -20, 18, -19, 17, 12, -15]
  claim <k> nsScan(consInts(-3, consInts(-11, consInts(-17, consInts(-20, consInts(18, consInts(-19, consInts(17, consInts(12, consInts(-15, nilInts))))))))), 0, 0, 0) => -19 </k>
  // case 181: [-15]
  claim <k> nsScan(consInts(-15, nilInts), 0, 0, 0) => noneV </k>
  // case 182: [17, 8, -18, 0, 17, -16, 13, -18, -11, -6]
  claim <k> nsScan(consInts(17, consInts(8, consInts(-18, consInts(0, consInts(17, consInts(-16, consInts(13, consInts(-18, consInts(-11, consInts(-6, nilInts)))))))))), 0, 0, 0) => -16 </k>
  // case 183: [9, 11, -20]
  claim <k> nsScan(consInts(9, consInts(11, consInts(-20, nilInts))), 0, 0, 0) => 9 </k>
  // case 184: [-13, 16]
  claim <k> nsScan(consInts(-13, consInts(16, nilInts)), 0, 0, 0) => 16 </k>
  // case 185: [-16, 16, -18, -4, -12]
  claim <k> nsScan(consInts(-16, consInts(16, consInts(-18, consInts(-4, consInts(-12, nilInts))))), 0, 0, 0) => -16 </k>
  // case 186: [17, -4, 14, 7]
  claim <k> nsScan(consInts(17, consInts(-4, consInts(14, consInts(7, nilInts)))), 0, 0, 0) => 7 </k>
  // case 187: [11, -20, -16, 15, -4]
  claim <k> nsScan(consInts(11, consInts(-20, consInts(-16, consInts(15, consInts(-4, nilInts))))), 0, 0, 0) => -16 </k>
  // case 188: [-6, 18, -13, 6, 6, 6]
  claim <k> nsScan(consInts(-6, consInts(18, consInts(-13, consInts(6, consInts(6, consInts(6, nilInts)))))), 0, 0, 0) => -6 </k>
  // case 189: [-12, -7]
  claim <k> nsScan(consInts(-12, consInts(-7, nilInts)), 0, 0, 0) => -7 </k>
  // case 190: [20, 1, 19, -8, 18, -3, -4, -15, -12]
  claim <k> nsScan(consInts(20, consInts(1, consInts(19, consInts(-8, consInts(18, consInts(-3, consInts(-4, consInts(-15, consInts(-12, nilInts))))))))), 0, 0, 0) => -12 </k>
  // case 191: [18, -2, -2, -5]
  claim <k> nsScan(consInts(18, consInts(-2, consInts(-2, consInts(-5, nilInts)))), 0, 0, 0) => -2 </k>
  // case 192: [7, 10, -2, -7, -15, -20, 19, -4, 0]
  claim <k> nsScan(consInts(7, consInts(10, consInts(-2, consInts(-7, consInts(-15, consInts(-20, consInts(19, consInts(-4, consInts(0, nilInts))))))))), 0, 0, 0) => -15 </k>
  // case 193: [11, 9, -5, 19, -4, -16]
  claim <k> nsScan(consInts(11, consInts(9, consInts(-5, consInts(19, consInts(-4, consInts(-16, nilInts)))))), 0, 0, 0) => -5 </k>
  // case 194: [5, 16, 2, 20]
  claim <k> nsScan(consInts(5, consInts(16, consInts(2, consInts(20, nilInts)))), 0, 0, 0) => 5 </k>
  // case 195: [18, 20, -16, 11, 10, -15, 9]
  claim <k> nsScan(consInts(18, consInts(20, consInts(-16, consInts(11, consInts(10, consInts(-15, consInts(9, nilInts))))))), 0, 0, 0) => -15 </k>
  // case 196: [-19, -5, -2, 2, -12]
  claim <k> nsScan(consInts(-19, consInts(-5, consInts(-2, consInts(2, consInts(-12, nilInts))))), 0, 0, 0) => -12 </k>
  // case 197: [-13, -16, -8, -2, -17, 7, 14, 7]
  claim <k> nsScan(consInts(-13, consInts(-16, consInts(-8, consInts(-2, consInts(-17, consInts(7, consInts(14, consInts(7, nilInts)))))))), 0, 0, 0) => -16 </k>
  // case 198: [7, 11, 4, 6, -4, 18, 15]
  claim <k> nsScan(consInts(7, consInts(11, consInts(4, consInts(6, consInts(-4, consInts(18, consInts(15, nilInts))))))), 0, 0, 0) => 4 </k>
  // case 199: [8, 7, 18, 13, 6, -10, 1, -19, 4, 12]
  claim <k> nsScan(consInts(8, consInts(7, consInts(18, consInts(13, consInts(6, consInts(-10, consInts(1, consInts(-19, consInts(4, consInts(12, nilInts)))))))))), 0, 0, 0) => -10 </k>
  // case 200: [-15, 4, 19, -13, 8, 13, -2, 3]
  claim <k> nsScan(consInts(-15, consInts(4, consInts(19, consInts(-13, consInts(8, consInts(13, consInts(-2, consInts(3, nilInts)))))))), 0, 0, 0) => -13 </k>
  // case 201: [10, -7, 7, 7, 0, -16]
  claim <k> nsScan(consInts(10, consInts(-7, consInts(7, consInts(7, consInts(0, consInts(-16, nilInts)))))), 0, 0, 0) => -7 </k>
  // case 202: [0, 11, -4, 11, -18, -11, -8, 13, 20, 5]
  claim <k> nsScan(consInts(0, consInts(11, consInts(-4, consInts(11, consInts(-18, consInts(-11, consInts(-8, consInts(13, consInts(20, consInts(5, nilInts)))))))))), 0, 0, 0) => -11 </k>
  // case 203: [7, -11]
  claim <k> nsScan(consInts(7, consInts(-11, nilInts)), 0, 0, 0) => 7 </k>
  // case 204: [-7, 17, -20, 0]
  claim <k> nsScan(consInts(-7, consInts(17, consInts(-20, consInts(0, nilInts)))), 0, 0, 0) => -7 </k>
  // case 205: [14, 10, -8, 7]
  claim <k> nsScan(consInts(14, consInts(10, consInts(-8, consInts(7, nilInts)))), 0, 0, 0) => 7 </k>
  // case 206: [-20, -18, 6]
  claim <k> nsScan(consInts(-20, consInts(-18, consInts(6, nilInts))), 0, 0, 0) => -18 </k>
  // case 207: [-9, -11, -14]
  claim <k> nsScan(consInts(-9, consInts(-11, consInts(-14, nilInts))), 0, 0, 0) => -11 </k>
  // case 208: [-7, -7, 19, 16, -14, -3, 6, 7, -11, -11]
  claim <k> nsScan(consInts(-7, consInts(-7, consInts(19, consInts(16, consInts(-14, consInts(-3, consInts(6, consInts(7, consInts(-11, consInts(-11, nilInts)))))))))), 0, 0, 0) => -11 </k>
  // case 209: [10, 6, -19]
  claim <k> nsScan(consInts(10, consInts(6, consInts(-19, nilInts))), 0, 0, 0) => 6 </k>
  // case 210: [-13, 3]
  claim <k> nsScan(consInts(-13, consInts(3, nilInts)), 0, 0, 0) => 3 </k>
  // case 211: [-10, -17, 18, -3, 1, -10, -7]
  claim <k> nsScan(consInts(-10, consInts(-17, consInts(18, consInts(-3, consInts(1, consInts(-10, consInts(-7, nilInts))))))), 0, 0, 0) => -10 </k>
  // case 212: [2, 11, 9, 9, -17, -10, 5]
  claim <k> nsScan(consInts(2, consInts(11, consInts(9, consInts(9, consInts(-17, consInts(-10, consInts(5, nilInts))))))), 0, 0, 0) => -10 </k>
  // case 213: [17, 2, -3, 0]
  claim <k> nsScan(consInts(17, consInts(2, consInts(-3, consInts(0, nilInts)))), 0, 0, 0) => 0 </k>
  // case 214: [-8, -1, -7]
  claim <k> nsScan(consInts(-8, consInts(-1, consInts(-7, nilInts))), 0, 0, 0) => -7 </k>
  // case 215: [2, 13, 6, -15, -3]
  claim <k> nsScan(consInts(2, consInts(13, consInts(6, consInts(-15, consInts(-3, nilInts))))), 0, 0, 0) => -3 </k>
  // case 216: [-5, 15, 14]
  claim <k> nsScan(consInts(-5, consInts(15, consInts(14, nilInts))), 0, 0, 0) => 14 </k>
  // case 217: [7, -5]
  claim <k> nsScan(consInts(7, consInts(-5, nilInts)), 0, 0, 0) => 7 </k>
  // case 218: [14, 0, 6, -18, -4, -20, 3, 19]
  claim <k> nsScan(consInts(14, consInts(0, consInts(6, consInts(-18, consInts(-4, consInts(-20, consInts(3, consInts(19, nilInts)))))))), 0, 0, 0) => -18 </k>
  // case 219: [-19]
  claim <k> nsScan(consInts(-19, nilInts), 0, 0, 0) => noneV </k>
  // case 220: [14, 18, -7, 10, 1]
  claim <k> nsScan(consInts(14, consInts(18, consInts(-7, consInts(10, consInts(1, nilInts))))), 0, 0, 0) => 1 </k>
  // case 221: [15, -15, -17, 13, -20, -11, -3, 14, -7]
  claim <k> nsScan(consInts(15, consInts(-15, consInts(-17, consInts(13, consInts(-20, consInts(-11, consInts(-3, consInts(14, consInts(-7, nilInts))))))))), 0, 0, 0) => -17 </k>
  // case 222: [2, -16, 9, -6, 18, 13]
  claim <k> nsScan(consInts(2, consInts(-16, consInts(9, consInts(-6, consInts(18, consInts(13, nilInts)))))), 0, 0, 0) => -6 </k>
  // case 223: [12, 2, 12, -20, 17, -20]
  claim <k> nsScan(consInts(12, consInts(2, consInts(12, consInts(-20, consInts(17, consInts(-20, nilInts)))))), 0, 0, 0) => 2 </k>
  // case 224: [7, 16, 0, -6, 2, -9, -6, -15, 19]
  claim <k> nsScan(consInts(7, consInts(16, consInts(0, consInts(-6, consInts(2, consInts(-9, consInts(-6, consInts(-15, consInts(19, nilInts))))))))), 0, 0, 0) => -9 </k>
  // case 225: [-20]
  claim <k> nsScan(consInts(-20, nilInts), 0, 0, 0) => noneV </k>
  // case 226: [3, 1, 8, -18, -11, -7, 0, -17, 14, -10]
  claim <k> nsScan(consInts(3, consInts(1, consInts(8, consInts(-18, consInts(-11, consInts(-7, consInts(0, consInts(-17, consInts(14, consInts(-10, nilInts)))))))))), 0, 0, 0) => -17 </k>
  // case 227: [13, 3, -11, -2, -6, -19, 14, 7]
  claim <k> nsScan(consInts(13, consInts(3, consInts(-11, consInts(-2, consInts(-6, consInts(-19, consInts(14, consInts(7, nilInts)))))))), 0, 0, 0) => -11 </k>
  // case 228: [-11, 3, 14, -20, 6, 19, 11]
  claim <k> nsScan(consInts(-11, consInts(3, consInts(14, consInts(-20, consInts(6, consInts(19, consInts(11, nilInts))))))), 0, 0, 0) => -11 </k>
  // case 229: [-5, 13, -2, -11]
  claim <k> nsScan(consInts(-5, consInts(13, consInts(-2, consInts(-11, nilInts)))), 0, 0, 0) => -5 </k>
  // case 230: [-17, -13]
  claim <k> nsScan(consInts(-17, consInts(-13, nilInts)), 0, 0, 0) => -13 </k>
  // case 231: [16, -3, 18]
  claim <k> nsScan(consInts(16, consInts(-3, consInts(18, nilInts))), 0, 0, 0) => 16 </k>
  // case 232: [-12, 15, -10]
  claim <k> nsScan(consInts(-12, consInts(15, consInts(-10, nilInts))), 0, 0, 0) => -10 </k>
  // case 233: [20, -13, -5, -6, -7, 5]
  claim <k> nsScan(consInts(20, consInts(-13, consInts(-5, consInts(-6, consInts(-7, consInts(5, nilInts)))))), 0, 0, 0) => -7 </k>
  // case 234: [17, -13]
  claim <k> nsScan(consInts(17, consInts(-13, nilInts)), 0, 0, 0) => 17 </k>
  // case 235: [8, -19, 14, -20]
  claim <k> nsScan(consInts(8, consInts(-19, consInts(14, consInts(-20, nilInts)))), 0, 0, 0) => -19 </k>
  // case 236: [18, -7, 7, 17, 19]
  claim <k> nsScan(consInts(18, consInts(-7, consInts(7, consInts(17, consInts(19, nilInts))))), 0, 0, 0) => 7 </k>
  // case 237: [-18, 17, 4, -5, -16]
  claim <k> nsScan(consInts(-18, consInts(17, consInts(4, consInts(-5, consInts(-16, nilInts))))), 0, 0, 0) => -16 </k>
  // case 238: [8, -12, 5, -8, -11, -17, 4, 14, 19, -8]
  claim <k> nsScan(consInts(8, consInts(-12, consInts(5, consInts(-8, consInts(-11, consInts(-17, consInts(4, consInts(14, consInts(19, consInts(-8, nilInts)))))))))), 0, 0, 0) => -12 </k>
  // case 239: [17, -1, -2]
  claim <k> nsScan(consInts(17, consInts(-1, consInts(-2, nilInts))), 0, 0, 0) => -1 </k>
  // case 240: [-12, 12, 7, -15, -8, 1, -5, -14, 19, 10]
  claim <k> nsScan(consInts(-12, consInts(12, consInts(7, consInts(-15, consInts(-8, consInts(1, consInts(-5, consInts(-14, consInts(19, consInts(10, nilInts)))))))))), 0, 0, 0) => -14 </k>
  // case 241: [19, 11, -19, -1, 19, -5, -14, -20]
  claim <k> nsScan(consInts(19, consInts(11, consInts(-19, consInts(-1, consInts(19, consInts(-5, consInts(-14, consInts(-20, nilInts)))))))), 0, 0, 0) => -19 </k>
  // case 242: [19, 0, -3, 10, 8, 4, -17, 8]
  claim <k> nsScan(consInts(19, consInts(0, consInts(-3, consInts(10, consInts(8, consInts(4, consInts(-17, consInts(8, nilInts)))))))), 0, 0, 0) => -3 </k>
  // case 243: [10, -18, -11, 13, 4]
  claim <k> nsScan(consInts(10, consInts(-18, consInts(-11, consInts(13, consInts(4, nilInts))))), 0, 0, 0) => -11 </k>
  // case 244: [1, -18, 11, -16, -17, -8, 13, 12, -9, 4]
  claim <k> nsScan(consInts(1, consInts(-18, consInts(11, consInts(-16, consInts(-17, consInts(-8, consInts(13, consInts(12, consInts(-9, consInts(4, nilInts)))))))))), 0, 0, 0) => -17 </k>
  // case 245: [-3, -5]
  claim <k> nsScan(consInts(-3, consInts(-5, nilInts)), 0, 0, 0) => -3 </k>
  // case 246: [-8, 18, -2, -2, -1, -7, 13, 4]
  claim <k> nsScan(consInts(-8, consInts(18, consInts(-2, consInts(-2, consInts(-1, consInts(-7, consInts(13, consInts(4, nilInts)))))))), 0, 0, 0) => -7 </k>
  // case 247: [-11, -15, 19, -11, -7, 8, -3, -2, 12]
  claim <k> nsScan(consInts(-11, consInts(-15, consInts(19, consInts(-11, consInts(-7, consInts(8, consInts(-3, consInts(-2, consInts(12, nilInts))))))))), 0, 0, 0) => -11 </k>
  // case 248: [4, 3]
  claim <k> nsScan(consInts(4, consInts(3, nilInts)), 0, 0, 0) => 4 </k>
  // case 249: [-5, 8, -16, 2, 11, 4, -9, -20]
  claim <k> nsScan(consInts(-5, consInts(8, consInts(-16, consInts(2, consInts(11, consInts(4, consInts(-9, consInts(-20, nilInts)))))))), 0, 0, 0) => -16 </k>
  // case 250: [15, 13, 14, -4, -15]
  claim <k> nsScan(consInts(15, consInts(13, consInts(14, consInts(-4, consInts(-15, nilInts))))), 0, 0, 0) => -4 </k>
  // case 251: [2, -3, 20, 14, -8, 2, 9, -19, 16]
  claim <k> nsScan(consInts(2, consInts(-3, consInts(20, consInts(14, consInts(-8, consInts(2, consInts(9, consInts(-19, consInts(16, nilInts))))))))), 0, 0, 0) => -8 </k>
  // case 252: [13, -17, 6, -2, 2, -10, -3]
  claim <k> nsScan(consInts(13, consInts(-17, consInts(6, consInts(-2, consInts(2, consInts(-10, consInts(-3, nilInts))))))), 0, 0, 0) => -10 </k>
  // case 253: [5, 9, 7, -7, 0]
  claim <k> nsScan(consInts(5, consInts(9, consInts(7, consInts(-7, consInts(0, nilInts))))), 0, 0, 0) => 0 </k>
  // case 254: [-5, -14, -20, -15, -8, -10, 19, -14, -10]
  claim <k> nsScan(consInts(-5, consInts(-14, consInts(-20, consInts(-15, consInts(-8, consInts(-10, consInts(19, consInts(-14, consInts(-10, nilInts))))))))), 0, 0, 0) => -15 </k>
  // case 255: [-9, 12]
  claim <k> nsScan(consInts(-9, consInts(12, nilInts)), 0, 0, 0) => 12 </k>
  // case 256: [-2, -16, 18, 17]
  claim <k> nsScan(consInts(-2, consInts(-16, consInts(18, consInts(17, nilInts)))), 0, 0, 0) => -2 </k>
  // case 257: [10, -10, 15, 12]
  claim <k> nsScan(consInts(10, consInts(-10, consInts(15, consInts(12, nilInts)))), 0, 0, 0) => 10 </k>
  // case 258: [-16, -12]
  claim <k> nsScan(consInts(-16, consInts(-12, nilInts)), 0, 0, 0) => -12 </k>
  // case 259: [18, 1, -18, 5]
  claim <k> nsScan(consInts(18, consInts(1, consInts(-18, consInts(5, nilInts)))), 0, 0, 0) => 1 </k>
  // case 260: [-14, 6, 5, 16, -15, 15, -16, -8]
  claim <k> nsScan(consInts(-14, consInts(6, consInts(5, consInts(16, consInts(-15, consInts(15, consInts(-16, consInts(-8, nilInts)))))))), 0, 0, 0) => -15 </k>
  // case 261: [20, 8, -12, 12, -19, -1, 16, 18, -19]
  claim <k> nsScan(consInts(20, consInts(8, consInts(-12, consInts(12, consInts(-19, consInts(-1, consInts(16, consInts(18, consInts(-19, nilInts))))))))), 0, 0, 0) => -12 </k>
  // case 262: [2, 16, 1, -10, 7, 8]
  claim <k> nsScan(consInts(2, consInts(16, consInts(1, consInts(-10, consInts(7, consInts(8, nilInts)))))), 0, 0, 0) => 1 </k>
  // case 263: [-14, 13, -19]
  claim <k> nsScan(consInts(-14, consInts(13, consInts(-19, nilInts))), 0, 0, 0) => -14 </k>
  // case 264: [15, 16]
  claim <k> nsScan(consInts(15, consInts(16, nilInts)), 0, 0, 0) => 16 </k>
  // case 265: [-17, -15, 18, -15, 16, 20]
  claim <k> nsScan(consInts(-17, consInts(-15, consInts(18, consInts(-15, consInts(16, consInts(20, nilInts)))))), 0, 0, 0) => -15 </k>
  // case 266: [3, -10, -3, 19, -20]
  claim <k> nsScan(consInts(3, consInts(-10, consInts(-3, consInts(19, consInts(-20, nilInts))))), 0, 0, 0) => -10 </k>
  // case 267: [15, 11, 14, -5, -18, -1, -9]
  claim <k> nsScan(consInts(15, consInts(11, consInts(14, consInts(-5, consInts(-18, consInts(-1, consInts(-9, nilInts))))))), 0, 0, 0) => -9 </k>
  // case 268: [2, -1, -8, 3, 6, 20, 9, -3]
  claim <k> nsScan(consInts(2, consInts(-1, consInts(-8, consInts(3, consInts(6, consInts(20, consInts(9, consInts(-3, nilInts)))))))), 0, 0, 0) => -3 </k>
  // case 269: [-19, 0]
  claim <k> nsScan(consInts(-19, consInts(0, nilInts)), 0, 0, 0) => 0 </k>
  // case 270: [-3, 15, -12]
  claim <k> nsScan(consInts(-3, consInts(15, consInts(-12, nilInts))), 0, 0, 0) => -3 </k>
  // case 271: [-11, -8, -11]
  claim <k> nsScan(consInts(-11, consInts(-8, consInts(-11, nilInts))), 0, 0, 0) => -8 </k>
  // case 272: [-12, -1, 3, 19, 0, -13, -2, 11, -11]
  claim <k> nsScan(consInts(-12, consInts(-1, consInts(3, consInts(19, consInts(0, consInts(-13, consInts(-2, consInts(11, consInts(-11, nilInts))))))))), 0, 0, 0) => -12 </k>
  // case 273: [-19, -10, 4, -8, -12, -2, 13]
  claim <k> nsScan(consInts(-19, consInts(-10, consInts(4, consInts(-8, consInts(-12, consInts(-2, consInts(13, nilInts))))))), 0, 0, 0) => -12 </k>
  // case 274: [6, -16, -7, -10]
  claim <k> nsScan(consInts(6, consInts(-16, consInts(-7, consInts(-10, nilInts)))), 0, 0, 0) => -10 </k>
  // case 275: [4]
  claim <k> nsScan(consInts(4, nilInts), 0, 0, 0) => noneV </k>
  // case 276: [3, 18]
  claim <k> nsScan(consInts(3, consInts(18, nilInts)), 0, 0, 0) => 18 </k>
  // case 277: [-1, 15, -12, 9, -6, -13, -1, -11]
  claim <k> nsScan(consInts(-1, consInts(15, consInts(-12, consInts(9, consInts(-6, consInts(-13, consInts(-1, consInts(-11, nilInts)))))))), 0, 0, 0) => -12 </k>
  // case 278: [-11]
  claim <k> nsScan(consInts(-11, nilInts), 0, 0, 0) => noneV </k>
  // case 279: [9, 9, -10, -20, 15, -7]
  claim <k> nsScan(consInts(9, consInts(9, consInts(-10, consInts(-20, consInts(15, consInts(-7, nilInts)))))), 0, 0, 0) => -10 </k>
  // case 280: [17, -7, 13, 2, 12, 10, 11]
  claim <k> nsScan(consInts(17, consInts(-7, consInts(13, consInts(2, consInts(12, consInts(10, consInts(11, nilInts))))))), 0, 0, 0) => 2 </k>
  // case 281: [19]
  claim <k> nsScan(consInts(19, nilInts), 0, 0, 0) => noneV </k>
  // case 282: [-15, 1, 7]
  claim <k> nsScan(consInts(-15, consInts(1, consInts(7, nilInts))), 0, 0, 0) => 1 </k>
  // case 283: [-11, -4, 2]
  claim <k> nsScan(consInts(-11, consInts(-4, consInts(2, nilInts))), 0, 0, 0) => -4 </k>
  // case 284: [-7, -8, -2, 1, -18, -15, 17, 18]
  claim <k> nsScan(consInts(-7, consInts(-8, consInts(-2, consInts(1, consInts(-18, consInts(-15, consInts(17, consInts(18, nilInts)))))))), 0, 0, 0) => -15 </k>
  // case 285: [17]
  claim <k> nsScan(consInts(17, nilInts), 0, 0, 0) => noneV </k>
  // case 286: [-6, -17, -13, -4, -16, -14, 16, 14, -5]
  claim <k> nsScan(consInts(-6, consInts(-17, consInts(-13, consInts(-4, consInts(-16, consInts(-14, consInts(16, consInts(14, consInts(-5, nilInts))))))))), 0, 0, 0) => -16 </k>
  // case 287: [12, 1, 4, -16, -11, -4, 18, 8, 2]
  claim <k> nsScan(consInts(12, consInts(1, consInts(4, consInts(-16, consInts(-11, consInts(-4, consInts(18, consInts(8, consInts(2, nilInts))))))))), 0, 0, 0) => -11 </k>
  // case 288: [6, -16, -15, 19, 6, 20]
  claim <k> nsScan(consInts(6, consInts(-16, consInts(-15, consInts(19, consInts(6, consInts(20, nilInts)))))), 0, 0, 0) => -15 </k>
  // case 289: [-17, 8, 17, -7, 15, 14, 9, -10, -13, 8]
  claim <k> nsScan(consInts(-17, consInts(8, consInts(17, consInts(-7, consInts(15, consInts(14, consInts(9, consInts(-10, consInts(-13, consInts(8, nilInts)))))))))), 0, 0, 0) => -13 </k>
  // case 290: [-13, -10, 10, 17, -8, 3, 17, -12, -17, 10]
  claim <k> nsScan(consInts(-13, consInts(-10, consInts(10, consInts(17, consInts(-8, consInts(3, consInts(17, consInts(-12, consInts(-17, consInts(10, nilInts)))))))))), 0, 0, 0) => -13 </k>
  // case 291: [8, 14, 18, -1, -11]
  claim <k> nsScan(consInts(8, consInts(14, consInts(18, consInts(-1, consInts(-11, nilInts))))), 0, 0, 0) => -1 </k>
  // case 292: [19, 2]
  claim <k> nsScan(consInts(19, consInts(2, nilInts)), 0, 0, 0) => 19 </k>
  // case 293: [5, -16, 5, 6]
  claim <k> nsScan(consInts(5, consInts(-16, consInts(5, consInts(6, nilInts)))), 0, 0, 0) => 5 </k>
  // case 294: [3, 7, -4]
  claim <k> nsScan(consInts(3, consInts(7, consInts(-4, nilInts))), 0, 0, 0) => 3 </k>
  // case 295: [-4, 16, 1, 18, 13, 5, -19, 15, -8]
  claim <k> nsScan(consInts(-4, consInts(16, consInts(1, consInts(18, consInts(13, consInts(5, consInts(-19, consInts(15, consInts(-8, nilInts))))))))), 0, 0, 0) => -8 </k>
  // case 296: [-13, -16]
  claim <k> nsScan(consInts(-13, consInts(-16, nilInts)), 0, 0, 0) => -13 </k>
  // case 297: [-16, -4, 19, -3, -7, -15, 2, -5]
  claim <k> nsScan(consInts(-16, consInts(-4, consInts(19, consInts(-3, consInts(-7, consInts(-15, consInts(2, consInts(-5, nilInts)))))))), 0, 0, 0) => -15 </k>
  // case 298: [16, 4, 12, 6, -11, -20, 17]
  claim <k> nsScan(consInts(16, consInts(4, consInts(12, consInts(6, consInts(-11, consInts(-20, consInts(17, nilInts))))))), 0, 0, 0) => -11 </k>
  // case 299: [7, -14, -13]
  claim <k> nsScan(consInts(7, consInts(-14, consInts(-13, nilInts))), 0, 0, 0) => -13 </k>
  // case 300: [-14]
  claim <k> nsScan(consInts(-14, nilInts), 0, 0, 0) => noneV </k>
  // case 301: [5]
  claim <k> nsScan(consInts(5, nilInts), 0, 0, 0) => noneV </k>
  // case 302: [-15, -12, 8, -16, 0, 19, -7, 10, 1, -5]
  claim <k> nsScan(consInts(-15, consInts(-12, consInts(8, consInts(-16, consInts(0, consInts(19, consInts(-7, consInts(10, consInts(1, consInts(-5, nilInts)))))))))), 0, 0, 0) => -15 </k>
  // case 303: [10, 15, -12, 5, -10, 19]
  claim <k> nsScan(consInts(10, consInts(15, consInts(-12, consInts(5, consInts(-10, consInts(19, nilInts)))))), 0, 0, 0) => -10 </k>
  // case 304: [5, 8, 2, -17, 11, 16, -18, 14, 4, 3]
  claim <k> nsScan(consInts(5, consInts(8, consInts(2, consInts(-17, consInts(11, consInts(16, consInts(-18, consInts(14, consInts(4, consInts(3, nilInts)))))))))), 0, 0, 0) => -17 </k>
  // case 305: [9, -19, 18, 3, -16]
  claim <k> nsScan(consInts(9, consInts(-19, consInts(18, consInts(3, consInts(-16, nilInts))))), 0, 0, 0) => -16 </k>
  // case 306: [-11, -10]
  claim <k> nsScan(consInts(-11, consInts(-10, nilInts)), 0, 0, 0) => -10 </k>
  // case 307: [-6, 15, 1, -16, -15, 9, 19]
  claim <k> nsScan(consInts(-6, consInts(15, consInts(1, consInts(-16, consInts(-15, consInts(9, consInts(19, nilInts))))))), 0, 0, 0) => -15 </k>
  // case 308: [3, -5, 14, 8, 10, -18]
  claim <k> nsScan(consInts(3, consInts(-5, consInts(14, consInts(8, consInts(10, consInts(-18, nilInts)))))), 0, 0, 0) => -5 </k>
  // case 309: [-7, 20, 4, 4]
  claim <k> nsScan(consInts(-7, consInts(20, consInts(4, consInts(4, nilInts)))), 0, 0, 0) => 4 </k>
  // case 310: [-2, 13, 10, -9]
  claim <k> nsScan(consInts(-2, consInts(13, consInts(10, consInts(-9, nilInts)))), 0, 0, 0) => -2 </k>
  // case 311: [-7, -4, -16, 0, -11, 11, -1, -12, -16, 0]
  claim <k> nsScan(consInts(-7, consInts(-4, consInts(-16, consInts(0, consInts(-11, consInts(11, consInts(-1, consInts(-12, consInts(-16, consInts(0, nilInts)))))))))), 0, 0, 0) => -12 </k>
  // case 312: [11, 4, 12, -17, 8, -7, 5, 15, 13]
  claim <k> nsScan(consInts(11, consInts(4, consInts(12, consInts(-17, consInts(8, consInts(-7, consInts(5, consInts(15, consInts(13, nilInts))))))))), 0, 0, 0) => -7 </k>
  // case 313: [-8, 5, 11, -3, 4]
  claim <k> nsScan(consInts(-8, consInts(5, consInts(11, consInts(-3, consInts(4, nilInts))))), 0, 0, 0) => -3 </k>
  // case 314: [1, 13, -17, 20]
  claim <k> nsScan(consInts(1, consInts(13, consInts(-17, consInts(20, nilInts)))), 0, 0, 0) => 1 </k>
  // case 315: [15, 14, -15, 8, 20]
  claim <k> nsScan(consInts(15, consInts(14, consInts(-15, consInts(8, consInts(20, nilInts))))), 0, 0, 0) => 8 </k>
  // case 316: [14, 9, 0, -2, 16, 8, -8, 19, 1, 7]
  claim <k> nsScan(consInts(14, consInts(9, consInts(0, consInts(-2, consInts(16, consInts(8, consInts(-8, consInts(19, consInts(1, consInts(7, nilInts)))))))))), 0, 0, 0) => -2 </k>
  // case 317: [-5, -12, -18]
  claim <k> nsScan(consInts(-5, consInts(-12, consInts(-18, nilInts))), 0, 0, 0) => -12 </k>
  // case 318: [0, 13]
  claim <k> nsScan(consInts(0, consInts(13, nilInts)), 0, 0, 0) => 13 </k>
  // case 319: [16]
  claim <k> nsScan(consInts(16, nilInts), 0, 0, 0) => noneV </k>
  // case 320: [-6, 19, -5]
  claim <k> nsScan(consInts(-6, consInts(19, consInts(-5, nilInts))), 0, 0, 0) => -5 </k>
  // case 321: [7, 4, -4, 9]
  claim <k> nsScan(consInts(7, consInts(4, consInts(-4, consInts(9, nilInts)))), 0, 0, 0) => 4 </k>
  // case 322: [4, 17, -18, 14, 13, -3, 13, -17, -14]
  claim <k> nsScan(consInts(4, consInts(17, consInts(-18, consInts(14, consInts(13, consInts(-3, consInts(13, consInts(-17, consInts(-14, nilInts))))))))), 0, 0, 0) => -17 </k>
  // case 323: [0, -12, -17, -3, 16, -8]
  claim <k> nsScan(consInts(0, consInts(-12, consInts(-17, consInts(-3, consInts(16, consInts(-8, nilInts)))))), 0, 0, 0) => -12 </k>
  // case 324: [-16, -5, 10, 10, 10, -4, -20, 7, 6]
  claim <k> nsScan(consInts(-16, consInts(-5, consInts(10, consInts(10, consInts(10, consInts(-4, consInts(-20, consInts(7, consInts(6, nilInts))))))))), 0, 0, 0) => -16 </k>
  // case 325: [9, -9, 11, 0, -8, -2, 14, -13, -10, 9]
  claim <k> nsScan(consInts(9, consInts(-9, consInts(11, consInts(0, consInts(-8, consInts(-2, consInts(14, consInts(-13, consInts(-10, consInts(9, nilInts)))))))))), 0, 0, 0) => -10 </k>
  // case 326: [-3, 4]
  claim <k> nsScan(consInts(-3, consInts(4, nilInts)), 0, 0, 0) => 4 </k>
  // case 327: [-3, 1, -15, -11]
  claim <k> nsScan(consInts(-3, consInts(1, consInts(-15, consInts(-11, nilInts)))), 0, 0, 0) => -11 </k>
  // case 328: [7]
  claim <k> nsScan(consInts(7, nilInts), 0, 0, 0) => noneV </k>
  // case 329: [2, -2, -16, 14]
  claim <k> nsScan(consInts(2, consInts(-2, consInts(-16, consInts(14, nilInts)))), 0, 0, 0) => -2 </k>
  // case 330: [-1, 4, -19, -7, -17, -19]
  claim <k> nsScan(consInts(-1, consInts(4, consInts(-19, consInts(-7, consInts(-17, consInts(-19, nilInts)))))), 0, 0, 0) => -17 </k>
  // case 331: [8, 8, -20, 8]
  claim <k> nsScan(consInts(8, consInts(8, consInts(-20, consInts(8, nilInts)))), 0, 0, 0) => 8 </k>
  // case 332: [10, 3, 17]
  claim <k> nsScan(consInts(10, consInts(3, consInts(17, nilInts))), 0, 0, 0) => 10 </k>
  // case 333: [-13, 10, -10]
  claim <k> nsScan(consInts(-13, consInts(10, consInts(-10, nilInts))), 0, 0, 0) => -10 </k>
  // case 334: [19, -13, 17, -17, 13, -5, -8]
  claim <k> nsScan(consInts(19, consInts(-13, consInts(17, consInts(-17, consInts(13, consInts(-5, consInts(-8, nilInts))))))), 0, 0, 0) => -13 </k>
  // case 335: [-2, 3, 1, -14]
  claim <k> nsScan(consInts(-2, consInts(3, consInts(1, consInts(-14, nilInts)))), 0, 0, 0) => -2 </k>
  // case 336: [-19, -10, -5, -4, -15, -5]
  claim <k> nsScan(consInts(-19, consInts(-10, consInts(-5, consInts(-4, consInts(-15, consInts(-5, nilInts)))))), 0, 0, 0) => -15 </k>
  // case 337: [-5, 0, -14]
  claim <k> nsScan(consInts(-5, consInts(0, consInts(-14, nilInts))), 0, 0, 0) => -5 </k>
  // case 338: [13, -4, 8]
  claim <k> nsScan(consInts(13, consInts(-4, consInts(8, nilInts))), 0, 0, 0) => 8 </k>
  // case 339: [19, -8, 7, 4, -13, 7, 20]
  claim <k> nsScan(consInts(19, consInts(-8, consInts(7, consInts(4, consInts(-13, consInts(7, consInts(20, nilInts))))))), 0, 0, 0) => -8 </k>
  // case 340: [-5, -14, -15, 2, -3, 5, 2, -18, -19]
  claim <k> nsScan(consInts(-5, consInts(-14, consInts(-15, consInts(2, consInts(-3, consInts(5, consInts(2, consInts(-18, consInts(-19, nilInts))))))))), 0, 0, 0) => -18 </k>
endmodule
