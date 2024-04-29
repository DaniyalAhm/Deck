import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CheckSession = () => {
    const navigate = useNavigate();
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        const intervalId = setInterval(() => {
            axios.get('/check-session')
                .then(response => {
                    if (response.data.status === 'ready') {
                        clearInterval(intervalId);
                        navigate('/topics');
                    }
                })
                .catch(error => {
                    console.error('Error checking session:', error);
                });
        }, 1000);  // Poll every 1000 milliseconds

        return () => clearInterval(intervalId);
    }, [navigate]);

    return (
        <div>
            {checking ? <p>Checking your session, please wait...</p> : null}
        </div>
    );
};

export default CheckSession;
