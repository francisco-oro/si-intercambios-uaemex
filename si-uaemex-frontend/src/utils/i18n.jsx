import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import usersModule from './translation/admin/usersModule'; // Traducción de "admin" -> usuarios
import generalTexts from './translation/GeneralTexts'; // Traducción general -> common

const resources = {
  en: {
    admin: usersModule.en, // Accede a la traducción en inglés para admin
    common: generalTexts.en, // Accede a la traducción en inglés para general
  },
  es: {
    admin: usersModule.es, // Accede a la traducción en español para admin
    common: generalTexts.es, // Accede a la traducción en español para general
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "en", // Idioma predeterminado
    fallbackLng: "en", // Idioma de respaldo en caso de que no se encuentre la traducción
    ns: ['common', 'admin'], // Define los namespaces disponibles
    defaultNS: 'common', // Namespace predeterminado
    interpolation: {
      escapeValue: false // React ya protege contra XSS
    }
  });

export default i18n;
