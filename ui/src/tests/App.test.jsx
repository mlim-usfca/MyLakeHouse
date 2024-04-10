import { render, screen } from '@testing-library/react'
import {App} from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { MemoryRouter, Route } from 'react-router-dom';


const mock = new MockAdapter(axios);

mock.onGet('http://localhost:8090/test').reply(200, { data: 'Mocked response' });

test('renders content', () => {
    render(<MemoryRouter initialEntries={['/']}>
        <App />
    </MemoryRouter>)
    const element = screen.getByText('Caspian')
    expect(element).toBeDefined()
})