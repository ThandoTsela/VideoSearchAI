import React from 'react';
import { X } from 'lucide-react';

interface VideoModalProps {
  url: string;
  onClose: () => void;
}

export function VideoModal({ url, onClose }: VideoModalProps) {
  const isYouTubeShorts = url.includes('youtube.com/shorts');
  const isInstagramReels = url.includes('instagram.com/reel');

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="relative w-full max-w-4xl mx-4">
        <button
          onClick={onClose}
          className="absolute -top-10 right-0 text-white hover:text-gray-300"
        >
          <X className="w-6 h-6" />
        </button>
        <div className="bg-black rounded-lg overflow-hidden aspect-video">
          {isYouTubeShorts || isInstagramReels ? (
            <div className="flex items-center justify-center h-full">
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-white underline"
              >
                {isYouTubeShorts
                  ? 'Watch this YouTube Short on YouTube'
                  : 'Watch this Instagram Reel on Instagram'}
              </a>
            </div>
          ) : (
            <iframe
              src={getEmbedUrl(url)}
              className="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title="Video player"
            />
          )}
        </div>
      </div>
    </div>
  );
}

const getEmbedUrl = (url: string): string => {
  // Handle YouTube URLs
  if (url.includes('youtube.com') || url.includes('youtu.be')) {
    let videoId = '';
    if (url.includes('v=')) {
      // Extract video ID from standard YouTube URLs
      videoId = url.split('v=')[1]?.split('&')[0] || '';
    } else if (url.includes('youtu.be')) {
      // Extract video ID from shortened YouTube URLs
      videoId = url.split('youtu.be/')[1]?.split('?')[0] || '';
    }
    return `https://www.youtube.com/embed/${videoId}?autoplay=1`; // Add autoplay
  }

  // Handle Instagram URLs
  if (url.includes('instagram.com')) {
    const reelUrl = url.split('?')[0]; // Remove query parameters
    return reelUrl.replace('/reel/', '/embed/');
  }

  // Return the original URL for other cases
  return url;
};