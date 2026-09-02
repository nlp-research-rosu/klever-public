# Independent rule-by-rule classification

Frozen source: `/reference/k-proof/verification.k`  
Verification-module closure: `VERIFICATION` only; `MPY` is an imported external semantics module.  
Inventory order is source order. The full source text, spans, normalized hashes, and complete source-rule IDs are in `reconstructed-inventory.json` and are cross-checked in `inventory-bijection.log`.

| # | Lines | Source-rule ID | Independent class | Source role |
|---:|---:|---|---|---|
| 1 | 9–16 | `rule-dd2fa97c98ff9da568d754c34bf8ae33fa6e3cbd8f9981aaa4bd7b6f529748c9` | DEFINITION | Exact macro expansion of `primeLoopBody`. |
| 2 | 19–35 | `rule-00b808d699e2afd3554db8e520d3ff061fc0668e2ac28206c5d877b11692e1cf` | DEFINITION | Exact macro expansion of `scanBody`. |
| 3 | 38–43 | `rule-59e9ea7317fadd4103ee90f8e6dc3bcb686098eeca881f43b8412ba64af29bbb` | DEFINITION | Exact macro expansion of `digitLoopBody`. |
| 4 | 46–56 | `rule-c3aa454c3b2e79181e07066aa69428eb616e31841e6d1b1dbcd7500c98c47ec0` | DEFINITION | Exact macro expansion of `targetBody`. |
| 5 | 61 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | DEFINITION | `allInts` empty-sequence base equation. |
| 6 | 62–63 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | DEFINITION | `allInts` structural recurrence. |
| 7 | 69 | `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | DEFINITION | Names projection definedness as `isInt`. |
| 8 | 74–76 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | DOMAIN_LEMMA | Relates cast definedness to the named predicate; not an execution rule or definition. |
| 9 | 78–80 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | DEFINITION | Primary guarded definition of `projectIntTotal`. |
| 10 | 82–84 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | DOMAIN_LEMMA | Reverse cast/projection bridge; a proof shortcut, not the primary definition. |
| 11 | 86 | `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | DEFINITION | Defining total-projection equation on an already-`Int` argument. |
| 12 | 87–89 | `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | DOMAIN_LEMMA | Idempotence shortcut derived from projection behavior. |
| 13 | 93–96 | `rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388` | DOMAIN_LEMMA | Specialized `applyCmp(">", Val, Int)` bridge. |
| 14 | 98–101 | `rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4` | DOMAIN_LEMMA | Specialized `applyCmp(">=", Val, Int)` bridge. |
| 15 | 103–106 | `rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914` | DOMAIN_LEMMA | Specialized `applyCmp("<", Int, Val)` bridge. |
| 16 | 108–111 | `rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a` | DOMAIN_LEMMA | Specialized `applyBin("%", Val, Int)` bridge. |
| 17 | 113–116 | `rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17` | DOMAIN_LEMMA | Specialized `applyBin("+", Val, Int)` bridge. |
| 18 | 120–121 | `rule-5b7a5a8c5b0b79a6600e5b1b37b21ae8e59cec0ce6ee325e42e7a003c7f5daf8` | DEFINITION | `primeTail` below-domain totalization base. |
| 19 | 122–123 | `rule-3b4a82170fbb388f70f21429e9e956f7d8c4231d7121b0e27f6a1b6e26cfc516` | DEFINITION | `primeTail` completed-scan base. |
| 20 | 124–128 | `rule-3ad3aef28971f515ab5c54a242a54cdcbc03015ea80193db44180cc6343d6771` | DEFINITION | Primary recursive equation for `primeTail`. |
| 21 | 133–137 | `rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91` | DOMAIN_LEMMA | Composite-divisor shortcut for `primeTail`. |
| 22 | 138–142 | `rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06` | DOMAIN_LEMMA | Backward fold for a nondividing previous divisor. |
| 23 | 145–146 | `rule-b78034ba7ab37f18f036d0065448793a9f65296528de6c94cf5fba8d1429c49f` | DEFINITION | Defines `isPrime` using `primeTail`. |
| 24 | 150–151 | `rule-1ad2316fc814518c5a86ddb9fbf319f68759e53eb36a6307e8dd9ae7039273bb` | DEFINITION | Positive branch of `selectPrime`. |
| 25 | 152–153 | `rule-1b6accb44e5d650ab2552e7418f4631911cc8a8e678ea20e8aee8dac4e259a1c` | DEFINITION | Complementary branch of `selectPrime`. |
| 26 | 157 | `rule-feeddd7ff495f24faf2e8867b16f2910b8042350fc678c951adb88f78fd3cc96` | DEFINITION | `largestPrime` empty-sequence base. |
| 27 | 158–160 | `rule-332a226482b34269d8ccea1f7423a3c2c69d40fbee021d7d672651026f29f285` | DEFINITION | `largestPrime` recurrence for an integer head. |
| 28 | 161–163 | `rule-1a849add29cec4756d9e847581eb3bc1b116644d4645c819706e9980e3e70311` | DEFINITION | Totalization recurrence for a noninteger head. |
| 29 | 167–168 | `rule-becef0c1813d6c021707da54654b7ef1b73b1b17fc894cb9b58f5802e83c6a9f` | DEFINITION | `digitSum` nonpositive base. |
| 30 | 169–173 | `rule-9807cef137ed9b921a5c7bc80b8297fa4156ae8a68b99973b8a0122a7d4497e4` | DEFINITION | Primary decimal recurrence for `digitSum`. |
| 31 | 174–178 | `rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51` | DOMAIN_LEMMA | Reverse fold from digit recurrence to `digitSum`. |
| 32 | 179–184 | `rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a` | DOMAIN_LEMMA | Same fold after expanding Python modulo normalization. |
| 33 | 185–191 | `rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231` | DOMAIN_LEMMA | Accumulator form of the normalized digit fold. |

Independent totals: 20 `DEFINITION`, 13 `DOMAIN_LEMMA`, 0 `OPERATIONAL_RULE`, and 0 `PROVED_DERIVED_LEMMA`. Every `[simplification]` or `[simplification(...)]` rule falls in `DEFINITION` or `DOMAIN_LEMMA`. None of the 13 domain lemmas was first proved as the exact same rule in an earlier Stage 1 proof against a module omitting it, so none qualifies as `PROVED_DERIVED_LEMMA`.

Relevance judgment: the cast/projection and dynamic-dispatch bridges are required by the `Val`-typed list scan; the two `primeTail` folds summarize the divisor loop; and the three `digitSum` folds summarize the decimal loop. All connect directly to the translated source body and the postcondition `digitSum(largestPrime(VS, 0))`; none is extraneous.
