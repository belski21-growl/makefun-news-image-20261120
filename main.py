"""News image publisher for make.fun — news-image-20261120.

A one-image entry: "Sum up 20 November's world news in one image".

The artwork itself ships beside this script as ``entry.png``.  This program
does not draw, fetch, or modify anything.  Its whole job is to hand the
shipped artwork over to the output directory, but only after proving —
twice, once on the source and once on the copy — that the bytes are exactly
the artwork we shipped.  Any surprise (wrong size, wrong hash, a JPEG that
does not start and end the way a JPEG must) aborts loudly instead of
publishing a corrupt file.

Pure standard library, no network, no randomness: the same input always
produces the same output, byte for byte.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

# --- The shipped artwork, as measured when it was packed -------------------
# entry.png: 317693 bytes, verified live with sha256sum before this rewrite.
ARTWORK_NAME = "entry.png"
ARTWORK_BYTES = 317693
ARTWORK_SHA256 = "5e74b9b8d3819915a6ff00d837f0d9a2447bab4cab2c2ddeaa59b919500a807f"

# JPEG framing markers: a file must open with SOI and close with EOI.
JPEG_OPEN = b"\xff\xd8"   # Start Of Image
JPEG_CLOSE = b"\xff\xd9"  # End Of Image

DEFAULT_OUTPUT_DIR = Path("/output")


@dataclass(frozen=True)
class ArtworkReport:
    """Everything we measured about one file holding the artwork."""

    path: Path
    size: int
    sha256: str
    opens_as_jpeg: bool
    closes_as_jpeg: bool

    @property
    def is_sound(self) -> bool:
        """True only when every measured fact matches the shipped artwork."""
        return (
            self.size == ARTWORK_BYTES
            and self.sha256 == ARTWORK_SHA256
            and self.opens_as_jpeg
            and self.closes_as_jpeg
        )

    def complaints(self) -> list[str]:
        """Human-readable list of every mismatch found, empty when sound."""
        gripes: list[str] = []
        if self.size != ARTWORK_BYTES:
            gripes.append(
                f"size is {self.size} bytes, expected {ARTWORK_BYTES}"
            )
        if self.sha256 != ARTWORK_SHA256:
            gripes.append(
                f"SHA-256 is {self.sha256}, expected {ARTWORK_SHA256}"
            )
        if not self.opens_as_jpeg:
            gripes.append("missing JPEG SOI marker (FFD8) at the start")
        if not self.closes_as_jpeg:
            gripes.append("missing JPEG EOI marker (FFD9) at the end")
        return gripes


def measure(path: Path) -> ArtworkReport:
    """Read a file and report its size, hash, and JPEG framing markers."""
    blob = path.read_bytes()
    return ArtworkReport(
        path=path,
        size=len(blob),
        sha256=hashlib.sha256(blob).hexdigest(),
        opens_as_jpeg=blob[:2] == JPEG_OPEN,
        closes_as_jpeg=blob[-2:] == JPEG_CLOSE,
    )


def insist_sound(report: ArtworkReport, role: str) -> None:
    """Abort with a clear error unless the measured file is the artwork."""
    problems = report.complaints()
    if problems:
        detail = "; ".join(problems)
        raise SystemExit(f"error: {role} {report.path} failed verification: {detail}")


def hand_over(source: Path, out_dir: Path) -> Path:
    """Verify the source, copy it, then verify the copy. Returns the copy."""
    checked_source = measure(source)
    insist_sound(checked_source, "source")

    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ARTWORK_NAME
    target.write_bytes(source.read_bytes())

    checked_target = measure(target)
    insist_sound(checked_target, "output")
    if checked_target.sha256 != checked_source.sha256:
        raise SystemExit(
            f"error: output {target} differs from source {source} after copy"
        )
    # Belt and braces: the hashes already agree, but confirm the bytes
    # themselves are identical before declaring success.
    if target.read_bytes() != source.read_bytes():
        raise SystemExit(
            f"error: output {target} bytes differ from source {source}"
        )
    return target


def main(argv: list[str]) -> int:
    """Publish entry.png to /output (or argv[1] when given)."""
    if len(argv) > 2:
        print(
            "usage: main.py [output-dir]",
            file=sys.stderr,
        )
        return 2

    here = Path(__file__).resolve().parent
    source = here / ARTWORK_NAME
    if not source.is_file():
        print(f"error: shipped artwork not found: {source}", file=sys.stderr)
        return 1

    out_dir = Path(argv[1]) if len(argv) == 2 else DEFAULT_OUTPUT_DIR
    published = hand_over(source, out_dir)
    print(f"published {published} ({ARTWORK_BYTES} bytes, SHA-256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
