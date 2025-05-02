import socket
import argparse
import matplotlib.pyplot as plt
from datetime import datetime

def scan_ports(host, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)
        sock.close()
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("host", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g. 20-100)", default="1-1024")
    args = parser.parse_args()

    host = args.host
    port_range = args.ports.split("-")
    start_port = int(port_range[0])
    end_port = int(port_range[1])

    print(f"[*] Scanning {host} from port {start_port} to {end_port}...\n")
    open_ports = scan_ports(host, start_port, end_port)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"scan_results_{timestamp}.txt"
    with open(txt_filename, "w") as f:
        for port in open_ports:
            f.write(f"Port {port} is OPEN\n")

    print(f"\n[+] Scan complete. Results saved to {txt_filename}")

    # Save visualization
    if open_ports:
        plt.figure(figsize=(10, 4))
        plt.bar(open_ports, [1]*len(open_ports), color='green')
        plt.xlabel("Open Ports")
        plt.title(f"Open Ports on {host}")
        plt.yticks([])
        png_filename = f"port_scan_{timestamp}.png"
        plt.savefig(png_filename)
        print(f"[+] Port scan visual saved to {png_filename}")
    else:
        print("[!] No open ports found.")

if __name__ == "__main__":
    main()
