"""
Test Slack webhook URL
"""

import os
import sys
import requests

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'
SLACK_CHANNEL_ID = 'C09QZMPG7MZ'

# Test 1: Simple text message
print("=" * 60)
print("Test 1: Simple text message")
print("=" * 60)
test_message_1 = {
    "text": "🧪 Test message from Weekly Report Bot - Simple format",
    "username": "Weekly Report Bot"
}

try:
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=test_message_1,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200 and response.text.strip() == "ok":
        print("✅ SUCCESS!\n")
    else:
        print("⚠️  Check response above\n")
except Exception as e:
    print(f"❌ Error: {str(e)}\n")

# Test 2: With channel ID override
print("=" * 60)
print("Test 2: With channel ID override")
print("=" * 60)
test_message_2 = {
    "channel": SLACK_CHANNEL_ID,
    "text": "🧪 Test message with channel ID override",
    "username": "Weekly Report Bot"
}

try:
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=test_message_2,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200 and response.text.strip() == "ok":
        print("✅ SUCCESS!\n")
    else:
        print("⚠️  Check response above\n")
except Exception as e:
    print(f"❌ Error: {str(e)}\n")

# Test 3: With blocks format (what we use in the report)
print("=" * 60)
print("Test 3: With blocks format (report format)")
print("=" * 60)
test_message_3 = {
    "channel": SLACK_CHANNEL_ID,
    "username": "Weekly Report Bot",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🧪 Test Report",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "If you see this formatted message, the webhook is working correctly! ✅"
            }
        }
    ]
}

try:
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=test_message_3,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200 and response.text.strip() == "ok":
        print("✅ SUCCESS! Blocks format works!")
        print("✅ Check your Slack channel 'oc_weekly_performance_update' for the test message")
    else:
        print("⚠️  Check response above")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("Testing Complete")
print("=" * 60)


