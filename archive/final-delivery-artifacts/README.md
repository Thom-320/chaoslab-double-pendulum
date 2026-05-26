# ChaosLab final delivery artifacts

This folder archives the review ZIPs, patches, and loose Markdown artifacts used during the final ChaosLab presentation iteration.

Policy applied before committing:

- Original source artifacts are copied once by SHA-256 into `source-files/`.
- ZIP contents are extracted into `extracted-no-mp4/`.
- `.mp4` entries, generated caches, virtual environments, `output/`, `tmp/`, and reference-video folders are not extracted.
- Exact duplicate source files and exact duplicate extracted files are skipped and recorded in the manifests.
- Raw MP4 files from Downloads are recorded in `manifests/skipped_files.csv` instead of committed as loose files. ZIP files are kept available for other agents, even when a ZIP internally contains MP4 files.
- Browser duplicate names such as `(1)` are treated as duplicates when their SHA-256 hash matches the canonical file.

Summary:

```json
{
  "source_candidates": 21,
  "source_unique_stored": 16,
  "source_duplicates_skipped": 4,
  "source_skipped": 1,
  "zips_stored": 10,
  "zips_extracted": 10,
  "entries_extracted_unique": 94,
  "entries_duplicate_skipped": 226,
  "entries_skipped": 17,
  "mp4_entries_skipped": 10
}
```

Use the current repository root as the source of truth for the deliverable. These archived folders exist for traceability, peer review, and comparison only.
