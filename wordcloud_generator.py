from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import numpy as np
from collections import Counter
import io
import base64

class WordCloudGenerator:
    def __init__(self):
        # Common English stop words plus some song-specific ones
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
            'just', 'don', 'should', 'now', 'oh', 'yeah', 'na', 'la', 'da', 'uh', 'mm', 'hmm',
            'ooh', 'ah', 'eh', 'hey', 'wo', 'whoa', 'got', 'get', 'go', 'come', 'came', 'going',
            'like', 'know', 'one', 'two', 'say', 'said', 'tell', 'told', 'way', 'back', 'could',
            'would', 'should', 'might', 'must', 'shall', 'let', 'make', 'take', 'give', 'put'
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess text for word cloud generation"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation and special characters, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Split into words and filter
        words = text.split()
        
        # Filter out stop words and short words
        filtered_words = [
            word for word in words 
            if word not in self.stop_words and len(word) > 2
        ]
        
        return ' '.join(filtered_words)
    
    def generate_wordcloud(self, lyrics, max_words=100, width=600, height=400, 
                          background_color='white', colormap='viridis'):
        """Generate a word cloud from lyrics"""
        try:
            # Preprocess the lyrics
            processed_text = self.preprocess_text(lyrics)
            
            if not processed_text.strip():
                raise Exception("No valid words found in lyrics after preprocessing")
            
            # Create WordCloud object
            wordcloud = WordCloud(
                width=width,
                height=height,
                background_color=background_color,
                max_words=max_words,
                relative_scaling=0.5,
                colormap=colormap,
                stopwords=self.stop_words,
                collocations=False,  # Avoid pairing words
                max_font_size=100,
                min_font_size=10,
                prefer_horizontal=0.7,
                scale=2,
                random_state=42  # For reproducible results
            ).generate(processed_text)
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(width/100, height/100))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            
            # Tight layout to remove extra whitespace
            plt.tight_layout(pad=0)
            
            return fig
            
        except Exception as e:
            raise Exception(f"Word cloud generation failed: {str(e)}")
    
    def get_word_frequencies(self, lyrics, top_n=20):
        """Get word frequencies from lyrics"""
        try:
            processed_text = self.preprocess_text(lyrics)
            words = processed_text.split()
            
            if not words:
                return {}
            
            # Count word frequencies
            word_freq = Counter(words)
            
            # Get top N words
            top_words = dict(word_freq.most_common(top_n))
            
            return top_words
            
        except Exception as e:
            raise Exception(f"Word frequency analysis failed: {str(e)}")
    
    def generate_custom_wordcloud(self, lyrics, custom_colors=None, custom_font=None):
        """Generate a custom styled word cloud"""
        try:
            processed_text = self.preprocess_text(lyrics)
            
            if not processed_text.strip():
                raise Exception("No valid words found in lyrics")
            
            # Custom color function
            def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                if custom_colors:
                    return np.random.choice(custom_colors)
                else:
                    # Default Taylor Swift themed colors
                    swift_colors = ['#8B4513', '#DAA520', '#DC143C', '#4B0082', '#2F4F4F', '#8B0000']
                    return np.random.choice(swift_colors)
            
            # Create WordCloud with custom styling
            wordcloud = WordCloud(
                width=800,
                height=600,
                background_color='white',
                max_words=150,
                relative_scaling=0.5,
                color_func=custom_color_func,
                stopwords=self.stop_words,
                collocations=False,
                max_font_size=120,
                min_font_size=15,
                prefer_horizontal=0.8,
                scale=3,
                random_state=42
            ).generate(processed_text)
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout(pad=0)
            
            return fig
            
        except Exception as e:
            raise Exception(f"Custom word cloud generation failed: {str(e)}")
