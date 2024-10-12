import subprocess

def verify_firmware_signature(firmware, signature):
    try:
        # Verify the signature using OpenSSL
        result = subprocess.run(
            ['openssl', 'dgst', '-sha256', '-verify', 'public_key.pem', '-signature', signature, firmware],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False
