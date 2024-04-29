// SearchBar.jsx
import React, { useState } from 'react';
import axios from 'axios'; // Make sure axios is imported for making HTTP requests

axios.defaults.withCredentials = true;

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const searchUrl = `http://localhost:5000/search?query=${encodeURIComponent(searchTerm)}`;

    axios.get(searchUrl)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error('Search failed:', error);
      });
  };

  return (
    
    <div className='SearchBar'>
    <form onSubmit={handleSubmit} className="search-form">
      <input
        type="text"
        placeholder="Search news..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-input"
      />
      <button type="submit" className="search-button">Search</button>
    </form>
    </div>
  );
};

export default SearchBar;
