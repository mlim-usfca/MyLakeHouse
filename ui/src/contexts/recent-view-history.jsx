import {createContext, useContext, useReducer} from 'react';

const RecentViewContext = createContext(null);

const RecentViewDispatchContext = createContext(null);

const initialRecentView = {
    tables: [],
};

export const RecentViewProvider = ({children}) => {
    const [recentView, dispatch] = useReducer(recentViewReducer, initialRecentView);

    return (
        <RecentViewContext.Provider value={recentView}>
            <RecentViewDispatchContext.Provider value={dispatch}>
                {children}
            </RecentViewDispatchContext.Provider>
        </RecentViewContext.Provider>
    );
};

export const recentViewReducer = (recentView, action) => {
    switch (action.type) {
        case 'add': {
            const curr = [...recentView.tables]
            if (!curr.find( rc => rc.table === action.value.table)) {
                curr.push(action.value)
            }
            return {
                ...recentView,
                tables: curr
            };
        }
        case 'remove': {
            const curr = [...recentView.tables]
            console.log(action)
            const index = curr.findIndex(rc => rc.table === action.value.table)
            if (index >= 0) {
                curr.splice(index, 1);
            }
            return {
                ...recentView,
                tables: curr
            };
        }
        default: {
            throw new Error(`No matching action ${action.type} found`);
        }
    }
};

export const useRecentView = () => useContext(RecentViewContext);

export const useRecentViewDispatch = () => useContext(RecentViewDispatchContext);