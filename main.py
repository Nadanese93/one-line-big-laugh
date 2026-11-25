#!/usr/bin/env python3
"""One Line, Big Laugh — Make.fun micro bounty entry.

Writes a single one-line joke to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""
import os
import sys
import tempfile

ENTRY = (
    "I returned a library book 30 years late \u2014 the fine was $8,400, "
    "so they gave me a payment plan, a plaque, and a key to the new wing "
    "I'd basically funded."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    text = ENTRY
    if not isinstance(text, str) or not text.strip():
        print("entry must not be whitespace-only", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    encoded = text.encode("utf-8")
    if not 1 <= len(text) <= 200:
        print(f"entry must be 1-200 chars, got {len(text)}", file=sys.stderr)
        return 1
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(encoded)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
        # Read-back verification: the file on disk must be byte-identical
        # to what was written, otherwise the entry is not trustworthy.
        with open(target, "rb") as fh:
            if fh.read() != encoded:
                raise IOError("read-back verification failed for entry.txt")
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
