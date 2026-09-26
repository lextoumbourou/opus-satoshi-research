#!/usr/bin/env python3
"""Fetch raw Bitcoin block headers (80 bytes each) in bulk from a public
Electrum server (blockchain.block.headers, up to 2016 per call) and save
height, hash, nTime, nBits, nonce to CSV. Verifies each header's
prev-hash link and proof-of-work target.

Usage: fetch_headers_electrum.py START END OUT.csv
"""
import csv, hashlib, json, socket, ssl, struct, sys, time

SERVERS = [("electrum.blockstream.info", 50002), ("electrum.emzy.de", 50002), ("bitcoin.lukechilds.co", 50002),
           ("fortress.qtornado.com", 443), ("electrum.bitaroo.net", 50002)]


def dsha(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


class Electrum:
    def __init__(self):
        last = None
        for host, port in SERVERS:
            try:
                ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                s = socket.create_connection((host, port), timeout=30)
                self.s = ctx.wrap_socket(s, server_hostname=host); self.f = self.s.makefile("rwb"); self.id = 0
                self.call("server.version", ["satoshi-research", "1.4"]); print("connected", host, file=sys.stderr)
                return
            except Exception as e:
                last = e
        raise SystemExit(f"no server: {last}")

    def call(self, method, params):
        self.id += 1
        self.f.write((json.dumps({"id": self.id, "method": method, "params": params}) + "\n").encode()); self.f.flush()
        while True:
            r = json.loads(self.f.readline())
            if r.get("id") == self.id:
                if "error" in r and r["error"]:
                    raise RuntimeError(r["error"])
                return r["result"]


def main(start, end, out):
    e = Electrum(); rows = []; prev = None; h = start
    while h <= end:
        n = min(2016, end - h + 1)
        res = e.call("blockchain.block.headers", [h, n])
        raw = bytes.fromhex(res["hex"])
        for i in range(res["count"]):
            hd = raw[80 * i : 80 * i + 80]
            ver, prevh, merkle, ntime, bits, nonce = struct.unpack("<I32s32sIII", hd)
            bh = dsha(hd)[::-1].hex()
            if prev is not None:
                assert prevh[::-1].hex() == prev, f"chain break at {h + i}"
            exp, mant = bits >> 24, bits & 0xFFFFFF
            target = mant * (1 << (8 * (exp - 3)))
            assert int(bh, 16) <= target, f"bad pow at {h + i}"
            rows.append((h + i, bh, ntime, hex(bits), nonce)); prev = bh
        h += res["count"]; time.sleep(0.3)
    with open(out, "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(["height", "hash", "ntime", "bits", "nonce"]); w.writerows(rows)
    print(f"wrote {len(rows)} headers {start}..{end}", file=sys.stderr)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
