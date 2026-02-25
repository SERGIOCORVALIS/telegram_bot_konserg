#!/usr/bin/env python3
"""
Script to test OpenRouter API keys functionality.
Tests each key with a simple request to check if it's valid and working.
"""

import asyncio
import os
import sys
from typing import Any

import aiohttp
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TEST_MODEL = "google/gemini-2.0-flash-exp:free"


async def test_api_key(session: aiohttp.ClientSession, api_key: str, key_name: str) -> dict[str, Any]:
    """Test a single API key."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://example.com",
        "X-Title": "API Key Tester",
    }
    
    payload = {
        "model": TEST_MODEL,
        "messages": [{"role": "user", "content": "Say 'test' if you can read this."}],
    }
    
    result = {
        "key_name": key_name,
        "key_preview": f"{api_key[:10]}...{api_key[-4:]}",
        "length": len(api_key),
        "status": "unknown",
        "error": None,
        "response_time": None,
    }
    
    try:
        import time
        start_time = time.time()
        
        async with session.post(OPENROUTER_URL, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
            response_time = time.time() - start_time
            result["response_time"] = round(response_time, 2)
            
            if response.status == 200:
                data = await response.json()
                choices = data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    result["status"] = "[OK] WORKING"
                    result["response_preview"] = content[:50] + "..." if len(content) > 50 else content
                else:
                    result["status"] = "[WARN] INVALID RESPONSE"
                    result["error"] = "No choices in response"
            elif response.status == 401:
                result["status"] = "[FAIL] UNAUTHORIZED"
                result["error"] = "Invalid API key or key expired"
            elif response.status == 429:
                result["status"] = "[RATE] RATE LIMITED"
                result["error"] = "Rate limit exceeded (key works but needs to wait)"
            elif response.status == 404:
                error_data = await response.json()
                error_msg = error_data.get("error", {}).get("message", "Not Found")
                result["status"] = "[FAIL] NOT FOUND"
                result["error"] = error_msg
            else:
                error_text = await response.text()
                result["status"] = f"[FAIL] ERROR {response.status}"
                result["error"] = error_text[:200] if len(error_text) > 200 else error_text
                
    except asyncio.TimeoutError:
        result["status"] = "[TIMEOUT] TIMEOUT"
        result["error"] = "Request timed out after 30 seconds"
    except Exception as e:
        result["status"] = "[EXCEPTION] EXCEPTION"
        result["error"] = str(e)[:200]
    
    return result


async def main():
    """Test all API keys."""
    load_dotenv()
    
    # Collect all API keys
    api_keys: list[tuple[str, str]] = []
    
    # Main key
    main_key = os.getenv("OPENROUTER_API_KEY")
    if main_key:
        main_key = main_key.strip().strip('"').strip("'")
        if main_key:
            api_keys.append(("OPENROUTER_API_KEY", main_key))
    
    # Additional keys
    for i in range(1, 10):
        key = os.getenv(f"OPENROUTER_API_KEY_{i}")
        if key:
            key = key.strip().strip('"').strip("'")
            if key:
                api_keys.append((f"OPENROUTER_API_KEY_{i}", key))
    
    if not api_keys:
        print("[ERROR] No API keys found in environment variables!")
        print("\nPlease set at least one of:")
        print("  - OPENROUTER_API_KEY")
        print("  - OPENROUTER_API_KEY_1, OPENROUTER_API_KEY_2, etc.")
        sys.exit(1)
    
    print(f"[TEST] Testing {len(api_keys)} API key(s) with model: {TEST_MODEL}\n")
    print("=" * 80)
    
    async with aiohttp.ClientSession() as session:
        results = []
        for key_name, api_key in api_keys:
            print(f"\nTesting {key_name}...")
            result = await test_api_key(session, api_key, key_name)
            results.append(result)
            
            # Print result
            print(f"  Key: {result['key_preview']} (length: {result['length']})")
            print(f"  Status: {result['status']}")
            if result.get('response_time'):
                print(f"  Response time: {result['response_time']}s")
            if result.get('error'):
                print(f"  Error: {result['error']}")
            if result.get('response_preview'):
                print(f"  Response: {result['response_preview']}")
            
            # Small delay between requests
            await asyncio.sleep(1)
    
    # Summary
    print("\n" + "=" * 80)
    print("\n[SUMMARY]")
    print("-" * 80)
    
    working = [r for r in results if "[OK]" in r["status"]]
    rate_limited = [r for r in results if "[RATE]" in r["status"]]
    failed = [r for r in results if "[FAIL]" in r["status"]]
    
    print(f"[OK] Working: {len(working)}/{len(results)}")
    if working:
        for r in working:
            print(f"   - {r['key_name']}: {r['key_preview']}")
    
    if rate_limited:
        print(f"\n[RATE] Rate Limited (but working): {len(rate_limited)}/{len(results)}")
        for r in rate_limited:
            print(f"   - {r['key_name']}: {r['key_preview']}")
    
    if failed:
        print(f"\n[FAIL] Failed: {len(failed)}/{len(results)}")
        for r in failed:
            print(f"   - {r['key_name']}: {r['key_preview']} - {r.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 80)
    
    # Exit code
    if working or rate_limited:
        print("\n[SUCCESS] At least one key is working! Bot should function correctly.")
        sys.exit(0)
    else:
        print("\n[ERROR] No working keys found! Please check your API keys.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[WARN] Test interrupted by user")
        sys.exit(130)

