import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import ContactsService from "../api/ContactsService";
import {useApiInterceptors} from "../hooks/useApiInterceptors";
import "../styles/contacts.css"
import Sidebar from "../components/contacts/Sidebar";
import WeatherService from "../api/WeatherService";

const Contacts = () => {
    useApiInterceptors();
    const [contacts, setContacts] = useState([]);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        city: '',
        email: '',
        phone: '',
    });
    const [errors, setErrors] = useState({});
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [selectedContact, setSelectedContact] = useState(null);
    const [weather, setWeather] = useState(null);
    const [isWeatherLoading, setIsWeatherLoading] = useState(false);
    const [fetchContacts, isLoading, fetchError] = useFetching(async () => {
        const data = await ContactsService.getContacts();
        setContacts(data.results || data);
    });
    const [createContact, isCreating, createError] = useFetching(async () => {
        const newContact = await ContactsService.createContact(formData);
        setContacts(prev => [newContact, ...prev]);
        setFormData({ first_name: '', last_name: '', city: '', email: '', phone: '' });
    });

    useEffect(() => {
        void fetchContacts();
    }, []);

    useEffect(() => {
        const loadWeather = async () => {
            if (!selectedContact?.city) {
                setWeather(null);
                return;
            }
            try {
                setIsWeatherLoading(true);
                const data = await WeatherService.getWeather(selectedContact.city);
                setWeather(data);
            } catch (e) {
                console.error('Weather load failed', e);
                setWeather(null);
            } finally {
                setIsWeatherLoading(false);
            }
        };
        void loadWeather();
    }, [selectedContact]);

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        try {
            await createContact();
        } catch (err) {
            if (err.response?.data) setErrors(err.response.data);
            console.error(err);
        }
    };

    return (
        <>
        <section className={"section_tb"}>
             <div className="container_1">
                <div className="tb_header">
                    <span className="text_medium_1">Contacts</span>
                    <input type="search" placeholder="search by name or city" />
                    <div className="tb_sorting">
                        <div>Sort</div>
                        <select>
                            <option value="date">Date</option>
                            <option value="surname">Surname</option>
                        </select>
                    </div>
                    <button type="button" className="add_contact" onClick={() => setIsFormOpen(true)}>
                        <div>+</div>
                        <div>Add Contact</div>
                    </button>
                    {isFormOpen && (
                    <form className="area_form_2" onSubmit={handleSubmit} onClick={e => e.stopPropagation()}>
                        <div className="form_2">
                            <div className="form_close" onClick={() => setIsFormOpen(false)}>✖</div>
                            <span className="form_header text_medium_1">Add New Contact</span>
                            <div className="flex_2">
                                <div className="flex_1">
                                    <label>Name</label>
                                    <input type="text" name="first_name" value={formData.first_name} onChange={handleChange}
                                           maxLength={100} required id="id_first_name"/>
                                </div>
                                <div className="flex_1">
                                    <label>Surname</label>
                                    <input type="text" name="last_name" value={formData.last_name} onChange={handleChange}
                                           maxLength={100} required id="id_last_name"/>
                                </div>
                            </div>
                            <div className="flex_1">
                                <label>City</label>
                                <input type="text" name="city" value={formData.city} onChange={handleChange} maxLength={100}
                                    id="id_city"/>
                            </div>
                            <div className="flex_2">
                                <div className="flex_1">
                                    <label>Email</label>
                                    <input type="email" name="email" value={formData.email} onChange={handleChange}
                                           placeholder="john@example.com" maxLength={254} required  id="id_email"/>
                                </div>
                                <div className="flex_1">
                                    <label>Phone</label>
                                    <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required
                                           placeholder="+48 000 000 000"  aria-invalid={errors.phone ? "true" : "false"}
                                           id="id_phone"
                                    />
                                    {errors.phone && (
                                        <div className="error-message" style={{ color: 'red' }}>
                                            {errors.phone}
                                        </div>
                                    )}
                                </div>
                            </div>
                            <div className="flex_3">
                                <div className="button_1" onClick={() => setIsFormOpen(false)}>cancel</div>
                                <button type="submit" name="contact_submit" className="button__submit" disabled={isCreating}>
                                    {isCreating ? 'Adding...' : 'submit'}
                                </button>
                            </div>
                        </div>
                    </form>
                    )}
                </div>
                 <div className="tb_row row_main">
                     <div>NAME</div>
                     <div>SURNAME</div>
                     <div>CITY</div>
                     <div>STATUS</div>
                     <div>DATE ADDED</div>
                 </div>
                 {isLoading ? (
                     <div>Loading contacts...</div>
                 ) : contacts.length === 0 ? (
                     <div className="tb_row">
                         <div>No contacts yet</div>
                     </div>
                 ) : (
                     contacts.map((contact, index) => (
                         <div key={index} className={`tb_row ${selectedContact === contact ? 'active' : ''}`}
                             onClick={() => setSelectedContact(contact)}
                         >
                             <div>{contact.first_name}</div>
                             <div>{contact.last_name}</div>
                             <div>{contact.city || '—'}</div>
                             <div className={`status status_${contact.status?.code || 'default'}`}>
                                 {contact.status?.title || 'Default'}
                             </div>
                             <div>{new Date(contact.created_at).toLocaleDateString()}</div>
                         </div>
                     ))
                 )}
             </div>
            {fetchError && <div style={{color: 'red'}}>Failed to load contacts</div>}
            {createError && <div style={{color: 'red'}}>Failed to add contact</div>}
        </section>
        <Sidebar contact={selectedContact} weather={weather}/>
        </>
    );
};

export default Contacts;