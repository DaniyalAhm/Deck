import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import NewsComponent from './components/Newscomponent'; // Your home component
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


// Mapping of topics to components for dynamic route generation
const topicComponents = {
  business: Business,
  technology: Technology,
  entertainment: Entertainment,
  health: Health,
  science: Science,
  sports: Sports,
  politics: Politics
};




const App = () => {
  const topicsList = ['Business', 'Technology', 'Entertainment', 'Health', 'Science', 'Sports', 'Politics'];
  return (
    <Router>
      <div className="App">
        <SearchBar />
        {/*Make a header for the app*/}
        <header className='header'>
          <div> <img src = {deck} alt= "Deck"/></div>
        </header>

        <Link to = "/register" className='register_tab'>Register/Login</Link>

        {/* Navigation links */}
        <nav className='NavBar'>

        <Link to="/picks-for-you" className='picks-for-you_tab'>Picks For You</Link>  {/* Link to the Picks For You page */}
        <Link to="/business" className='topic-business'>Business</Link>
        <Link to="/technology" className='topic-technology'>Technology</Link>
        <Link to="/entertainment" className='topic-entertainment'>Entertainment</Link>
        <Link to="/health" className='topic-health'>Health</Link>
        <Link to="/science" className='topic-science'>Science</Link>
        <Link to="/sports" className='topic-sports'>Sports</Link>
        <Link to="/politics" className='topic-politics'>Politics</Link>
        
        </nav>
        

        {/* Route definitions */}
        <Routes>
          <Route path="/" element={<NewsComponent />}  />
          <Route path="/register" element={<AuthenticationPage />} />
          <Route path="/picks-for-you" element={<PicksForYou />} />
          {topicsList.map((topic, index) => (
            <Route key={index} path={`/${topic.toLowerCase()}`} element={React.createElement(topicComponents[topic.toLowerCase()])} />
          ))}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
