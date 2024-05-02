import { render, screen } from '@testing-library/react'
import {App} from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { MemoryRouter, Route } from 'react-router-dom';
import {MessageProvider} from "@/contexts/message.jsx";
import { SearchDB } from '@/components/pages/search/SearchDB';


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}/test`).reply(200, { data: 'Mocked response' });

test('renders content', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/']}>
            <App />
        </MemoryRouter>
    </MessageProvider>)
    const element = screen.getByText('Caspian')
    expect(element).toBeDefined()
})


mock.onGet(`${import.meta.env.VITE_HOST}/dashboard/list-databases`).reply(200, { data: 'Mocked response' });

test('renders search database with no db_list', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/']}>
            <SearchDB/>
        </MemoryRouter>
    </MessageProvider>)
    const element = screen.getByText('Search For Database')
    expect(element).toBeDefined()
})