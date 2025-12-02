"""
Simplified Google Slides presentation with storytelling style and meaningful graphics
Focuses on content first, styling can be done manually
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle

# Mosaic Images URLs for all 10 slides (generated from Mosaic)
MOSAIC_IMAGES = {
    'hero': 'https://grab.design/api/images/4J3l9q1hvkoe',  # Hero Slide
    'team_unity': 'https://grab.design/api/images/MAnzjbEU1qEK',  # The Journey Begins
    'trust_partnership': 'https://grab.design/api/images/5yOBjLofGLA4',  # A Moment of Honesty
    'culture': 'https://grab.design/api/images/D1NYj4Oim37A',  # Culture as Foundation
    'joy': 'https://grab.design/api/images/9Yl2jq1cJLqK',  # The Source of Joy
    'innovation_thinking': 'https://grab.design/api/images/GYL1jpKcaWNv',  # Our New Way
    'empowerment_triad': 'https://grab.design/api/images/pN3j5x8TJ3rG',  # The Empowerment Triad
    'path_forward': 'https://grab.design/api/images/29gJnq1Ie2yQ',  # The Path Forward
    'commitment': 'https://grab.design/api/images/NgYmJaziRoB2',  # Our Commitment
    'promise': 'https://grab.design/api/images/Rb1lJWei41nk',  # The Promise
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

def create_storytelling_slides():
    """Create storytelling slide structure"""
    requests = []
    
    # Slide 1: Hero Slide
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })
    
    # Slide 2: The Journey Begins
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 3: A Moment of Honesty
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 4: Culture as Foundation
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 5: The Source of Joy
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 6: Our New Way
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })
    
    # Slide 7: The Empowerment Triad
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })
    
    # Slide 8: The Path Forward
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 9: Our Commitment
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
        }
    })
    
    # Slide 10: The Promise
    requests.append({
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })
    
    return requests

def create_storytelling_content(service, presentation_id):
    """Add storytelling content with visuals"""
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    page_size = presentation.get('pageSize', {})
    page_width = page_size.get('width', {}).get('magnitude', 720)
    page_height = page_size.get('height', {}).get('magnitude', 405)
    
    requests = []
    
    # Slide 1: Hero Slide
    if len(slides) > 0:
        slide = slides[0]
        # Add hero background image
        if MOSAIC_IMAGES['hero']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['hero'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': page_height, 'unit': 'PT'},
                            'width': {'magnitude': page_width, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 0,
                            'translateY': 0,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        # Title text box
        requests.append({
            'createShape': {
                'objectId': 'hero_title',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 120, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 600) / 2,
                        'translateY': 100,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': 'hero_title',
                'text': 'Our Culture of Excellence\nPerformance by Design'
            }
        })
        
        # Subtitle text box
        requests.append({
            'createShape': {
                'objectId': 'hero_subtitle',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 40, 'unit': 'PT'},
                        'width': {'magnitude': 400, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 400) / 2,
                        'translateY': 230,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': 'hero_subtitle',
                'text': 'Day 1 Opening Framework'
            }
        })
    
    # Slide 2: The Journey Begins
    if len(slides) > 1:
        slide = slides[1]
        # Add team unity image
        if MOSAIC_IMAGES['team_unity']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['team_unity'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'The Journey Begins'
                }
            })
            
            content = """Good morning, team. We're here in Penang to take a pause from the daily grind.

First, I want to acknowledge the work you do. This team performs, and I've seen your commitment since I joined in April.

But I didn't bring us here just because we're doing okay. I brought us here because I believe this team has the potential to be the highest-performing, most united commercial team in the region.

We have a massive opportunity in Penang, and to capture our full potential, we must be a united team.

These next three days are an investment. This is not a 'eat and play' trip. This is a strategic workshop designed to reset and rebuild, to equip us with new tools, and most importantly, new ways of working together."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 3: A Moment of Honesty
    if len(slides) > 2:
        slide = slides[2]
        # Add trust partnership image
        if MOSAIC_IMAGES['trust_partnership']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['trust_partnership'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'A Moment of Honesty'
                }
            })
            
            content = """Before we get into the activities, I need to have a difficult and candid conversation with you.

Honestly, this part isn't easy. I've been thinking a lot about how to say this, because I'm genuinely afraid I might say something wrong or accidentally trigger someone.

But I know that having this conversation is far more important than my own fear. The future of our team, and the trust we need to build, is more important than my own comfort.

My ask is that you please work with me as we struggle through this together. Listen with an open heart. That is the only way we will leave here as the single, united team I know we can be."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 4: Culture as Foundation
    if len(slides) > 3:
        slide = slides[3]
        # Add culture foundation image
        if MOSAIC_IMAGES['culture']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['culture'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'Culture as Foundation'
                }
            })
            
            content = """You've all heard the saying, "Culture eats strategy for breakfast."

We can have the best commercial strategy in the world, but if our culture—how we treat each other, how we handle conflict, how we hold ourselves accountable—is broken, we will fail.

Our purpose here is to define and commit to our own culture of excellence. This isn't just about hitting business goals; it's about building a team where we uphold the Grab principles:

Heart • Hunger • Honour • Humility

In everything we do."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 5: The Source of Joy
    if len(slides) > 4:
        slide = slides[4]
        # Add joy from work image
        if MOSAIC_IMAGES['joy']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['joy'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'The Source of Joy'
                }
            })
            
            content = """True joy from our careers doesn't come from money, or power, or prestige. Those things are side effects.

Joy comes from earning your success, which means:

Creating Value: Believing that your work is needed and that you are serving other people.

Lifting Others: Doing something that is good for other people.

The purpose of your job, through your work, is to love, dignify, and lift other people up.

Zero Tolerance Mandate:
• Retaliation and backbiting are unacceptable.
• No Triangulation: Complaining to a third party instead of speaking directly—ends today.
• Open & Direct Communication: All feedback must come to me directly.

The standard is integrity: doing the right thing, even when no one is watching."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 6: Our New Way
    if len(slides) > 5:
        slide = slides[5]
        # Add innovation thinking image
        if MOSAIC_IMAGES['innovation_thinking']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['innovation_thinking'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 200, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 250,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        # Title
        requests.append({
            'createShape': {
                'objectId': 'transformation_title',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 60, 'unit': 'PT'},
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
                'objectId': 'transformation_title',
                'text': 'Our New Way: From Task-Givers to Thinking Partners'
            }
        })
        
        # Content
        requests.append({
            'createShape': {
                'objectId': 'transformation_content',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 200, 'unit': 'PT'},
                        'width': {'magnitude': 500, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 50,
                        'translateY': 120,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': 'transformation_content',
                'text': 'A huge part of "dignifying others" is respecting their intelligence and creativity.\n\nWe will no longer be a team of "task-givers" and "checklist-executors." We will be a team of Thinking Partners.\n\nThis means we don\'t just delegate tasks; we delegate problems.\n\nThe weak manage output. The strong design cognition.\n\nWe will be a team that designs cognition.'
            }
        })
    
    # Slide 7: The Empowerment Triad
    if len(slides) > 6:
        slide = slides[6]
        # Add empowerment triad visualization
        if MOSAIC_IMAGES['empowerment_triad']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['empowerment_triad'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 150, 'unit': 'PT'},
                            'width': {'magnitude': 500, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': (page_width - 500) / 2,
                            'translateY': 350,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        # Title
        requests.append({
            'createShape': {
                'objectId': 'triad_title',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 50, 'unit': 'PT'},
                        'width': {'magnitude': 500, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 500) / 2,
                        'translateY': 20,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': 'triad_title',
                'text': 'Our Empowerment Triad'
            }
        })
        
        # Three columns
        triad_content = [
            ('Define the Nature\n\nThe Why & Stakes\n\nYou will always know why something is vital, what success buys us, and what failure costs us.', (page_width - 1800) / 2),
            ('Pose the Question\n\nThe Challenge\n\nI will give you my best thinking, then ask you to "find the flaws," "go two levels deeper," or "beat my standard."', (page_width - 1800) / 2 + 600),
            ('Empower & Anchor\n\nThe Trust & Standard\n\nYou will have full autonomy on the how. My focus is on the outcome. "Beat my standard."', (page_width - 1800) / 2 + 1200)
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
                            'height': {'magnitude': 220, 'unit': 'PT'},
                            'width': {'magnitude': 550, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x_pos,
                            'translateY': 100,
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
    
    # Slide 8: The Path Forward
    if len(slides) > 7:
        slide = slides[7]
        # Add workshop activities image
        if MOSAIC_IMAGES['path_forward']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['path_forward'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'The Path Forward'
                }
            })
            
            content = """This is a "build-to-ship" workshop. We will be in mixed teams—permanent and FTT—tackling checkpoint races, collaborative sprints, and field simulations.

These activities will create "purposeful, playful pressure." We will practice:

• Making "trust moves"—asking, clarifying, and committing
• Giving brave, honest feedback
• Receiving a "problem" instead of a "task"
• Managing clear handoffs and supporting our teammates

After every activity, we will debrief. We will talk about how our behaviors linked to the 4H values and our new "no-triangulation" norm."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 9: Our Commitment
    if len(slides) > 8:
        slide = slides[8]
        # Add commitment/charter image
        if MOSAIC_IMAGES['commitment']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['commitment'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        page_elements = slide.get('pageElements', [])
        if len(page_elements) >= 2:
            title_id = page_elements[0]['objectId']
            body_id = page_elements[1]['objectId']
            
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': 'Our Commitment'
                }
            })
            
            content = """We are not leaving here with just good memories. We are leaving with a plan to sustain this.

Our most important objective is to co-create and sign our own Team Norm Charter. This charter will be drafted by us, for us. It will define our shared rules for feedback, escalation, and anti-gossip behavior.

This charter will be visibly displayed in our workspace. It is not just a document; it is our public commitment to each other. We will build simple, inspectable routines to make sure we stick to it."""
            
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': content
                }
            })
    
    # Slide 10: The Promise
    if len(slides) > 9:
        slide = slides[9]
        # Add promise/commitment image
        if MOSAIC_IMAGES['promise']:
            requests.append({
                'createImage': {
                    'url': MOSAIC_IMAGES['promise'],
                    'elementProperties': {
                        'pageObjectId': slide['objectId'],
                        'size': {
                            'height': {'magnitude': 200, 'unit': 'PT'},
                            'width': {'magnitude': 300, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': page_width - 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            })
        
        requests.append({
            'createShape': {
                'objectId': 'closing_text',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 250, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 600) / 2,
                        'translateY': (page_height - 250) / 2,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': 'closing_text',
                'text': 'My Ask of You:\n\nBe 100% Present • Speak with Honour\nListen with Humility • Create a Safe Space\n\nMy Commitment:\n\nI commit to listening, being open, and holding everyone—including myself—accountable to these new standards.\n\nThis is our reset. This is day one of the new Penang Commercial team.\n\nLet\'s get to work.'
            }
        })
    
    return requests

def main():
    """Main function"""
    print('Authenticating with Google Slides API...')
    service = authenticate()
    
    print('Creating presentation...')
    presentation_id = create_slide_presentation(
        service,
        'Our Culture of Excellence: Performance by Design'
    )
    
    print('Creating storytelling slides...')
    requests = create_storytelling_slides()
    body = {'requests': requests}
    
    try:
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body=body).execute()
        print(f'Created {len(response.get("replies"))} slides')
        
        print('Adding storytelling content with images...')
        content_requests = create_storytelling_content(service, presentation_id)
        
        if content_requests:
            body = {'requests': content_requests}
            response = service.presentations().batchUpdate(
                presentationId=presentation_id,
                body=body).execute()
            print(f'Added content to {len(response.get("replies"))} elements')
        
        print(f'\n[SUCCESS] Storytelling presentation created successfully!')
        print(f'[VIEW] https://docs.google.com/presentation/d/{presentation_id}/edit')
        print(f'\n[NOTE] Apply Grab design colors manually in Google Slides for best results.')
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

