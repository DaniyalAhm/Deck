// NewsComponent.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import loadingGif from './loading.gif';



axios.defaults.withCredentials = true;

const Sports = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Make a GET request to the Flask backend '/news' endpoint
    axios.get('/Sports')
      .then(response => {
        // Handle success
        setNews(response.data.articles);
        setLoading(false);
      })
      .catch(error => {
        // Handle error
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

export default Sports;
