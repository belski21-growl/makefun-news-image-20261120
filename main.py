"""Ship the r2-fix front-page artwork for make.fun - news-image-20261120.

The entry is one image, "THE WORLD IN ONE DAY - Friday, 20 November
2026", shipped beside this script as ``entry.png``. The file is really a
JPEG (the rules tell the format apart by its first bytes, so the .png
name is fine). This program draws nothing, reaches for no network and
writes nothing but the one output file: it fingerprints the shipped
artwork (byte count, SHA-256, and the JPEG start/end markers), streams
it to the output directory in 64 KiB chunks, then fingerprints the copy
the same way and refuses to report success unless the two fingerprints
agree exactly. Any mismatch stops the run with a plain error message
and a non-zero exit code.

Python 3.13, standard library only, fully deterministic: the same
shipped file always publishes the same bytes.
"""

import hashlib
import os
import sys

# The artwork as packed for the r2-fix round (measured live with sha256sum).
FILE_NAME = "entry.png"
EXPECTED_SIZE = 373859
EXPECTED_SHA256 = (
    "e0010bd35157f8d5916b19b2c5aae20d97827f2c60a2262e44fcd7812ea77b5b"
)
SIZE_LIMIT = 1048576

# A JPEG must begin with SOI (FFD8) and end with EOI (FFD9).
SOI = b"\xff\xd8"
EOI = b"\xff\xd9"

CHUNK = 65536
DEFAULT_OUT = "/output"


def fail(message):
    """Stop the run with a plain error; nothing is published."""
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_fingerprint(path):
    """Return (size, sha256 hex, first-two-bytes, last-two-bytes)."""
    digest = hashlib.sha256()
    size = 0
    head = b""
    tail = b""
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            if size == 0:
                head = block[:2]
            tail = block[-2:]
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest(), head, tail


def jpeg_segments_sound(path):
    """Walk the JPEG marker segments from SOI to EOI.

    A file can carry the right first and last bytes yet be truncated
    in the middle, so prove the structure too: every marker must have
    its declared length inside the file, and the walk must land exactly
    on the EOI marker at the end. Returns True when the walk succeeds.
    """
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) < 4 or data[:2] != SOI:
        return False
    pos = 2
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            return False
        marker = data[pos + 1]
        if marker == 0xD9:  # EOI
            return pos + 2 == len(data)
        if marker == 0xD8 or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            pos += 2  # standalone marker, no length field
            continue
        if pos + 4 > len(data):
            return False
        length = (data[pos + 2] << 8) | data[pos + 3]
        if length < 2 or pos + 2 + length > len(data):
            return False
        pos += 2 + length
        if marker == 0xDA:  # SOS: compressed scan data follows.
            # Scan data runs to EOI; 0xFF00 is a stuffed data byte and
            # 0xFFD0-0xFFD7 are restart markers, not segment headers.
            while pos + 1 < len(data):
                if data[pos] != 0xFF:
                    pos += 1
                    continue
                following = data[pos + 1]
                if following == 0x00 or 0xD0 <= following <= 0xD7:
                    pos += 2
                    continue
                if following == 0xD9:  # EOI
                    return pos + 2 == len(data)
                return False
            return False
    return False


def confirm_artwork(path, label):
    """Refuse unless *path* is byte-for-byte the packed artwork."""
    if not os.path.isfile(path):
        fail(label + " artwork not found: " + path)
    size, digest, head, tail = read_fingerprint(path)
    if size != EXPECTED_SIZE:
        fail("%s %s: %d bytes, expected %d"
             % (label, path, size, EXPECTED_SIZE))
    if size > SIZE_LIMIT:
        fail("%s %s: %d bytes, over the 1 MiB limit"
             % (label, path, size))
    if digest != EXPECTED_SHA256:
        fail("%s %s: SHA-256 %s, expected %s"
             % (label, path, digest, EXPECTED_SHA256))
    if head != SOI or tail != EOI:
        fail(label + " " + path
             + ": not a whole JPEG (missing FFD8 start or FFD9 end)")
    if not jpeg_segments_sound(path):
        fail(label + " " + path
             + ": JPEG marker walk does not reach a clean EOI")


def ship(source, out_dir):
    """Verify the shipped file, stream-copy it, verify the copy."""
    confirm_artwork(source, "source")
    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError as exc:
            fail("cannot create output directory %s: %s" % (out_dir, exc))
    target = os.path.join(out_dir, FILE_NAME)
    if os.path.abspath(target) == os.path.abspath(source):
        fail("output %s is the shipped file itself; refusing to copy "
             "a file onto itself" % target)
    with open(source, "rb") as reader, open(target, "wb") as writer:
        while True:
            block = reader.read(CHUNK)
            if not block:
                break
            writer.write(block)
    confirm_artwork(target, "output")
    return target


def main(argv):
    """Publish entry.png to /output, or to argv[1] when given."""
    if len(argv) > 2:
        print("usage: main.py [output-dir]", file=sys.stderr)
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, FILE_NAME)
    out_dir = argv[1] if len(argv) == 2 else DEFAULT_OUT
    target = ship(source, out_dir)
    print("published %s (%d bytes, SHA-256 verified)"
          % (target, EXPECTED_SIZE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
