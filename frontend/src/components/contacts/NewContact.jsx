import React, {useState} from 'react';
import {useFetching} from "../../hooks/useFetching";
import ContactsService from "../../api/ContactsService";

const NewContact = ({ setIsFormOpen, setContacts }) => {
    const [errors, setErrors] = useState({});
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        city: '',
        email: '',
        phone: '',
        status_code: 'default',
    });
    const phoneRegex = /^(?:\+48|0048)?[1-9]\d{8}$/;
    const [createContact, isCreating, createError] = useFetching(
        async (data) => await ContactsService.createContact(data)
    );

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
        setErrors(prev => ({ ...prev, [e.target.name]: null }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});

        if (!phoneRegex.test(formData.phone)) {
            setErrors({ phone: 'Invalid Polish phone number'});
            return;
        }

        try {
            const newContact = await createContact(formData);

            if (newContact) {
                setContacts(prev => [newContact, ...prev]);
                setFormData({
                    first_name: '',
                    last_name: '',
                    city: '',
                    email: '',
                    phone: '',
                    status_code: 'default',
                });
                setIsFormOpen(false);
            }
        } catch (err) {
            if (createError) {
                setErrors(createError.response?.data || {});
            }
        }
    };


    return (
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
                               placeholder="john@example.com" maxLength={254} required id="id_email"/>
                    </div>
                    <div className="flex_1">
                        <label>Phone</label>
                        <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required
                               placeholder="+48 000 000 000" aria-invalid={errors.phone ? "true" : "false"}
                               id="id_phone"
                        />

                    </div>
                </div>
                <div className="flex_3">
                    <div className="button_1" onClick={() => setIsFormOpen(false)}>cancel</div>
                    {createError && (
                        <div className="error-message">Failed to add contact</div>
                    )}
                    {errors.phone && (
                         <div className="error-message">{errors.phone}</div>
                     )}
                    <button type="submit" name="contact_submit" className="button__submit" disabled={isCreating}>
                        {isCreating ? 'Adding...' : 'submit'}
                    </button>
                </div>
            </div>
        </form>
    );
};

export default NewContact;