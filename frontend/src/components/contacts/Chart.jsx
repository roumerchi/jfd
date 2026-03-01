import React, {useMemo} from 'react';
import {BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer} from 'recharts';

const Chart = ({contacts}) => {
    const data = useMemo(() => {
        const counts = contacts.reduce((acc, c) => {
            const city = c.city || '—'; // если нет города
            acc[city] = (acc[city] || 0) + 1;
            return acc;
        }, {});

        return Object.entries(counts).map(([city, count]) => ({city, count}));
    }, [contacts]);


    return (
        <section className={"section_chart"}>
            <div className={"container_1 container_chart"}>
                <ResponsiveContainer>
                    <BarChart data={data} margin={{top: 20, right: 30, left: 0, bottom: 20}}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="city"/>
                        <YAxis allowDecimals={false}/>
                        <Tooltip/>
                        <Bar dataKey="count" fill="#8884d8"/>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </section>
    );
};

export default Chart;