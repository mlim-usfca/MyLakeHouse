import i18n from "i18next";

import {initReactI18next} from 'react-i18next'

const resources = {
    en: {
        translation: {
            searchMenu: "Search",
            globalSettings: "Global Settings",
            recentActivity: "Recent Activity",
            sparkPerformance: "Spark Performance"
        }
    },
    es: {
        translation: {
            searchMenu: "Busqueda",
            globalSettings: "Configuración Global",
            recentActivity: "Actividad Reciente",
            sparkPerformance: "Rendimiento de Spark"
        }
    },
    fr: {
        translation: {
            searchMenu: "Recherche",
            globalSettings: "Paramètres globaux",
            recentActivity: "Activité Récente",
            sparkPerformance: "Performance de Spark"
        }
    },
    cn: {
        translation: {
            searchMenu: "搜索",
            globalSettings: "全局设置",
            recentActivity: "近期活动",
            sparkPerformance: "Spark性能"
        },
    },
    it: {
        translation: {
            searchMenu: "Ricerca",
            globalSettings: "Impostazioni globali",
            recentActivity: "Attività Recente",
            sparkPerformance: "Prestazioni di Spark"
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