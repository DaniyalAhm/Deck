import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import NewsComponent from './components/Newscomponent'; // Your home component
import SearchBar from './components/Searchbar';
import PicksForYou from './components/PicksForYou';
import AuthenticationPage from './components/AuthenticationPage';
import './App.css';
import ByTopics from './components/By Topics';
import deck from './deck.png';
const App = () => {
  return (
    <Router>
      <div className="App">
        <SearchBar />
        {/*Make a header for the app*/}
        <header className='header'>
          <div> <img src = {deck} alt= "Deck"/></div>
        </header>
        {/* Navigation links */}
        <nav>
          <Link to="/register" className='register_tab'>Register/Login</Link>  {/* Link to the registration page */}
          <Link to="/picks-for-you" className='picks-for-you_tab'>Picks For You</Link>  {/* Link to the Picks For You page */}

        </nav>
        <ByTopics/>

        {/* Route definitions */}
        <Routes>
          <Route path="/" element={<NewsComponent />}  />
          <Route path="/register" element={<AuthenticationPage />} />
          <Route path="/picks-for-you" element={<PicksForYou />} />
          <Route path="/topics" element={<ByTopics />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
