# -*- coding: utf-8 -*-
"""GiWiFi campus network auto-login script - background monitoring edition."""
import re
import base64
import urllib.parse
import json
import time
import logging
import sys
import os

ACCOUNT = "19015310530"
PASSWORD = "s1301246"
CHECK_INTERVAL = 30
LOG_FILE = os.path.expanduser("~/auto_login.log")

LOGIN_URL = "http://172.27.253.230/gportal/Web/loginAction"
LOGIN_PAGE = "http://172.27.253.230/gportal/web/login?wlanacname=SDZYY"
AES_KEY = b"1234567887654321"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def aes_encrypt_cbc_zero(key, iv, plain):
    try:
        from Crypto.Cipher import AES
        pad_len = (16 - len(plain) % 16) % 16
        padded = plain + b'\x00' * pad_len
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(padded)
    except ImportError:
        pass
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        pad_len = (16 - len(plain) % 16) % 16
        padded = plain + b'\x00' * pad_len
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(padded) + encryptor.finalize()
    except ImportError:
        pass
    import subprocess
    b64_plain = base64.b64encode(plain).decode()
    key_str = key.decode()
    iv_str = iv.decode()
    ps_code = ('$keyBytes = [System.Text.Encoding]::UTF8.GetBytes("{0}"); '
               '$ivBytes  = [System.Text.Encoding]::UTF8.GetBytes("{1}"); '
               '$dataBytes = [Convert]::FromBase64String("{2}"); '
               '$padLen = [math]::Ceiling($dataBytes.Length / 16) * 16; '
               '$padded = New-Object byte[] $padLen; '
               '[Array]::Copy($dataBytes, $padded, $dataBytes.Length); '
               '$aes = [System.Security.Cryptography.Aes]::Create(); '
               '$aes.Key = $keyBytes; $aes.IV = $ivBytes; '
               '$aes.Mode = [System.Security.Cryptography.CipherMode]::CBC; '
               '$aes.Padding = [System.Security.Cryptography.PaddingMode]::None; '
               '$enc = $aes.CreateEncryptor().TransformFinalBlock($padded, 0, $padded.Length); '
               '[Convert]::ToBase64String($enc)').format(key_str, iv_str, b64_plain)
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_code],
        capture_output=True, text=True, timeout=15
    )
    return base64.b64decode(result.stdout.strip())


def is_online():
    import ssl
    import urllib.request
    try:
        req = urllib.request.Request("https://www.baidu.com", method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        urllib.request.urlopen(req, timeout=5, context=ctx)
        return True
    except Exception:
        return False


def do_login():
    import ssl
    import urllib.request
    try:
        req = urllib.request.Request(LOGIN_PAGE)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        log.warning("Cannot reach login page: %s", e)
        return False

    def get_val(name):
        m = re.search(r'name="' + name + r'"\s+value="([^"]*)"', html)
        return m.group(1) if m else ""

    sign = get_val("sign")
    iv = get_val("iv")
    sta_ip = get_val("sta_ip")
    request_ip = get_val("request_ip")
    nas_name = get_val("nas_name")

    if not sign or not iv:
        log.warning("Could not parse login page (missing sign/iv).")
        return False

    fields = [
        ("sign", sign), ("sta_vlan", ""), ("sta_port", ""),
        ("sta_ip", sta_ip), ("nas_ip", ""), ("nas_name", nas_name),
        ("last_url", ""), ("request_ip", request_ip),
        ("device_mode", "Windows NT"), ("device_type", "1"),
        ("device_os_type", "3"), ("is_mobile", "0"),
        ("iv", iv), ("login_type", "1"), ("account_type", "2"),
        ("user_account", ACCOUNT), ("user_password", PASSWORD),
    ]
    form_data = urllib.parse.urlencode(fields)

    iv_bytes = iv.encode("utf-8")
    data_bytes = form_data.encode("utf-8")
    encrypted = aes_encrypt_cbc_zero(AES_KEY, iv_bytes, data_bytes)
    enc_b64 = base64.b64encode(encrypted).decode()

    post_body = urllib.parse.urlencode({"data": enc_b64, "iv": iv}).encode()
    try:
        req = urllib.request.Request(LOGIN_URL, data=post_body, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120")
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        result = json.loads(resp.read().decode())
        if result.get("status") == 1:
            log.info("LOGIN SUCCESS")
            return True
        else:
            log.warning("Login failed: %s", result.get("info", result))
            return False
    except Exception as e:
        log.warning("POST error: %s", e)
        return False


def main():
    log.info("=" * 50)
    log.info("GiWiFi monitor started (check every %ds)", CHECK_INTERVAL)
    log.info("Account: %s", ACCOUNT)
    log.info("Log file: %s", LOG_FILE)
    log.info("=" * 50)
    consecutive_failures = 0
    while True:
        try:
            if is_online():
                consecutive_failures = 0
                time.sleep(CHECK_INTERVAL)
                continue
            log.info("Offline detected, attempting login...")
            if do_login():
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    log.warning("%d consecutive failures, waiting %ds...",
                                consecutive_failures, CHECK_INTERVAL * 2)
                    time.sleep(CHECK_INTERVAL * 2)
                    consecutive_failures = 0
                    continue
        except Exception as e:
            log.error("Unexpected error: %s", e)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
