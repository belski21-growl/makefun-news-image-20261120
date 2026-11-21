"""Publish the r2 front-page artwork for make.fun — news-image-20261120.

The entry is one image, "THE WORLD IN ONE DAY — Friday, 20 November
2026", shipped beside this script as ``entry.png`` (a JPEG file carrying
the .png name, which the rules allow: the format is told apart by the
first bytes).  This program draws nothing, fetches nothing and writes
nothing but the one output file.  It reads the shipped artwork, proves
it is exactly the file that was packed (byte count, SHA-256, and the
JPEG start/end markers), copies it to the output directory, and proves
the copy the same way before reporting success.  Any mismatch aborts
with a plain error message and a non-zero exit code.

Standard library only, no network, no randomness: the same shipped
file always publishes the same bytes.
"""

import hashlib
import shutil
import sys
from pathlib import Path

# The artwork as packed for round 2 (measured live with sha256sum).
FILE_NAME = "entry.png"
EXPECTED_SIZE = 341440
EXPECTED_SHA256 = (
    "aba7330862a21dad7dabacbf7aeabb5feb02ca7047d5547e5db34dd272599fdc"
)

# A JPEG must begin with SOI (FFD8) and end with EOI (FFD9).
SOI = b"\xff\xd8"
EOI = b"\xff\xd9"

DEFAULT_OUT = Path("/output")


def die(message):
    """Print an error and stop the run without publishing anything."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest_file(path):
    """Return (size, sha256 hex) for the file at *path*."""
    data = Path(path).read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def framing_ok(path):
    """True when the file opens with FFD8 and closes with FFD9."""
    data = Path(path).read_bytes()
    return data[:2] == SOI and data[-2:] == EOI


def check_file(path, label):
    """Refuse unless *path* is byte-for-byte the packed artwork."""
    size, digest = digest_file(path)
    if size != EXPECTED_SIZE:
        die(f"{label} {path}: {size} bytes, expected {EXPECTED_SIZE}")
    if digest != EXPECTED_SHA256:
        die(f"{label} {path}: SHA-256 {digest}, expected {EXPECTED_SHA256}")
    if not framing_ok(path):
        die(f"{label} {path}: not a whole JPEG (missing FFD8 start or FFD9 end)")


def publish_entry(source, out_dir):
    """Verify the shipped file, copy it, verify the copy. Return its path."""
    check_file(source, "source")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / FILE_NAME
    shutil.copyfile(source, target)
    check_file(target, "output")
    # The hashes already agree, but confirm the bytes themselves match
    # before declaring success: a hash collision in theory, a bad copy
    # in practice, would both slip past a hash-only check.
    if target.read_bytes() != source.read_bytes():
        die(f"output {target} bytes differ from source {source} after copy")
    return target


def run(argv):
    """Publish entry.png to /output, or to argv[1] when given."""
    if len(argv) > 2:
        print("usage: main.py [output-dir]", file=sys.stderr)
        return 2
    here = Path(__file__).resolve().parent
    source = here / FILE_NAME
    if not source.is_file():
        die(f"shipped artwork not found: {source}")
    out_dir = Path(argv[1]) if len(argv) == 2 else DEFAULT_OUT
    target = publish_entry(source, out_dir)
    print(f"published {target} ({EXPECTED_SIZE} bytes, SHA-256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv))
