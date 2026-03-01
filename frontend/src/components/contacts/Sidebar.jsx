import React from 'react';
import {formatDateTime} from "../../utils";
import ContactsService from "../../api/ContactsService";
import {useFetching} from "../../hooks/useFetching";

const Sidebar = ({contact, weather, setContacts, setSelectedContact, setWeather}) => {
    const [deleteContact, , ] = useFetching(async (pk) => {
        return await ContactsService.removeContacts(pk)
    });

    const handleDelete = async () => {
        if (!contact) return;
        if (!window.confirm(`Are you sure you want to delete ${contact.first_name} ${contact.last_name}?`)) return;
        await deleteContact(contact.id);
        setContacts(prev => prev.filter(c => c.id !== contact.id));
        setSelectedContact(null);
        setWeather(null);
    };

    return (
        <section className="area-sb">
            {contact ? (
                <div className="container_1 container_small weather_active" id="weather-box">
                    <svg className={"svg_remove"} onClick={handleDelete}>
                        <use xlinkHref={"#bin"}></use>
                    </svg>
                    <div>Phone: {contact.phone}</div>
                    <div>Email: {contact.email || '—'}</div>

                    {weather && (
                        <div className="flex_3">
                            <div>{weather.temperature}°C</div>
                            <div>
                                <div>Wind: {weather.wind_speed} km/h</div>
                            </div>
                        </div>
                    )}

                    {weather && (
                        <div>Updated: {formatDateTime(weather.updated_at)}</div>
                    )}
                </div>
            ) : (
                <div className="container_1 container_small weather_active">
                    <div>Select a contact to view details</div>
                </div>
            )}
            <div className="container_1 container_medium">
                <div>IMPORT CONTACTS</div>
            </div>
        </section>
    );
};

export default Sidebar;