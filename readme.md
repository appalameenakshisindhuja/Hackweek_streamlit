# Taylor Swift Lyrics Word Cloud Generator

## Overview

This is a Streamlit web application that allows users to search for Taylor Swift songs, fetch their lyrics from the Genius API, and generate beautiful word clouds from the lyrics text. The application provides an interactive interface for exploring Taylor Swift's songwriting through visual word frequency analysis.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface for user interaction
- **Lyrics Fetching**: Dedicated module for interacting with the Genius API
- **Word Cloud Generation**: Specialized component for text processing and visualization
- **Session Management**: Streamlit's built-in session state for maintaining user data

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Technology**: Streamlit framework
- **Responsibilities**: 
  - Page configuration and layout management
  - User input handling
  - Component initialization with caching
  - Session state management

### 2. Lyrics Fetcher (`lyrics_fetcher.py`)
- **Purpose**: Interface with Genius API for song search and lyrics retrieval
- **Key Features**:
  - Song search with Taylor Swift artist filtering
  - Web scraping for lyrics extraction
  - Error handling for API requests
  - Request timeout management

### 3. Word Cloud Generator (`wordcloud_generator.py`)
- **Purpose**: Text processing and word cloud visualization
- **Key Features**:
  - Comprehensive stop words filtering
  - Text preprocessing and cleaning
  - Custom word frequency analysis
  - Visual word cloud generation

## Data Flow

1. **User Input**: User enters a Taylor Swift song title
2. **Song Search**: Application queries Genius API for matching songs
3. **Artist Filtering**: Results are filtered to ensure Taylor Swift authorship
4. **Lyrics Retrieval**: Song URL is used to scrape lyrics content
5. **Text Processing**: Lyrics are cleaned and preprocessed for analysis
6. **Word Cloud Generation**: Processed text is converted to visual word cloud
7. **Display**: Results are presented in the Streamlit interface

## External Dependencies

### APIs
- **Genius API**: Primary data source for song information and lyrics
  - Requires API key via `GENIUS_API_KEY` environment variable
  - RESTful API with rate limiting considerations

### Python Libraries
- **Streamlit**: Web application framework
- **Requests**: HTTP client for API interactions
- **BeautifulSoup**: HTML parsing for web scraping
- **WordCloud**: Word cloud generation library
- **Matplotlib**: Visualization backend
- **NumPy**: Numerical operations support

## Deployment Strategy

The application is designed for cloud deployment with the following considerations:

- **Environment Variables**: API key configuration through environment variables
- **Caching Strategy**: Streamlit resource caching for performance optimization
- **Error Handling**: Graceful degradation when API services are unavailable
- **Timeout Management**: Request timeouts to prevent hanging connections

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 28, 2025. Initial setup