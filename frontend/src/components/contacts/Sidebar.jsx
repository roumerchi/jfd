import React from 'react';
import {formatDateTime} from "../../utils";

const Sidebar = ({contact, weather}) => {
    return (
        <section className="area-sb">
            {contact ? (
                <div className="container_1 container_small weather_active" id="weather-box">
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
                <div className="container_1 container_small">
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