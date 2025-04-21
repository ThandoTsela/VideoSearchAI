from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import re
import requests
import urllib.parse
from typing import Optional, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

import json
from typing import Dict, Any
import random

try:
     import tomllib
except ModuleNotFoundError:
     import tomli as tomllib
with open("src/services/videoURLs.toml", mode="rb") as fp:
     config = tomllib.load(fp)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

class VideoResponse(BaseModel):
    id: str
    url: str
    title: str
    aiDescription: str
    detectedObjects: List[str]
    transcription: str

class VideoSummarizer:
    def __init__(self):
        """
        Initialize summarizer with Llama 3 via Ollama
        """
        self.llm = OllamaLLM(
            model="llama3", 
            temperature=0.7, 
            num_ctx=4096)
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.map_prompt = PromptTemplate(
            template="""
            Analyze this video segment:
            {text}
            
            Extract:
            - Key points
            - Important facts
            - Central arguments
            Key Points:
            """,
            input_variables=["text"]
        )
        
        self.combine_prompt = PromptTemplate(
            template="""
            Create a structured summary from these points in the given order and make sure that the response is under one of the titles for data extraction purposes:
            {text}
            
            Include:
            1. Overview
            2. Core Content and key takeaways(3-5 bullet points)
            3. Identified Objects
            """,
            input_variables=["text"]
        )
        
        self.chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce",
            map_prompt=self.map_prompt,
            combine_prompt=self.combine_prompt,
            verbose=False
        )

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract ID from YouTube/Instagram URLs
        """
        # YouTube patterns
        youtube_patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?]*)',
            r'(?:youtube\.com/shorts/)([^&\n?]*)'
        ]
        
        # Instagram pattern
        instagram_pattern = r'(?:instagram\.com/)(?:reel|reels)/([^/?]*)'
    
        for pattern in youtube_patterns:
            match = re.search(pattern, url)
            if match:
                return {'source': 'youtube', 'id': match.group(1)}
    
        insta_match = re.search(instagram_pattern, url)
        if insta_match:
            return {'source': 'instagram', 'id': insta_match.group(1)}
        
        return None

    def get_transcript(self, video_info: Dict[str, str]) -> str:
        """
        Get transcript/text from different platforms
        """
        try:
            if video_info['source'] == 'youtube':
                transcript = YouTubeTranscriptApi.get_transcript(video_info['id'])
                return " ".join([entry['text'] for entry in transcript])
            
            elif video_info['source'] == 'instagram':
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                encoded_url = urllib.parse.quote_plus(f"https://www.instagram.com/reel/{video_info['id']}/")

                # response = requests.get(
                #    f"https://www.instagram.com/p/{video_info['id']}/?__a=1&__d=dis", 
                #    headers=headers)
                
                response = requests.get(
                    f"https://www.instagram.com/reel/{video_info['id']}/embed/captioned/",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code != 200:
                    return "Could not fetch Instagram content"
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try multiple methods to extract caption
                caption = soup.find('div', {'class': 'Caption'}) or \
                        soup.find('meta', property='og:description') or \
                        soup.find('title')
                
                return caption.get_text().strip() if caption else "No caption available"
                
        except Exception as e:
            raise Exception(f"Error getting content: {str(e)}")

    def summarize_video(self, video_url: str) -> Dict[str, Any]:
        """
        Summarize video from any supported platform
        """
        try:
            video_info = self.extract_video_id(video_url)
            if not video_info:
                return {"status": "error", "message": "Unsupported URL format"}
            
            # Get content based on platform
            content = self.get_transcript(video_info)
            
            # Split content into chunks
            texts = self.text_splitter.create_documents([content])
            
            # Generate summary
            summary = self.chain.invoke({"input_documents": texts})["output_text"]
            
            return {
                "status": "success",
                "summary": summary,
                "platform": video_info['source'],
                "video_id": video_info['id'],
                "model": "llama3"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# def main():
#     summarizer = VideoSummarizer()
    
#     # Test with different video types
#     # test_urls = [
#     #     "https://www.youtube.com/watch?v=LVQwUj1qP8s&t=3s&ab_channel=HealthcareTriage",  # Regular YouTube - Healthcare
#     #     "https://www.youtube.com/shorts/tPNKE6vZoQ8",  # YouTube Shorts - barrista coffee
#     #     "https://www.instagram.com/reel/DCRvQ5MuIWy/?utm_source=ig_web_copy_link",  # Instagram Reel - workout push ups
#     #     "https://www.youtube.com/shorts/yQ121gMqsik", # YouTube Shorts - berkowitz introduction
#     #     "https://www.youtube.com/watch?v=yY9U89S-Wig&ab_channel=zap" #Youtube video - AzizDrives talking about gemera
#     # ]
    
#     for url in config['test_urls']:
#         print(f"\nSummarizing: {url}")
#         result = summarizer.summarize_video(url)
        
#         if result["status"] == "success":
#             print(f"\nPlatform: {result['platform'].upper()}")
#             print(f"\nSummary:\n{result['summary']}")
#         else:
#             print(f"Error: {result['message']}")

# if __name__ == "__main__":
#     main()

def scrape_video_metadata(url: str) -> Dict[str, Any]:
    """Scrape title, username, thumbnail from YouTube/Instagram URLs"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if 'youtube.com' in url:
            # YouTube scraping
            title = soup.find('meta', property='og:title')
            title = title['content'] if title else "Untitled YouTube Video"
            
            username = soup.find('link', itemprop='name')
            username = username['content'] if username else "YouTube Creator"
            
            thumbnail = soup.find('meta', property='og:image')
            thumbnail = thumbnail['content'] if thumbnail else f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}"
            
            # Try to get location from description
            description = soup.find('meta', property='og:description')
            description = description['content'] if description else ""
            location_match = re.search(r'(\b\w+\b(?:\s+\b\w+\b){1,3})', description)
            location = location_match.group(0) if location_match else random.choice(['New York, NY', 'Los Angeles, CA'])
            
            # Extract hashtags from description
            hashtags = re.findall(r'#(\w+)', description)[:3]
            
        elif 'instagram.com' in url:
            # Instagram scraping
            title = soup.find('title')
            title = title.text if title else "Untitled Instagram Video"
            
            username = soup.find('meta', property='instapp:owner_user_name')
            username = username['content'] if username else "instagram_user"
            
            thumbnail = soup.find('meta', property='og:image')
            thumbnail = thumbnail['content'] if thumbnail else f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}"
            
            # Try to get location
            location_tag = soup.find('a', href=lambda x: x and '/explore/locations/' in x)
            location = location_tag.text if location_tag else random.choice(['New York, NY', 'Los Angeles, CA'])
            
            # Extract hashtags
            hashtag_tags = soup.find_all('a', href=lambda x: x and '/tags/' in x)
            hashtags = [tag.text for tag in hashtag_tags][:3]
        
        return {
            'title': title,
            'username': username,
            'thumbnail': thumbnail,
            'location': location,
            'hashtags': hashtags
        }
        
    except Exception as e:
        print(f"Scraping error for {url}: {str(e)}")
        return {
            'title': "Untitled Video",
            'username': "unknown_user",
            'thumbnail': f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}",
            'location': random.choice(['New York, NY', 'Los Angeles, CA', 'Bali, Indonesia', 'London, UK']),
            'hashtags': []
        }

def extract_ai_description(summary: str) -> str:
    """Extract description between **Overview** and **Core Content** with better handling"""
    # First try strict pattern matching
    overview_match = re.search(
        r'\*\*Overview\*\*\s*(.*?)\s*\*\*Core Content',
        summary,
        re.DOTALL
    )
    
    if overview_match:
        description = overview_match.group(1).strip()
        # Clean up any remaining markdown artifacts
        description = re.sub(r'\*\*|\n\s*\n', ' ', description)
        return description
    
    # Fallback: Extract first meaningful paragraph if standard markers not found
    first_paragraph = re.split(r'\n\s*\n', summary)[0]
    return first_paragraph.strip()

def extract_objects_from_summary(summary: str) -> List[str]:
    """More robust object extraction handling different formats"""
    # Pattern 1: **Identified Objects** followed by list
    objects_section = re.search(
        r'\*\*Identified Objects\*\*[:\n]*(.*?)(?:\*\*|$)',
        summary,
        re.DOTALL
    )
    
    if objects_section:
        objects_text = objects_section.group(1).strip()
        # Handle both numbered and bulleted lists
        objects = [
            re.sub(r'^[\d\.\-\*\s]+', '', line).strip()
            for line in objects_text.split('\n')
            if line.strip() and not line.strip().startswith('**')
        ]
        if objects:
            return objects
    
    # Pattern 2: Look for "• Object" pattern anywhere in summary
    bullet_objects = re.findall(r'•\s*([^\n]+)', summary)
    if bullet_objects:
        return [obj.strip() for obj in bullet_objects]
    
    # Pattern 3: Numbered list
    numbered_objects = re.findall(r'\d+\.\s*([^\n]+)', summary)
    if numbered_objects:
        return [obj.strip() for obj in numbered_objects]
    
    # Final fallback: Return empty list
    return []

def load_existing_mock_data(filepath: str) -> Dict[str, Any]:
    """Load existing mock data if file exists"""
    if not os.path.exists(filepath):
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract the dictionary part
            dict_content = re.search(
                r'mockVideos:\s*VideoMetadataDict\s*=\s*({.*?});',
                content,
                re.DOTALL
            )
            if dict_content:
                # Convert TypeScript-style quotes to JSON
                json_str = dict_content.group(1)
                return json.loads(json_str)
    except Exception as e:
        print(f"Error loading existing data: {e}")
    return {}

def main():
    summarizer = VideoSummarizer()
    output_file = 'src/mockData.ts'
    
    # Load existing data
    existing_data = load_existing_mock_data(output_file)
    updated_data = existing_data.copy()
    
    for url in config['test_urls']:
        # Skip if URL already exists
        if url in updated_data:
            print(f"Skipping existing URL: {url}")
            continue
            
        print(f"\nProcessing: {url}")
        
        # Scrape metadata
        scraped_data = scrape_video_metadata(url)
        
        # Get AI analysis
        result = summarizer.summarize_video(url)
        
        if result["status"] == "success":
            # Extract the specific parts we need
            ai_description = extract_ai_description(result['summary'])
            detected_objects = extract_objects_from_summary(result['summary'])
            
            # Generate mock data entry
            updated_data[url] = {
                'id': str(len(updated_data) + 1),
                'url': url,
                'thumbnail': scraped_data['thumbnail'],
                'title': scraped_data['title'],
                'username': scraped_data['username'],
                'location': scraped_data['location'],
                'hashtags': scraped_data['hashtags'],
                'aiDescription': ai_description.replace("'", r"\'"),  # Properly escape single quotes
                'transcription': result.get('transcription', '')[:200] + '...',
                'engagement': {
                    'likes': random.randint(1000, 50000),
                    'comments': random.randint(50, 1000),
                    'shares': random.randint(50, 2000)
                },
                'detectedObjects': detected_objects or ['object1', 'object2']  # fallback
            }
            print(f"Added: {url}")
        else:
            print(f"Error processing {url}: {result['message']}")
    
    # Generate TypeScript content
    ts_content = f"""import {{ VideoMetadataDict }} from './types';

export const mockVideos: VideoMetadataDict = {json.dumps(updated_data, indent=2, ensure_ascii=False)};
"""
    
    # Write to file (overwrite mode)
    with open('src/mockData.ts', 'a', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"\nUpdated {output_file} with {len(updated_data)} entries")

if __name__ == "__main__":
    main()