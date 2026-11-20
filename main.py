"""news-image-20261120 entry: write the pre-rendered front page to /output/entry.png.

The image is a static file shipped in this repository (entry.png, JPEG bytes
under the .png name, as the rules allow). This program deterministically
copies its exact bytes to the output directory. Standard library only, no
network access, no randomness: two runs write byte-identical output.

Integrity is checked twice: the shipped source is verified before copying
(size, SHA-256 and the JPEG start/end markers), and the written copy is
verified again afterwards, so a corrupt source or a truncated write fails
loudly instead of shipping a broken image to the judge.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Fingerprint of the shipped image, recorded at build time (20 Nov 2026).
EXPECTED_SIZE = 317693
EXPECTED_SHA256 = "5e74b9b8d3819915a6ff00d837f0d9a2447bab4cab2c2ddeaa59b919500a807f"
JPEG_SOI = b"\xff\xd8"  # start of image
JPEG_EOI = b"\xff\xd9"  # end of image

CHUNK = 65536


def _fail(message: str) -> "SystemExit":
    return SystemExit("error: news-image-20261120: " + message)


def _sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _check_jpeg_markers(path: str, size: int) -> None:
    """The file must start with SOI and end with EOI: a whole JPEG image,
    every segment through to its end marker, as the rules require."""
    with open(path, "rb") as f:
        head = f.read(2)
        f.seek(max(0, size - 2))
        tail = f.read(2)
    if head != JPEG_SOI:
        raise _fail(
            "%s does not start with the JPEG SOI marker (FFD8); "
            "not a whole JPEG image" % path
        )
    if tail != JPEG_EOI:
        raise _fail(
            "%s does not end with the JPEG EOI marker (FFD9); "
            "image is truncated" % path
        )


def _verify(path: str, role: str) -> None:
    size = os.path.getsize(path)
    if size != EXPECTED_SIZE:
        raise _fail(
            "%s %s is %d bytes, expected %d; refusing to continue"
            % (role, path, size, EXPECTED_SIZE)
        )
    if _sha256_of(path) != EXPECTED_SHA256:
        raise _fail("%s %s failed its SHA-256 check" % (role, path))
    _check_jpeg_markers(path, size)


def _prepare_output_dir(out_dir: str) -> str:
    """Validate the output directory before any write happens, so a bad
    destination fails fast with a clear message instead of dying mid-copy."""
    if not out_dir:
        raise _fail(
            "MAKEFUN_OUTPUT_DIR is set but empty; unset it to use /output"
        )
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        raise _fail(
            "output path %s exists and is not a directory; "
            "point MAKEFUN_OUTPUT_DIR at a directory" % out_dir
        )
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        raise _fail("cannot create output directory %s: %s" % (out_dir, exc))
    if not os.access(out_dir, os.W_OK):
        raise _fail("output directory %s is not writable" % out_dir)
    return out_dir


def main() -> int:
    out_dir = _prepare_output_dir(
        os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    )
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if os.path.isdir(dst):
        raise _fail(
            "output path %s is a directory, cannot write the image there"
            % dst
        )

    # 1. Verify the shipped source before copying anything.
    if not os.path.isfile(src):
        raise _fail("shipped image missing: %s not found" % src)
    _verify(src, "source")

    # 2. Stream-copy the bytes (never loads the whole file into memory).
    try:
        with open(src, "rb") as f_in, open(dst, "wb") as f_out:
            while True:
                chunk = f_in.read(CHUNK)
                if not chunk:
                    break
                f_out.write(chunk)
    except OSError as exc:
        raise _fail("failed writing %s: %s" % (dst, exc))

    # 3. Verify the written copy: size + SHA-256 + JPEG markers.
    _verify(dst, "output")
    return 0


if __name__ == "__main__":
    sys.exit(main())
