import { render, screen, waitFor } from '@testing-library/react';
import {App} from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { MemoryRouter, Route } from 'react-router-dom';
import {MessageProvider} from "@/contexts/message.jsx";
import { SearchDB } from '@/components/pages/search/SearchDB';


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}/dashboard/list-databases`).reply(200, {db_list: ["toyDb"] });

test('renders search database with db_list', async() => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/']}>
            <SearchDB/>
        </MemoryRouter>
    </MessageProvider>)
    await waitFor(() => {
        const element = screen.getByText('toyDb');
        expect(element).toBeDefined();
    });
})

mock.onGet(`${import.meta.env.VITE_HOST}/dashboard/list-tables?db_name=toyDb`).reply(200, 
    [
      {
        "table_name": "taxis1",
        "last_updated": "2024-05-02 at 14:25 PDT"
      },
      {
        "table_name": "taxis2",
        "last_updated": "2024-05-02 at 14:26 PDT"
      }
    ]);

test('renders search table', async() => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/searchtable/toyDb']}>
            <SearchTable/>
        </MemoryRouter>
    </MessageProvider>)
    await waitFor(() => {
        const element = screen.getByText('taxis1');
        expect(element).toBeDefined();
    });
})