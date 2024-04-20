// components/PicksForYou.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PicksForYou = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/picks-for-you')
      .then(response => {
        setNews(response.data.articles);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);


  if (loading) {
    return <div>Loading news...</div>;
  }

  if (error === 500) {
    return <div>Sorry you must be logged in to use this Feature!</div>;
  }

  if (error) {  
    return <div>There was an error getting the news: {error.message}</div>;
  }

  return (
    <div>
      {news && news.length > 0 ? (
        news.map((article, index) => (
          <div key={index} className="article">
            <h2 className='articleTitle'>{article.title} </h2>
            {article.urlToImage && (
              <img src={article.urlToImage} alt={article.title} width="20%" />
            )}
            <p>{article.description}</p>
            <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
          </div>
        ))
      ) : (
        <div>No news articles found.</div>
      )}
    </div>
  );
};




export default PicksForYou;
