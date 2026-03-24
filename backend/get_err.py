import urllib.request
import urllib.error
import json

for port in [8000]:
    print(f"\n=== Testing port {port} ===")
    req = urllib.request.Request(
        f'http://localhost:{port}/api/scheme-recommendation',
        data=b'{"soil_type":"Black","land_size":2.5,"water_availability":"Medium","state":"Telangana","district":"Warangal"}',
        headers={'Content-Type': 'application/json'}
    )
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        print(f"SUCCESS: {len(data.get('recommended_schemes', []))} schemes returned")
        for s in data.get('recommended_schemes', []):
            print(f"  - {s['name']}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode())
    except Exception as e:
        print(f"Error: {e}")
