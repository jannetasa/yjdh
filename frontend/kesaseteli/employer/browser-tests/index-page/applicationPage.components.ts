import {
  getErrorMessage,
  screenContext,
  setDataToPrintOnFailure,
  withinContext,
} from '@frontend/shared/browser-tests/utils/testcafe.utils';
import Company from '@frontend/shared/src/types/company';
import Invoicer from '@frontend/shared/src/types/invoicer';
import TestController from 'testcafe';

export const getApplicationPageComponents = (t: TestController) => {
  const screen = screenContext(t);
  const within = withinContext(t);
  const companyTable = async (company: Company) => {
    const selectors = {
      companyTable() {
        return screen.findByRole('grid', { name: /yrityksen tiedot/i });
      },
    };
    const expectations = {
      async isPresent() {
        await t
          .expect(selectors.companyTable().exists)
          .ok(await getErrorMessage(t));
      },
      async isCompanyDataPresent() {
        await t
          .expect(screen.findByLabelText('Yritys').textContent)
          .eql(company.name, await getErrorMessage(t));
        await t
          .expect(screen.findByLabelText(/y-tunnus/i).textContent)
          .eql(company.business_id, await getErrorMessage(t));
        if (company.industry?.length > 0) {
          await t
            .expect(screen.findByLabelText(/toimiala/i).textContent)
            .eql(company.industry, await getErrorMessage(t));
        }
        if (company.street_address?.length > 0) {
          await t
            .expect(screen.findByLabelText(/yritysmuoto/i).textContent)
            .eql(company.street_address, await getErrorMessage(t));
        }
        if (company.postcode?.length > 0) {
          await t
            .expect(screen.findByLabelText(/postiosoite/i).textContent)
            .eql(company.postcode, await getErrorMessage(t));
        }
      },
    };
    const actions = {};
    await expectations.isPresent();
    return {
      selectors,
      expectations,
      actions,
    };
  };
  const invoicerForm = async () => {
    const formSelector = screen.getByRole('form', {
      name: /työnantajan tiedot/i,
    });
    const withinForm = (): ReturnType<typeof within> => within(formSelector);

    const selectors = {
      invoicerForm() {
        return screen.findByRole('form', {
          name: /työnantajan tiedot/i,
        });
      },
      invoicerNameInput() {
        return withinForm().findByRole('textbox', {
          name: /yhteyshenkilön nimi/i,
        });
      },
      invoicerEmailInput() {
        return withinForm().findByRole('textbox', {
          name: /yhteyshenkilön sähköposti/i,
        });
      },
      invoicerPhoneInput() {
        return withinForm().findByRole('textbox', {
          name: /yhteyshenkilön puhelinnumero/i,
        });
      },
      saveAndContinueButton() {
        return withinForm().findByRole('button', {
          name: /tallenna ja jatka/i,
        });
      },
    };
    const expectations = {
      async isPresent() {
        await t
          .expect(selectors.invoicerForm().exists)
          .ok(await getErrorMessage(t), { timeout: 10000 });
      },
      async isFulFilledWith({
        invoicer_name,
        invoicer_email,
        invoicer_phone_number,
      }: Invoicer) {
        await t
          .expect(selectors.invoicerForm().exists)
          .ok(await getErrorMessage(t));
        await t
          .expect(selectors.invoicerNameInput().value)
          .eql(invoicer_name, await getErrorMessage(t));
        await t
          .expect(selectors.invoicerEmailInput().value)
          .eql(invoicer_email, await getErrorMessage(t));
        await t
          .expect(selectors.invoicerPhoneInput().value)
          .eql(invoicer_phone_number, await getErrorMessage(t));
      },
    };

    const actions = {
      async fillName(name: string) {
        setDataToPrintOnFailure(t, 'invoicer_name', name);

        await t.typeText(selectors.invoicerNameInput(), name, {
          replace: true,
        });
      },
      async fillEmail(email: string) {
        setDataToPrintOnFailure(t, 'invoicer_email', email);
        await t.typeText(selectors.invoicerEmailInput(), email, {
          replace: true,
        });
      },
      async fillPhone(phone: string) {
        setDataToPrintOnFailure(t, 'invoicer_phone_number', phone);
        await t.typeText(selectors.invoicerPhoneInput(), phone, {
          replace: true,
        });
      },
      async clickSaveAndContinueButton() {
        await t.click(selectors.saveAndContinueButton());
      },
    };

    await expectations.isPresent();
    return {
      selectors,
      expectations,
      actions,
    };
  };
  return {
    companyTable,
    invoicerForm,
  };
};
