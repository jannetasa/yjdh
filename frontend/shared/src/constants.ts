export const MAIN_CONTENT_ID = 'main_content';
export const INVALID_FIELD_CLASS = 'invalid-field';

export enum ATTACHMENT_CONTENT_TYPES {
  APPLICATION_PDF = 'application/pdf',
  IMAGE_PNG = 'image/png',
  IMAGE_JPEG = 'image/jpeg',
}

// For the following regex constants, see: frontend/shared/src/__tests__/constants.test.ts
export const ADDRESS_REGEX = /^([\d (),./A-Za-zÄÅÖäåö-]+)$/;
export const COMPANY_BANK_ACCOUNT_NUMBER = /^FI\d{16}$/;
export const PHONE_NUMBER_REGEX =
  /^((\+358[ -]*)+|(\\(\d{2,3}\\)[ -]*)|(\d{2,4})[ -]*)*?\d{3,4}?[ -]*\d{3,4}?$/;
export const POSTAL_CODE_REGEX = /^\d{5}$/;
export const NAMES_REGEX =
  /^[\w',.ÄÅÖäåö-][^\d!#$%&()*+/:;<=>?@[\\\]_{|}~¡¿÷ˆ]+$/;
export const CITY_REGEX = /^[ A-Za-zÄÅÖäåö-]+$/;
