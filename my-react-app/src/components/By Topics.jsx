import React from "react";
import { useState } from "react";   
import { Link } from 'react-router-dom';
import axios from "axios";

const topicsList = ['Business', 'Technology', 'Entertainment', 'Health', 'Science', 'Sports', 'Politics'];

//Adding axios for backend


const ByTopics = () => {

    return (
        <div>
        <ul>
        <nav className="Topics">
        {topicsList.map((topic, index) => (
          <Link key={index} to={`/topics/${topic.toLowerCase()}`} className={`topic-${topic.toLowerCase()}`}>
            {topic}
          </Link>
        ))}
        </nav>
        </ul>
    </div>
);
};

export default ByTopics;