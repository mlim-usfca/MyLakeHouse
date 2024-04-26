import {createContext, useContext, useReducer} from 'react';

const MessageContext = createContext(null);

const MessageDispatchContext = createContext(null);

const initialMessage = {
    isOpen: true,
        type: "test",
    msg: "hello",
    delay: 3000
};

export const MessageProvider = ({children}) => {
    const [message, dispatch] = useReducer(messageReducer, initialMessage);

    return (
        <MessageContext.Provider value={message}>
            <MessageDispatchContext.Provider value={dispatch}>
                {children}
            </MessageDispatchContext.Provider>
        </MessageContext.Provider>
    );
};

export const messageReducer = (recentView, action) => {
    switch (action.type) {
        case 'success': {
            return {
                isOpen: true,
                type: "success",
                ...action.value
            };
        }
        case 'error': {
            return {
                isOpen: true,
                type: "error",
                ...action.value
            };
        }
        case 'reset': {
            return {
                isOpen: false,
                type: "",
                ...action.value
            };
        }
        default: {
            throw new Error(`No matching action ${action.type} found`);
        }
    }
};

export const useToastMessage = () => useContext(MessageContext);

export const useToastMessageDispatch = () => useContext(MessageDispatchContext);