\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\title{Deck - Your Daily News Dashboard}
\date{}

\begin{document}

\maketitle

\section*{Overview}
Deck is a dynamic news aggregation application designed to deliver the latest and most relevant news articles from a variety of sources. This application leverages the power of React for the frontend, providing a seamless and responsive user interface. The backend is powered by Flask, ensuring efficient server-side logic and API management.

\section*{Technologies Used}
\begin{itemize}
    \item \textbf{Frontend:} React.js - A JavaScript library for building user interfaces.
    \item \textbf{Backend:} Flask - A micro web framework written in Python, used for handling backend operations.
    \item \textbf{Database:} MongoDB - A NoSQL database that offers high performance, high availability, and easy scalability.
    \item \textbf{APIs:}
    \begin{itemize}
        \item Reddit API: For fetching trending news and discussions from various subreddits.
        \item News API: For obtaining breaking news headlines and searching for news from multiple sources.
    \end{itemize}
    \item \textbf{Web Scraping:}
    \begin{itemize}
        \item BeautifulSoup: A Python library for pulling data out of HTML and XML files. It's used to scrape websites that do not offer an API.
    \end{itemize}
\end{itemize}

\section*{Features}
\begin{itemize}
    \item News Feed: Aggregates news from multiple sources to provide a comprehensive view of current events.
    \item Customizable Dashboard: Users can customize their news feed based on their preferences and interests.
    \item Search Functionality: Allows users to search for news articles by keywords.
    \item Social Media Integration: Directly fetches news from trending social media topics using the Reddit API.
\end{itemize}

\section*{Setup Instructions}
\begin{enumerate}
    \item Clone the Repository:
    \begin{verbatim}
    git clone https://github.com/yourgithubusername/Deck.git
    cd Deck
    \end{verbatim}
    \item Install Dependencies:
    \begin{itemize}
        \item For the frontend:
        \begin{verbatim}
        cd client
        npm install
        npm start
        \end{verbatim}
        \item For the backend:
        \begin{verbatim}
        cd server
        pip install -r requirements.txt
        flask run
        \end{verbatim}
    \end{itemize}
    \item Database Configuration:
    \begin{itemize}
        \item Ensure MongoDB is set up and running.
        \item Adjust the database connection settings in \texttt{dbSetup.js}.
    \end{itemize}
    \item API Keys:
    \begin{itemize}
        \item Obtain API keys for Reddit and News API.
        \item Configure environmental variables for secure access.
    \end{itemize}
\end{enumerate}

\section*{Contributions}
We welcome contributions to Deck. Please feel free to fork the repository, make improvements, and submit a pull request. Check out the issues tab for pending improvements and bug fixes.

\end{document}
