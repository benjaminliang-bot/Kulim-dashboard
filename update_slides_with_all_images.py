"""
Script to update the Google Slides presentation with all Mosaic images
Run this after all Mosaic images are generated
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle

# All Mosaic Images for each slide
SLIDE_IMAGES = {
    'hero': None,  # Will be updated
    'journey': 'https://grab.design/api/images/MAnzjbEU1qEK',  # Team Unity
    'honesty': 'https://grab.design/api/images/5yOBjLofGLA4',  # Trust Partnership
    'culture': None,  # Will be updated
    'joy': None,  # Will be updated
    'transformation': 'https://grab.design/api/images/GYL1jpKcaWNv',  # Innovation Thinking
    'triad': 'https://grab.design/api/images/pN3j5x8TJ3rG',  # Empowerment Triad
    'path_forward': None,  # Will be updated
    'commitment': None,  # Will be updated
    'promise': None,  # Will be updated
}

SCOPES = ['https://www.googleapis.com/auth/presentations']

# Update this with your presentation ID
PRESENTATION_ID = '1s30Spc24cvDBO9X9PUdIFlLmq2Rsnevsn_xY4L3mKto'

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

def add_images_to_slides(service, presentation_id, image_urls):
    """Add images to all slides"""
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    page_size = presentation.get('pageSize', {})
    page_width = page_size.get('width', {}).get('magnitude', 720)
    page_height = page_size.get('height', {}).get('magnitude', 405)
    
    requests = []
    
    # Slide 1: Hero Slide
    if len(slides) > 0 and image_urls.get('hero'):
        slide = slides[0]
        requests.append({
            'createImage': {
                'url': image_urls['hero'],
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
    
    # Slide 4: Culture as Foundation
    if len(slides) > 3 and image_urls.get('culture'):
        slide = slides[3]
        requests.append({
            'createImage': {
                'url': image_urls['culture'],
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
    
    # Slide 5: The Source of Joy
    if len(slides) > 4 and image_urls.get('joy'):
        slide = slides[4]
        requests.append({
            'createImage': {
                'url': image_urls['joy'],
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
    
    # Slide 8: The Path Forward
    if len(slides) > 7 and image_urls.get('path_forward'):
        slide = slides[7]
        requests.append({
            'createImage': {
                'url': image_urls['path_forward'],
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
    
    # Slide 9: Our Commitment
    if len(slides) > 8 and image_urls.get('commitment'):
        slide = slides[8]
        requests.append({
            'createImage': {
                'url': image_urls['commitment'],
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
    
    # Slide 10: The Promise
    if len(slides) > 9 and image_urls.get('promise'):
        slide = slides[9]
        requests.append({
            'createImage': {
                'url': image_urls['promise'],
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
    
    return requests

def main():
    """Main function"""
    print('Authenticating with Google Slides API...')
    service = authenticate()
    
    # All Mosaic image URLs
    image_urls = {
        'hero': 'https://grab.design/api/images/4J3l9q1hvkoe',  # Hero slide
        'culture': 'https://grab.design/api/images/D1NYj4Oim37A',  # Culture foundation
        'joy': 'https://grab.design/api/images/9Yl2jq1cJLqK',  # Source of joy
        'path_forward': 'https://grab.design/api/images/29gJnq1Ie2yQ',  # Path forward
        'commitment': 'https://grab.design/api/images/NgYmJaziRoB2',  # Commitment
        'promise': None,  # Will update after job completes
    }
    
    print('Adding images to slides...')
    requests = add_images_to_slides(service, PRESENTATION_ID, image_urls)
    
    if requests:
        body = {'requests': requests}
        try:
            response = service.presentations().batchUpdate(
                presentationId=PRESENTATION_ID,
                body=body).execute()
            print(f'Added {len(response.get("replies"))} images to slides')
        except HttpError as error:
            print(f'An error occurred: {error}')
    else:
        print('No images to add (URLs not yet available)')
    
    print(f'\n[NOTE] Update image_urls dictionary with Mosaic job results and run again')
    print(f'[VIEW] https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit')

if __name__ == '__main__':
    main()

