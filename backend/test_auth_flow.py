import requests

BASE_URL = "http://localhost:8000/api"

def test_auth_flow():
    print("1. Testing Registration...")
    reg_data = {
        "email": "testfarmer@test.com",
        "password": "securepassword123",
        "full_name": "Test Farmer",
        "phone": "1234567890",
        "state": "California",
        "district": "Central Valley",
        "role": "farmer"
    }
    r = requests.post(f"{BASE_URL}/auth/signup", json=reg_data)
    print(f"Status: {r.status_code}, Response: {r.text}")
    if r.status_code != 200:
        if "Email already registered" in r.text or "Phone already registered" in r.text:
            print("User already exists, proceeding to login...")
            pass
        else:
            assert False, f"Registration failed: {r.text}"
    
    print("\n2. Testing Send OTP...")
    send_otp_data = {
        "phone": "1234567890"
    }
    r = requests.post(f"{BASE_URL}/auth/send-otp", json=send_otp_data)
    print(f"Status: {r.status_code}, Response: {r.text}")
    if r.status_code != 200:
        if "Phone number already verified" in r.text:
            print("Phone already verified, skipping OTP flow...")
        else:
            assert False, f"Send OTP failed: {r.text}"

    print("\n2.5 Testing OTP Verification (bypassing for test)...")
    # For testing, we won't assert it strictly because it's random in memory
    otp_data = {
        "phone": "1234567890",
        "otp": "123456" 
    }
    r = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_data)
    print(f"Status: {r.status_code}, Response: {r.text}")
    if r.status_code != 200:
        if "Phone number already verified" in r.text:
            print("Phone already verified, proceeding...")
        else:
            assert False, f"OTP verification failed: {r.text}"

    print("\n3. Testing Login...")
    login_data = {
        "email": "testfarmer@test.com",
        "password": "securepassword123"
    }
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {r.status_code}, Response: {r.text}")
    assert r.status_code == 200, "Login failed"
    
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n4. Testing GET /me...")
    r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {r.status_code}, Response: {r.text}")
    assert r.status_code == 200, "Get user failed"
    
    print("\n5. Testing Create Land...")
    land_data = {
        "land_size": 25.5,
        "soil_type": "Loamy",
        "water_availability": "Borewell",
        "primary_crop": "Wheat",
        "district": "Central Valley",
        "village": "Farm Town"
    }
    r = requests.post(f"{BASE_URL}/profile/land", json=land_data, headers=headers)
    print(f"Status: {r.status_code}, Response: {r.text}")
    assert r.status_code == 200, "Create land failed"
    
    print("\n6. Testing Get Lands...")
    r = requests.get(f"{BASE_URL}/profile/land", headers=headers)
    print(f"Status: {r.status_code}, Response: {r.text}")
    assert r.status_code == 200, "Get lands failed"
    
    print("\nAll backend integration tests passed successfully!")

if __name__ == "__main__":
    test_auth_flow()
