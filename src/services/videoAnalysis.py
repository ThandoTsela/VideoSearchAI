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
            Create a structured summary from these points:
            {text}
            
            Include:
            1. Overview
            2. Core Content and key takeaways(3-5 bullet points)
            3. list of Identified objects
            
            Final Summary:
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

def main():
    summarizer = VideoSummarizer()
    
    # Test with different video types
    test_urls = [
        "https://www.youtube.com/watch?v=LVQwUj1qP8s&t=3s&ab_channel=HealthcareTriage",  # Regular YouTube - Healthcare
        "https://www.youtube.com/shorts/tPNKE6vZoQ8",  # YouTube Shorts - barrista coffee
        "https://www.instagram.com/reel/DCRvQ5MuIWy/?utm_source=ig_web_copy_link",  # Instagram Reel - workout push ups
        "https://www.youtube.com/shorts/yQ121gMqsik", # YouTube Shorts - berkowitz introduction
        "https://www.youtube.com/watch?v=yY9U89S-Wig&ab_channel=zap" #Youtube video - AzizDrives talking about gemera
    ]
    
    for url in test_urls:
        print(f"\nSummarizing: {url}")
        result = summarizer.summarize_video(url)
        
        if result["status"] == "success":
            print(f"\nPlatform: {result['platform'].upper()}")
            print(f"\nSummary:\n{result['summary']}")
        else:
            print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()