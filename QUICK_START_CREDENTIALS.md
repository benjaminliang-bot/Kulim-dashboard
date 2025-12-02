# Quick Start: Getting Google API Credentials

## Step 1: Enable Google Slides API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing one)
   - Click "Select a project" → "New Project"
   - Name it: "Culture of Excellence Slides"
   - Click "Create"

## Step 2: Enable Google Slides API

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Slides API"
3. Click on "Google Slides API"
4. Click **"Enable"**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"OAuth client ID"**
4. If prompted, configure OAuth consent screen:
   - User Type: **External** (or Internal if you have Google Workspace)
   - App name: "Culture of Excellence Slides"
   - User support email: Your email
   - Developer contact: Your email
   - Click **"Save and Continue"**
   - Scopes: Click **"Save and Continue"** (skip for now)
   - Test users: Add your email, click **"Save and Continue"**
5. Back to creating OAuth client ID:
   - Application type: **"Desktop app"**
   - Name: "Culture of Excellence Slides Client"
   - Click **"Create"**
6. Download the credentials:
   - Click **"Download JSON"** (or copy the JSON)
   - Save it as `credentials.json` in the same folder as `create_google_slides.py`

## Step 4: Run the Script

Once `credentials.json` is in place, run:
```bash
py create_google_slides.py
```

The first time you run it:
- A browser window will open
- Sign in with your Google account
- Click "Allow" to grant permissions
- The script will create `token.pickle` for future use

## Troubleshooting

**Error: credentials.json not found**
- Make sure `credentials.json` is in the same folder as the script

**Error: Access blocked**
- Make sure you added your email as a test user in OAuth consent screen

**Error: API not enabled**
- Go back to Step 2 and enable Google Slides API

