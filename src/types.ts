export interface VideoMetadata {
  id: string;
  url: string;
  thumbnail: string;
  title: string;
  username: string;
  location?: string;
  hashtags: string[];
  aiDescription: string;
  transcription: string;
  engagement: {
    likes: number;
    comments: number;
    shares: number;
  };
  detectedObjects: string[];
}