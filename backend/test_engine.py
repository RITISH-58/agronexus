import urllib.request
import urllib.error
import json

base = "http://localhost:8000/api"

def test(label, url, payload):
    print(f"\n{'='*60}\n{label}\n{'='*60}")
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])
        if len(json.dumps(data)) > 1500:
            print("... (truncated)")
        print("✅ SUCCESS")
        return data
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# 1. Trending Businesses
test("1. Trending Businesses", f"{base}/entrepreneur/trending-businesses", {})

# 2. Crop Opportunities
test("2. Crop Opportunities - Rice", f"{base}/entrepreneur/business-opportunities", {"crop": "rice"})

# 3. Search
test("3. Search - 'oil'", f"{base}/entrepreneur/search", {"query": "oil"})
test("4. Search - 'food' + low investment", f"{base}/entrepreneur/search", {"query": "food", "investment_filter": "low"})

# 5. Business Plan
test("5. Business Plan", f"{base}/entrepreneur/business-plan", {"business_name": "Peanut Butter Manufacturing"})

# 6. Legacy endpoints
test("6. Legacy /entrepreneur-mode", f"{base}/entrepreneur-mode", {"crop": "turmeric"})
