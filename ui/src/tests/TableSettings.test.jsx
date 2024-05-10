import { render, screen } from '@testing-library/react'
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import {MemoryRouter, Route, Routes} from 'react-router-dom';
import { MessageProvider } from "@/contexts/message.jsx";
import {TableSettings} from "@/components/pages/tables/TableSettings.jsx";


const mock = new MockAdapter(axios);

mock.onGet(`${import.meta.env.VITE_HOST}:${import.meta.env.VITE_BE_API_PORT}/props/getTableProps?db_name=blade&table_name=runner`).reply(200, { data: {
        "owner": "root",
        "created-at": "2024-05-09T18:59:03.092928220Z",
        "write.parquet.compression-codec": "zstd"
    } });

test('renders content', () => {
    render(<MessageProvider>
        <MemoryRouter initialEntries={[`/blade/runner/properties`]}>
            <Routes>
                <Route path="/:db/:tbl/properties" element={<TableSettings />}/>
            </Routes>
        </MemoryRouter>
    </MessageProvider>)
    const element = screen.getByText('blade.runner')
    expect(element).toBeDefined()
})