// NewsComponent.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import loadingGif from './loading.gif';




const Entertainment = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/Entertainment')
      .then(response => {
        console.log("News data:", response.data);  // Log the data received
        setNews(response.data.articles);  // Make sure this matches the structure of your data
        setLoading(false);
      })
      .catch(error => {
        console.error("Fetching error:", error);
        setError(error);
        setLoading(false);
      });
  }, []);


  if (loading) {
    //TODO PUT LOADING GIF HERE

    return <div><img src={loadingGif} alt="Loading" className='Loading'/></div>;

  }

  if (error) {

 

    return <div>Error: {error.message}</div>;
  }

  return (
    <div className='articles-container'>
      {news && news.length > 0 ? (
        news.map((article, index) => (
          <div key={index} className="article">
            <h2 className='articleTitle'>{article.title} </h2>
            {article.urlToImage && (
              <img src={article.urlToImage} alt={article.title} width="20%" />
            )}
            <p>{article.description}</p>
            <a href={article.url} target="_blank" rel="noopener noreferrer" className='Read_more'>Read more</a>
          </div>
        ))
      ) : (
        <div> Error no news is being fetched from APIs</div>
      )}
    </div>
  );
};

export default Entertainment;
