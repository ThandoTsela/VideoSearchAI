import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { VideoCard } from './components/VideoCard';
import { mockVideos } from './mockData';
import { VideoMetadata } from './types';
import { Camera } from 'lucide-react';
import Fuse from 'fuse.js';

function App() {
  const [searchResults, setSearchResults] = useState<VideoMetadata[]>(mockVideos);

  const handleSearch = (query: string, filters: string[]) => {
    // In a real application, this would make an API call with the query and filters

    // If the query is empty, return all videos
    if (!query.trim()) {
      setSearchResults(mockVideos);
      return;
    }

    // Perform fuzzy search using Fuse.js
    const fuse = new Fuse(mockVideos, {
      keys: ['title', 'username', 'aiDescription', 'transcription', 'hashtags', 'detectedObjects', 'location'],
      includeScore: true,
      threshold: 0.5, // Adjust threshold for fuzziness (0 = exact match, 1 = very loose match)
    });

    const results = fuse.search(query).map(result => result.item);

    // const results = mockVideos.filter(video => {
    //   const searchString = `
    //     ${video.title.toLowerCase()}
    //     ${video.username.toLowerCase()}
    //     ${video.aiDescription.toLowerCase()}
    //     ${video.transcription.toLowerCase()}
    //     ${video.hashtags.join(' ').toLowerCase()}
    //     ${video.detectedObjects.join(' ').toLowerCase()}
    //     ${video.location?.toLowerCase() || ''}
    //   `;
      
    //   return searchString.includes(query.toLowerCase());
    // });
    
    setSearchResults(results);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 py-4 mb-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Camera className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">VideoSearch AI</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 pb-12">
        <SearchBar onSearch={handleSearch} />
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {searchResults.map(video => (
            <VideoCard key={video.id} video={video} />
          ))}
        </div>

        {searchResults.length === 0 && (
          <div className="text-center mt-12">
            <p className="text-gray-500">No videos found matching your search criteria.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;