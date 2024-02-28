import socket
import asyncio
import termcolor
import concurrent.futures

async def scan(target, port, timeout=1):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(target, port), timeout=timeout
        )

        service_banner = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        service_banner = service_banner.decode().strip()

        print(f"[+] Port {port} Open: {service_banner}")
        writer.close()
    except (asyncio.TimeoutError, socket.error) as e:
        print(f"[-] Port {port} Error: {e}")

async def scan_target(target, ports):
    print('\n' + f'Starting Scan For {target}')

    tasks = [scan(target, port) for port in range(1, ports + 1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    targets = input("[*] Enter Targets To Scan (split them by ,): ")
    ports = int(input("[*] Enter How Many Ports You Want To Scan: "))

    log_file = input("[*] Enter the log file path (press Enter for no logging): ").strip()

    async def main():
        if ',' in targets:
            print(termcolor.colored("[*] Scanning Multiple Targets", 'green'))
            for ip_addr in targets.split(','):
                print(f"Scanning IP Address: {ip_addr.strip()}")
                await scan_target(ip_addr.strip(), ports)
        else:
            print(f"Scanning IP Address: {targets}")
            await scan_target(targets, ports)

    asyncio.run(main())
