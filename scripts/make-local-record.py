"""Generate a local Release Evidence Record worksheet from observed lab state.

The event journal preserves post-update steps; earlier steps require manual evidence.
"""
from datetime import datetime, timezone
from pathlib import Path
from journal_local import read_events

ROOT = Path(__file__).resolve().parents[1]


def field(state, env, suffix):
    path = state / f'{env}.{suffix}'
    lines = path.read_text(encoding='utf-8').splitlines() if path.is_file() else []
    return lines if len(lines) == 2 else None


def build_record(root):
    state = root / '.lab' / 'state'
    evidence = root / '.lab' / 'evidence'
    built_file = state / 'last-built'
    built = built_file.read_text(encoding='utf-8').splitlines() if built_file.is_file() else []
    events = read_events(evidence / 'events.jsonl')
    lines = [
        '# Release Evidence Record — Local Docker lab worksheet', '',
        f'Generated (UTC): {datetime.now(timezone.utc).isoformat()}', '',
        '> **Scope:** Two disposable Docker containers on one computer, not AWS or production.',
        '> **Identity:** A local Docker image ID is **not** a published registry manifest digest.',
        '> **Trust:** This file and its journal are editable local teaching evidence, not signed provenance or an access-control audit.',
        '> **History:** The timeline contains only events recorded after the event-journalling scripts were installed.',
        '',
        '## CHANGE and PROVE', '',
        '- Source identity: the build uses a reader-supplied revision **label** (`good-v1` / `candidate-v2`), not a verified Git commit SHA.',
        '- Automated tests: enter the actual command and result of `./scripts/validate-repo.sh` (not collected by this worksheet).',
        '- Security scans, coverage floor and signing: **NOT RUN / NOT IMPLEMENTED** in this local lab.',
        '- Approval: local `--approve` is a reader acknowledgement, **not** a protected production approval.',
        '',
        '## PACKAGE — most recently built image (snapshot)', '',
        f'- Image ID: `{built[0] if len(built) == 2 else "NOT RECORDED"}`',
        f'- Revision label: `{built[1] if len(built) == 2 else "NOT RECORDED"}`',
        '- Published registry manifest digest: **NOT AVAILABLE**; a separate GHCR workflow is required.',
        '',
        '## PROMOTE and VERIFY — current state (snapshot, not release history)', '',
    ]
    for env in ('staging', 'production'):
        current = field(state, env, 'current')
        verified = field(state, env, 'verified')
        previous = field(state, env, 'previous-verified')
        lines.extend([
            f'### {env.title()}',
            f'- Currently deployed: `{current[0]}` / `{current[1]}`' if current else '- Currently deployed: not recorded',
            f'- Currently verified: **PASS** (`{verified[1]}`)' if verified and current == verified else '- Currently verified: **NOT VERIFIED**',
            f'- Saved previous verified image: `{previous[0]}` / `{previous[1]}`' if previous else '- Saved previous verified image: not recorded',
            '',
        ])
    lines.extend(['## Chronological events actually observed by the scripts', ''])
    if events:
        lines.extend([
            '| Time (UTC) | Action | Environment | Revision label | Image ID | Result / note |',
            '| --- | --- | --- | --- | --- | --- |',
        ])
        for event in events:
            # All journal fields are emitted by fixed script values and validated on read.
            timestamp = event['timestamp_utc']
            action = event['event']
            environment = event['environment']
            revision = event['revision_label']
            image_id = event['image_id']
            status = event['status']
            note = event['note'] or '—'
            lines.append(f'| {timestamp} | {action} | {environment} | `{revision}` | `{image_id}` | {status}; {note} |')
    else:
        lines.append('**No machine-recorded event history exists.** This may be an older run before journalling was added. Use actual Terminal output and saved failure logs to document it; do not infer an earlier deployment from the latest state files.')
    lines.extend(['', '## Failure evidence and recovery', ''])
    log_path = evidence / 'production-before-rollback.log'
    archived_logs = sorted(evidence.glob('production-before-rollback-*.log'))
    if archived_logs:
        lines.append(f'- Archived production rollback log files: **{len(archived_logs)}** under `.lab/evidence/` (each lab recovery keeps its own file).')
    if log_path.is_file():
        log = log_path.read_text(encoding='utf-8', errors='replace')
        failures = log.count('"GET /health HTTP/1.1" 500')
        lines.append(f'- Saved production pre-rollback log: `.lab/evidence/production-before-rollback.log` (observed HTTP 500 response lines: **{failures}**).')
        lines.append('- This log may be from a run before event journalling; confirm its timestamps and release association manually.')
    else:
        lines.append('- Saved production pre-rollback log: **NOT FOUND** (inspect the terminal output and container state).')
    lines.extend([
        '- Recovery decision and person authorising it: **READER TO COMPLETE**.',
        '- Recovery target availability and compatibility: **READER TO CONFIRM**. `--compatible` records acknowledgement, not independent proof.',
        '- Post-recovery result: use the verification event above, if present, and the actual terminal output.',
        '- Cause and improvement: in the controlled exercise, `SIMULATE_FAILURE=1` made production-lab `/health` return 500; document a proposed configuration validation and owner.',
        '',
        '## Reader decisions (required to finish the Record)', '',
        '- **Promotion:** What evidence justified moving this candidate to each environment?',
        '- **Recovery:** Was the previous release actually verified, retained and compatible, and who made that judgement?',
        '- **Improvement:** What control would reject the broken configuration before release; who owns the change and when will it be checked?',
        '',
        '## Evidence limitations', '',
        '- No real 5% canary, production traffic, AWS/ECR deployment, OIDC enforcement, protected approval, security scanning or signing was demonstrated.',
        '- The local image ID is not a remote registry digest; use the separate GitHub Actions exercise for registry-based identity.',
        '',
    ])
    return '\n'.join(lines)


def main():
    out = ROOT / '.lab' / 'evidence' / 'local-release-record.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_record(ROOT), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
