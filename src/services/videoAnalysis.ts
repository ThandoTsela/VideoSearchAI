import axios from 'axios';
import { isURL } from 'validator';

interface VideoAnalysisResponse {
  summary: string;
  detectedObjects: string[];
}

export async function analyzeVideo(url: string): Promise<VideoAnalysisResponse> {
  // Validate the URL
  if (!isURL(url)) {
    console.error('Invalid URL:', url);
    return {
      summary: "Invalid video URL.",
      detectedObjects: [],
    };
  }

  try {
    const yourAuthToken = 'your-auth-token-here'; // Replace with actual token
    const response = await axios.post('/api/analyze-video', { url }, {
      headers: {
        'Authorization': `Bearer ${yourAuthToken}`, // Add if needed
        'Content-Type': 'application/json',
      },
      timeout: 5000, // 5 seconds
    });
    return response.data;
  } catch (error) {
    const err = error as any;
    console.error('Error analyzing video:', err.response?.data || err.message);
    return {
      summary: "Unable to analyze video at this time.",
      detectedObjects: [],
    };
  }
}

const videoUrl = 'https://example.com/video.mp4';

analyzeVideo(videoUrl)
  .then((analysis) => {
    console.log('Video Summary:', analysis.summary);
    console.log('Detected Objects:', analysis.detectedObjects);
  })
  .catch((error) => {
    console.error('Unexpected error:', error);
  });