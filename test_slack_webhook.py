"""
Test Slack webhook connection
"""

import os
import sys
import json
import requests

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/aaaajqkcgywrijyttf45nfhyma')

def test_webhook():
    """Test the Slack webhook with a simple message"""
    
    # Test message - simple format
    test_message_simple = {
        "text": "🧪 Test message from Weekly Report Bot - Simple format"
    }
    
    # Test message - with channel override
    test_message_channel = {
        "channel": "oc_weekly_performance_update",
        "text": "🧪 Test message from Weekly Report Bot - With channel name"
    }
    
    # Test message - blocks format (what we're currently using)
    test_message_blocks = {
        "channel": "oc_weekly_performance_update",
        "username": "Weekly Report Bot",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🧪 *Test Message*\nThis is a test to verify the Slack webhook is working correctly."
                }
            }
        ]
    }
    
    print("=" * 60)
    print("Testing Slack Webhook Connection")
    print("=" * 60)
    print(f"\nWebhook URL: {SLACK_WEBHOOK_URL}")
    print(f"Channel: oc_weekly_performance_update")
    print("\n" + "=" * 60)
    
    # Test 1: Simple format
    print("\n📤 Test 1: Sending simple message format...")
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=test_message_simple,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Simple format: SUCCESS")
        else:
            print(f"❌ Simple format: FAILED - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: With channel name
    print("\n📤 Test 2: Sending message with channel name...")
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=test_message_channel,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Channel name format: SUCCESS")
        else:
            print(f"❌ Channel name format: FAILED - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Blocks format (current format)
    print("\n📤 Test 3: Sending message with blocks format (current)...")
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=test_message_blocks,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Blocks format: SUCCESS")
        else:
            print(f"❌ Blocks format: FAILED - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing Complete")
    print("=" * 60)
    print("\n💡 Note: Slack webhooks are typically configured for a specific channel.")
    print("   If the channel name doesn't work, the webhook will post to its default channel.")
    print("   Check the webhook configuration in Slack to see which channel it's set to.")

if __name__ == '__main__':
    test_webhook()


