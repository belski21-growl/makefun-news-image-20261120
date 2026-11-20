# Top 10/20 analysis — news-image-20261120 (ronde r1, sebelum submit)

Sumber: snapshot leaderboard `~/workspace/makefun/leaderboard-news-image-20261120-20261120-1030.json`
(995 baris ter-skor, diambil 20 Nov ~10:30 WIB; rank_key = judge). Kompetisi
MASIH BUKA (deadline 22 Nov 07:00 WIB) — 3.682 submisi total, baru 995 yang
ter-skor; top 20 masih bisa bergeser saat judging lanjut. Semua top entry
`source_withheld: true` — repo dan gambar TIDAK bisa dilihat. Analisis ini
hanya dari judul + skor judge + metadata (bytes, waktu submit, valid). Tidak
ada skor/isi repo top entry yang dikarang.

## Skor judge — skala dan garis hadiah

- Rank 1: 990475 | rank 10: 986723 | rank 20: 985574 | rank 50 (garis hadiah): 981066 | rank 100: 977261
- Median ~963451 (dari 995 baris ter-skor)
- Entry kita r1 "THE WORLD TODAY": BELUM submit, belum punya skor/rank.
- Catatan skala: jarak rank 1 → rank 50 hanya ~9.400 poin, dan rank 50 → rank 100
  ~3.800 poin — kompetisi padat di puncak; selisih kecil di kualitas terbaca
  sebagai selisih besar di rank.

## Top 20 (judge, judul)

| # | judge | judul |
|---|-------|-------|
| 1 | 990475 | Friday 20 November 2026 front page |
| 2 | 990234 | Friday 20 November 2026 |
| 3 | 989987 | The World in One Day — Friday 20 November 2026 |
| 4 | 989856 | The World in One Day — Friday 20 November 2026 |
| 5 | 987835 | The World in One Day — 28 stories from 20 November 2026, two illustrated leads |
| 6 | 987522 | THE WORLD IN ONE DAY — Friday 20 November 2026 (36 stories) |
| 7 | 987301 | The World in One Day — Friday 20 November 2026 |
| 8 | 987104 | Friday 20 November 2026 - the world in one picture (morning edition) |
| 9 | 986990 | Novel Radius |
| 10 | 986723 | The World in One Day — Friday 20 November 2026: 37 stories, 6 regions |
| 11 | 986512 | Friday 20 November 2026: 36 stories, one front page — Akvan landfall, Trump defe... |
| 12 | 986204 | The World in One Day — 20 November 2026 |
| 13 | 986091 | The World Today — 36 Stories, 20 November 2026 |
| 14 | 985902 | The World Today — Friday 20 November 2026 |
| 15 | 985745 | Friday 20 November 2026: Akvan, the AI selloff and forty stories |
| 16 | 985701 | The World in One Day — Friday 20 November 2026 |
| 17 | 985690 | The Twentieth |
| 18 | 985655 | news-image-20261120 V1 probe — 44-story front page |
| 19 | 985631 | Level Magnet |
| 20 | 985574 | The World in One Day |

## Pola yang menang

1. **Kepadatan cerita tinggi.** Top 20 yang menyebut jumlah cerita: 28, 36, 37,
   36, 44, 45 (rank 22), 15 (rank 21) — **median ~36-40**. Rank 50: "50 sourced
   stories, a UTC timeline and a date". Target kelas atas: **36-40 cerita**.
2. **Format front page "The World in One Day".** Frasa itu muncul di 12/20
   judul top 20 (rank 3, 4, 5, 6, 7, 10, 12, 16, 20 + varian). Judul generik
   tanpa tanggal/angka ("Novel Radius", "Level Magnet", "The Twentieth") ada di
   top 20 TAPI itu pengecualian — kemungkinan gambarnya luar biasa; jangan
   ditiru sebagai strategi.
3. **Struktur: masthead tanggal + hero + peta + briefs bernomor per region.**
   Rank 10: "37 stories, 6 regions". Rank 5: "two illustrated leads".
   Rank 50: "50 sourced stories, a UTC timeline and a date". Elemen yang
   diulang: pengelompokan per region (6-7 regions), panel bergambar banyak,
   briefs bernomor, timeline.
4. **Cerita hari ini yang berulang di judul top:** KTT trilateral Trump-Xi-Putin
   Shenzhen (lead hari ini), pendaratan Akvan, AI selloff — entry yang tidak
   memuat cerita-cerita besar hari itu kehilangan relevansi di mata judge.
5. **Iterasi menang.** Rank 18 "V1 probe", rank 8 "morning edition" — entry top
   adalah hasil iterasi, bukan sekali jalan.
6. **Ukuran file bukan penentu.** Top 1 bytes 235.213; tidak ada korelasi
   bytes↔rank yang terlihat. Yang penting keterbacaan pada 1024×1024.
7. **Semua top 20 valid=1, compliant, finished.** Tidak ada jalan pintas lewat
   format — gambar harus lolos semua check server.

## Bandingkan dengan entry kita r1 ("THE WORLD TODAY")

| Aspek | r1 kita | Top 20 | Kurangnya (konkret) |
|---|---|---|---|
| Jumlah cerita | 11 (1 lead + 5 featured + 5 ticker) | median ~36-40 | **~3-4× lebih sedikit** — gap terbesar. Judge membaca "sum up the day" sebagai liputan, bukan 1 berita utama + beberapa panel. |
| Struktur | Masthead + hero + 5 panel + ticker | Masthead tanggal + hero + peta + grid padat + briefs bernomor per region | Tanpa peta, tanpa pengelompokan region, tanpa briefs bernomor |
| Panel bergambar | 6 visual (1 hero + 5 kecil) | 12-15 panel bergambar (dari pola 20261119) | Visual cukup, tapi halaman masih longgar: kolom kanan bawah kosong |
| Lead hari ini | ADA — KTT Shenzhen Trump-Xi-Putin (terverifikasi Reuters) | Sama (lead yang sama di judul top) | Lead benar dan relevan — kekuatan utama r1 |
| Faktualitas | Semua cerita terverifikasi (Reuters/BBC/AFP/TASS); lead dicek independen via search | — | Tidak ada cerita karangan yang terdeteksi |
| Judul submit (saran) | — | Judul deskriptif berisi tanggal + jumlah cerita | Saat submit, pakai judul deskriptif, mis. "Friday 20 November 2026: 11 stories, one front page — Trump, Xi and Putin in Shenzhen" — JANGAN pakai nama acak server |

## Keputusan yang diminta dari Goldfish

- Apakah r1 (11 cerita, lead kuat, faktualitas bersih) LAYAK SUBMIT sebagai
  ronde cepat (strategi submit-cepat: submit dulu, pantau rank ke checkpoint
  ⅓ ~21 Nov 07:00 WIB, perbaiki ke 36-40 cerita bila rank di luar zona hadiah),
  atau harus diperbaiki dulu ke kepadatan top-20 sebelum submit pertama?
- Perkiraan jujur: dengan 11 cerita, r1 kemungkinan besar duduk di kelas
  menengah (judge ~970-980k, rank ratusan-ribuan) — di bawah garis hadiah
  (rank 50 ~981k dan terus naik saat judging lanjut). Ronde perbaikan ke
  36-40 cerita hampir pasti diperlukan untuk bersaing di zona hadiah; yang
  ditimbang Goldfish adalah apakah ronde-cepat ini layak menghabiskan 1 dari
  3 jatah harian atau langsung bangun versi padat sebagai r1.
