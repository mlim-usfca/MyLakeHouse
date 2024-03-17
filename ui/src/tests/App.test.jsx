import { render, screen } from '@testing-library/react'
import {App} from '@/App.jsx'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);

mock.onGet('http://localhost:8090/test').reply(200, { data: 'Mocked response' });

test('renders content', () => {
    render(<App />)
    const element = screen.getByText('Left Column Test')
    expect(element).toBeDefined()
})