import i18n from "i18next";

import {initReactI18next} from 'react-i18next'

const resources = {
    en: {
        translation: {
            searchMenu: "Search"
        }
    },
    es: {
        translation: {
            searchMenu: "Busqueda"
        }
    }
}

i18n.use(initReactI18next).init({
    resources,
    fallbackLng: "en",
    lng: "en",
    interpolation: {
        escapeValue: false
    }
})