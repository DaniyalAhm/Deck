import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import NewsComponent from './components/Newscomponent';
import SearchBar from './components/Searchbar';
import PicksForYou from './components/PicksForYou';
import AuthenticationPage from './components/AuthenticationPage';
import './App.css';
import deck from './deck.png';
import Business from './components/Business';
import Technology from './components/Technology';
import Entertainment from './components/Entertainment';
import Health from './components/Health';
import Science from './components/Science';
import Sports from './components/Sports';
import Politics from './components/Politics';
import Set_user_topics from './components/topics';
import axios from 'axios';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get('/is_active_session')
      .then(response => {
        if(response.data.active) {
          setLoggedIn(true);
          // Fetch user information only if the session is active
          fetchUserInfo();
        } else {
          setLoggedIn(false);
          setUser(null);  // Reset user information if not logged in
        }
      })
      .catch(error => {
        console.log('Error checking session:', error);
        setLoggedIn(false);
      });
  }, []);

  const fetchUserInfo = () => {
    axios.get('/getuser_info')
      .then(response => {
        setUser(response.data);
      })
      .catch(error => {
        console.log('Error fetching user info:', error);
      });
  };

  return (
    <Router>
      <div className="App">
        <SearchBar />
        <header className='header'>
          <div><img src={deck} alt="Deck"/></div>
        </header>

        {loggedIn ? (
          <h1 className='register_tab'>Welcome back, {user?.name}</h1>
        ) : (
          <Link to="/register" className='register_tab'>Register/Login</Link>
        )}

        <nav className='NavBar'>
          <Link to="/picks-for-you" className='picks-for-you_tab'>Picks For You</Link>
          <Link to="/business" className='topic-business'>Business</Link>
          <Link to="/technology" className='topic-technology'>Technology</Link>
          <Link to="/entertainment" className='topic-entertainment'>Entertainment</Link>
          <Link to="/health" className='topic-health'>Health</Link>
          <Link to="/science" className='topic-science'>Science</Link>
          <Link to="/sports" className='topic-sports'>Sports</Link>
          <Link to="/politics" className='topic-politics'>Politics</Link>
        </nav>

        <Routes>
          <Route path="/" element={<NewsComponent />} />
          <Route path="/register" element={<AuthenticationPage />} />
          <Route path="/picks-for-you" element={<PicksForYou />} />
          <Route path="/business" element={<Business />} />
          <Route path="/technology" element={<Technology />} />
          <Route path="/entertainment" element={<Entertainment />} />
          <Route path="/health" element={<Health />} />
          <Route path="/science" element={<Science />} />
          <Route path="/sports" element={<Sports />} />
          <Route path="/politics" element={<Politics />} />
          <Route path="/topics" element={<Set_user_topics />} />
          <Route path="*" element={<h1>404 Not Found</h1>} />
          //Oauth route
        </Routes>
      </div>
    </Router>
  );
};

export default App;
