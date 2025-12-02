"""
Test Slack Web API with bot token
"""

import os
import sys
import requests

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLACK_BOT_TOKEN = 'xapp-1-A09R2EKGR8V-9884800284896-3faca7ffa148f4fdf3a9c5e241e5a0d32183ea2578c82f3edeef7ce6a72c5755'
SLACK_CHANNEL_ID = 'C09QZMPG7MZ'

# Slack Web API endpoint
url = "https://slack.com/api/chat.postMessage"

# Prepare headers
headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Test message
payload = {
    "channel": SLACK_CHANNEL_ID,
    "text": "🧪 Test message from Weekly Report Bot - If you see this, the Slack API is working!",
    "username": "Weekly Report Bot"
}

print("📤 Testing Slack Web API...")
print(f"Channel ID: {SLACK_CHANNEL_ID}")
print(f"Token: {SLACK_BOT_TOKEN[:20]}...\n")

try:
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=10
    )
    
    result = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {result}\n")
    
    if response.status_code == 200 and result.get("ok"):
        print("✅ SUCCESS! Message sent to Slack")
        print(f"✅ Message timestamp: {result.get('ts', 'N/A')}")
        print("✅ Check your Slack channel 'oc_weekly_performance_update' for the test message")
    else:
        print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        if result.get('error') == 'invalid_auth':
            print("   The token might be invalid or expired")
        elif result.get('error') == 'channel_not_found':
            print("   The channel ID might be incorrect")
        elif result.get('error') == 'not_in_channel':
            print("   The bot needs to be added to the channel")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")


