import React, { useState } from 'react';
import { Search, Sliders } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string, filters: string[]) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);

  const filters = [
    'Content', 'Speech', 'Location', 'Hashtags', 'Objects'
  ];

  const handleSearch = () => {
    onSearch(query, selectedFilters);
  };

  const toggleFilter = (filter: string) => {
    setSelectedFilters(prev => 
      prev.includes(filter) 
        ? prev.filter(f => f !== filter)
        : [...prev, filter]
    );
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="Search videos..."
            className="w-full px-4 py-2 pr-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <Search 
            className="absolute right-3 top-2.5 text-gray-400 cursor-pointer"
            onClick={handleSearch}
          />
        </div>
        <button
          className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50"
          onClick={() => setShowFilters(!showFilters)}
        >
          <Sliders className="w-5 h-5 text-gray-600" />
        </button>
      </div>

      {showFilters && (
        <div className="flex flex-wrap gap-2 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
          {filters.map(filter => (
            <button
              key={filter}
              className={`px-3 py-1 rounded-full text-sm ${
                selectedFilters.includes(filter)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => toggleFilter(filter)}
            >
              {filter}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}