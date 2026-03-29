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
---

## Phase 5: Position Validation (Validate → Update → Re-validate)

**CRITICAL RULE:** Validators must check the study against what the **position database says**, NOT against the validator's own theological training knowledge. If the DB says the HIST position is X, and the study attributes Y to HIST, that is a misrepresentation even if the validator's training knowledge thinks Y is defensible. The DB is the authority on what each position holds.

### Three-step process:
1. **Phase 5a — First Validation**: Run all position validators. Each writes a validation report.
2. **Phase 5b — Targeted Update** (if issues found): Read ALL validation reports, then make ONE targeted update pass on `03-analysis.md` and `CONCLUSION.md` to fix the identified issues. Do NOT rewrite from scratch — make surgical edits to fix specific problems. Do NOT change content that validators approved.
3. **Phase 5c — Re-validation**: Run all position validators AGAIN on the updated files. Any issues that STILL remain after the update go to the gap ledger. Issues that were fixed are noted as resolved in the re-validation report.

If Phase 5a finds zero issues, skip 5b and 5c entirely.

**COMPARE/SYNTHESIS validation focus:** Check whether the study **accurately represents** each position.
Do NOT flag missing arguments — the COMPARE study only compares what the perspective studies already said.
DO flag if a position is **misrepresented, strawmanned, or unfairly weakened.**
Also verify that the **Specification-Match Matrix** (if applicable) accurately reflects each position's
E/N/I classifications from their respective perspective studies' Claim Verification tables.
A COMPARE study should not upgrade an I-A(2) LOW match to I-A(1) HIGH.

### HIST Validation (port 9882)

Launch a subagent that:
1. Reads `D:/bible/tools/hist-position/DB-SUMMARY.md` to understand the HIST position
2. Reads `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/CONCLUSION.md` and `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/03-analysis.md`
3. Searches the HIST position DB (port 9882):
   ```bash
   cd "D:\bible\tools\hist-position\search" && python search_client.py "QUERY" --top 15
   ```
4. Check whether the HIST position is **accurately represented** in the comparison:
   - Is any HIST argument **strawmanned** (presented weaker than it actually is)?
   - Is any HIST argument **mischaracterized** (attributed claims the position doesn't make)?
   - Are the HIST position's **admitted weaknesses** fairly stated (not exaggerated)?
   - Are the HIST position's **strengths** acknowledged where they exist?
   - Are there arguments the perspective study covered that the COMPARE study ignored?
6. Writes `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/hist-validation.md` with findings
   - Include a summary line: `LAYER 1 ISSUES: X` (count of representation problems)
   - Include a summary line: `LAYER 2 ISSUES: Y` (count of grounding problems)
   - For each issue, specify the exact section, the nature of the problem, and what needs to change

### PRET Validation (port 9884)

Launch a subagent that:
1. Reads `D:/bible/tools/pret-position/DB-SUMMARY.md` to understand the PRET position
2. Reads `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/CONCLUSION.md` and `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/03-analysis.md`
3. Searches the PRET position DB (port 9884):
   ```bash
   cd "D:\bible\tools\pret-position\search" && python search_client.py "QUERY" --top 15
   ```
4. Check whether the PRET position is **accurately represented** in the comparison:
   - Is any PRET argument **strawmanned** (presented weaker than it actually is)?
   - Is any PRET argument **mischaracterized** (attributed claims the position doesn't make)?
   - Are the PRET position's **admitted weaknesses** fairly stated (not exaggerated)?
   - Are the PRET position's **strengths** acknowledged where they exist?
   - Are there arguments the perspective study covered that the COMPARE study ignored?
6. Writes `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/pret-validation.md` with findings
   - Include a summary line: `LAYER 1 ISSUES: X` (count of representation problems)
   - Include a summary line: `LAYER 2 ISSUES: Y` (count of grounding problems)
   - For each issue, specify the exact section, the nature of the problem, and what needs to change

### FUT Validation (port 9883)

Launch a subagent that:
1. Reads `D:/bible/tools/fut-position/DB-SUMMARY.md` to understand the FUT position
2. Reads `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/CONCLUSION.md` and `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/03-analysis.md`
3. Searches the FUT position DB (port 9883):
   ```bash
   cd "D:\bible\tools\fut-position\search" && python search_client.py "QUERY" --top 15
   ```
4. Check whether the FUT position is **accurately represented** in the comparison:
   - Is any FUT argument **strawmanned** (presented weaker than it actually is)?
   - Is any FUT argument **mischaracterized** (attributed claims the position doesn't make)?
   - Are the FUT position's **admitted weaknesses** fairly stated (not exaggerated)?
   - Are the FUT position's **strengths** acknowledged where they exist?
   - Are there arguments the perspective study covered that the COMPARE study ignored?
6. Writes `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/fut-validation.md` with findings
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
Each validator writes `D:\Bible\bible-studies\dan3-18-COMPARE-daniel-8-9/{position}-revalidation.md`.

For any issues that STILL remain after the update:
**APPEND** them to the gap ledger at `D:\Bible\bible-studies\dan3-gap-ledger.md`
Format each entry as:
```
### [dan3-18-COMPARE-daniel-8-9] {POSITION} — [brief description]
- **Study:** dan3-18-COMPARE-daniel-8-9
- **Position:** {POSITION}
- **Issue:** [strawmanned / mischaracterized / omitted from comparison / weakness exaggerated]
- **Detail:** [what specifically is wrong and what it should say]
- **Affected sections:** [which sections of CONCLUSION.md / 03-analysis.md need updating]
- **Note:** Persisted after one update attempt
```
Do NOT write redo.txt. The gap ledger will be processed by `--fix-gaps`.

**The validation agent may also search bible-studies, EGW, Secrets Unsealed, or the web to verify its findings. If it discovers a new argument that is biblical and compatible with the position, it can add it to the position DB.**
