# Google Slides Creation Guide
## Our Culture of Excellence: Performance by Design

This guide provides three methods to create your Google Slides presentation:

---

## Method 1: Automated Python Script (Recommended)

### Prerequisites:
1. Install Python packages:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. Enable Google Slides API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable "Google Slides API"
   - Create OAuth 2.0 credentials (Desktop application)
   - Download credentials as `credentials.json`
   - Place `credentials.json` in the same directory as `create_google_slides.py`

3. Run the script:
   ```bash
   python create_google_slides.py
   ```

4. First run will open browser for authentication
5. After authentication, the script will create the presentation automatically

**Note:** The Python script creates the basic structure. You'll need to manually format colors and styling using the design tokens below.

---

## Method 2: Manual Creation (Easiest)

### Step 1: Create New Presentation
1. Go to [Google Slides](https://slides.google.com)
2. Create a new presentation
3. Title it: "Our Culture of Excellence: Performance by Design"

### Step 2: Apply Grab Design Colors

**Custom Theme Colors:**
1. Go to **Slide → Change theme → Customize**
2. Click **Colors → Customize**
3. Set these colors:
   - **Primary 1:** `#00b14f` (Grab Green)
   - **Primary 2:** `#17b5a6` (Grab Teal)
   - **Primary 3:** `#00804a` (Grab Green Bold)
   - **Primary 4:** `#005339` (Grab Green Boldest)
   - **Accent 1:** `#1e948a` (Grab Teal Bold)
   - **Accent 2:** `#f76708` (Alert Notice)

### Step 3: Typography Settings
1. Go to **Slide → Change theme → Customize → Fonts**
2. Set font family to **Inter** (or use Arial as fallback)
3. Heading font: **Inter Bold (600)**
4. Body font: **Inter Regular (400)**

### Step 4: Create Slides
Use the content from `google_slides_content_structure.md` to create each slide:

1. **Slide 1: Title Slide**
   - Title: "Our Culture of Excellence: Performance by Design"
   - Subtitle: "Day 1 Opening Framework"
   - Add a 6px green bar at the top (Rectangle shape, color: #00b14f)

2. **Slide 2-10:** Follow the structure in `google_slides_content_structure.md`

### Step 5: Design Elements

**For Highlight Boxes:**
- Background color: `#f8fffe` or `rgba(0, 177, 79, 0.15)`
- Border left: 4px solid, color: `#00b14f`
- Border radius: 8px

**For Zero Tolerance Section:**
- Background color: `#fff4eb`
- Border left: 4px solid, color: `#f76708`

**For 4H Values Badges:**
- Background: Gradient from `#00b14f` to `#17b5a6`
- Text color: White
- Border radius: 24px
- Padding: 12px 24px

**For Empowerment Triad:**
- Use 3-column layout
- White background
- Border: 2px solid `#b1eaba`
- Border radius: 12px

---

## Method 3: Import HTML Template

1. Open the `culture_of_excellence_slide.html` file in your browser
2. Take screenshots of each section
3. Insert images into Google Slides
4. Add text boxes on top with the actual content

---

## Grab Design Tokens Reference

### Colors (Light Mode)
- **Brand Primary Default:** `#00b14f`
- **Brand Primary Bold:** `#00804a`
- **Brand Primary Boldest:** `#005339`
- **Brand Secondary Default:** `#17b5a6`
- **Brand Secondary Bold:** `#1e948a`
- **Text Dark:** `#184440`
- **Background Soft:** `#f8fffe`
- **Alert Notice Default:** `#f76708`
- **Alert Notice Soft:** `#fff4eb`

### Typography (Duxton Web)
- **Heading-01:** 40px, 600 weight, 1.2 line-height
- **Heading-02:** 32px, 600 weight, 1.25 line-height
- **Heading-03:** 24px, 600 weight, 1.33 line-height
- **Heading-04:** 20px, 600 weight, 1.4 line-height
- **Body-01:** 18px, 400 weight, 1.44 line-height
- **Body-02:** 16px, 400 weight, 1.5 line-height
- **Body-03:** 14px, 400 weight, 1.43 line-height

---

## Quick Checklist

- [ ] Create Google Slides presentation
- [ ] Apply Grab color theme (green/teal)
- [ ] Set Inter font (or Arial fallback)
- [ ] Create 10-11 slides with content
- [ ] Add green accent bar to title slide
- [ ] Style highlight boxes with green borders
- [ ] Style zero tolerance section with orange accent
- [ ] Create 4H value badges with gradient
- [ ] Create 3-column layout for Empowerment Triad
- [ ] Add closing slide with "Let's get to work"

---

## Design Tips

1. **Consistency:** Use the same color scheme throughout
2. **White Space:** Don't overcrowd slides - leave breathing room
3. **Visual Hierarchy:** Use larger fonts for headings, smaller for body
4. **Contrast:** Ensure text is readable against backgrounds
5. **Alignment:** Align elements consistently (left-align text, center-align titles)

---

## Need Help?

Refer to:
- `google_slides_content_structure.md` - Full content for all slides
- `culture_of_excellence_slide.html` - Visual reference
- `create_google_slides.py` - Automated creation script

---

**Good luck with your presentation! 🚀**

