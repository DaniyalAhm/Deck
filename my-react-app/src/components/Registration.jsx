import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
axios.defaults.withCredentials = true;

const Registration = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true); // Set loading to true to start the loading state
    try {
      // Perform the registration
      const response = await axios.post('/register', {
        name,
        email,
        password
      });
      setMessage(response.data.message || 'Registration successful!');
      navigate('/topics'); // Navigate after successful registration
    } catch (error) {
      // Handle any errors
      setMessage(error.response?.data?.error || 'Registration failed!');
    } finally {
      setIsLoading(false); // Set loading to false regardless of the outcome
    }
  };


  const handleOAuthClick = () => {
    window.location.href = 'http://127.0.0.1:5000/oauth_register'; // Direct URL to initiate OAuth
  };
  

  return (
    <div className="registration">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <label className='Name-Register'>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <label className='Email-Register'>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className='Password-Register'>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit" disabled={isLoading}>Register</button>
      </form>

      <h1>Or sign up with Google</h1>
      <button onClick={handleOAuthClick} disabled={isLoading}>Sign in with Google</button>

      {message && <p>{message}</p>}
    </div>
  );
};

export default Registration;
