import { VideoMetadata } from './types';

export const mockVideos: VideoMetadata[] = [
  {
    id: '1',
    url: 'https://www.youtube.com/shorts/tPNKE6vZoQ8',
    thumbnail: 'https://images.unsplash.com/photo-1682687220742-aba19b51f36d',
    title: 'Making the perfect latte art',
    username: 'coffeeart',
    location: 'New York, NY',
    hashtags: ['coffee', 'latteart', 'barista'],
    aiDescription: 'A skilled barista demonstrates the technique of creating intricate latte art patterns using steamed milk and espresso.',
    transcription: 'Today I\'ll show you how to create the perfect rosetta pattern in your latte.',
    engagement: {
      likes: 15000,
      comments: 230,
      shares: 450
    },
    detectedObjects: ['coffee cup', 'milk pitcher', 'espresso machine', 'steam wand']
  },
  {
    id: '2',
    url: 'https://www.youtube.com/shorts/_qn3bsvLnik',
    thumbnail: 'https://images.unsplash.com/photo-1682687221038-404670d5f335',
    title: 'Sunset yoga flow',
    username: 'yogalife',
    location: 'Bali, Indonesia',
    hashtags: ['yoga', 'mindfulness', 'sunset'],
    aiDescription: 'A yoga instructor performs a flowing sequence of poses against a beautiful sunset backdrop on a beach.',
    transcription: 'Begin in mountain pose, taking deep breaths as we flow into our first sun salutation.',
    engagement: {
      likes: 25000,
      comments: 450,
      shares: 800
    },
    detectedObjects: ['yoga mat', 'beach', 'sunset', 'person exercising']
  }
];