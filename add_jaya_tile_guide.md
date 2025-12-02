# Guide: Adding "Jaya for Business Entry" Tile to Grab MEX Merchant App

## Overview
This guide provides step-by-step instructions for adding a new home screen tile in the Grab MEX merchant app for "Jaya for Business Entry" feature.

## Prerequisites
- Access to Grab MEX merchant app codebase
- Developer account with appropriate permissions
- Understanding of the app's navigation/tile system

---

## Step 1: Locate Tile Configuration Files

### For React Native / Mobile Apps:
1. Navigate to the merchant app's home screen component
2. Look for tile configuration files (typically in):
   - `src/screens/home/TileConfig.tsx` or `.js`
   - `src/components/home/HomeTiles.tsx`
   - `src/config/tiles.json`
   - `src/navigation/homeScreenConfig.ts`

### For Native iOS/Android:
- iOS: Check `HomeViewController.swift` or similar
- Android: Check `HomeActivity.kt` or `HomeFragment.kt`

**Screenshot Location**: Take a screenshot of your IDE showing the tile configuration file structure.

---

## Step 2: Understand Existing Tile Structure

1. Review existing tiles in the home screen configuration
2. Identify the pattern for tile definitions:
   - Tile ID/Key
   - Display name
   - Icon/Image reference
   - Navigation route/action
   - Visibility conditions (country, merchant type, etc.)

**Example Structure:**
```typescript
{
  id: 'tile_id',
  title: 'Tile Display Name',
  icon: 'icon_name',
  route: '/destination',
  visibleFor: ['country_ids'],
  enabled: true
}
```

**Screenshot Location**: Show the existing tile configuration code with annotations.

---

## Step 3: Add New Tile Configuration

### Add the Jaya tile entry to your configuration:

```typescript
// Add this to your tiles array
{
  id: 'jaya_business_entry',
  title: 'Jaya for Business',
  subtitle: 'Business Entry',
  icon: 'jaya_business_icon', // or use icon path
  route: '/jaya/business-entry',
  visibleFor: ['MY'], // Malaysia, adjust as needed
  merchantTypes: ['all'], // or specific merchant types
  enabled: true,
  order: 5 // Position in tile grid
}
```

**Screenshot Location**: 
- Screenshot of code editor with the new tile configuration added
- Show before/after comparison if possible

---

## Step 4: Add Icon/Asset

1. Add the Jaya business entry icon to your assets:
   - iOS: Add to `Assets.xcassets` or image bundle
   - Android: Add to `res/drawable/` or `res/mipmap/`
   - React Native: Add to `src/assets/icons/`

2. Reference the icon in your tile configuration:
   ```typescript
   icon: require('../assets/icons/jaya_business_entry.png')
   // or
   icon: 'jaya_business_entry' // if using icon font/vector
   ```

**Screenshot Location**: 
- Screenshot of asset folder showing the new icon file
- Screenshot of app with icon displayed (if available)

---

## Step 5: Create Navigation Route/Screen

1. If the destination screen doesn't exist, create it:
   ```typescript
   // Example: src/screens/jaya/BusinessEntryScreen.tsx
   import React from 'react';
   
   export const JayaBusinessEntryScreen = () => {
     // Screen implementation
   };
   ```

2. Add route to navigation:
   ```typescript
   // In your navigation config
   {
     name: 'JayaBusinessEntry',
     component: JayaBusinessEntryScreen,
     options: { title: 'Jaya for Business Entry' }
   }
   ```

**Screenshot Location**: 
- Screenshot of the new screen component code
- Screenshot of navigation configuration

---

## Step 6: Implement Business Entry Logic

1. Create the business entry functionality:
   - Form fields for business entry data
   - API integration for submission
   - Validation logic
   - Success/error handling

**Screenshot Location**: 
- Screenshot of the business entry form implementation
- Screenshot of API integration code

---

## Step 7: Add Feature Flags (if needed)

If the feature should be controlled by feature flags:

```typescript
// In feature flag config
{
  key: 'jaya_business_entry_enabled',
  enabled: true,
  countries: ['MY'],
  merchantTypes: ['all']
}

// In tile config
enabled: FeatureFlags.isEnabled('jaya_business_entry_enabled')
```

**Screenshot Location**: 
- Screenshot of feature flag configuration

---

## Step 8: Update Translations

Add translations for the tile:

```json
// In your i18n files
{
  "jaya_business_entry": {
    "title": "Jaya for Business",
    "subtitle": "Business Entry",
    "description": "Enter your business details"
  }
}
```

**Screenshot Location**: 
- Screenshot of translation files with new entries

---

## Step 9: Test the Implementation

1. **Unit Tests**: Test tile configuration and navigation
2. **Integration Tests**: Test the full flow from tile tap to screen
3. **Manual Testing**:
   - Verify tile appears on home screen
   - Tap tile to navigate
   - Complete business entry form
   - Verify data submission

**Screenshot Location**: 
- Screenshot of app home screen showing new tile
- Screenshot of navigation to business entry screen
- Screenshot of completed business entry form

---

## Step 10: Code Review & Deployment

1. Create a pull request with:
   - Tile configuration changes
   - New screen/component code
   - Icon assets
   - Tests
   - Updated documentation

2. Include in PR description:
   - Purpose: Add Jaya for Business Entry tile
   - Affected files
   - Testing checklist
   - Screenshots of the changes

**Screenshot Location**: 
- Screenshot of PR with all changes
- Screenshot of code review comments

---

## Visual Checklist

### App Screenshots Needed:
1. ✅ Home screen BEFORE adding tile
2. ✅ Home screen AFTER adding tile (showing new tile)
3. ✅ Tile detail/configuration view
4. ✅ Navigation to business entry screen
5. ✅ Business entry form/screen
6. ✅ Success screen after submission
7. ✅ Error handling screens (if applicable)

---

## Common Issues & Solutions

### Issue: Tile not appearing
- **Check**: Visibility conditions (country, merchant type)
- **Check**: Feature flag status
- **Check**: App version/build

### Issue: Icon not showing
- **Check**: Icon path is correct
- **Check**: Icon file exists in assets
- **Check**: Icon format is supported

### Issue: Navigation not working
- **Check**: Route is defined in navigation config
- **Check**: Screen component exists and is exported
- **Check**: Route name matches configuration

---

## Additional Resources

- Grab MEX Merchant App Documentation
- Tile System Architecture Docs
- Navigation Guide
- Feature Flag Management Guide

---

## Notes

- Replace placeholder icon paths with actual asset locations
- Adjust country codes and merchant types based on requirements
- Ensure compliance with app design guidelines
- Coordinate with backend team for API endpoints

---

## Next Steps

1. [ ] Locate merchant app codebase
2. [ ] Review existing tile implementations
3. [ ] Add Jaya tile configuration
4. [ ] Create business entry screen
5. [ ] Add assets (icons, images)
6. [ ] Implement business logic
7. [ ] Add tests
8. [ ] Submit PR for review
9. [ ] Deploy to staging
10. [ ] Test in staging environment
11. [ ] Deploy to production

