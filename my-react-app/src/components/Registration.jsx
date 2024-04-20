import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Registration = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [topics, setTopics] = useState(['stuff']); // To store the list of topics
  const [selectedTopics, setSelectedTopics] = useState([]); // To store the user's selected topics
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/topics') // Fetch the topics from the backend
      .then(response => {
        setTopics(response.data); // Assuming the backend sends an array of topics
      })
      .catch(error => {
        console.log('Error fetching topics:', error);
      });
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    const userData = {
      name, 
      email, 
      password, 
      topics: selectedTopics
    };

    axios.post('/register', userData)
      .then(response => {
        setMessage(response.data.message);
        redirectTo('/'); // Redirect on successful registration
      })
      .catch(error => {
        setMessage(error.response.data.message);
      });

      redirectTo('/'); // Redirect on successful registration
  };

  const handleTopicChange = (topic) => {
    setSelectedTopics(prevSelectedTopics =>
      prevSelectedTopics.includes(topic)
        ? prevSelectedTopics.filter(t => t !== topic) // Remove topic if it's already selected
        : [...prevSelectedTopics, topic] // Add topic if it's not already selected
    );
  };

  const redirectTo = (path) => {
    window.location.assign(path);
  }

  return (
    <div className="registration">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />  
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        <fieldset>
          <legend>What topics are you interested in?</legend>
          {topics.map(topic => (
            <label key={topic}>
              <input
              
                type="checkbox"
                value={topic}
                checked={selectedTopics.includes(topic)}
                onChange={() => handleTopicChange(topic)}
              />
              {topic}
            </label>
          ))}
        </fieldset>
        
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Registration;
