import React from 'react';
import { render, screen } from '@testing-library/react'
import { SparkPerformance } from '@/components/pages/spark/SparkPerformance.jsx';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}/test`).reply(200, { data: 'Mocked response' });

test('renders the Grafana dashboard', () => {
    render(
            <SparkPerformance />);

    const iframe = screen.getByRole('iframe');
    expect(iframe).toBeInTheDocument();
    expect(iframe).toHaveAttribute(
        'src',
        `${process.env.VITE_HOST}:3001/d/ddkn6773qomwwf/sql-query-duration?orgId=1&from=1714782930603&to=1714783830603&viewPanel=1`
    );
});