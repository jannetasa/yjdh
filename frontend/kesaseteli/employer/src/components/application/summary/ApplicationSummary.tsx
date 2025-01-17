import { $ApplicationSummaryField } from 'kesaseteli/employer/components/application/summary/ApplicationSummary.sc';
import EmploymentSummary from 'kesaseteli/employer/components/application/summary/EmploymentSummary';
import useApplicationApi from 'kesaseteli/employer/hooks/application/useApplicationApi';
import { useTranslation } from 'next-i18next';
import React from 'react';
import FormSection from 'shared/components/forms/section/FormSection';
import {
  $Hr,
  FormSectionProps,
} from 'shared/components/forms/section/FormSection.sc';
import FormSectionHeading from 'shared/components/forms/section/FormSectionHeading';
import PageLoadingSpinner from 'shared/components/pages/PageLoadingSpinner';

type Props = {
  header?: FormSectionProps['header'];
  tooltip?: FormSectionProps['tooltip'];
};
const ApplicationSummary: React.FC<Props> = ({ header, tooltip }) => {
  const { t } = useTranslation();
  const { applicationQuery } = useApplicationApi();
  if (applicationQuery.isSuccess) {
    const {
      company,
      contact_person_name,
      contact_person_email,
      contact_person_phone_number,
      street_address,
      is_separate_invoicer,
      invoicer_email,
      invoicer_name,
      invoicer_phone_number,
      summer_vouchers,
    } = applicationQuery.data;

    return (
      <>
        <FormSection header={header} tooltip={tooltip} columns={1}>
          <FormSectionHeading
            header={t('common:application.step3.employerTitle')}
            size="m"
          />
          <FormSectionHeading
            header={`${company.name}, ${company.business_id}`}
            size="s"
            as="div"
            data-testid="company-heading"
          />
          <$ApplicationSummaryField data-testid="company-data">
            {company.industry}, {company.company_form}, {company.postcode}{' '}
            {company.city}
          </$ApplicationSummaryField>
          <$ApplicationSummaryField data-testid="contact-person">
            {contact_person_name}, {contact_person_email},
            {contact_person_phone_number}
          </$ApplicationSummaryField>
          <$ApplicationSummaryField data-testid="street-address">
            {street_address}
          </$ApplicationSummaryField>
          {is_separate_invoicer && (
            <$ApplicationSummaryField data-testid="invoicer">
              {t('common:application.form.inputs.is_separate_invoicer')}:{' '}
              {invoicer_name}, {invoicer_email}, {invoicer_phone_number}
            </$ApplicationSummaryField>
          )}
        </FormSection>
        <FormSection
          header={t('common:application.step3.employmentTitle')}
          size="m"
          columns={1}
          withoutDivider
        >
          {summer_vouchers.map((employment, index) => (
            <React.Fragment key={employment.id}>
              <EmploymentSummary index={index} />
              <$Hr />
            </React.Fragment>
          ))}
        </FormSection>
      </>
    );
  }
  return <PageLoadingSpinner />;
};
export default ApplicationSummary;
