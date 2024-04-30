import i18n from "i18next";

import {initReactI18next} from 'react-i18next'

const resources = {
    en: {
        translation: {
            searchMenu: "Search",
            globalSettings: "Global Settings",
            recentActivity: "Recent Activity"
        }
    },
    es: {
        translation: {
            searchMenu: "Busqueda",
            globalSettings: "Configuración Global",
            recentActivity: "Actividad Reciente"
        }
    },
    fr: {
        translation: {
            searchMenu: "Recherche",
            globalSettings: "Paramètres globaux",
            recentActivity: "Activité Récente"
        }
    },
    cn: {
        translation: {
            searchMenu: "搜索",
            globalSettings: "全局设置",
            recentActivity: "近期活动"
        },
    },
    it: {
        translation: {
            searchMenu: "Ricerca",
            globalSettings: "Impostazioni globali",
            recentActivity: "Attività Recente"
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