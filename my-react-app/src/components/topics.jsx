import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
//TODO: Implement the set_user_topics component
//TODO: Handle the user's selected topics
//TODO: Beneficial for Oauth Code Flow
axios.defaults.withCredentials = true;


const Set_user_topics = () => {

const [topics, setTopics] = useState(['Stuff']); // To store the list of topics
const [selectedTopics, setSelectedTopics] = useState([]); // To store the user's selected topics
const [user_id, setUser_id] = useState(''); // To store the user's selected topics
const navigate = useNavigate();

useEffect(() => {
    axios.get('/topics') // Fetch the topics from the backend
      .then(response => {
        setTopics(response.data); // Assuming the backend sends an array of topics
      })
      .catch(error => {
        console.log('Error fetching topics:', error);
      });
  }, []);

useEffect(() => {
    axios.get('/getuser_info')
        .then(response => {
            setUser_id(response.data.topics);
        })
        .catch(error => {
            console.log('Error fetching user topics:', error);
        });   
});


const handleTopicChange = (topic) => {
    setSelectedTopics(prevTopics =>
        prevTopics.includes(topic)
            ? prevTopics.filter(t => t !== topic)
            : [...prevTopics, topic]
    );
};

const handleSubmit = async (event) => {
    event.preventDefault();
        const response  = await axios.post('/update_user_topics', {topics: selectedTopics})
    
    navigate('/picks-for-you');
    }

 return (
<form onSubmit={handleSubmit} className="topics-form">
<fieldset>
<legend>What topics are you interested in? </legend>
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
<button type="submit" className="submit-button">Submit</button>
</fieldset>
</form>
);
}

export default Set_user_topics;