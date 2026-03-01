import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import {useApiInterceptors} from "../hooks/useApiInterceptors";
import "../styles/contacts.css"
import Sidebar from "../components/contacts/Sidebar";
import WeatherService from "../api/WeatherService";
import NewContact from "../components/contacts/NewContact";
import ContactsService from "../api/ContactsService";
import Chart from "../components/contacts/Chart";

const Contacts = () => {
    useApiInterceptors();
    const [contacts, setContacts] = useState([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [selectedContact, setSelectedContact] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [weather, setWeather] = useState(null);
    const [sortCreated, setSortCreated] = useState('none');
    const [sortLastName, setSortLastName] = useState('none');
    const [fetchContacts, isLoading, fetchError] = useFetching(async (page = 1, ordering = '') => {
        const data = await ContactsService.getContacts(page, ordering);
        setContacts(data.results || []);
        setCurrentPage(page);
        setTotalPages(Math.ceil(data.count / 10));
    });
    const [fetchWeather, , ] = useFetching(async () => {
        return await WeatherService.getWeather(selectedContact.city);
    }, 1000, 3);

    useEffect(() => {
        void fetchContacts();
    }, []);

    useEffect(() => { // first page after changin sorting
        void fetchContacts(1, buildOrdering());
    }, [sortCreated, sortLastName]);

    useEffect(() => {
        if (!selectedContact?.city) {
            setWeather(null);
            return;
        }
        const loadWeather = async () => {
            const data = await fetchWeather();
            if (!data) {
                setWeather(null);
                return;
            }
            setWeather(data);
        };
        void loadWeather();
    }, [selectedContact?.city]);

    const buildOrdering = () => {
        const ordering = [];
        if (sortCreated === 'asc') ordering.push('created_at');
        if (sortCreated === 'desc') ordering.push('-created_at');
        if (sortLastName === 'asc') ordering.push('last_name');
        if (sortLastName === 'desc') ordering.push('-last_name');
        return ordering.join(',');
    };
    const handleSortCreatedChange = (e) => {setSortCreated(e.target.value);};
    const handleSortLastNameChange = (e) => {setSortLastName(e.target.value);};

    const handlePageChange = (page) => {
        if (page < 1 || page > totalPages || page === currentPage) return;
        void fetchContacts(page, buildOrdering());
    };

    const renderPagination = () => {
        const pages = [];
        let startPage = Math.max(currentPage - 5, 1);
        let endPage = startPage + 9;

        if (endPage > totalPages) {
            endPage = totalPages;
            startPage = Math.max(endPage - 11, 1);
        }
        for (let i = startPage; i <= endPage; i++) {
            pages.push(
                <button className={`pagination_item  ${i === currentPage && 'pagination_item_selected'}`}
                    key={i} onClick={() => handlePageChange(i)}
                    disabled={i === currentPage || isLoading}
                >
                    {i}
                </button>
            );
        }

        return pages;
    };
    return (
        <>
        <section className={"section_tb"}>
             <div className="container_1">
                <div className="tb_header">
                    <span className="text_medium_1">Contacts</span>
                    <div className="tb_sorting">
                        <label>Date</label>
                        <select value={sortCreated} onChange={handleSortCreatedChange}>
                            <option value="none">—</option>
                            <option value="asc">asc</option>
                            <option value="desc">desc</option>
                        </select>
                    </div>
                    <div className="tb_sorting">
                        <label>Surname</label>
                        <select value={sortLastName} onChange={handleSortLastNameChange}>
                            <option value="none">—</option>
                            <option value="asc">asc</option>
                            <option value="desc">desc</option>
                        </select>
                    </div>
                    <button type="button" className="add_contact" onClick={() => setIsFormOpen(true)}>
                        <div>+</div>
                        <div>Add Contact</div>
                    </button>
                    {isFormOpen && <NewContact setIsFormOpen={setIsFormOpen} setContacts={setContacts}/>}
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
                 <div className={'pagination_list'}>
                     {renderPagination()}
                 </div>
             </div>
            {fetchError && <div style={{color: 'red'}}>Failed to load contacts</div>}
        </section>
        <Sidebar contact={selectedContact} weather={weather} setContacts={setContacts}
                 setSelectedContact={setSelectedContact} setWeather={setWeather}/>
        <Chart contacts={contacts}/>
        </>
    );
};

export default Contacts;