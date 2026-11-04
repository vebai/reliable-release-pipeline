"""Append a local teaching-lab event; not a signed or tamper-evident audit log."""
import argparse
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / '.lab' / 'evidence' / 'events.jsonl'
IMAGE_PATTERN = re.compile(r'^sha256:[0-9a-f]{64}$')
REVISION_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
ALLOWED = {
    'BUILD': {'BUILT'},
    'PROMOTE': {'DEPLOYED_UNVERIFIED'},
    'VERIFY': {'PASS', 'FAIL'},
    'RECOVER': {'STARTED', 'VERIFIED', 'FAILED'},
}


def append_event(path, event, environment, image_id, revision, status, note=''):
    if event not in ALLOWED or status not in ALLOWED[event]:
        raise ValueError('Invalid event type or status')
    if environment not in ('local', 'staging', 'production'):
        raise ValueError('Invalid environment')
    if event == 'BUILD' and environment != 'local':
        raise ValueError('Build event environment must be local')
    if event != 'BUILD' and environment == 'local':
        raise ValueError('Deployment event requires staging or production')
    if not IMAGE_PATTERN.fullmatch(image_id):
        raise ValueError('Expected a complete Docker image ID')
    if not REVISION_PATTERN.fullmatch(revision):
        raise ValueError('Expected a local revision label')
    if note not in ('', 'normal', 'simulated-health-500', 'http-check-failed',
                    'known-good-verified', 'compatibility-acknowledged'):
        raise ValueError('Unsupported note')
    entry = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'event': event,
        'environment': environment,
        'image_id': image_id,
        'revision_label': revision,
        'status': status,
        'note': note,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as out:
        out.write(json.dumps(entry, sort_keys=True) + '\n')
    return entry


def read_events(path):
    if not path.is_file():
        return []
    events = []
    for line_no, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        try:
            event = json.loads(raw)
            if not isinstance(event, dict) or not all(
                key in event for key in ('timestamp_utc', 'event', 'environment',
                                          'image_id', 'revision_label', 'status', 'note')
            ):
                raise ValueError('missing event fields')
            if event['event'] not in ALLOWED or event['status'] not in ALLOWED[event['event']]:
                raise ValueError('unexpected event/status')
            if not IMAGE_PATTERN.fullmatch(event['image_id']):
                raise ValueError('invalid image ID')
            if not REVISION_PATTERN.fullmatch(event['revision_label']):
                raise ValueError('invalid revision label')
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
            raise ValueError(f'Invalid journal entry at line {line_no}: {exc}') from exc
        events.append(event)
    return events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('event', choices=sorted(ALLOWED))
    parser.add_argument('environment', choices=('local', 'staging', 'production'))
    parser.add_argument('image_id')
    parser.add_argument('revision')
    parser.add_argument('status')
    parser.add_argument('--note', default='')
    args = parser.parse_args()
    append_event(JOURNAL, args.event, args.environment, args.image_id,
                 args.revision, args.status, args.note)


if __name__ == '__main__':
    main()
