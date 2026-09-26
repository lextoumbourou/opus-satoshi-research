## Satoshi's Coins

This repo contains:

1. Information on **The Patoshi Pattern** -- clues identifying Satoshi's 1.1 Million BTC.
2. Software for **reassigning** a subset of Satoshi's coins, via hardfork. This is called the "Satoshi Half-Airdrop" (SHAD).


## 1. Information

How Satoshi marked his coins:

* Sergio Demian Lerner's 2013 Research -- [here](https://bitslog.com/2013/04/17/the-well-deserved-fortune-of-satoshi-nakamoto/), [here](https://bitslog.com/2020/08/22/the-patoshi-mining-machine/), [here](https://bitslog.com/2019/04/16/the-return-of-the-deniers-and-the-revenge-of-patoshi/), and [here](https://bitslog.com/2020/06/22/a-new-mystery-in-patoshi-timestamps/#comment-59299).
* W_S_Bitcoin's Latest Research -- see [here](https://x.com/w_s_bitcoin/status/2069812036184281284), [here](https://x.com/w_s_bitcoin/status/2058919808549175720), [here](https://x.com/BITCOINALLCAPS/status/2060077325845180872), [here](https://x.com/w_s_bitcoin/status/2060308541349490792), and especially [WickedSmartBitcoin.com/patoshi_pattern](https://wickedsmartbitcoin.com/patoshi_pattern).
* [Jameson Lopp's Patoshi Tools](https://github.com/jlopp/bitcoin-utils/tree/master). Specifically, [findPatoshiMiningStreaks.php](https://github.com/jlopp/bitcoin-utils/blob/eb5b7cfe98ea846a30ffd87b04e9a4137cf3bde7/findPatoshiMiningStreaks.php#L3) — the source for block-heights in `patoshi-blocks.txt`.

SHAD - The Satoshi Half-Airdrop:

* ["Stealing Satoshi's Coins" -- You'll Thank Me Later](https://x.com/Truthcoin/status/2076672742351425702?s=20)
* [The Moral Case for SHAD](https://hidden.ecash.com/003f02a73a2700c4c7747415fdcc72f5ad06067ab7c46ec43d1e8daa8a45a4fc/shad.pdf)


## 2. Software

### Input Files

| File | Role |
|---|---|
| `patoshi-blocks.txt` | Input block-height list for step 1 (21,953 heights available) |
| `dryrun-3.csv` | Raw destination set: `no, quantity, Address, P2PKH Script, WIF` |
| `fetch_coinbase.py` | Step 1 — fetches coinbase outputs via Esplora explorers |
| `parse_destinations.py` | Step 2 — validates addresses ↔ scripts, converts to sats |
| `txlib.py` | Legacy (pre-segwit) tx serializer + txid; self-tested vs block 170 |
| `build_reassignment.py` | Steps 3–7 — builds the txs, emits the deliverables |
| `verify_build.py` | Independent verifier — decodes raw hex without `txlib` |


### Generated files

| File | Produced by | Notes |
|---|---|---|
| `coinbase-utxos.csv` | step 1 | ~10,010 rows, 2.2 MB. **Slow to rebuild** — thousands of live explorer calls, subject to rate limits. Worth keeping as a cached input even though it's derived. |
| `destinations.csv` | step 2 | 122 P2PKH destinations, 421,651 BTC total. Rebuilds instantly. |
| `reassignment-txs.csv` | step 4 | **CRITICAL FILE:** `txid, raw_hex`. |
| `reassignment-audit.csv` | step 4 | Per-tx metadata, joins to the deliverable on `txid`. |


### Details

Builds a set of Bitcoin transactions that reassign the value in early
"patoshi" coinbase outputs to a defined list of destination addresses.

Each transaction spends coinbase UTXOs as inputs and pays out P2PKH destinations
plus one change output. The transactions are serialized with **empty
scriptSigs** — they are meant to be [whitelisted by txid in a modified node](https://github.com/ecash-com/bitcoin/blob/drynet3/src/repo_txns.h]
(`setRepurposeTx` in `repo_txns.h`), which skips script verification for those
txids, so no signing or private keys are ever involved.

The critical file is `reassignment-txs.csv` (txid + raw hex per tx). The node's
`setRepurposeTx` txid set is not built here, it is just the `txid` column of
that CSV, trivially reproduced in whatever form the node needs.


### Pipeline

Run in order from the repo root. Python 3, standard library only — nothing to
install.

```
# Step 1 — fetch coinbase UTXOs for every height in patoshi-blocks.txt
#   Needs network access (blockstream.info + mempool.space). Resumable.
#   Default caps at 10,010 blocks (~500,502 BTC), enough to fund the payout.
python3 fetch_coinbase.py            # -> coinbase-utxos.csv

# Step 2 — parse the raw destination list into a validated set
python3 parse_destinations.py        # dryrun-3.csv -> destinations.csv

# Step 3 — self-test the serializer (optional but recommended)
python3 txlib.py                     # reproduces the block-170 tx exactly

# Step 4 — build the reassignment transactions
#   Args: [FEE_RATE_SAT_VB=100] [N_TX=one-tx-per-destination]
python3 build_reassignment.py        # -> reassignment-txs.csv,
                                     #    reassignment-audit.csv

# Step 5 — independently verify the built transactions
python3 verify_build.py              # re-decodes raw hex, checks conservation
```


### Design decisions

- **Empty scriptSigs.** Every input uses a 0-byte scriptSig (varint `0x00`),
  not a placeholder. The node skips `CheckInputScripts` for whitelisted txids,
  so scriptSig content is irrelevant to validity, and empty passes all other
  consensus/standardness checks. This choice is load-bearing: **the txid is the
  double-SHA256 of the empty-scriptSig serialization.** Do not change the
  scriptSig form after txids are generated — it changes every txid.

- **Inputs consumed in ascending block-height order, minimized.** Only as many
  coinbase UTXOs as needed to cover outputs + fee + change are used.

- **Change → genesis-block P2PK pubkey.** Change from each tx goes to the
  genesis coinbase pubkey (`4104678afdb0…d5fac`). Chosen because the genesis
  coinbase is not in the input set (no self-reference) and is
  consensus-unspendable (not in the UTXO set), so the change key carries only
  change.

- **Batching.** Default is one transaction per destination (max auditability).
  Pass `N_TX` to instead balance destinations into `N_TX` groups. Either way
  the whole set fits in a single ~1 MB block.

### Current build parameters

122 txs (one per destination), fee 100 sat/vByte, ~8,512 of ~10,010 inputs
consumed, ~3,950 BTC change to genesis, whole set ~0.364 MB. All build-time and
verifier checks pass.

