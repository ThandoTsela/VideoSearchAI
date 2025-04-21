import { VideoMetadataDict } from './types';

export const mockVideos: VideoMetadataDict = {
  'https://www.instagram.com/reel/DHBZVUxRu9x/?igsh=MWVlcDRuejVkOWdrbA==': {
    'id': '7',
    'url': 'https://www.instagram.com/reel/DHBZVUxRu9x/?igsh=MWVlcDRuejVkOWdrbA==',
    'thumbnail': 'https://images.unsplash.com/photo-1682687220742-aba19b51f36d',
    'title': 'Making the perfect latte art',
    'username': 'coffeeart',
    'location': 'New York, NY',
    'hashtags': ['coffee', 'latteart', 'barista'],
    'aiDescription': 'A skilled barista demonstrates the technique of creating intricate latte art patterns using steamed milk and espresso.',
    'transcription': 'Today I\'ll show you how to create the perfect rosetta pattern in your latte.',
    'engagement': {
      'likes': 15000,
      'comments': 230,
      'shares': 450
    },
    'detectedObjects': ['coffee cup', 'milk pitcher', 'espresso machine', 'steam wand']
  },
  'https://www.youtube.com/watch?v=1JE2uBVUZyM&t=505s&ab_channel=Codepur': {
    'id': '6',
    'url': 'https://www.youtube.com/watch?v=1JE2uBVUZyM&t=505s&ab_channel=Codepur',
    'thumbnail': 'https://images.unsplash.com/photo-1682687221038-404670d5f335',
    'title': 'Sunset yoga flow',
    'username': 'yogalife',
    'location': 'Bali, Indonesia',
    'hashtags': ['yoga', 'mindfulness', 'sunset'],
    'aiDescription': 'A yoga instructor performs a flowing sequence of poses against a beautiful sunset backdrop on a beach.',
    'transcription': 'Begin in mountain pose, taking deep breaths as we flow into our first sun salutation.',
    'engagement': {
      'likes': 25000,
      'comments': 450,
      'shares': 800
    },
    'detectedObjects': ['yoga mat', 'beach', 'sunset', 'person exercising']
  },
  "https://www.youtube.com/watch?v=LVQwUj1qP8s&t=3s&ab_channel=HealthcareTriage": {
    "id": "1",
    "url": "https://www.youtube.com/watch?v=LVQwUj1qP8s&t=3s&ab_channel=HealthcareTriage",
    "thumbnail": "https://i.ytimg.com/vi/LVQwUj1qP8s/maxresdefault.jpg",
    "title": "Medical Data Sharing and Your Tracker",
    "username": "Healthcare Triage",
    "location": "The news is full",
    "hashtags": [],
    "aiDescription": "The video segment discusses the current state of healthcare technology, highlighting both challenges and opportunities for improvement. The speaker emphasizes the importance of people\\'s behavior change in driving progress, rather than relying solely on new technology.",
    "transcription": "...",
    "engagement": {
      "likes": 39699,
      "comments": 664,
      "shares": 1550
    },
    "detectedObjects": [
      "•"
    ]
  },
  "https://www.youtube.com/shorts/tPNKE6vZoQ8": {
    "id": "2",
    "url": "https://www.youtube.com/shorts/tPNKE6vZoQ8",
    "thumbnail": "https://i.ytimg.com/vi/tPNKE6vZoQ8/hq720.jpg?sqp=-oaymwEkCJUDENAFSFryq4qpAxYIARUAAAAAJQAAyEI9AICiQ3gB0AEB&rs=AOn4CLArgW6H9dGtZqr_q9kNTQc3O98cPw",
    "title": "Are you struggling with your latte art? Perhaps a new pitcher might help ☕️ #coffee #latte #barista",
    "username": "Artisti Coffee Roasters.",
    "location": "New York, NY",
    "hashtags": [
      "lattes",
      "coffeeshorts",
      "coffeevideo"
    ],
    "aiDescription": "The quality of latte art is often dependent on the design of the jug used to pour foam. A standard jug may not be sufficient to achieve perfect latte art, even with proper temperature, texture, and shot quality.",
    "transcription": "...",
    "engagement": {
      "likes": 6171,
      "comments": 601,
      "shares": 1834
    },
    "detectedObjects": [
      "• Standard jug (big round mouth, lacking a good taper)",
      "• New-style jug (better design with a better taper and fine pouring tip)"
    ]
  },
  "https://www.instagram.com/reel/DCRvQ5MuIWy/?utm_source=ig_web_copy_link": {
    "id": "3",
    "url": "https://www.instagram.com/reel/DCRvQ5MuIWy/?utm_source=ig_web_copy_link",
    "thumbnail": "https://scontent-iad3-2.cdninstagram.com/v/t51.29350-15/466669695_907321674682816_3250104124243534624_n.jpg?stp=cmp1_dst-jpg_e35_s640x640_tt6&_nc_cat=105&ccb=1-7&_nc_sid=18de74&_nc_ohc=5gxMJL5JHBYQ7kNvwGLnA1m&_nc_oc=Admn4MNUjvLyVnvVV2x_Hva_sHkAWTKp3apx_4NVTymnk7EgytR-V751-3Tb5lolRIE&_nc_zt=23&_nc_ht=scontent-iad3-2.cdninstagram.com&_nc_gid=3u0W50tCAWI5nXAmq86taQ&oh=00_AfHJudWXtcum9NzBsM_F6yTv82a8GOSw5cKJ4C5qbGkeGw&oe=680C5F6E",
    "title": "Squat University | A KEY technique tip for push-ups! Send this to a friend who needs it! \n.\nShout out macsthenics/TT for the opening stitched video &... | Instagram",
    "username": "instagram_user",
    "location": "Los Angeles, CA",
    "hashtags": [],
    "aiDescription": "The provided video segment is a brief introduction to a technique tip for push-ups.",
    "transcription": "...",
    "engagement": {
      "likes": 22575,
      "comments": 824,
      "shares": 1873
    },
    "detectedObjects": [
      "None."
    ]
  },
  "https://www.youtube.com/shorts/yQ121gMqsik": {
    "id": "4",
    "url": "https://www.youtube.com/shorts/yQ121gMqsik",
    "thumbnail": "https://i.ytimg.com/vi/yQ121gMqsik/oar2.jpg?sqp=-oaymwEkCJUDENAFSFqQAgHyq4qpAxMIARUAAAAAJQAAyEI9AICiQ3gB&rs=AOn4CLBFucnILZalbgsp6AISSgSZWaospg",
    "title": "The Most TERRIFYING Ring Introduction Of All Time 🥶",
    "username": "ShortsForFun",
    "location": "The Most TERRIFYING Ring",
    "hashtags": [
      "scary",
      "goosebumps",
      "chilling"
    ],
    "aiDescription": "This segment provides an introduction to a professional boxer, highlighting his achievements and credentials. The text presents several key facts about the boxer\\'s record, titles, and unique records.",
    "transcription": "...",
    "engagement": {
      "likes": 6992,
      "comments": 530,
      "shares": 91
    },
    "detectedObjects": [
      "Boxer"
    ]
  },
  "https://www.youtube.com/watch?v=yY9U89S-Wig&ab_channel=zap": {
    "id": "5",
    "url": "https://www.youtube.com/watch?v=yY9U89S-Wig&ab_channel=zap",
    "thumbnail": "https://i.ytimg.com/vi/yY9U89S-Wig/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AHOBYACgAqKAgwIABABGGUgSyhEMA8=&rs=AOn4CLAfaT2PWocCGsZ9rRva43kd52oX4A",
    "title": "koenigsegg gemera reaction",
    "username": "zap",
    "location": "Los Angeles, CA",
    "hashtags": [],
    "aiDescription": "Koenigsegg, a renowned car manufacturer, has introduced the Jumeirah, a new vehicle featuring an impressive power output.",
    "transcription": "...",
    "engagement": {
      "likes": 7823,
      "comments": 354,
      "shares": 917
    },
    "detectedObjects": [
      "• Koenigsegg Jumeirah"
    ]
  }
};
