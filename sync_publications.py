#!/usr/bin/env python3
"""Sync the publication list on the Kun Universe docs from a SciX library.

Fetches the SciX library's bibcodes, resolves structured metadata through the
SciX search API, and writes `docs/source/publications_auto.rst` (the Sphinx
`publication.rst` page pulls it in via `.. include::`).

SciX (https://scixplorer.org) supersedes the NASA ADS website; it exposes the
same `/v1` REST API under a new host.

Environment:
    SCIX_API_TOKEN  SciX API token (required, from scixplorer.org/user/settings/token;
                    falls back to ADS_API_TOKEN for backwards compatibility)
    SCIX_LIB_ID     Library id (optional; defaults to the Kun publication library;
                    falls back to ADS_LIB_ID)

Usage:
    python sync_publications.py [--dry-run]   # --dry-run prints RST instead of writing
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

API = "https://api.scixplorer.org/v1"
DEFAULT_LIB_ID = "HmogSP7pQ2mJGCUovnBHGg"  # Kun Universe publication library
TOKEN_URL = "https://scixplorer.org/user/settings/token"
ABS_URL = "https://scixplorer.org/abs/{bibcode}/abstract"
FIELDS = ["bibcode", "title", "author", "year", "pubdate", "pub", "doi"]
ROWS = 200

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(HERE, "docs", "source", "publications_auto.rst")


def _request(method, url, payload=None, token=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")[:500]
        hint = {
            401: "SCIX_API_TOKEN is invalid or revoked — regenerate at " + TOKEN_URL,
            403: "token cannot access the library — confirm the library belongs to "
                 "the same SciX account that owns the token",
            404: "library not found — check SCIX_LIB_ID",
            400: "bad request — check query/fields in the script",
        }.get(err.code, "")
        raise SystemExit(f"SciX API {err.code} {err.reason} on {method} {url}\n  {hint}\n  {detail}") from None


def get_library_documents(lib_id, token):
    """Return the list of bibcodes in the library (paginated; the endpoint
    defaults to only 20 rows, so we page through by `num_documents`)."""
    docs, start, rows, total = [], 0, 200, None
    while True:
        url = (f"{API}/biblib/libraries/{urllib.parse.quote(lib_id)}"
               f"?start={start}&rows={rows}&fl=bibcode&sort=date%20desc")
        data = _request("GET", url, token=token)
        metadata = data.get("metadata") or {}
        if total is None:
            total = metadata.get("num_documents", 0)
            print(f"[scix] library '{metadata.get('name', lib_id)}': {total} papers")
        batch = data.get("documents") or []
        docs.extend(batch)
        start += rows
        if not batch or start >= total or len(batch) < rows:
            break
    return docs


def search_docs(bibcodes, token):
    """Resolve structured metadata for the given bibcodes (reverse chronological).

    Uses the search endpoint via GET (the endpoint does not accept POST).
    """
    if not bibcodes:
        return []
    query = " OR ".join(f'bibcode:"{b}"' for b in bibcodes)
    docs, start = [], 0
    while True:
        qs = urllib.parse.urlencode({
            "q": query,
            "fl": ",".join(FIELDS),
            "rows": ROWS,
            "start": start,
            "sort": "pubdate desc",
        }, safe=",")
        data = _request("GET", f"{API}/search/query?{qs}", token=token)
        found = data.get("response", {}).get("docs", [])
        docs.extend(found)
        num_found = data.get("response", {}).get("numFound", 0)
        start += len(found)
        if start >= num_found or not found:
            break
    return docs


def display_name(raw):
    """SciX author strings may be 'Family, Given' — normalize to 'Given Family'."""
    raw = (raw or "").strip()
    if ", " in raw:
        fam, given = raw.split(", ", 1)
        return (given.strip() + " " + fam.strip()).strip()
    return raw


def first_str(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def rst_escape(text):
    """Escape the characters that carry meaning in RST inline markup."""
    for ch in ("\\", "*", "`"):
        text = text.replace(ch, "\\" + ch)
    return text


def build_rst_publication(doc):
    """Format one SciX record as a three-line RST enumerated-list item."""
    title = rst_escape(first_str(doc.get("title")))
    authors = ", ".join(display_name(a) for a in (doc.get("author") or []))
    bibcode = doc.get("bibcode") or ""
    link = ABS_URL.format(bibcode=bibcode)
    return (
        f"#. | **{title}**\n"
        f"   | {authors}\n"
        f"   | `{bibcode} <{link}>`_"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="print RST to stdout instead of writing the file")
    args = parser.parse_args()

    token = (os.environ.get("SCIX_API_TOKEN")
             or os.environ.get("ADS_API_TOKEN") or "").strip()
    if not token:
        print(f"ERROR: SCIX_API_TOKEN is not set. Get one at {TOKEN_URL}",
              file=sys.stderr)
        sys.exit(1)
    lib_id = (os.environ.get("SCIX_LIB_ID")
              or os.environ.get("ADS_LIB_ID") or DEFAULT_LIB_ID).strip()

    bibcodes = get_library_documents(lib_id, token)
    docs = search_docs(bibcodes, token)

    items = [build_rst_publication(d) for d in docs]
    header = (
        ".. This file is auto-generated by sync_publications.py from the SciX\n"
        "   library. Do not edit by hand.\n"
        "\n"
    )
    blob = header + "\n".join(items) + "\n"
    print(f"[scix] wrote {len(items)} publications to {os.path.relpath(OUTPUT)}")

    if args.dry_run:
        sys.stdout.write(blob)
        return
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(blob)


if __name__ == "__main__":
    main()
