import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { SparkPerformance } from '@/components/pages/spark/SparkPerformance.jsx';

describe('SparkPerformance', () => {
    test('renders the Grafana dashboard iframe', () => {
        render(<SparkPerformance />);

        const iframe = screen.getByRole('iframe');
        expect(iframe).toBeInTheDocument();
        expect(iframe).toHaveAttribute(
            'src',
            `${process.env.VITE_HOST}:3001/d/ddkn6773qomwwf/sql-query-duration?orgId=1&from=1714782930603&to=1714783830603&viewPanel=1`
        );
    });
});
