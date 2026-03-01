import React, {useState} from 'react';
import "../styles/auth.css"
import {useAuth} from "../context";

const Auth = () => {
    const { login } = useAuth();
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [errors, setErrors] = useState(null);

    const handleChange = (e) => {
        setFormData(prev => ({...prev, [e.target.name]: e.target.value}));
        setErrors(null);
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        const errorMessage = await login(formData.username, formData.password);
        if (errorMessage) {
            setErrors(errorMessage)
        }
    };

    return (
        <form className="area_form" onSubmit={handleSubmit}>
            <div className="form_1">
                <span>Authorization</span>
                <div className="flex_1">
                    <label htmlFor="username">Username</label>
                    <input type="text" name="username" id="username" value={formData.username} onChange={handleChange} required/>
                </div>
                <div className="flex_1">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password" value={formData.password} onChange={handleChange} required/>
                </div>
                <div className="flex_3" style={{justifyContent: "flex-end"}}>
                    {errors && <div className="error-message" style={{ color: 'red' }}>{errors}</div>}
                    <button type="submit" className="button__submit">
                        {'Log In'}
                    </button>
                </div>
            </div>
        </form>
    );
};

export default Auth;