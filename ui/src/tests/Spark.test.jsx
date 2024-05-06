import React from 'react';
import { MemoryRouter, Route } from 'react-router-dom';
import { SparkPerformance } from '@/components/pages/spark/SparkPerformance.jsx';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import {MessageProvider} from "@/contexts/message.jsx";


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}/test`).reply(200, { data: 'Mocked response' });

test('renders the Grafana dashboard', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/spark-performance']}>
            <SparkPerformance />
        </MemoryRouter>
    </MessageProvider>)

    const iframe = screen.getByRole('iframe');
    expect(iframe).toBeInTheDocument();
    expect(iframe).toHaveAttribute(
        'src',
        `${process.env.VITE_HOST}:3001/d/ddkn6773qomwwf/sql-query-duration?orgId=1&from=1714782930603&to=1714783830603&viewPanel=1`
    );
});