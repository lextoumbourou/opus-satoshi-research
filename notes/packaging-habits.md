# Release-packaging habits: Satoshi vs candidates (VERIFIED data; INFERENCE weak-moderate)

Satoshi (2008–2010):
- Windows-native packaging: WinRAR (<3.62) in 2008–09, then Info-ZIP 2.3 on Win32/NTFS with NT security-descriptor extra fields.
- **Every release's file times normalised to the version number** (00:00:01 = 0.0.1; 01:00 = 0.1.0; 01:01…01:03 for patches; 02:00 = 0.2.0; 01:01 for 0.3.x point releases).
- Linux tarballs built as root.
- Machine on UK time.

| Candidate | Archive examined (original bytes) | Packing platform | Owner / user | File times | Machine zone at the time |
|---|---|---|---|---|---|
| Adam Back | hashcash-1.18…1.22 .tgz/.zip, win32 exe/dll zips (2005–06), hashcash.org | **Info-ZIP 2.3 on Unix** (Windows binaries packed on Linux) | `adam` uid 500 | natural | UK (+0 Mar 2006 / +1 Apr 2006) |
| Adam Back | credlib-0.08/0.09 .tgz/.zip (Feb–Mar 2007), cypherspace.org | Info-ZIP 2.3 on Unix | `adam` 500 (0.09); 0.08 tarred on the web host as `u35279131/ftpusers`, a 1&1-style account name | natural | **N. American Eastern** (−5 Feb / −4 Mar 2007, new US/Canada DST rule) |
| Wei Dai | cryptopp552.zip (Aug 2007), cryptopp560.zip (Mar 2009), originals via Wayback | Windows zipper, host 0 / v2.0 (Explorer-style) | n/a | natural | n/a (no UTC fields) |
| Len Sassaman | mixmaster_3.0.0.orig.tar.gz (3 Mar 2008), Debian snapshot (upstream bytes) | GNU tar, Linux | **`rabbi`** (Sassaman's handle) | natural | n/a |
| Hal Finney | bitcoin-0.1.0.tgz repack (Jan 2009) | GNU tar, Linux | `hal` 500 | preserved Satoshi's | US Pacific (−8) |

Observations:
- None of the candidates' own releases shows Satoshi's version-number timestamp habit, and the two Linux-centric candidates (Back, Sassaman) packaged on Unix.
- Satoshi's release engineering looks like a Windows-first developer's, in the style of Microsoft product releases. That fits his own statements ("Everything is always harder to build on Windows than Linux"; testing with "MSVC 6.0 SP6 and GCC 3.4.5").
- Back's machine zone tracked his location (UK 2006 → N. America 2007 → UK 2008 → Malta 2010+).
- Caveat: habits change, and a careful Satoshi could adopt habits different from his public persona. Weak-to-moderate evidence against Back and Sassaman as the *packager*. (Satoshi's packaging was the same one machine from mid-2010 onward.)
