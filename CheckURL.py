import requests
import sys
from pyfiglet import figlet_format
from termcolor import colored

# --- Konfigurasi Banner ---
TOOL_INFO = "Instagram: @abbasyasin_ | Tools by: Eror707Forbidden"


def display_banner():
    """Menampilkan banner CheckerParameter menggunakan pyfiglet dan info tools."""
    banner = figlet_format("Check URL", font="slant")
    print(colored(banner, 'cyan'))
    print(colored("-" * 60, 'magenta'))
    print(colored(TOOL_INFO.center(60), 'yellow'))
    print(colored("-" * 60, 'magenta'))
    print("\n")


def get_color(status_code):
    """Menentukan warna output berdasarkan kode status HTTP."""

    if status_code == "TIMEOUT":
        return 'yellow', 'TIMEOUT'
    elif status_code == "CONN_ERROR":
        return 'yellow', 'CONN_ERROR'

    # Status Integer
    if status_code == 200:
        return 'green', 'SUCCESS'
    elif 300 <= status_code < 400:
        return 'blue', 'REDIRECT'
    elif status_code == 403:
        return 'red', 'FORBIDDEN'
    elif status_code == 404:
        return 'red', 'NOT FOUND'
    elif 500 <= status_code < 600:
        return 'magenta', 'SERVER ERR'
    else:
        return 'white', 'UNKNOWN'


def try_protocol(url):
    """Menguji apakah website menggunakan HTTPS atau HTTP."""
    protocols = ["https://", "http://"]

    for proto in protocols:
        target = proto + url
        try:
            response = requests.get(target, timeout=7, allow_redirects=True)
            return target, response.status_code
        except requests.exceptions.RequestException:
            continue  # Coba protokol berikutnya

    return url, "CONN_ERROR"


def check_url_status(url):
    """Memeriksa status URL penuh (termasuk protokol)."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Kali-Tool; Linux) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        return url, response.status_code

    except requests.exceptions.RequestException as e:
        if 'Timeout' in str(e):
            return url, "TIMEOUT"
        return url, "CONN_ERROR"


def main():
    display_banner()

    if len(sys.argv) != 2:
        print(colored("Penggunaan:", 'red'), "python3 Testparameter.py <nama_file_url>")
        sys.exit(1)

    url_file = sys.argv[1]

    success_urls = []

    print(colored(f"{'URL':<80} | {'STATUS':<15}", 'yellow', attrs=['bold']))
    print(colored("=" * 96, 'yellow'))

    try:
        with open(url_file, 'r') as f:
            for line in f:
                raw = line.strip()

                if not raw:
                    continue

                # --- AUTO PROTOCOL DETECTION ---
                if not raw.startswith("http"):
                    target_url, status_code = try_protocol(raw)
                else:
                    target_url, status_code = check_url_status(raw)

                color, status_label = get_color(status_code)

                print(f"{target_url:<80} | {colored(str(status_code) + ' ' + status_label, color, attrs=['bold'])}")

                if isinstance(status_code, int) and status_code == 200:
                    success_urls.append(target_url)

    except FileNotFoundError:
        print(colored(f"\n[ERROR] File '{url_file}' tidak ditemukan.", 'red'))
        sys.exit(1)

    # --- Opsi Setelah Scanning ---
    if success_urls:
        print(colored("\n" + "=" * 96, 'green', attrs=['bold']))
        print(colored(f"[✅ SUKSES] Ditemukan {len(success_urls)} URL dengan status 200 OK.", 'green', attrs=['bold']))
        print(colored("=" * 96, 'green', attrs=['bold']))

        while True:
            choice = input(colored("Simpan URL 200 OK ke file? (y/n): ", 'yellow')).lower()
            if choice == 'y':
                outname = input(colored("Masukkan nama file output (contoh: hasil_ok.txt): ", 'cyan'))
                if not outname.endswith(".txt"):
                    outname += ".txt"

                with open(outname, 'w') as out_f:
                    for url in success_urls:
                        out_f.write(url + '\n')

                print(colored(f"\n[INFO] Disimpan: {outname}", 'green'))
                break

            elif choice == 'n':
                print(colored("[INFO] URL tidak disimpan. Selesai.", 'cyan'))
                break

            else:
                print(colored("[!] Masukkan 'y' atau 'n' saja.", 'red'))

    else:
        print(colored("\n[INFO] Tidak ada URL yang berhasil diakses (200 OK).", 'cyan'))


if __name__ == "__main__":
    main()
