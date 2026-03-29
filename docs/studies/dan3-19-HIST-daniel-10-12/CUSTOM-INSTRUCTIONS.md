# Custom Instructions for Dan3 Series

## Reference Boundaries

In `03-analysis.md` and `CONCLUSION.md`, you may cite:
- **Scripture** — the sole doctrinal authority
- **dan3-XX studies** — this series builds on itself
- **Companion series** — formal study series with their own methodology and evidence DBs:
  - `hist-XX` (historicism, 19 studies)
  - `rev-XX` (Revelation, 26+ studies)
  - `revs-XX` (Revelation structure, 47 studies)
  - `sanc-XX` (sanctuary, 30 studies)
  - `law-XX` (law, 33 studies)
  - `cmd-XX` (commandments, 17 studies)
  - `etc6-XX` (eschatology, 27 studies)
  - `pvj-XX` (parables/vineyard/judgment, 22 studies)
- **Series documents** (plan, methodology, HIST arguments doc)

You may NOT cite in analysis/conclusion:
- **Standalone studies** (daniel-XX, dan10-XX, michael-the-archangel, rome-XX,
  2-thessalonians-2-man-of-sin, nt-ties-XX, time-times-XX, abomination-XX, etc.)
- **External corpora** (EGW, Bohr/Secrets Unsealed)

Standalone studies and external corpora inform phases 1-3 (reference, scoping, research)
only. The research agent gathers the biblical data those sources pointed to.

## Series Identity
- Series prefix: `dan3`
- Evidence DB series tag: `dan3`

## Phase 2.5: Position Prompt Review
After the scoping agent writes PROMPT.md but BEFORE the research agent runs, launch a **prompt reviewer** for each relevant position. The reviewer checks whether PROMPT.md covers the arguments the position DB expects for this chapter, and appends any missing research directives.

### HIST Prompt Review (port 9882)

Launch a subagent that:
1. Reads `D:/bible/tools/hist-position/DB-SUMMARY.md` to understand what the HIST position argues for this chapter
2. Reads `D:\Bible\bible-studies\dan3-19-HIST-daniel-10-12/PROMPT.md`
3. Searches the HIST position DB (port 9882) for arguments relevant to this study's chapter:
   ```bash
   cd "D:\bible\tools\hist-position\search" && python search_client.py "QUERY" --top 20
   ```
4. For each HIST argument NOT already covered by PROMPT.md's verse lists, focus areas, or research directives:
   - Append a research directive to PROMPT.md telling the research agent to gather the needed data
   - Include specific verses to retrieve, Strong's numbers to look up, or parsers to run
5. Append directives to the end of PROMPT.md under a new section:
   `## Additional Research Directives (HIST Position Review)`
   Do NOT rewrite or remove existing content — only append.

---

## Phase 5: Position Validation (Validate → Update → Re-validate)

**CRITICAL RULE:** Validators must check the study against what the **position database says**, NOT against the validator's own theological training knowledge. If the DB says the HIST position is X, and the study attributes Y to HIST, that is a misrepresentation even if the validator's training knowledge thinks Y is defensible. The DB is the authority on what each position holds.

### Three-step process:
1. **Phase 5a — First Validation**: Run all position validators. Each writes a validation report.
2. **Phase 5b — Targeted Update** (if issues found): Read ALL validation reports, then make ONE targeted update pass on `03-analysis.md` and `CONCLUSION.md` to fix the identified issues. Do NOT rewrite from scratch — make surgical edits to fix specific problems. Do NOT change content that validators approved.
3. **Phase 5c — Re-validation**: Run all position validators AGAIN on the updated files. Any issues that STILL remain after the update go to the gap ledger. Issues that were fixed are noted as resolved in the re-validation report.

If Phase 5a finds zero issues, skip 5b and 5c entirely.

**PERSPECTIVE/STEELMAN validation focus — TWO LAYERS:**

**Layer 1 — Accurate Representation:** Check whether the study accurately and completely represents the position's arguments per the position DB. (Same as before.)

**Layer 2 — Biblical/Historical Grounding:** After confirming the arguments are accurately presented, evaluate whether each major claim is actually biblically and/or historically founded:

For each specification match or major argument the study presents:
- **Biblical grounding:** Does the cited verse actually support the claimed match, or does the study assert a match without demonstrating textual correspondence? Are there verses that contradict the claimed match that the study ignores?
- **Historical grounding:** Are historical claims (events, dates, identifications) supported by documented historical evidence, or are they asserted without sourcing? Are there historical facts that contradict the claim?
- **Linguistic grounding:** Are linguistic arguments (word meanings, stem functions, cognate evidence) supported by lexical sources, or are they overstated beyond what the evidence shows?

The validator should flag:
- **MISCLASSIFIED**: A claim classified at the wrong E/N/I tier (e.g., an I-A(2) LOW claim classified as N-tier, or an I-B item classified as I-A because competing evidence was ignored)
- **UNGROUNDED**: A claim presented as established that lacks biblical or historical support
- **MISSING COUNTER-EVIDENCE**: Biblical or historical evidence against a claim that the study ignores, which would change the classification (e.g., turn I-A into I-B)
- **UNVERIFIED HISTORICAL CLAIM**: A historical assertion graded E-HIS that should be I-HIS, or one made without any cited source at all
- **CHAIN DEPTH ERROR**: An I-A item with incorrect chain-depth notation (e.g., marked I-A(1) when it actually depends on two prior inferences, making it I-A(3))

Layer 2 issues should be listed separately from Layer 1 issues in the validation report.

### HIST Validation (port 9882)

Launch a subagent that:
1. Reads `D:/bible/tools/hist-position/DB-SUMMARY.md` to understand the HIST position
2. Reads `D:\Bible\bible-studies\dan3-19-HIST-daniel-10-12/CONCLUSION.md` and `D:\Bible\bible-studies\dan3-19-HIST-daniel-10-12/03-analysis.md`
3. Searches the HIST position DB (port 9882):
   ```bash
   cd "D:\bible\tools\hist-position\search" && python search_client.py "QUERY" --top 15
   ```
4. **Layer 1 — Accurate Representation.** For each argument in the DB relevant to this study's chapter:
   - Is it PRESENT in the study? (adequately covered)
   - Is it MISSING? (not mentioned at all)
   - Is it MISREPRESENTED? (mentioned but incorrectly or weakly)
5. **Layer 2 — Biblical/Historical Grounding.** For each major claim in the study's Claim Verification table and analysis:
   a. **Specification-match classification:** Is each match classified at the right E/N/I tier? Does the cited verse actually say what the study claims (E), or is the study asserting an identification the text doesn't make (I-A)? Is there competing evidence that would make it I-B instead of I-A? Retrieve the verse text if needed to verify.
   b. **Chain depth accuracy:** If a match is classified I-A(1), verify it really is one step from E/N. If it depends on a prior inference (e.g., fourth beast = Rome is itself I-A, and horn arises from fourth beast, so horn = papal Rome is I-A(2) not I-A(1)), flag the error.
   c. **Historical claims:** Are E-HIS claims really documented by primary sources? Are I-HIS claims acknowledged as inferred? If the study says 'Antiochus banned Sabbath observance' or 'the papacy changed the calendar' or 'ten barbarian kingdoms divided Rome,' is historical documentation cited? Flag UNVERIFIED HISTORICAL CLAIM if not.
   d. **Linguistic claims:** Are E-LEX claims really supported by BDB/HALOT? Is a hapax classified as E-LEX when it should be I-LEX (meaning inferred from cognates)? Is a stem function being treated as settled when grammarians disagree?
   e. **Missing counter-evidence:** Are there biblical verses or historical facts that directly challenge a claim, which would change its classification (e.g., turn I-A into I-B) but are not mentioned?
   f. **Confidence accuracy:** Does the confidence rating (HIGH/MED/LOW) match the methodology's criteria (convergence of E/N support, chain depth, competing evidence)?
6. Writes `D:\Bible\bible-studies\dan3-19-HIST-daniel-10-12/hist-validation.md` with findings
   - Include a summary line: `LAYER 1 ISSUES: X` (count of representation problems)
   - Include a summary line: `LAYER 2 ISSUES: Y` (count of grounding problems)
   - For each issue, specify the exact section, the nature of the problem, and what needs to change

### Phase 5b: Targeted Update

If ANY validator found issues (LAYER 1 or LAYER 2 ISSUES > 0), perform ONE update pass:
1. Read ALL `*-validation.md` files in the study folder
2. For each Layer 1 issue:
   - If MISREPRESENTED: Fix the specific claim to match what the position DB says
   - If MISSING: Add the missing argument in the appropriate section
   - If STRAWMANNED: Strengthen the presentation to match the DB's actual argument
   - If WEAKNESS EXAGGERATED: Adjust the language to be fair
3. For each Layer 2 issue:
   - If MISCLASSIFIED: Correct the E/N/I tier and confidence to match the evidence
   - If UNGROUNDED: Add the missing biblical/historical evidence, or reclassify to a lower tier
   - If MISSING COUNTER-EVIDENCE: Add to Tensions/Counter-evidence column; if it creates
     competing E/N evidence, reclassify from I-A to I-B and apply the resolution protocol
   - If UNVERIFIED HISTORICAL CLAIM: Cite a primary source, or reclassify from E-HIS to I-HIS
   - If CHAIN DEPTH ERROR: Correct the I-A(n) notation to reflect actual inference steps
4. Use the Edit tool to make surgical changes — do NOT rewrite entire files
5. Keep all existing content that was NOT flagged

### Phase 5c: Re-validation

After the update, re-run ALL validators using the same process as Phase 5a.
Each validator writes `D:\Bible\bible-studies\dan3-19-HIST-daniel-10-12/{position}-revalidation.md`.

For any issues that STILL remain after the update:
**APPEND** them to the gap ledger at `D:\Bible\bible-studies\dan3-gap-ledger.md`
Format each entry as:
```
### [dan3-19-HIST-daniel-10-12] {POSITION} — [brief description]
- **Study:** dan3-19-HIST-daniel-10-12
- **Position:** {POSITION}
- **Layer:** [1 or 2]
- **Issue:** [L1: missing / misrepresented / weak] or [L2: misclassified / ungrounded / missing-counter-evidence / unverified-historical / chain-depth-error]
- **Detail:** [what specifically is wrong and what it should say]
- **Affected sections:** [which sections of CONCLUSION.md / 03-analysis.md need updating]
- **Note:** Persisted after one update attempt
```
Do NOT write redo.txt. The gap ledger will be processed by `--fix-gaps`.

**The validation agent may also search bible-studies, EGW, Secrets Unsealed, or the web to verify its findings. If it discovers a new argument that is biblical and compatible with the position, it can add it to the position DB.**
