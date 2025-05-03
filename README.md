
# ⚡ LAN SNIFFER & ARP SPOOFER TOOL 💀

🔥 **Advanced MITM Sniffing Toolkit** untuk nge-sniff, spoof, dan dominasi jaringan lokal! Fitur lengkap: ARP spoofing, packet sniffing, auto vendor detection, real-time suspicious keyword alert, auto pcap dump, dan UI CLI keren pakai Rich!

---

## ⚙️ INSTALLASI

### 🔧 Requirements:
- Python 3.10+
- `scapy`
- `rich`
- `mac-vendor-lookup`
- `playsound` (opsional, buat buzzer alert)

### 💣 Install Semua Dependency:
```bash
pip install scapy rich mac-vendor-lookup
pip install git+https://github.com/TaylorSMarks/playsound.git@dev # karena `playsound` dari PyPI sering error
```

> **NOTE**: Jika `playsound` tetap error, disable aja fitur buzzer-nya di script.

---

## 🚀 CARA PAKAI

1. **Jalankan script dengan hak administrator / root**
   ```bash
   sudo python off2.py   # Linux / Termux
   ```

   ```powershell
   Start-Process python -ArgumentList 'off2.py' -Verb runAs   # Windows PowerShell (Admin)
   ```

2. Tool bakal:
   - Scan seluruh subnet `x.x.x.1/24`
   - Spoof ARP ke semua target & gateway
   - Tampilkan daftar IP, MAC, dan vendor
   - Sniff semua paket TCP
   - Alert kalau ada keyword mencurigakan kayak `password`, `admin`, dll
   - Simpan semua paket ke file `sniffed.pcap`

3. Tekan `CTRL + C` buat **restore ARP table otomatis** & exit dengan elegan.

---

## 🧠 FITUR SADIS

- ✅ Auto LAN scanner
- 🔥 ARP poisoning full duplex (victim <=> gateway)
- 💾 Auto pcap log (`sniffed.pcap`)
- 🎯 MAC Vendor lookup
- 🚨 Suspicious Keyword Detector
- 🔊 Optional Buzzer Alert pakai `alert.mp3`
- 🤖 UI CLI powerful pakai `rich`

---

## 📛 WARNING

> ⚠️ **PENTING**: TOOL INI DIBUAT UNTUK **PENGETESAN & PENDIDIKAN** DI JARINGAN SENDIRI!
> 
> 🔥 Penyalahgunaan terhadap jaringan orang lain = **tanggung jawab pengguna** sepenuhnya.
> 
> 🧠 Pahami hukum di tempat lo sebelum pake!

---

## ✨ CREDIT

- Script by: **[WAK MODE🔥 Underground Ops]**
- Built with 🖤 using Python, Scapy, Rich
- MAC lookup: [`mac-vendor-lookup`](https://pypi.org/project/mac-vendor-lookup/)
- Audio alert: [`playsound`](https://github.com/TaylorSMarks/playsound)

---

## 💌 KONTAK

Mau upgrade fitur? Tambah auto redirect HTTP? Inject JS sadis?  
WAKK DM AJA‼️

---

FULL SEND‼️🔥 TINGGAL SPOOF, SNIFF, DOMINATE 💻💣
