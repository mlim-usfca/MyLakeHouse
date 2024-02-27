import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { OverViewPage } from './pages/overview/OverViewPage.jsx';
import { GlobalConfigPage } from './pages/global-configuration/GlobalConfigPage.jsx';

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
      }
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
