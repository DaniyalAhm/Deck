import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const redirectTo = (path) => {
    window.location.assign(path);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const userData = {
      email,
      password,
    };

    axios.post('/Login', userData)
      .then(response => {
        setMessage(response.data.message);
        redirectTo('/'); 
      })
      .catch(error => {
        setMessage(error.response.data.message);
      });
  };

  return (
    <div className="Login">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label>
          Password:
          <input 
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit">Login</button>
      </form>
      {message && <div>{message}</div>}
    </div>
  );
}

export default Login;
