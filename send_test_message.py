"""
Send a simple test message to verify webhook works
"""

import os
import sys
import requests

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://join.slack.com/share/enQtOTg2OTU1NzQ3OTU1My01ZmEzODZhOGRjZDQ4MzVkNTBmZDQxM2UzYWE4NjVmZjBiMTQxNzE3MWJiM2UxM2UyZDhmYjE1MmFiYzhjNTdj')

# Test with channel ID
test_message = {
    "channel": "C09QZMPG7MZ",
    "text": "🧪 Test message from Weekly Report Bot - If you see this, the webhook is working!",
    "username": "Weekly Report Bot"
}

print("📤 Sending test message to Slack...")
print(f"Webhook URL: {SLACK_WEBHOOK_URL}")
print("\nNote: The message will be sent to the channel configured in the webhook settings.")
print("If you don't see it in 'oc_weekly_performance_update', check the webhook configuration.\n")

try:
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=test_message,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        # Check if response is actually from Slack (should be "ok")
        if response.text.strip() == "ok":
            print("✅ SUCCESS! Message sent to Slack")
            print("✅ Check your Slack channel for the test message")
        else:
            print(f"⚠️  Warning: Unexpected response: {response.text[:200]}")
            print("   The webhook might not be configured correctly")
    else:
        print(f"❌ FAILED: Status code {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

