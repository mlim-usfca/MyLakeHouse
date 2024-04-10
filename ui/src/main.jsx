import React from 'react'
import ReactDOM from 'react-dom/client'
import {App} from './App.jsx'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { SnapshotPage } from './components/pages/snapshot/SnapshotPage.jsx';
import { OverViewPage } from './components/pages/overview/OverViewPage.jsx';
import { GlobalConfigPage } from './components/pages/global-configuration/GlobalConfigPage.jsx';
import { SearchDB } from './components/pages/search/SearchDB.jsx';
import { SearchTable } from './components/pages/search/SearchTable.jsx';
import { TablePage } from './components/pages/table/TablePage.jsx';

const theme = createTheme({
  components: {
    MuiGrid2: {
      defaultProps: {
        // all grids under this theme will apply
        // negative margin on the top and left sides.
        disableEqualOverflow: true,
      },
    },
  },
});


const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <OverViewPage />,
      },
      {
        path: '/config',
        element: <GlobalConfigPage />,
      },
      {
        path: '/searchDB',
        element: <SearchDB/>,
      },
      {
        path: '/searchTable/:database',
        element: <SearchTable/>,
      },
      {
        path: 'table/:database/:table',
        element: <TablePage/>,
      },
      {
        path: 'snapshot/:database/:table',
        element: <SnapshotPage/>,
      },
    ],
  },
]);



ReactDOM.createRoot(document.getElementById('root')).render(
  <ThemeProvider theme={theme}>
    <RouterProvider router={router}>
      <App />
    </RouterProvider>
  </ThemeProvider>
)
