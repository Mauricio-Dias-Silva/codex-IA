
import os

def fix_env():
    file_path = ".env"
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        print(f"Original size: {len(content)} bytes")
        
        # Primitively brute-force fix: remove null bytes which are likely artifacts of copy-paste/utf-16
        # This assumes the file SHOULD be ascii/utf-8 text.
        cleaned = content.replace(b'\x00', b'')
        
        # Also fix potential weird line endings mixed
        cleaned = cleaned.replace(b'\r\r\n', b'\r\n')
        
        with open(file_path, "wb") as f:
            f.write(cleaned)
            
        print(f"Cleaned size: {len(cleaned)} bytes")
        print("✅ .env file sanitized. Null bytes removed.")
        
        # Verify
        with open(file_path, "r", encoding="utf-8") as f:
            print("Preview of first 50 chars:")
            print(f.read(50))
            
    except Exception as e:
        print(f"❌ Error fixing env: {e}")

if __name__ == "__main__":
    fix_env()
