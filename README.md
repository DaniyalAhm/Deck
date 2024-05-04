# Deck - Your Daily News Dashboard

## Overview
Deck is a dynamic news aggregation application designed to deliver the latest and most relevant news articles from a variety of sources. This application leverages the power of React for the frontend, providing a seamless and responsive user interface. The backend is powered by Flask, ensuring efficient server-side logic and API management.

## Technologies Used
- **Frontend**: React.js - A JavaScript library for building user interfaces.
- **Backend**: Flask - A micro web framework written in Python, used for handling backend operations.
- **Database**: MongoDB - A NoSQL database that offers high performance, high availability, and easy scalability.
- **APIs**:
  - **Reddit API**: For fetching trending news and discussions from various subreddits.
  - **News API**: For obtaining breaking news headlines and searching for news from multiple sources.
- **Web Scraping**:
  - **BeautifulSoup**: A Python library for pulling data out of HTML and XML files. It's used to scrape websites that do not offer an API.

## Features
- **News Feed**: Aggregates news from multiple sources to provide a comprehensive view of current events.
- **Customizable Dashboard**: Users can customize their news feed based on their preferences and interests.
- **Search Functionality**: Allows users to search for news articles by keywords.
- **Social Media Integration**: Directly fetches news from trending social media topics using the Reddit API.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone git@github.com:DaniyalAhm/411-project.git
   cd 411-project
   touch /backend/.env
   
2. **Enter API Keys**
    ```bash
        echo "NEWS_API=YOUR_API_KEY_HERE" >> /backend/..env
        echo "REDDIT_API=YOUR_API_KEY_HERE" >> /backend/.env
        echo "MONGO_URI=YOUR_MONGO_DATABASE_HERE" >> /backend/.env
        echo "GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE" >> /backend/.env

        


## Known Bugs
Sometimes SSL requests do not go through in web scrapping, this is because of website we are trying to scrap from has a invalid signature error, this will be fixed in the future

## Credits
- Canwbu
- cliz101
