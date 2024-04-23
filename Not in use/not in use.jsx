import React from "react";
import { useState } from "react";   
import { Link, navigate } from 'react-router-dom';
import axios from "axios";
import { useEffect } from "react";
import loadingGif from './loading.gif';

const topicsList = ['Business', 'Technology', 'Entertainment', 'Health', 'Science', 'Sports', 'Politics'];

//Adding axios for backend

const ByTopics = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [topic, setTopic] = useState(''); 
  const navigate = useNavigate();

  useEffect(() => {
    if (topic in topicsList) { 
      axios.get(`/topics/${topic}`)
        .then(response => {
          setNews(response.data.articles);
          setLoading(false);
        })
        .catch(error => {
          setError(error);
          setLoading(false);
        });
    }
  }, [topic])




  if (loading) {
    //TODO PUT LOADING GIF HERE

    return <div><img src={loadingGif} alt="Loading" className='Loading'/></div>;

  }

  if (error) {

    return <div>Error: {error.message}</div>;
  }

  const onTopicClick = (topic) => {
    setTopic(topic);
    navigate(`/topics/${topic.toLowerCase()}`);
  }


    return (
        <div>
        <ul>
        <div>
        <nav className="Topics">
   
        </nav>
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

        </ul>
    </div>
);
};
export default ByTopics;

