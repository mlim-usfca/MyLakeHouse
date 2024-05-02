import { render, screen } from '@testing-library/react'
import {App} from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { MemoryRouter, Route } from 'react-router-dom';
import {MessageProvider} from "@/contexts/message.jsx";


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


mock.onGet(`${import.meta.env.VITE_HOST}/list-database`).reply(200, { data: 'Mocked response' });

test('renders content', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/']}>
            <App />
        </MemoryRouter>
    </MessageProvider>)
    const element = screen.getByText('SEARCH FOR DATABASE')
    expect(element).toBeDefined()
})