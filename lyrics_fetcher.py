import requests
import re
import os
from bs4 import BeautifulSoup
import time

class LyricsFetcher:
    def __init__(self):
        self.api_key = os.getenv("GENIUS_API_KEY", "")
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Taylor Swift Lyrics App"
        }
    
    def search_song(self, query):
        """Search for a song on Genius"""
        search_url = f"{self.base_url}/search"
        params = {
            "q": f"Taylor Swift {query}"
        }
        
        try:
            response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("response") and data["response"].get("hits"):
                # Filter for Taylor Swift songs
                for hit in data["response"]["hits"]:
                    song = hit.get("result", {})
                    artist = song.get("primary_artist", {})
                    
                    # Check if it's a Taylor Swift song
                    if artist and "taylor swift" in artist.get("name", "").lower():
                        return {
                            "id": song.get("id"),
                            "title": song.get("title"),
                            "url": song.get("url"),
                            "artist": artist.get("name")
                        }
            
            return None
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Search request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Search error: {str(e)}")
    
    def get_lyrics_from_url(self, song_url):
        """Scrape lyrics from Genius song page"""
        try:
            # Add delay to be respectful to the server
            time.sleep(1)
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(song_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors for lyrics
            lyrics_selectors = [
                'div[data-lyrics-container="true"]',
                'div[class*="lyrics"]',
                'div[class*="Lyrics__Container"]',
                '[data-lyrics-container]'
            ]
            
            lyrics_text = ""
            
            for selector in lyrics_selectors:
                lyrics_containers = soup.select(selector)
                if lyrics_containers:
                    for container in lyrics_containers:
                        # Remove script and style elements
                        for script in container(["script", "style"]):
                            script.decompose()
                        
                        # Get text and clean it
                        text = container.get_text(separator='\n', strip=True)
                        if text:
                            lyrics_text += text + '\n'
                    
                    if lyrics_text.strip():
                        break
            
            if not lyrics_text.strip():
                # Fallback: try to find any div with lyrics-like content
                all_divs = soup.find_all('div')
                for div in all_divs:
                    text = div.get_text(strip=True)
                    if len(text) > 100 and any(word in text.lower() for word in ['verse', 'chorus', 'bridge', 'outro', 'intro']):
                        lyrics_text = text
                        break
            
            if lyrics_text.strip():
                # Clean up the lyrics
                lyrics_text = self.clean_lyrics(lyrics_text)
                return lyrics_text
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch lyrics page: {str(e)}")
        except Exception as e:
            raise Exception(f"Lyrics extraction error: {str(e)}")
    
    def clean_lyrics(self, lyrics):
        """Clean and format lyrics text"""
        # Remove common non-lyric elements
        lines_to_remove = [
            r'\[.*?\]',  # Remove [Verse 1], [Chorus], etc.
            r'^\d+$',    # Remove standalone numbers
            r'^embed$',  # Remove "embed" text
            r'.*lyrics.*genius.*',  # Remove Genius attribution
            r'.*see.*live.*',  # Remove "see live" text
        ]
        
        lines = lyrics.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line should be removed
            should_remove = False
            for pattern in lines_to_remove:
                if re.search(pattern, line, re.IGNORECASE):
                    should_remove = True
                    break
            
            if not should_remove and len(line) > 1:
                cleaned_lines.append(line)
        
        # Join lines and clean up extra whitespace
        cleaned_lyrics = '\n'.join(cleaned_lines)
        cleaned_lyrics = re.sub(r'\n\s*\n', '\n\n', cleaned_lyrics)  # Fix multiple newlines
        cleaned_lyrics = re.sub(r'[ \t]+', ' ', cleaned_lyrics)  # Fix multiple spaces
        
        return cleaned_lyrics.strip()
    
    def fetch_lyrics(self, song_title):
        """Main method to fetch lyrics for a song"""
        if not self.api_key:
            raise Exception("Genius API key not found. Please set GENIUS_API_KEY environment variable.")
        
        try:
            # Search for the song
            song_info = self.search_song(song_title)
            
            if not song_info:
                return None
            
            # Get lyrics from the song URL
            lyrics = self.get_lyrics_from_url(song_info["url"])
            
            if not lyrics:
                raise Exception("Could not extract lyrics from the page")
            
            return lyrics
            
        except Exception as e:
            raise Exception(f"Failed to fetch lyrics: {str(e)}")
