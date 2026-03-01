import React, {useEffect} from 'react';
import AuthService from "../api/AuthService";
import {Link} from "react-router-dom";
import {useAuth} from "../context";

const Header = () => {
    const { isAuth } = useAuth();

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            AuthService.verifyAccessTokenApi(token)
                .then(() => {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                })
                .catch(() => {
                    localStorage.removeItem('accessToken');
                });
        }
    }, []);

    return (
        <div className="header">
            <div>Sitename</div>
            <nav className="flex space-x-1">
                <Link to={"/contacts/"} data-discover="true">
                    <button className="selected">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                             stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                             className="lucide lucide-users w-4 h-4 mr-2" aria-hidden="true">
                            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                            <path d="M16 3.128a4 4 0 0 1 0 7.744"></path>
                            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                        </svg>
                        <span>Contacts</span>
                    </button>
                </Link>
            </nav>
            <Link to={"/auth/"} className="button_1 flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                     className="lucide lucide-circle-user w-5 h-5 text-primary" aria-hidden="true">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="10" r="3"></circle>
                    <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"></path>
                </svg>
                <span>{isAuth ? "Logged" : 'Log In'}</span>
            </Link>
        </div>
    );
};

export default Header;