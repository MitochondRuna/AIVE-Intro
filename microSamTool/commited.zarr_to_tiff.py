#!/usr/bin/env python3
"""
microsam_committed_to_tiff.py
-----------------------------
Convert MICRO-SAM 'committed_objects' (Zarr array on disk) -> plain TIFF labels
(multipage .tif)

Requisites: numpy, tifffile
-conda activate micro-sam 
-pip install zarr tifffile 
-pip install zarr numcodecs tifffile numpy 

ASSUMPTIONS (micro-sam only):
  - Folder contains hidden ".zarray" JSON.
  - Chunk files are named "z.y.x" (e.g., 0.1.0).
  - Compressor is 'zlib'.
  - dimension_separator is '.'.
  - Integer label dtype (usually uint32), background = 0.

OUTPUT:
  - 2D labels -> single-page TIFF
  - 3D labels (Z,Y,X) -> multipage TIFF (one page per Z)

USAGE:
  python microsam_committed_to_tiff.py /path/to/committed_objects out_labels.tif
  python microsam_committed_to_tiff.py /path/to/committed_objects out_labels.tif --imagej
  python microsam_committed_to_tiff.py /path/to/committed_objects out_labels.tif --bigtiff --compression zlib
"""

from __future__ import annotations

import argparse
import json
import re
import zlib
from pathlib import Path
from typing import Tuple

import numpy as np
import tifffile

# ----------------------------
# Constants / small utilities
# ----------------------------

# Recognize chunk filenames like "0.1.0" -> (zc, yc, xc)
CHUNK_NAME_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

def _err(msg: str) -> None:
    """Exit with a clear error message."""
    raise SystemExit(f"ERROR: {msg}")


# ----------------------------
# Metadata I/O
# ----------------------------

def load_metadata(root: Path) -> Tuple[Tuple[int, ...], Tuple[int, ...], np.dtype]:
    """
    Read Zarr metadata from '.zarray' and validate micro-sam layout.

    Returns:
      shape  : (Z, Y, X)
      chunks : (Zc, Yc, Xc)
      dtype  : numpy dtype (e.g., uint32)
    """
    meta_path = root / ".zarray"
    if not meta_path.exists():
        _err(f"{meta_path} not found. Are you pointing at the 'committed_objects' folder?")

    meta = json.loads(meta_path.read_text())
    shape  = tuple(meta["shape"])           # e.g., (Z, Y, X)
    chunks = tuple(meta["chunks"])          # e.g., (Zc, Yc, Xc)
    dtype  = np.dtype(meta["dtype"])        # e.g., "<u4" -> uint32

    comp   = (meta.get("compressor") or {}).get("id", "zlib")
    dimsep = meta.get("dimension_separator", ".")

    if comp != "zlib":
        _err(f"compressor '{comp}' not supported (expected 'zlib').")
    if dimsep != ".":
        _err(f"dimension_separator '{dimsep}' not supported (expected '.').")

    return shape, chunks, dtype


# ----------------------------
# Chunk decoding + placement
# ----------------------------

def parse_chunk_name(name: str) -> Tuple[int, int, int] | None:
    """Return (zc, yc, xc) from '0.1.0' or None if it doesn't match."""
    m = CHUNK_NAME_RE.match(name)
    return tuple(map(int, m.groups())) if m else None


def chunk_roi(idx: Tuple[int, int, int],
              chunks: Tuple[int, int, int],
              shape: Tuple[int, int, int]) -> Tuple[slice, slice, slice]:
    """
    Compute the destination ROI (slices) in the full array for a chunk index.
    Handles edge tiles that are smaller than the nominal chunk size.
    """
    zc, yc, xc = idx
    z0, z1 = zc * chunks[0], min((zc + 1) * chunks[0], shape[0])
    y0, y1 = yc * chunks[1], min((yc + 1) * chunks[1], shape[1])
    x0, x1 = xc * chunks[2], min((xc + 1) * chunks[2], shape[2])
    return slice(z0, z1), slice(y0, y1), slice(x0, x1)


def decode_chunk_bytes(path: Path, dtype: np.dtype) -> np.ndarray:
    """Read a chunk file, zlib-decompress, and interpret as 1D array of dtype."""
    dec = zlib.decompress(path.read_bytes())
    return np.frombuffer(dec, dtype=dtype)


def reshape_chunk(flat: np.ndarray,
                  full_chunk_shape: Tuple[int, int, int],
                  roi_shape: Tuple[int, int, int]) -> np.ndarray:
    """
    Reshape a flat chunk into (Zc,Yc,Xc) and crop for edges,
    or accept already edge-sized chunks (matching roi_shape).
    """
    full_elems = int(np.prod(full_chunk_shape))
    roi_elems  = int(np.prod(roi_shape))

    if flat.size == full_elems:
        vol = flat.reshape(full_chunk_shape, order="C")
        z, y, x = roi_shape
        return vol[:z, :y, :x]
    if flat.size == roi_elems:
        return flat.reshape(roi_shape, order="C")

    _err(f"chunk size {flat.size} not compatible with full {full_chunk_shape} or edge {roi_shape}")


# ----------------------------
# Reconstruction
# ----------------------------

def reconstruct_volume(root: Path,
                       shape: Tuple[int, int, int],
                       chunks: Tuple[int, int, int],
                       dtype: np.dtype) -> np.ndarray:
    """
    Iterate all chunk files under 'root', decode and place them into a full array.
    Missing chunks remain 0 (background).
    """
    print("[step] Allocating output array…")
    arr = np.zeros(shape, dtype=dtype)

    placed = 0
    for p in root.iterdir():
        if not p.is_file():
            continue
        idx = parse_chunk_name(p.name)
        if idx is None:
            continue

        zsl, ysl, xsl = chunk_roi(idx, chunks, shape)
        roi_shape = (zsl.stop - zsl.start, ysl.stop - ysl.start, xsl.stop - xsl.start)

        flat      = decode_chunk_bytes(p, dtype)
        chunk_vol = reshape_chunk(flat, chunks, roi_shape)

        arr[zsl, ysl, xsl] = chunk_vol
        placed += 1

    if placed == 0:
        _err("found zero chunk files. Is this the correct folder?")
    print(f"[info] Placed {placed} chunk(s).")
    return arr


# ----------------------------
# Output helpers
# ----------------------------


def write_plain_tiff(path: Path,
                     data: np.ndarray,
                     compression: str | None,
                     bigtiff: bool,
                     imagej: bool) -> None:
    """
    Write a plain TIFF (non-OME). If imagej=True, write ImageJ hyperstack tags
    so Fiji opens it as a stack (still a .tif, not OME-XML).

    For 3D data with shape (Z, Y, X), this writes a multipage TIFF (one page per Z).
    """
    # Normalize compression arg for tifffile
    comp = None if (compression is None or compression.lower() == "none") else compression

    # Ensure dtype is integer (labels). If bool, make it uint8.
    if data.dtype == np.bool_:
        data = data.astype(np.uint8, copy=False)

    # photometric='minisblack' is appropriate for grayscale/label integer data
    print(f"[step] Writing TIFF → {path} (pages={data.shape[0] if data.ndim==3 else 1}, "
          f"compression={comp or 'none'}, imagej={'yes' if imagej else 'no'})")

    # tifffile handles (Z,Y,X) as multipage. imagej=True adds ImageJ tags.
    tifffile.imwrite(
        path.as_posix(),
        data,
        compression=comp,
        bigtiff=bigtiff,
        imagej=imagej,           # still a plain .tif, just with ImageJ metadata
        photometric="minisblack"
    )
    print("[done] Saved:", path)


# ----------------------------
# CLI
# ----------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MICRO-SAM committed_objects → plain TIFF labels (.tif)")
    p.add_argument("committed_dir", help="Path to micro-sam 'committed_objects' folder (contains .zarray).")
    p.add_argument("out_tiff", help="Output TIFF path (e.g., labels.tif).")
    p.add_argument("--keep-uint32", action="store_true",
                   help="Keep uint32 even if downcast to uint16 would be safe.")
    p.add_argument("--bigtiff", action="store_true",
                   help="Write BigTIFF (recommended if output may exceed ~4 GB).")
    p.add_argument("--compression", default="zlib",
                   help="TIFF compression: zlib (default), lzw, none.")
    p.add_argument("--imagej", action="store_true",
                   help="Add ImageJ hyperstack tags (still .tif, not OME).")
    return p.parse_args()


# ----------------------------
# Main
# ----------------------------

def main() -> None:
    args = parse_args()

    root = Path(args.committed_dir)
    out  = Path(args.out_tiff)

    print("[step] Reading metadata (.zarray)…")
    shape, chunks, dtype = load_metadata(root)
    print(f"[info] shape={shape} chunks={chunks} dtype={dtype}")

    print("[step] Reconstructing volume from chunks…")
    vol = reconstruct_volume(root, shape, chunks, dtype)
    print(f"[info] volume: shape={vol.shape}, dtype={vol.dtype}, max={int(vol.max())}")


    # Write as plain TIFF (2D -> single image, 3D -> multipage stack)
    write_plain_tiff(out, vol, compression=args.compression, bigtiff=args.bigtiff, imagej=args.imagej)


if __name__ == "__main__":
    main()
