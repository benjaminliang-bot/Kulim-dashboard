"""
Enhanced Google Slides presentation with storytelling style, meaningful graphics, and Grab design language
Uses Mosaic-generated images and Grab design tokens
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle
import time
import requests

# Grab Design Tokens (Duxton)
GRAB_COLORS = {
    'brand_primary': {'red': 0.0, 'green': 0.694, 'blue': 0.310},  # #00b14f
    'brand_primary_bold': {'red': 0.0, 'green': 0.502, 'blue': 0.290},  # #00804a
    'brand_primary_boldest': {'red': 0.0, 'green': 0.325, 'blue': 0.224},  # #005339
    'brand_secondary': {'red': 0.090, 'green': 0.710, 'blue': 0.651},  # #17b5a6
    'brand_secondary_bold': {'red': 0.118, 'green': 0.580, 'blue': 0.541},  # #1e948a
    'text_dark': {'red': 0.094, 'green': 0.267, 'blue': 0.251},  # #184440
    'background_soft': {'red': 0.973, 'green': 1.0, 'blue': 0.996},  # #f8fffe
    'alert_notice': {'red': 0.969, 'green': 0.404, 'blue': 0.031},  # #f76708
}

# Mosaic Images URLs (generated from Mosaic)
MOSAIC_IMAGES = {
    'team_unity': 'https://grab.design/api/images/MAnzjbEU1qEK',  # Team collaboration
    'trust_partnership': 'https://grab.design/api/images/5yOBjLofGLA4',  # Trust and partnership
    'growth_journey': 'https://grab.design/api/images/Yq7PJWDUPebx',  # Growth and achievement
    'innovation_thinking': 'https://grab.design/api/images/GYL1jpKcaWNv',  # Thinking partners
    'empowerment_triad': 'https://grab.design/api/images/pN3j5x8TJ3rG',  # Empowerment triad visualization
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
    """Create a new presentation with Grab theme"""
    presentation = {
        'title': title,
        'locale': 'en_US'
    }
    presentation = service.presentations().create(body=presentation).execute()
    presentation_id = presentation.get('presentationId')
    print(f'Created presentation with ID: {presentation_id}')
    return presentation_id

def hex_to_rgb_color(color_hex):
    """Convert hex color to Google Slides RGB format"""
    color_hex = color_hex.lstrip('#')
    r = int(color_hex[0:2], 16) / 255.0
    g = int(color_hex[2:4], 16) / 255.0
    b = int(color_hex[4:6], 16) / 255.0
    return {
        'red': r,
        'green': g,
        'blue': b
    }

def create_storytelling_slides():
    """Create storytelling slide structure"""
    requests = []
    
    # Slide 1: Hero Slide - Opening Scene
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
    
    # Slide 6: Our New Way - Transformation
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

def insert_image(service, presentation_id, slide_id, image_url, x, y, width, height):
    """Insert an image into a slide"""
    try:
        # Download image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            # Upload to Google Slides
            return {
                'createImage': {
                    'url': image_url,
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {
                            'height': {'magnitude': height, 'unit': 'PT'},
                            'width': {'magnitude': width, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x,
                            'translateY': y,
                            'unit': 'PT'
                        }
                    }
                }
            }
    except Exception as e:
        print(f'Warning: Could not insert image: {e}')
        return None

def create_storytelling_content(service, presentation_id):
    """Add storytelling content with visuals"""
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    page_size = presentation.get('pageSize', {})
    page_width = page_size.get('width', {}).get('magnitude', 720)
    page_height = page_size.get('height', {}).get('magnitude', 405)
    
    requests = []
    
    # Slide 1: Hero Slide - Opening Scene
    if len(slides) > 0:
        slide = slides[0]
        # Add title text box
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'hero_title',
                'style': {
                    'fontSize': {'magnitude': 36, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                    'bold': True,
                    'foregroundColor': {'rgbColor': hex_to_rgb_color('#005339')}
                },
                'fields': 'fontSize,fontFamily,bold,foregroundColor'
            }
        })
        
        # Add subtitle
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'hero_subtitle',
                'style': {
                    'fontSize': {'magnitude': 20, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#1e948a')}
                },
                'fields': 'fontSize,fontFamily,foregroundColor'
            }
        })
        
        # Add green accent bar at top
        requests.append({
            'createShape': {
                'objectId': 'hero_accent',
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 6, 'unit': 'PT'},
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
        requests.append({
            'updateShapeProperties': {
                'objectId': 'hero_accent',
                'shapeProperties': {
                    'shapeBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': hex_to_rgb_color('#00b14f')}
                        }
                    }
                },
                'fields': 'shapeBackgroundFill.solidFill.color'
            }
        })
    
    # Slide 2: The Journey Begins - Storytelling
    if len(slides) > 1:
        slide = slides[1]
        # Add team unity image
        if MOSAIC_IMAGES['team_unity']:
            img_request = {
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
            }
            requests.append(img_request)
        
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 3: A Moment of Honesty
    if len(slides) > 2:
        slide = slides[2]
        # Add trust partnership image
        if MOSAIC_IMAGES['trust_partnership']:
            img_request = {
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
            }
            requests.append(img_request)
        
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 4: Culture as Foundation
    if len(slides) > 3:
        slide = slides[3]
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 5: The Source of Joy
    if len(slides) > 4:
        slide = slides[4]
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 6: Our New Way - Transformation
    if len(slides) > 5:
        slide = slides[5]
        # Add innovation thinking image
        if MOSAIC_IMAGES['innovation_thinking']:
            img_request = {
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
            }
            requests.append(img_request)
        
        # Create title
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'transformation_title',
                'style': {
                    'fontSize': {'magnitude': 28, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                    'bold': True,
                    'foregroundColor': hex_to_rgb_color('#00804a')
                },
                'fields': 'fontSize,fontFamily,bold,foregroundColor'
            }
        })
        
        # Create content box
        requests.append({
            'createShape': {
                'objectId': 'transformation_content',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 200, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 600) / 2,
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'transformation_content',
                'style': {
                    'fontSize': {'magnitude': 16, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                    'foregroundColor': hex_to_rgb_color('#184440')
                },
                'fields': 'fontSize,fontFamily,foregroundColor'
            }
        })
    
    # Slide 7: The Empowerment Triad
    if len(slides) > 6:
        slide = slides[6]
        # Add empowerment triad visualization
        if MOSAIC_IMAGES['empowerment_triad']:
            img_request = {
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
            }
            requests.append(img_request)
        
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'triad_title',
                'style': {
                    'fontSize': {'magnitude': 28, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                    'bold': True,
                    'foregroundColor': hex_to_rgb_color('#00804a')
                },
                'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': obj_id,
                    'style': {
                        'fontSize': {'magnitude': 14, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
            # Add background color
            requests.append({
                'updateShapeProperties': {
                    'objectId': obj_id,
                    'shapeProperties': {
                        'shapeBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': hex_to_rgb_color('#f8fffe')}
                        }
                        }
                    },
                    'fields': 'shapeBackgroundFill.solidFill.color'
                }
            })
    
    # Slide 8: The Path Forward
    if len(slides) > 7:
        slide = slides[7]
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 9: Our Commitment
    if len(slides) > 8:
        slide = slides[8]
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
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'bold': True,
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#00804a')}
                    },
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
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
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'fontFamily': 'Inter',
                        'foregroundColor': {'rgbColor': hex_to_rgb_color('#184440')}
                    },
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
    
    # Slide 10: The Promise - Closing
    if len(slides) > 9:
        slide = slides[9]
        # Create closing text
        requests.append({
            'createShape': {
                'objectId': 'closing_text',
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide['objectId'],
                    'size': {
                        'height': {'magnitude': 100, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': (page_width - 600) / 2,
                        'translateY': (page_height - 100) / 2,
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
        requests.append({
            'updateTextStyle': {
                'objectId': 'closing_text',
                'style': {
                    'fontSize': {'magnitude': 20, 'unit': 'PT'},
                    'fontFamily': 'Inter',
                    'bold': True,
                    'foregroundColor': hex_to_rgb_color('#00804a')
                },
                'fields': 'fontSize,fontFamily,bold,foregroundColor'
            }
        })
    
    return requests

def main():
    """Main function to create storytelling presentation"""
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
        
        print('Adding storytelling content with Grab design language...')
        content_requests = create_storytelling_content(service, presentation_id)
        
        if content_requests:
            body = {'requests': content_requests}
            response = service.presentations().batchUpdate(
                presentationId=presentation_id,
                body=body).execute()
            print(f'Updated {len(response.get("replies"))} elements')
        
        print(f'\n[SUCCESS] Storytelling presentation created successfully!')
        print(f'[VIEW] https://docs.google.com/presentation/d/{presentation_id}/edit')
        print(f'\n[NOTE] Mosaic images can be added manually once jobs are complete.')
        print(f'[NOTE] Check Mosaic job status and add images to slides for enhanced visual storytelling.')
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

