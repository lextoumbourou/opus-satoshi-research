| source_type | venue group | items | with UTC timestamp | earliest (UTC) | latest (UTC) |
|---|---|---:|---:|---|---|
| code_comment | Bitcoin pre-release source | 5 | 0 | - | - |
| code_comment | Bitcoin v0.1.0 source | 23 | 0 | - | - |
| email | private email | 185 | 181 | 2008-08-20T17:30:39Z | 2011-04-26T08:29:00Z |
| forum | SourceForge project news | 1 | 1 | 2009-01-13T20:46:54Z | 2009-01-13T20:46:54Z |
| forum | bitcointalk.org | 539 | 539 | 2009-11-22T18:04:28Z | 2010-12-12T18:22:33Z |
| mailing_list | bitcoin-list@lists.sourceforge.net | 16 | 16 | 2008-12-10T17:00:23Z | 2010-12-13T16:11:53Z |
| mailing_list | cryptography@metzdowd.com | 18 | 18 | 2008-10-31T18:10:00Z | 2009-01-25T15:47:10Z |
| mailing_list | p2p-research mailing list | 5 | 5 | 2009-02-11T22:30:54Z | 2009-02-13T18:45:41Z |
| p2pfoundation | p2pfoundation.ning.com forum | 4 | 4 | 2009-02-11T22:27:00Z | 2014-03-07T01:17:00Z |
| svn_commit | bitcoin SourceForge SVN | 159 | 159 | 2009-10-21T01:08:05Z | 2010-12-15T22:43:51Z |
| whitepaper | bitcoin.org/bitcoin.pdf | 1 | 1 | 2009-03-24T17:33:15Z | 2009-03-24T17:33:15Z |
| **all** | | **956** | **924** | 2008-08-20T17:30:39Z | 2014-03-07T01:17:00Z |

Timestamp precision by source type: code_comment/none: 28; email/minute: 35; email/second: 149; email/unknown: 1; forum/second: 540; mailing_list/second: 39; p2pfoundation/minute: 4; svn_commit/second: 159; whitepaper/second: 1

Time-zone basis by source type (explicit = zone in source; verified = display zone checked; inferred/assumed = see notes; unknown/none = no UTC): code_comment/none: 28; email/assumed: 16; email/explicit: 149; email/inferred: 16; email/unknown: 4; forum/explicit: 1; forum/verified: 539; mailing_list/explicit: 31; mailing_list/verified: 8; p2pfoundation/verified: 4; svn_commit/explicit: 159; whitepaper/explicit: 1

whitespace_preserved by source type: code_comment/True: 28; email/False: 20; email/True: 165; forum/True: 539; forum/partial: 1; mailing_list/True: 39; p2pfoundation/False: 4; svn_commit/True: 159; whitepaper/False: 1

Private copies of public list posts not counted separately (duplicate_of_public): 9 (email-trammell-0005, email-trammell-0009, email-malmi-0041, email-malmi-0132, email-malmi-0200, email-malmi-0220, email-malmi-0231, email-malmi-0247, email-malmi-0249)

UTC hour-of-day of Satoshi's items, A: only items whose time zone is explicit in the source or verified (second/minute precision; excludes authenticity=disputed and duplicate_message_of items):

```
hour          email          forum   mailing_list  p2pfoundation     svn_commit     whitepaper         all
00                6             32              0              0             12              0          50
01                7             23              2              0             10              0          42
02                6             15              2              0              9              0          32
03                5             10              1              0              2              0          18
04                5              9              1              0              5              0          20
05               14              3              1              0              3              0          21
06                6              3              1              0              1              0          11
07                2              0              0              0              0              0           2
08                0              0              0              0              0              0           0
09                0              1              0              0              1              0           2
10                0              0              0              0              0              0           0
11                0              0              0              0              0              0           0
12                0              3              0              0              0              0           3
13                0              5              0              0              2              0           7
14                2             14              0              0              2              0          18
15                9             18              1              0              7              0          35
16                8             45              6              1             18              0          78
17               17             65              3              0             11              1          97
18               16             65              6              0             13              0         100
19               14             43              3              0             13              0          73
20               13             43              3              1              8              0          68
21                7             55              1              0             14              0          77
22                9             46              5              1             15              0          76
23                3             42              2              0             13              0          60
total           149            540             38              3            159              1         890
```

UTC hour-of-day, B: all items with a UTC timestamp incl. inferred/assumed zones (same exclusions):

```
hour          email          forum   mailing_list  p2pfoundation     svn_commit     whitepaper         all
00               10             32              0              0             12              0          54
01                8             23              2              0             10              0          43
02                7             15              2              0              9              0          33
03                6             10              1              0              2              0          19
04                5              9              1              0              5              0          20
05               15              3              1              0              3              0          22
06                6              3              1              0              1              0          11
07                3              0              0              0              0              0           3
08                1              0              0              0              0              0           1
09                1              1              0              0              1              0           3
10                0              0              0              0              0              0           0
11                0              0              0              0              0              0           0
12                1              3              0              0              0              0           4
13                1              5              0              0              2              0           8
14                2             14              0              0              2              0          18
15               10             18              1              0              7              0          36
16               11             45              6              1             18              0          81
17               18             65              3              0             11              1          98
18               18             65              6              0             13              0         102
19               18             43              3              0             13              0          77
20               15             43              3              1              8              0          70
21               10             55              1              0             14              0          80
22               12             46              5              1             15              0          79
23                3             42              2              0             13              0          60
total           181            540             38              3            159              1         922
```

Whitespace sanity data: count of sentence ends ('.', '?', '!' followed by spaces and a capital letter) in `text`, by number of spaces, for items with whitespace_preserved == true (text inside [code] blocks is not excluded):

| source_type | venue group | items | 1 space | 2 spaces | 3+ spaces |
|---|---|---:|---:|---:|---:|
| code_comment | Bitcoin pre-release source | 5 | 7 | 11 | 0 |
| code_comment | Bitcoin v0.1.0 source | 23 | 2 | 31 | 0 |
| email | private email | 165 | 20 | 909 | 0 |
| forum | bitcointalk.org | 539 | 36 | 1505 | 2 |
| mailing_list | bitcoin-list@lists.sourceforge.net | 16 | 0 | 43 | 0 |
| mailing_list | cryptography@metzdowd.com | 18 | 1 | 146 | 0 |
| mailing_list | p2p-research mailing list | 5 | 0 | 44 | 0 |
| svn_commit | bitcoin SourceForge SVN | 159 | 0 | 1 | 0 |


bitcointalk 'Last Edit' times of Satoshi's posts (separate activity events, n=103; UTC hour):

```
00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
10  3  3  5  1  1  1  0  0  0  0  0  2  5  2  3 14  6 13  7  7 10  6  4
```
