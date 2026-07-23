import requests
import sys

TARGET_URL = "https://demo.owasp-juice.shop/rest/products/search"
SQLI_PAYLOAD = "test'"

DB_ERRORS = [
    "sqlite_error",
    "sqlite",
    "sql syntax",
    "syntax error",
    "near",
    "database error",
    "unterminated string",
    "unclosed quotation mark"
]


def scan_vulnerability():
    print("=" * 60)
    print(f"Initializing automated scan on {TARGET_URL}")
    print(f"Transmitting payload: {SQLI_PAYLOAD}")
    print("=" * 60)

    try:
        response = requests.get(
            TARGET_URL,
            params={"q": SQLI_PAYLOAD},
            timeout=20,
            allow_redirects=True,
            headers={
                "User-Agent": "Educational-SQLi-Checker/1.0"
            }
        )

        page_content = response.text.lower()

        detected_signature = None

        for error in DB_ERRORS:
            if error in page_content:
                detected_signature = error
                break

        print(f"HTTP status: {response.status_code}")
        print(f"Final URL: {response.url}")

        if detected_signature:
            print("[ALERT] Database error signature detected.")
            print(f"Signature: {detected_signature.upper()}")

            print("\nServer response:")
            print(response.text[:1000])

        elif response.status_code >= 500:
            print("[POSSIBLE] Server error returned after the payload.")
            print("A database error may have occurred.")

        else:
            print("[CLEAN] No visible database error signature detected.")
            print("This result does not prove that the parameter is secure.")

    except requests.exceptions.Timeout:
        print("[ERROR] The connection timed out.")
        sys.exit(1)

    except requests.exceptions.SSLError as error:
        print(f"[ERROR] SSL certificate problem: {error}")
        sys.exit(1)

    except requests.exceptions.ConnectionError as error:
        print(f"[ERROR] Connection failed: {error}")
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Request failed: {error}")
        sys.exit(1)


scan_vulnerability()