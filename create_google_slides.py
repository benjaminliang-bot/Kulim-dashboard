"""
Script to create Google Slides presentation using Google Slides API
Based on Grab's design language (Duxton design tokens)

Requirements:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Before running:
    1. Enable Google Slides API in Google Cloud Console
    2. Create OAuth 2.0 credentials and download credentials.json
    3. Place credentials.json in the same directory as this script
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle

# Grab Design Tokens (Duxton)
GRAB_COLORS = {
    'brand_primary': '#00b14f',
    'brand_primary_bold': '#00804a',
    'brand_primary_boldest': '#005339',
    'brand_secondary': '#17b5a6',
    'brand_secondary_bold': '#1e948a',
    'text_dark': '#184440',
    'background_soft': '#f8fffe',
    'alert_notice': '#f76708',
    'alert_notice_soft': '#fff4eb',
}

SCOPES = ['https://www.googleapis.com/auth/presentations']

def authenticate():
    """Authenticate and return service object"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('slides', 'v1', credentials=creds)

def create_slide_presentation(service, title):
    """Create a new presentation"""
    presentation = {
        'title': title
    }
    presentation = service.presentations().create(body=presentation).execute()
    presentation_id = presentation.get('presentationId')
    print(f'Created presentation with ID: {presentation_id}')
    return presentation_id

def rgb_to_hex(rgb_string):
    """Convert RGB string to hex color"""
    # Already in hex format from our tokens
    return rgb_string

def hex_to_color(color_hex):
    """Convert hex color to Google Slides color format"""
    color_hex = color_hex.lstrip('#')
    r = int(color_hex[0:2], 16) / 255.0
    g = int(color_hex[2:4], 16) / 255.0
    b = int(color_hex[4:6], 16) / 255.0
    return {
        'rgbColor': {
            'red': r,
            'green': g,
            'blue': b
        }
    }

def create_requests_for_slides():
    """Create all slide requests"""
    requests = []
    
    # Slide 1: Title Slide
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_ONLY'
            },
            'placeholderIdMappings': []
        }
    })
    
    # Slide 2: The "Why"
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 3: A Candid Start
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 4: The "What" - Culture
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 5: The "What" - Joy & Zero Tolerance
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 6: New Way of Working
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 7: Empowerment Triad
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'BLANK'
            }
        }
    })
    
    # Slide 8: The "How"
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 9: The "So What?"
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    # Slide 10: My Ask & My Commitment
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_BODY'
            }
        }
    })
    
    return requests

def add_content_to_slides(service, presentation_id):
    """Add content to all slides"""
    
    # Get the presentation structure
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    
    requests = []
    
    # Slide 1: Title
    if len(slides) > 0:
        title_id = slides[0]['pageElements'][0]['objectId']
        subtitle_id = slides[0]['pageElements'][1]['objectId'] if len(slides[0]['pageElements']) > 1 else None
        
        requests.append({
            'insertText': {
                'objectId': title_id,
                'text': 'Our Culture of Excellence: Performance by Design'
            }
        })
        
        if subtitle_id:
            requests.append({
                'insertText': {
                    'objectId': subtitle_id,
                    'text': 'Day 1 Opening Framework'
                }
            })
    
    # Slide 2: The "Why"
    if len(slides) > 1:
        slide = slides[1]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '1. The "Why": Acknowledge the Present, Frame the Future'
                }
            })
            
            content = """Acknowledge Performance: First, I want to acknowledge the work you do. This team performs, and I've seen your commitment since I joined in April.

State the Opportunity: But I didn't bring us here just because we're doing okay. I brought us here because I believe this team has the potential to be the highest-performing, most united commercial team in the region. We have a massive opportunity in Penang, and to capture our full potential, we must be a united team.

Set the Purpose: These next three days are an investment. This is not a 'eat and play' trip. This is a strategic workshop designed to reset and rebuild, to equip us with new tools, and most importantly, new ways of working together."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 3: A Candid Start
    if len(slides) > 2:
        slide = slides[2]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '2. A Candid Start (The "How" We Begin)'
                }
            })
            
            content = """Before we get into the activities, I need to have a difficult and candid conversation with you. Honestly, this part isn't easy. I've been thinking a lot about how to say this, because I'm genuinely afraid I might say something wrong or accidentally trigger someone.

But I know that having this conversation is far more important than my own fear. The future of our team, and the trust we need to build, is more important than my own comfort.

My ask is that you please work with me as we struggle through this together. Listen with an open heart. That is the only way we will leave here as the single, united team I know we can be."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 4: The "What" - Culture
    if len(slides) > 3:
        slide = slides[3]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '3. The "What": Our Culture, Our Joy, & Our New Standard'
                }
            })
            
            content = """Culture Eats Strategy for Breakfast

We can have the best commercial strategy in the world, but if our culture—how we treat each other, how we handle conflict, how we hold ourselves accountable—is broken, we will fail.

Grab 4H Values: Heart • Hunger • Honour • Humility

Our purpose here is to define and commit to our own culture of excellence. This isn't just about hitting business goals; it's about building a team where we uphold the Grab principles of Heart, Hunger, Honour, and Humility in everything we do."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 5: The "What" - Joy & Zero Tolerance
    if len(slides) > 4:
        slide = slides[4]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '3. The "What" (continued)'
                }
            })
            
            content = """The Source of Joy in Work

True joy from our careers doesn't come from money, or power, or prestige. Those things are side effects.

Joy comes from earning your success, which means:
• Creating Value: Believing that your work is needed and that you are serving other people.
• Lifting Others: Doing something that is good for other people.

The purpose of your job, through your work, is to love, dignify, and lift other people up.

Zero Tolerance Mandate

• Zero Tolerance for Toxic Behavior: Retaliation and backbiting are unacceptable.
• No Triangulation: Complaining about someone to a third party instead of speaking to them or to me—ends today.
• Open & Direct Communication: All feedback and complaints must come to me directly. This is the only way to solve issues and build trust.

The standard is integrity: doing the right thing, even when no one is watching."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 6: New Way of Working
    if len(slides) > 5:
        slide = slides[5]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '4. Our New Way of Working: From Task-Givers to Thinking Partners'
                }
            })
            
            content = """A huge part of "dignifying others" is respecting their intelligence and creativity. In the past, maybe we've been managed, or we ourselves have managed, as "task-givers."

That old model stops today. Our new culture of excellence requires a new way of working. We will no longer be a team of "task-givers" and "checklist-executors." We will be a team of Thinking Partners.

This means we don't just delegate tasks; we delegate problems. This is my commitment to you, and it's what I expect us to practice with each other.

The weak manage output. The strong design cognition. We will be a team that designs cognition."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 7: Empowerment Triad (BLANK layout - need to create text boxes)
    if len(slides) > 6:
        slide = slides[6]
        # For blank slide, we'll add a title text box
        page_width = presentation.get('pageSize', {}).get('width', {}).get('magnitude', 720)
        page_height = presentation.get('pageSize', {}).get('height', {}).get('magnitude', 405)
        
        # Create title text box
        requests.append({
            'createShape': {
                'objectId': 'triad_title',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 72, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 600) / 2,
                        'translateY': 40,
                        'unit': 'PT'
                    }
                }
            }
        })
        
        requests.append({
            'insertText': {
                'objectId': 'triad_title',
                'text': '4. Our New Way of Working (continued)\nOur "Empowerment Triad"'
            }
        })
        
        # Create three text boxes for triad
        triad_content = [
            ('Define the Nature\nThe Why & Stakes - You will always know why something is vital, what success buys us, and what failure costs us.', (page_width - 1800) / 2),
            ('Pose the Question\nThe Challenge - I will give you my best thinking, and then ask you to "find the flaws," "go two levels deeper," or "beat my standard." This flips the dynamic: you become the expert, and I become the challenger.', (page_width - 1800) / 2 + 600),
            ('Empower & Anchor\nThe Trust & Standard - You will have full autonomy on the how. My focus is on the outcome. I will replace "follow my method" with "beat my standard," and I trust you to rise to that challenge.', (page_width - 1800) / 2 + 1200)
        ]
        
        for i, (text, x_pos) in enumerate(triad_content):
            obj_id = f'triad_{i}'
            requests.append({
                'createShape': {
                    'objectId': obj_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 550, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x_pos,
                            'translateY': 140,
                            'unit': 'PT'
                        }
                    }
                }
            })
            requests.append({
                'insertText': {
                    'objectId': obj_id,
                    'text': text
                }
            })
    
    # Slide 8: The "How"
    if len(slides) > 7:
        slide = slides[7]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '5. The "How": Our Work for the Next 3 Days'
                }
            })
            
            content = """This is a "build-to-ship" workshop. We will be in mixed teams—permanent and FTT—tackling checkpoint races, collaborative sprints, and field simulations.

Practice New Habits: These activities will create "purposeful, playful pressure." They are designed to be our very first practice of this new "Thinking Partner" model:

• We will practice making "trust moves"—like asking, clarifying, and committing.
• We will practice giving brave, honest feedback.
• We will practice how to receive a "problem" instead of a "task."
• We will practice managing clear handoffs and supporting our teammates.

The Debrief is Key: After every activity, we will debrief. We will talk about how our behaviors linked to the 4H values and our new "no-triangulation" norm."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 9: The "So What?"
    if len(slides) > 8:
        slide = slides[8]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '6. The "So What?": Our Commitment (The Deliverable)'
                }
            })
            
            content = """A Lasting Commitment: We are not leaving here with just good memories. We are leaving with a plan to sustain this.

The Team Norm Charter: Our most important objective is to co-create and sign our own Team Norm Charter. This charter will be drafted by us, for us. It will define our shared rules for feedback, escalation, and anti-gossip behavior.

Make it Real: This charter will be visibly displayed in our workspace. It is not just a document; it is our public commitment to each other. We will build simple, inspectable routines to make sure we stick to it."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 10: My Ask & My Commitment
    if len(slides) > 9:
        slide = slides[9]
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': '7. My Ask & My Commitment (Set Ground Rules)'
                }
            })
            
            content = """My Ask of You:
• Be 100% Present: Engage fully.
• Speak with Honour: Be honest, but respectful. Challenge ideas, not people.
• Listen with Humility: Be open to learning something new, even from those you may have had friction with.
• What's Said Here, Stays Here: This is a safe space for candor.

My Commitment to You: In return, I commit to listening, to being open, and to holding everyone—including myself—accountable to these new standards.

This is our reset. This is day one of the new Penang Commercial team."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 11: Closing (add as new slide)
    requests.append({
        'createSlide': {
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_ONLY'
            }
        }
    })
    
    if requests:
        body = {'requests': requests}
        try:
            response = service.presentations().batchUpdate(
                presentationId=presentation_id,
                body=body).execute()
            print(f'Updated {len([r for r in response.get("replies", []) if "createSlide" not in str(r)])} slides')
            
            # Add closing slide content
            presentation = service.presentations().get(presentationId=presentation_id).execute()
            slides = presentation.get('slides', [])
            if len(slides) >= 11:
                closing_requests = [{
                    'insertText': {
                        'objectId': slides[10]['pageElements'][0]['objectId'],
                        'text': "Let's get to work."
                    }
                }]
                service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': closing_requests}).execute()
                print('Added closing slide content')
        except HttpError as error:
            print(f'An error occurred: {error}')

def main():
    """Main function to create the presentation"""
    print('Authenticating with Google Slides API...')
    service = authenticate()
    
    print('Creating presentation...')
    presentation_id = create_slide_presentation(
        service, 
        'Our Culture of Excellence: Performance by Design'
    )
    
    print('Creating slides...')
    requests = create_requests_for_slides()
    body = {'requests': requests}
    
    try:
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body=body).execute()
        print(f'Created {len(response.get("replies"))} slides')
        
        print('Adding content to slides...')
        add_content_to_slides(service, presentation_id)
        
        print(f'\n[SUCCESS] Presentation created successfully!')
        print(f'[VIEW] https://docs.google.com/presentation/d/{presentation_id}/edit')
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

