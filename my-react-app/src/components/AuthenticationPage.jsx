import React from 'react';
import Login from './Login';  // Ensure this path is correct
import Registration from './Registration';  // Ensure this path is correct

const AuthenticationPage = () => {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-around', width: '100%' }}>
            <Login />
            <Registration />
            {/* Making a vertical bar*/}
            <div className='bar'></div>
        </div>
    );
}

export default AuthenticationPage;
