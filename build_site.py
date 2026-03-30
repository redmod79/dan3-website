#!/usr/bin/env python3
"""
build_site.py — Build the Daniel: Three Views Compared website.

Scans D:/bible/bible-studies/dan3-* for all 36 studies,
copies files into docs/studies/, generates mkdocs.yml and index.md,
and copies shared assets from etc-website.
"""

import os
import re
import shutil
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
STUDIES_SRC = Path("D:/bible/bible-studies")
ETC_WEBSITE = Path("D:/bible/etc-website")
DOCS = PROJECT_ROOT / "docs"
DOCS_STUDIES = DOCS / "studies"

# ── Study metadata ─────────────────────────────────────────────────
SHORT_TITLES = {
    "dan3-00": "Methodology & Evidence Framework",
    "dan3-01": "Literary Architecture of Daniel",
    "dan3-02": "Historicity & Dating Evidence",
    "dan3-03": "HIST: Daniel 2",
    "dan3-04": "PRET: Daniel 2",
    "dan3-05": "FUT: Daniel 2",
    "dan3-06": "COMPARE: Daniel 2",
    "dan3-07": "HIST: Daniel 7",
    "dan3-08": "PRET: Daniel 7",
    "dan3-09": "FUT: Daniel 7",
    "dan3-10": "COMPARE: Daniel 7",
    "dan3-11": "HIST: Daniel 8",
    "dan3-12": "PRET: Daniel 8",
    "dan3-13": "FUT: Daniel 8",
    "dan3-14": "COMPARE: Daniel 8",
    "dan3-15": "HIST: Daniel 8-9 & 70 Weeks",
    "dan3-16": "PRET: Daniel 8-9 & 70 Weeks",
    "dan3-17": "FUT: Daniel 8-9 & 70 Weeks",
    "dan3-18": "COMPARE: Daniel 8-9 & 70 Weeks",
    "dan3-19": "HIST: Daniel 10-12",
    "dan3-20": "PRET: Daniel 10-12",
    "dan3-21": "FUT: Daniel 10-12",
    "dan3-22": "COMPARE: Daniel 10-12",
    "dan3-23": "The Day-Year Principle",
    "dan3-24": "NT Use of Daniel",
    "dan3-25": "Daniel-Revelation Connections",
    "dan3-26": "Counter-Arguments & Responses",
    "dan3-27": "HIST Steelman",
    "dan3-28": "PRET Steelman",
    "dan3-29": "FUT Steelman",
    "dan3-30": "Grand Synthesis",
    "dan3-31": "HIST Framework",
    "dan3-32": "PRET Framework",
    "dan3-33": "FUT Framework",
    "dan3-34": "Framework Comparison",
    "dan3-35": "Final Synthesis",
}

FULL_TITLES = {
    "dan3-00": "What is the evidence classification system, what positions are being compared, and what analytical tools does this series use?",
    "dan3-01": "What is the literary structure of Daniel's prophetic chapters?",
    "dan3-02": "What historical and linguistic evidence bears on Daniel's composition date and historical reliability?",
    "dan3-03": "How does historicism read Daniel 2, and what is the textual basis for identifying the four kingdoms?",
    "dan3-04": "How does the preterist school read Daniel 2, and what is the textual basis for alternative kingdom identifications?",
    "dan3-05": "How does dispensationalist futurism read Daniel 2, and what is the textual basis for the gap between Rome and the stone?",
    "dan3-06": "Daniel 2 three-way comparison and evidence classification",
    "dan3-07": "How does historicism read Daniel 7?",
    "dan3-08": "How does the preterist school read Daniel 7, and what is the textual basis for identifying the little horn as Antiochus IV?",
    "dan3-09": "How does dispensationalist futurism read Daniel 7?",
    "dan3-10": "Daniel 7 three-way comparison — specification-match adjudication and evidence classification",
    "dan3-11": "How does historicism read Daniel 8?",
    "dan3-12": "How does the preterist school read Daniel 8 with Antiochus IV as the little horn?",
    "dan3-13": "How does dispensationalist futurism read Daniel 8 with a type/antitype little horn?",
    "dan3-14": "Daniel 8 three-way comparison and evidence classification",
    "dan3-15": "How does historicism read the Daniel 8-9 connection and the 70 weeks?",
    "dan3-16": "How does the preterist school read Daniel 8-9 and the 70 weeks?",
    "dan3-17": "How does dispensationalist futurism read Daniel 8-9 and the 70 weeks?",
    "dan3-18": "Daniel 8-9 and the 70 weeks: three-way comparison",
    "dan3-19": "How does historicism read Daniel 10-12?",
    "dan3-20": "How does the preterist school read Daniel 10-12?",
    "dan3-21": "How does dispensationalist futurism read Daniel 10-12?",
    "dan3-22": "Daniel 10-12: three-way comparison — evidence classification and specification-match adjudication",
    "dan3-23": "What is the biblical basis for the day-year principle, and how should it be classified?",
    "dan3-24": "Do NT authors treat Daniel 7-12 as a unified prophetic corpus?",
    "dan3-25": "How does Revelation develop Daniel's prophetic themes?",
    "dan3-26": "What are the strongest counter-arguments for each position, and how do they respond?",
    "dan3-27": "The complete historicist case across all of Daniel",
    "dan3-28": "The complete preterist case across all of Daniel",
    "dan3-29": "The complete futurist case across all of Daniel",
    "dan3-30": "Grand synthesis: what Daniel's prophetic visions establish, suggest, and leave disputed",
    "dan3-31": "What is the historicist reading of Daniel as a complete interpretive system?",
    "dan3-32": "What is the preterist reading of Daniel as a complete interpretive system?",
    "dan3-33": "What is the futurist reading of Daniel as a complete interpretive system?",
    "dan3-34": "How do the three interpretive systems compare at the structural level?",
    "dan3-35": "Final assessment: framework-evidence alignment, graded viability, and convergence",
}

# Cluster groupings
CLUSTERS = [
    {
        "name": "Foundation",
        "desc": "Establishing the methodology, literary structure, and historicity of Daniel before comparing interpretive positions.",
        "studies": ["dan3-00", "dan3-01", "dan3-02"],
    },
    {
        "name": "Daniel 2 -- The Image",
        "desc": "Three positional readings of Daniel 2 (four metals and stone), followed by a comparative analysis.",
        "studies": ["dan3-03", "dan3-04", "dan3-05", "dan3-06"],
    },
    {
        "name": "Daniel 7 -- The Beasts",
        "desc": "Three positional readings of Daniel 7 (four beasts, little horn, judgment), followed by comparison.",
        "studies": ["dan3-07", "dan3-08", "dan3-09", "dan3-10"],
    },
    {
        "name": "Daniel 8 -- The Ram and Goat",
        "desc": "Three positional readings of Daniel 8 (ram, goat, little horn), followed by comparison.",
        "studies": ["dan3-11", "dan3-12", "dan3-13", "dan3-14"],
    },
    {
        "name": "Daniel 8-9 -- The 70 Weeks",
        "desc": "Three positional readings of the Daniel 8-9 connection and the 70 weeks prophecy, followed by comparison.",
        "studies": ["dan3-15", "dan3-16", "dan3-17", "dan3-18"],
    },
    {
        "name": "Daniel 10-12 -- The Final Vision",
        "desc": "Three positional readings of Daniel's most detailed prophecy, followed by comparison.",
        "studies": ["dan3-19", "dan3-20", "dan3-21", "dan3-22"],
    },
    {
        "name": "Cross-Cutting Studies",
        "desc": "Thematic investigations that cut across all vision cycles: the day-year principle, NT usage of Daniel, Daniel-Revelation connections, and counter-arguments.",
        "studies": ["dan3-23", "dan3-24", "dan3-25", "dan3-26"],
    },
    {
        "name": "Steelman Compilations",
        "desc": "Each position's complete case compiled and stress-tested across all of Daniel.",
        "studies": ["dan3-27", "dan3-28", "dan3-29"],
    },
    {
        "name": "Framework Analysis",
        "desc": "Zooming out from details to systems: what each position IS as an interpretive framework, compared side by side.",
        "studies": ["dan3-31", "dan3-32", "dan3-33", "dan3-34"],
    },
    {
        "name": "Synthesis",
        "desc": "Grand evidence synthesis (399 items) and final framework-plus-evidence capstone assessment.",
        "studies": ["dan3-30", "dan3-35"],
    },
]

# Standard study files (in display order for nav)
STUDY_FILES = [
    ("CONCLUSION.md", None),           # Landing page (no label = index page)
    ("03-analysis.md", "Analysis"),
    ("02-verses.md", "Verses"),
    ("04-word-studies.md", "Word Studies"),
    ("01-topics.md", "Topics"),
    ("PROMPT.md", "Research Scope"),
    ("00-references.md", "References"),
]

# Validation files (position-specific)
VALIDATION_FILES = [
    ("hist-validation.md", "HIST Validation"),
    ("pret-validation.md", "PRET Validation"),
    ("fut-validation.md", "FUT Validation"),
    ("hist-revalidation.md", "HIST Revalidation"),
]

# Raw data file display names
RAW_DATA_NAMES = {
    "concept-context": "Concept Context",
    "existing-studies": "Existing Studies",
    "greek-parsing": "Greek Parsing",
    "hebrew-parsing": "Hebrew Parsing",
    "hebrew-parsing-raw": "Hebrew Parsing (Raw)",
    "naves-topics": "Nave's Topics",
    "naves-raw-output": "Nave's Topics (Raw)",
    "parallels": "Cross-Testament Parallels",
    "parallels-raw": "Parallels (Raw)",
    "strongs-lookups": "Strong's Lookups",
    "strongs-raw-output": "Strong's Lookups (Raw)",
    "strongs": "Strong's Lookups",
    "web-research": "Web Research",
    "grammar-references": "Grammar References",
    "evidence-tally": "Evidence Tally",
    "study-db-queries": "Study DB Queries",
    "apocrypha-searches": "Apocrypha Searches",
    "perspective-claims": "Perspective Claims",
    # dan3-30 synthesis raw data
    "compare-tallies": "Compare Tallies",
    "constraining-effects": "Constraining Effects",
    "counter-arguments": "Counter-Arguments",
    "evidence-db-full": "Evidence DB (Full)",
    "ib-resolutions": "I-B Resolutions",
    "specification-matrices": "Specification Matrices",
    "steelman-weaknesses": "Steelman Weaknesses",
}


def get_raw_data_name(filename: str) -> str:
    """Get a display name for a raw-data file."""
    stem = Path(filename).stem
    if stem in RAW_DATA_NAMES:
        return RAW_DATA_NAMES[stem]
    return stem.replace("-", " ").title()


def find_study_folders() -> list[tuple[str, Path]]:
    """Find all dan3-NN-* folders in the studies source directory."""
    folders = []
    for d in sorted(STUDIES_SRC.iterdir()):
        if d.is_dir() and re.match(r"dan3-\d{2}-", d.name):
            slug = d.name
            num = slug.split("-")[1]
            key = f"dan3-{num}"
            folders.append((key, d))
    return folders


def copy_study(key: str, src: Path, preserved_simples: dict):
    """Copy a study folder into docs/studies/."""
    dest = DOCS_STUDIES / src.name
    dest.mkdir(parents=True, exist_ok=True)

    # Copy standard files
    for fname, _ in STUDY_FILES:
        src_file = src / fname
        if src_file.exists():
            shutil.copy2(src_file, dest / fname)

    # Restore preserved conclusion-simple.md, or copy from source
    simple_path = dest / "conclusion-simple.md"
    if src.name in preserved_simples:
        simple_path.write_text(preserved_simples[src.name], encoding="utf-8")
    else:
        simple_src = src / "conclusion-simple.md"
        if simple_src.exists():
            shutil.copy2(simple_src, dest / "conclusion-simple.md")

    # Copy validation files
    for fname, _ in VALIDATION_FILES:
        src_file = src / fname
        if src_file.exists():
            shutil.copy2(src_file, dest / fname)

    # Copy CUSTOM-INSTRUCTIONS.md if present
    custom = src / "CUSTOM-INSTRUCTIONS.md"
    if custom.exists():
        shutil.copy2(custom, dest / "CUSTOM-INSTRUCTIONS.md")

    # Copy METADATA.yaml if present
    meta = src / "METADATA.yaml"
    if meta.exists():
        shutil.copy2(meta, dest / "METADATA.yaml")

    # Copy raw-data/ (both .md and .txt files)
    raw_src = src / "raw-data"
    if raw_src.exists() and raw_src.is_dir():
        raw_dest = dest / "raw-data"
        raw_dest.mkdir(parents=True, exist_ok=True)
        for f in raw_src.iterdir():
            if f.is_file():
                # Convert .txt to .md for MkDocs rendering
                if f.suffix == ".txt":
                    dest_file = raw_dest / (f.stem + ".md")
                    content = f.read_text(encoding="utf-8", errors="replace")
                    # Wrap in code block if it looks like raw data
                    dest_file.write_text(f"# {get_raw_data_name(f.name)}\n\n```\n{content}\n```\n", encoding="utf-8")
                else:
                    shutil.copy2(f, raw_dest / f.name)

    return dest


def build_nav_entry(key: str, slug: str) -> dict:
    """Build a nav entry for one study."""
    num = key.split("-")[1]
    short_title = SHORT_TITLES.get(key, slug)
    nav_title = f"{num} -- {short_title}"

    dest = DOCS_STUDIES / slug
    items = []

    # Landing page: conclusion-simple.md if it exists, else CONCLUSION.md
    simple = dest / "conclusion-simple.md"
    conclusion = dest / "CONCLUSION.md"
    if simple.exists():
        items.append(f"studies/{slug}/conclusion-simple.md")
        if conclusion.exists():
            items.append({"Conclusion": f"studies/{slug}/CONCLUSION.md"})
    elif conclusion.exists():
        items.append(f"studies/{slug}/CONCLUSION.md")

    # Other standard files
    for fname, label in STUDY_FILES:
        if label is None:
            continue
        fpath = dest / fname
        if fpath.exists():
            items.append({label: f"studies/{slug}/{fname}"})

    # Validation files
    for fname, label in VALIDATION_FILES:
        fpath = dest / fname
        if fpath.exists():
            items.append({label: f"studies/{slug}/{fname}"})

    # Custom instructions
    custom = dest / "CUSTOM-INSTRUCTIONS.md"
    if custom.exists():
        items.append({"Custom Instructions": f"studies/{slug}/CUSTOM-INSTRUCTIONS.md"})

    # Raw data files
    raw_dir = dest / "raw-data"
    if raw_dir.exists() and raw_dir.is_dir():
        raw_items = []
        for f in sorted(raw_dir.iterdir()):
            if f.is_file() and f.suffix == ".md":
                display = get_raw_data_name(f.name)
                raw_items.append({display: f"studies/{slug}/raw-data/{f.name}"})
        if raw_items:
            items.append({"Raw Data": raw_items})

    return {nav_title: items}


def generate_mkdocs_yml(study_folders: list[tuple[str, Path]]):
    """Generate mkdocs.yml."""
    slug_map = {key: src.name for key, src in study_folders}

    lines = []
    lines.append('site_name: "Daniel: Three Views Compared"')
    lines.append("site_description: A 31-study comparative investigation of Daniel's prophecies through Historicist, Preterist, and Futurist lenses. 399 evidence items classified.")
    lines.append("")
    lines.append("theme:")
    lines.append("  name: material")
    lines.append("  custom_dir: overrides")
    lines.append("  palette:")
    lines.append("    - scheme: default")
    lines.append("      primary: indigo")
    lines.append("      accent: deep orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-7")
    lines.append("        name: Switch to dark mode")
    lines.append("    - scheme: slate")
    lines.append("      primary: indigo")
    lines.append("      accent: deep orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-4")
    lines.append("        name: Switch to light mode")
    lines.append("  features:")
    lines.append("    - navigation.instant")
    lines.append("    - navigation.tracking")
    lines.append("    - navigation.tabs")
    lines.append("    - navigation.sections")
    lines.append("    - navigation.top")
    lines.append("    - navigation.indexes")
    lines.append("    - search.suggest")
    lines.append("    - search.highlight")
    lines.append("    - content.tabs.link")
    lines.append("    - toc.follow")
    lines.append("  font:")
    lines.append("    text: Roboto")
    lines.append("    code: Roboto Mono")
    lines.append("")
    lines.append("plugins:")
    lines.append("  - search")
    lines.append("")
    lines.append("markdown_extensions:")
    lines.append("  - abbr")
    lines.append("  - admonition")
    lines.append("  - attr_list")
    lines.append("  - def_list")
    lines.append("  - footnotes")
    lines.append("  - md_in_html")
    lines.append("  - tables")
    lines.append("  - toc:")
    lines.append("      permalink: true")
    lines.append("  - pymdownx.details")
    lines.append("  - pymdownx.superfences")
    lines.append("  - pymdownx.highlight:")
    lines.append("      anchor_linenums: true")
    lines.append("  - pymdownx.inlinehilite")
    lines.append("  - pymdownx.tabbed:")
    lines.append("      alternate_style: true")
    lines.append("  - pymdownx.tasklist:")
    lines.append("      custom_checkbox: true")
    lines.append("")
    lines.append("extra:")
    lines.append("  social:")
    lines.append("    - icon: fontawesome/solid/book-bible")
    lines.append("      link: /")
    lines.append("")
    lines.append("extra_javascript:")
    lines.append("  - javascripts/verse-popup.js")
    lines.append("  - javascripts/study-breadcrumbs.js")
    lines.append("  - javascripts/external-links.js")
    lines.append("")
    lines.append("extra_css:")
    lines.append("  - stylesheets/extra.css")
    lines.append("")
    lines.append("nav:")
    lines.append("  - Home: index.md")
    lines.append("  - Studies:")
    lines.append("")

    for cluster in CLUSTERS:
        lines.append(f"    # ── {cluster['name']} ──")
        lines.append(f'    - "{cluster["name"]}":')
        lines.append("")
        for key in cluster["studies"]:
            slug = slug_map.get(key)
            if not slug:
                continue
            nav_entry = build_nav_entry(key, slug)
            for title, items in nav_entry.items():
                lines.append(f'      - "{title}":')
                for item in items:
                    if isinstance(item, str):
                        lines.append(f"        - {item}")
                    elif isinstance(item, dict):
                        for label, val in item.items():
                            if isinstance(val, list):
                                lines.append(f"        - {label}:")
                                for sub in val:
                                    if isinstance(sub, dict):
                                        for slabel, spath in sub.items():
                                            lines.append(f'          - "{slabel}": {spath}')
                                    else:
                                        lines.append(f"          - {sub}")
                            else:
                                lines.append(f"        - {label}: {val}")
        lines.append("")

    lines.append("  - Methodology: methodology.md")
    lines.append('  - "Tools & Process": tools.md')

    yml_path = PROJECT_ROOT / "mkdocs.yml"
    yml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated {yml_path}")


def generate_index_md():
    """Generate docs/index.md."""
    content = []

    content.append("# Daniel: Three Views Compared")
    content.append("")
    content.append("*A 31-study comparative investigation of Daniel's prophecies through Historicist, Preterist, and Futurist lenses. 399 evidence items classified across 126 inferences.*")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## The Question")
    content.append("")
    content.append("Three major schools of prophetic interpretation compete for how to read Daniel's visions:")
    content.append("")
    content.append("- **Historicism (HIST):** The prophecies span continuous history from the prophet's time to the second coming")
    content.append("- **Preterism (PRET):** The prophecies were fulfilled primarily in the Hellenistic/Roman period (by the 2nd century BC or 1st century AD)")
    content.append("- **Futurism (FUT):** The prophecies are primarily about a future tribulation period, with gaps in the prophetic timeline")
    content.append("")
    content.append("Rather than assuming any position, this series investigates the biblical evidence from the ground up across 31 studies. Each vision cycle (Daniel 2, 7, 8, 8-9, 10-12) is examined three times -- once from each position's perspective -- and then subjected to a comparative analysis that classifies every evidence item.")
    content.append("")
    content.append("## The Approach")
    content.append("")
    content.append("Each study is a genuine investigation. The agents gathered ALL relevant evidence, presented what each side claims, and let the biblical text speak for itself. No study presupposed its conclusion. Evidence was classified into hierarchical tiers:")
    content.append("")
    content.append("- **Explicit (E):** What the text directly says -- a quote or close paraphrase")
    content.append("- **Necessary Implication (N):** What unavoidably follows from explicit statements")
    content.append("- **Inference** (four types):")
    content.append("    - **I-A (Evidence-Extending):** Systematizes E/N items using only the text's own vocabulary")
    content.append("    - **I-B (Competing-Evidence):** Both sides cite E/N support; resolved by Scripture-interprets-Scripture")
    content.append("    - **I-C (Compatible External):** External reasoning that does not contradict E/N")
    content.append("    - **I-D (Counter-Evidence External):** External concepts that require overriding E/N statements")
    content.append("")
    content.append("**Hierarchy:** E > N > I-A > I-B (resolved by SIS) > I-C > I-D")
    content.append("")
    content.append("[**Read the Methodology**](methodology.md){ .md-button }")
    content.append(" ")
    synth_simple = DOCS_STUDIES / "dan3-30-grand-synthesis" / "conclusion-simple.md"
    if synth_simple.exists():
        content.append("[**Skip to the Grand Synthesis**](studies/dan3-30-grand-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Skip to the Grand Synthesis**](studies/dan3-30-grand-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## The 31 Studies")
    content.append("")

    for cluster in CLUSTERS:
        content.append(f"### {cluster['name']}")
        content.append("")
        content.append(cluster["desc"])
        content.append("")
        content.append("| # | Study | Question |")
        content.append("|---|-------|----------|")
        for key in cluster["studies"]:
            num = key.split("-")[1]
            short = SHORT_TITLES.get(key, key)
            full = FULL_TITLES.get(key, short)
            slug = None
            for d in sorted(STUDIES_SRC.iterdir()):
                if d.is_dir() and d.name.startswith(f"{key}-"):
                    slug = d.name
                    break
            if slug:
                simple_path = DOCS_STUDIES / slug / "conclusion-simple.md"
                if simple_path.exists():
                    link = f"studies/{slug}/conclusion-simple.md"
                else:
                    link = f"studies/{slug}/CONCLUSION.md"
                content.append(f"| {num} | [{short}]({link}) | {full} |")
            else:
                content.append(f"| {num} | {short} | {full} |")
        content.append("")

    content.append("---")
    content.append("")
    content.append("## What Each Study Contains")
    content.append("")
    content.append("Every study includes multiple layers of research, all accessible through the navigation:")
    content.append("")
    content.append("| File | Contents |")
    content.append("|------|----------|")
    content.append("| **Conclusion** | The final evidence classification with Explicit/Necessary Implication/Inference tables, tally, and assessment |")
    content.append("| **Analysis** | Verse-by-verse analysis, identified patterns, connections between passages, all-sides arguments |")
    content.append("| **Verses** | Full KJV text for every passage examined, organized thematically |")
    content.append("| **Word Studies** | Hebrew and Greek word studies with Strong's numbers, semantic ranges, and parsing |")
    content.append("| **Topics** | Nave's Topical Bible entries and key research findings |")
    content.append("| **Research Scope** | The original research question and scope that guided the investigation |")
    content.append("| **References** | Prior study references consulted during research |")
    content.append("| **Validation** | Position-specific validation reports (HIST, PRET, FUT) where applicable |")
    content.append("| **Raw Data** | Nave's topic output, Strong's lookups, Greek/Hebrew parsing, cross-testament parallels |")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## Evidence Summary (from Study 30)")
    content.append("")
    content.append("Study 30 synthesized the evidence from Studies 0-29 on the central question of how Daniel's prophetic visions should be read. The synthesis classified **399 total evidence items** across 126 inferences.")
    content.append("")
    content.append("### Tier Distribution")
    content.append("")
    content.append("| Tier | Count |")
    content.append("|------|-------|")
    content.append("| E (Explicit) | 210 |")
    content.append("| N (Necessary Implication) | 63 |")
    content.append("| I-A (Evidence-Extending) | 101 |")
    content.append("| I-B (Competing-Evidence) | 13 |")
    content.append("| I-C (Compatible External) | 7 |")
    content.append("| I-D (Counter-Evidence External) | 5 |")
    content.append("| **Total** | **399** |")
    content.append("")
    content.append("### Positional I-A to I-D Ratios")
    content.append("")
    content.append("The ratio of I-A (strongest inference) to I-D (weakest inference) items reveals how much each position depends on overriding explicit text:")
    content.append("")
    content.append("| Position | I-A : I-D Ratio |")
    content.append("|----------|----------------|")
    content.append("| **HIST** (Historicism) | 38 : 0 |")
    content.append("| **PRET** (Preterism) | 33 : 1 |")
    content.append("| **FUT** (Futurism) | 22 : 4 |")
    content.append("")
    content.append("Historicism requires zero items that override explicit text. Preterism requires one. Futurism requires four.")
    content.append("")
    synth_simple2 = DOCS_STUDIES / "dan3-30-grand-synthesis" / "conclusion-simple.md"
    if synth_simple2.exists():
        content.append("[**Read the Grand Synthesis**](studies/dan3-30-grand-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Read the Grand Synthesis**](studies/dan3-30-grand-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## Source Restrictions")
    content.append("")
    content.append("This series uses **no denominational or extra-biblical sources** as authoritative evidence. Permitted sources are:")
    content.append("")
    content.append("- Scripture (KJV text with Hebrew/Greek/Aramaic analysis)")
    content.append("- Secular and church historians (for verifying prophetic claims against historical events)")
    content.append("- Scholarly commentators from all traditions")
    content.append("- Hebrew, Aramaic, and Greek lexicons, grammars, and concordances")
    content.append("")
    content.append("The question is always: **What does the Bible say?**")
    content.append("")

    index_path = DOCS / "index.md"
    index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    print(f"  Generated {index_path}")


def generate_tools_md():
    """Generate docs/tools.md."""
    content = """# Research Tools & Process

*This page describes the automated research system and investigative methodology that produced the 36 studies in this series.*

---

## Investigative Stance

Each study is produced by an agent that functions as an **investigator, not an advocate.** This distinction governs every step of the process:

- **Gather evidence from all sides.** Each vision cycle is examined three times -- once from the Historicist perspective, once from the Preterist perspective, and once from the Futurist perspective. A fourth comparative study adjudicates between them.
- **Do not assume a conclusion before examining the evidence.** The conclusion emerges FROM the evidence, not the reverse.
- **State what the text says, not opinions about it.** The agent does not use editorial characterizations like "genuine tension," "strongest argument," or "non-intuitive reading." It states what each passage says and what each interpretive position infers from it.
- **Never use language like "irrefutable," "obviously," or "clearly proves."** Use "the text states," "this is consistent with."

---

## The Three-Position Comparative Methodology

This series examines Daniel's prophecies through three lenses systematically:

1. **Positional Studies (HIST/PRET/FUT):** Each position gets a dedicated study per vision cycle where it presents its strongest case using the evidence classification framework. The agent investigates that position's reading with full access to the biblical text and research tools.

2. **Comparative Studies (COMPARE):** After all three positions have been presented, a comparative study adjudicates between them using specification-match analysis -- how well does each position's reading match what the text actually specifies?

3. **Steelman Compilations:** Studies 27-29 compile each position's complete case across ALL vision cycles, stress-testing the cumulative evidence.

4. **Grand Synthesis:** Study 30 brings everything together with 399 classified evidence items across 126 inferences.

---

## How the Studies Were Produced

Each study was generated by a multi-agent pipeline, a Claude Code skill that answers Bible questions through tool-driven research. The pipeline ensures that:

- **Scope comes from tools, not training knowledge.** The AI does not decide which verses are relevant based on what it was trained on. Instead, tools search topical dictionaries, concordances, and semantic indexes to discover what Scripture says about the topic.
- **Research and analysis are separated.** The agent that gathers data is not the same agent that draws conclusions. This prevents confirmation bias.
- **Every claim is traceable.** Raw tool output is preserved in each study's `raw-data/` folder, so every finding can be verified against its source.

### The Multi-Agent Pipeline

```
Phase 1: Scoping Agent
   | Discovers topics, verses, Strong's numbers, related studies
   | Writes PROMPT.md (the research brief)

Phase 2: Research Agent
   | Reads PROMPT.md
   | Retrieves all verse text, runs parallels, word studies, parsing
   | Writes 01-topics.md, 02-verses.md, 04-word-studies.md
   | Saves raw tool output to raw-data/

Phase 3: Analysis Agent
   | Reads clean research files
   | Applies the evidence classification methodology
   | Writes 03-analysis.md and CONCLUSION.md

Phase 4: Validation Agent(s)
   | Reads CONCLUSION.md against the biblical text
   | Produces position-specific validation reports
   | Identifies misclassifications, unsupported claims, missing evidence
```

**Why multiple agents?**

- The **scoping agent** prevents training-knowledge bias. Scope comes from tool discovery, not from what the AI "knows" about theology.
- The **research agent** gets a fresh context window dedicated to data gathering. This maximizes the amount of data it can collect without running out of context.
- The **analysis agent** gets a fresh context window loaded with clean, organized research. This maximizes its capacity for synthesis and careful reasoning.
- The **validation agent(s)** provide independent quality control, checking each position's evidence claims against the actual text.

---

## The Study Files

Each study directory contains these files, produced by the pipeline:

| File | Produced By | Contents |
|------|-------------|----------|
| `PROMPT.md` | Scoping Agent | The research brief: tool-discovered topics, verses, Strong's numbers, related studies, and focus areas |
| `01-topics.md` | Research Agent | Nave's Topical Bible entries with all verse references for each topic |
| `02-verses.md` | Research Agent | Full KJV text for every verse examined, organized thematically |
| `04-word-studies.md` | Research Agent | Strong's concordance data: Hebrew/Greek words, definitions, translation statistics, verse occurrences |
| `raw-data/` | Research Agent | Raw tool output archived by category (Strong's lookups, parsing, parallels, etc.) |
| `03-analysis.md` | Analysis Agent | Verse-by-verse analysis with full evidence classification applied |
| `CONCLUSION.md` | Analysis Agent | Evidence tables (E/N/I), tally, and final assessment |
| `*-validation.md` | Validation Agent | Position-specific validation checking evidence claims against the text |

---

## Data Sources

The tools draw from these primary data sources:

| Source | Description | Size |
|--------|-------------|------|
| **KJV Bible** | Complete King James Version text | 31,102 verses |
| **Nave's Topical Bible** | Orville J. Nave's topical dictionary | 5,319 topics |
| **Strong's Concordance** | James Strong's exhaustive concordance with Hebrew/Greek lexicon | Every word in the KJV mapped to original language |
| **BHSA** (Biblia Hebraica Stuttgartensia Amstelodamensis) | Hebrew Bible linguistic database via Text-Fabric | Full morphological parsing of every Hebrew word |
| **N1904** (Nestle 1904) | Greek New Testament linguistic database via Text-Fabric | Full morphological parsing of every Greek word |
| **Textus Receptus** | Byzantine Greek text tradition | For textual variant comparison |
| **LXX Mapping** | Septuagint translation correspondences | Hebrew-to-Greek word mappings |
| **Sentence embeddings** | Pre-computed semantic vectors | For semantic search across all sources |

---

## Position Databases: How Each View Gets a Fair Hearing

A distinctive feature of this series is that each interpretive position has its own **dedicated argument database** -- a curated collection of that position's strongest arguments, verified against its own scholarly tradition. These databases ensure that no position is straw-manned or under-represented.

### Historicist Position Database (942 arguments)

The historicist database represents the traditional Protestant reading of Daniel as continuous prophecy spanning from Babylon to the Second Coming. Its arguments were verified against Ellen White's writings, SDA pioneer scholarship (Uriah Smith, William Miller, Josiah Litch, S.N. Haskell), LeRoy Froom's *Prophetic Faith of Our Fathers*, and Stephen Bohr's study notes.

The database contains textual/grammatical arguments (e.g., the *gadal/yether* progression requiring the little horn to exceed both Persia and Greece), vocabulary chains binding Daniel's chapters into a unified prophetic corpus (e.g., the *biyn* chain across Dan 8-12), cross-references to Revelation (186 catalogued allusions), day-year principle evidence (13 supporting lines), and documented historical fulfillments.

### Preterist Position Database (412 arguments)

The preterist database represents the reading of Daniel's prophecies as referring primarily to the Maccabean crisis of 167-164 BC. Sources include Jerome's Commentary on Daniel (preserving Porphyry's 3rd-century arguments -- the earliest systematic preterist case), Albert Barnes, John Calvin, Matthew Henry, and modern critical scholars (Collins, Goldingay, Kitchen).

The database contains dating/composition arguments (linguistic evidence, Dead Sea Scrolls), Antiochus IV identification evidence, Dan 11:1-35 verse-by-verse Ptolemaic-Seleucid correspondences (the preterist position's strongest section), literary genre arguments, and the position's own acknowledged weaknesses (Dan 11:40-45 problems, everlasting kingdom language, *gadal/yether* progression).

### Futurist Position Database (466 arguments)

The futurist database represents the dispensationalist reading that inserts a gap between Daniel's 69th and 70th weeks and places the climactic fulfillment in a future tribulation. Sources include J.N. Darby's *Synopsis* (the origin of dispensationalism), John Walvoord, J. Dwight Pentecost, Thomas Ice, Harold Hoehner, and Robert Anderson.

The database contains gap/parenthesis arguments, revived-Rome theory, future Antichrist identification, type/antitype reasoning (Antiochus as historical type), literal time-period arguments, the Israel/Church distinction, Third Temple evidence, and counter-arguments to historicist and preterist readings.

### How the Databases Are Used

The databases serve two critical functions in the study pipeline:

1. **Prompt Review (Phase 2.5):** Before the research agent runs, a reviewer checks whether the research scope covers the arguments each position's database expects for that chapter. Missing arguments are added as research directives. This prevents the study from accidentally omitting a position's key claims.

2. **Position Validation (Phase 5):** After the analysis is written, dedicated validators check the study against each position's database. The validator asks: Is each argument accurately represented? Is it present, missing, or misrepresented? Are the evidence classifications correct? This catches both straw-manning (weakening a position's case) and over-claiming (classifying evidence at a higher tier than warranted).

The databases are the authority on what each position holds. If the database says the historicist position argues X, and the study attributes Y to historicism, that is a misrepresentation -- even if the validator's own training knowledge thinks Y is defensible. This constraint keeps the investigation honest.

---

## Evidence Classification Methodology

The core of the methodology is a three-tier evidence classification system that distinguishes between what Scripture directly states, what necessarily follows from it, and what positions claim it implies.

### The Three Tiers

**E -- Explicit.** "The Bible says X." You can point to a verse that says X. A close paraphrase of the actual words of a specific verse, with no concept, framework, or interpretation added beyond what the words themselves require.

**N -- Necessary Implication.** "The Bible implies X." You can point to verses that, when combined, force X with no alternative. Every reader from any theological position must agree this follows -- no additional reasoning is required.

**I -- Inference.** "A position claims the Bible teaches X." No verse explicitly states X, and no combination of verses necessarily implies X. Something must be added beyond what the text contains.

**Critical rule:** Inferences cannot block explicit statements or necessary implications. If E and N items establish X, the existence of passages that *could be inferred* to teach not-X does not prevent X from being established.

---

### The 4-Type Inference Taxonomy

Inferences are further classified on two dimensions:

|  | Derived from E/N | Not derived from E/N |
|--|--|--|
| **Aligns with E/N** | **I-A** (Evidence-Extending) | **I-C** (Compatible External) |
| **Conflicts with E/N** | **I-B** (Competing-Evidence) | **I-D** (Counter-Evidence External) |

**I-A (Evidence-Extending):** Uses only vocabulary and concepts found in E/N statements. An inference only because it systematizes multiple E/N items into a broader claim. Strongest inference type.

**I-B (Competing-Evidence):** Some E/N statements support it, but other E/N statements appear to contradict it. Genuine textual tension where both sides can cite Scripture. Requires the SIS Resolution Protocol.

**I-C (Compatible External):** Reasoning from outside the text (theological tradition, philosophical framework, historical context) that does not contradict any E/N statement. Supplemental only.

**I-D (Counter-Evidence External):** External concepts that require overriding, redefining, or qualifying E/N statements to be maintained. Weakest inference type.

**Evidence hierarchy:** E > N > I-A > I-B (resolved by SIS) > I-C > I-D

---

### Positional Classification

In this comparative series, evidence items are classified by which position they support (HIST, PRET, FUT, or Neutral/Shared). Items are classified positionally **only when one position must deny the textual observation.** Factual observations that all positions must accept are classified Neutral regardless of which side cites them.

[**Read the Full Methodology**](methodology.md){ .md-button }
"""
    tools_path = DOCS / "tools.md"
    tools_path.write_text(content, encoding="utf-8")
    print(f"  Generated {tools_path}")


def copy_assets():
    """Copy shared assets from etc-website."""
    js_src = ETC_WEBSITE / "docs" / "javascripts"
    js_dest = DOCS / "javascripts"
    js_dest.mkdir(parents=True, exist_ok=True)
    for fname in ["verse-popup.js", "study-breadcrumbs.js", "external-links.js",
                   "verses.json", "strongs.json"]:
        src = js_src / fname
        if src.exists():
            shutil.copy2(src, js_dest / fname)
            print(f"  Copied {fname}")
        else:
            print(f"  WARNING: {src} not found")

    css_src = ETC_WEBSITE / "docs" / "stylesheets" / "extra.css"
    css_dest = DOCS / "stylesheets"
    css_dest.mkdir(parents=True, exist_ok=True)
    if css_src.exists():
        shutil.copy2(css_src, css_dest / "extra.css")
        print(f"  Copied extra.css")


def copy_methodology():
    """Copy methodology: try dan3-series-methodology.md first, fall back to dan3-00 CONCLUSION.md."""
    dest = DOCS / "methodology.md"
    src_series = STUDIES_SRC / "dan3-series-methodology.md"
    src_dan3_00 = None

    # Find dan3-00 folder
    for d in sorted(STUDIES_SRC.iterdir()):
        if d.is_dir() and d.name.startswith("dan3-00-"):
            src_dan3_00 = d / "CONCLUSION.md"
            break

    if src_series.exists():
        shutil.copy2(src_series, dest)
        print(f"  Copied methodology from {src_series.name}")
    elif src_dan3_00 and src_dan3_00.exists():
        shutil.copy2(src_dan3_00, dest)
        print(f"  Copied methodology from dan3-00 CONCLUSION.md")
    else:
        print(f"  WARNING: No methodology source found")


def generate_deploy_yml():
    """Generate .github/workflows/deploy.yml."""
    deploy_dir = PROJECT_ROOT / ".github" / "workflows"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    content = """name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - master

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure Git credentials
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Actions"

      - uses: actions/setup-python@v5
        with:
          python-version: 3.x

      - name: Cache MkDocs dependencies
        uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ hashFiles('**/requirements.txt') }}
          path: .cache
          restore-keys: mkdocs-material-

      - name: Install MkDocs Material
        run: pip install mkdocs-material

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
"""
    (deploy_dir / "deploy.yml").write_text(content, encoding="utf-8")
    print(f"  Generated deploy.yml")


def generate_gitignore():
    """Generate .gitignore."""
    content = """site/
.venv/
__pycache__/
node_modules/
"""
    (PROJECT_ROOT / ".gitignore").write_text(content, encoding="utf-8")
    print(f"  Generated .gitignore")


def generate_readme(study_folders: list[tuple[str, Path]]):
    """Generate README.md."""
    lines = []
    lines.append("# Daniel: Three Views Compared")
    lines.append("")
    lines.append("A 31-study comparative investigation of Daniel's prophecies through Historicist, Preterist, and Futurist lenses. 399 evidence items classified.")
    lines.append("")
    lines.append("## Studies")
    lines.append("")
    lines.append("| # | Study | Question |")
    lines.append("|---|-------|----------|")
    for key, src in study_folders:
        num = key.split("-")[1]
        short = SHORT_TITLES.get(key, key)
        full = FULL_TITLES.get(key, short)
        lines.append(f"| {num} | {short} | {full} |")
    lines.append("")
    lines.append("## Built With")
    lines.append("")
    lines.append("- [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)")
    lines.append("- Interactive Bible verse and Strong's number popups")
    lines.append("- Full KJV text and Strong's Concordance data")

    (PROJECT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated README.md")


def main():
    print("=" * 60)
    print("Building Daniel: Three Views Compared website")
    print("=" * 60)

    # Preserve any existing conclusion-simple.md files before cleaning
    preserved_simples = {}
    if DOCS_STUDIES.exists():
        for d in DOCS_STUDIES.iterdir():
            if d.is_dir():
                simple = d / "conclusion-simple.md"
                if simple.exists():
                    preserved_simples[d.name] = simple.read_text(encoding="utf-8")
        shutil.rmtree(DOCS_STUDIES)
    DOCS_STUDIES.mkdir(parents=True)
    print(f"  Preserved {len(preserved_simples)} conclusion-simple.md files")

    # Find all study folders
    print("\n[1/7] Finding study folders...")
    study_folders = find_study_folders()
    print(f"  Found {len(study_folders)} studies")

    # Copy studies
    print("\n[2/7] Copying study files...")
    for key, src in study_folders:
        dest = copy_study(key, src, preserved_simples)
        print(f"  {key}: {src.name} -> {dest.relative_to(PROJECT_ROOT)}")

    # Copy methodology
    print("\n[3/7] Copying methodology...")
    copy_methodology()

    # Copy shared assets
    print("\n[4/7] Copying shared assets from etc-website...")
    copy_assets()

    # Generate mkdocs.yml
    print("\n[5/7] Generating mkdocs.yml...")
    generate_mkdocs_yml(study_folders)

    # Generate index.md
    print("\n[6/7] Generating index.md and tools.md...")
    generate_index_md()
    generate_tools_md()

    # Generate supporting files
    print("\n[7/7] Generating supporting files...")
    generate_deploy_yml()
    generate_gitignore()
    generate_readme(study_folders)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"  Studies: {len(study_folders)}")
    print(f"  Output: {DOCS}")
    print("\nNext steps:")
    print("  1. cd dan3-website && python add_blb_links.py docs/")
    print("  2. mkdocs serve")
    print("=" * 60)


if __name__ == "__main__":
    main()
