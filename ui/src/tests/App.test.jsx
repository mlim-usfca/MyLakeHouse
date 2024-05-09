import { render, screen } from '@testing-library/react'
import { App } from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { MemoryRouter, Route } from 'react-router-dom';
import { MessageProvider } from "@/contexts/message.jsx";


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}:${import.meta.env.VITE_BE_API_PORT}/test`).reply(200, { data: 'Mocked response' });

test('renders content', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={['/']}>
            <App />
        </MemoryRouter>
    </MessageProvider>)
    const element = screen.getByText('Caspian')
    expect(element).toBeDefined()
})