export const IS_CLIENT = typeof window !== 'undefined';

export enum ROUTES {
  HOME = '/',
  APPLICATION_FORM = '/application',
}

export enum SUPPORTED_LANGUAGES {
  FI = 'fi',
  SV = 'sv',
  EN = 'en',
}

export const DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES.FI;

export const COMMON_I18N_NAMESPACES = ['common'] as const;

export const PRIVACY_POLICY_LINKS = {
  fi: 'https://www.hel.fi/1',
  en: 'https://www.hel.fi/2',
  sv: 'https://www.hel.fi/3',
} as const;
