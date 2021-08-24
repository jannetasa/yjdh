import CompanyInfoHeader, {
  CompanyProp,
} from 'kesaseteli/employer/components/companyInfo/CompanyInfoHeader';
import useCompanyQuery from 'kesaseteli/employer/hooks/useCompanyQuery';
import { useTranslation } from 'next-i18next';
import React from 'react';
import LoadingSkeleton from 'react-loading-skeleton';
import isServerSide from 'shared/server/is-server-side';

import { $CompanyInfoCell, $CompanyInfoGrid } from './CompanyInfoGrid.sc';

type Props = {
  applicationId: string;
};

const CompanyInfoGrid: React.FC<Props> = ({ applicationId }: Props) => {
  const { t } = useTranslation();
  const { data: company, error, isLoading } = useCompanyQuery(applicationId);
  const CompanyFieldCell: React.FC<CompanyProp> = ({ field }: CompanyProp) => (
    <$CompanyInfoCell aria-labelledby={field} role="gridcell">
      {isLoading && !isServerSide() && <LoadingSkeleton width="90%" />}
      {(!isLoading && !error && company?.[field]) || ''}
    </$CompanyInfoCell>
  );

  return (
    <$CompanyInfoGrid
      role="grid"
      aria-label={t(`common:application.step1.companyInfoGrid.title`)}
    >
      <CompanyInfoHeader field="name" />
      <CompanyInfoHeader field="business_id" />
      <CompanyInfoHeader field="industry" />
      <CompanyInfoHeader field="company_form" />
      <CompanyInfoHeader field="postcode" />
      <CompanyInfoHeader field="city" />
      <CompanyFieldCell field="name" />
      <CompanyFieldCell field="business_id" />
      <CompanyFieldCell field="industry" />
      <CompanyFieldCell field="company_form" />
      <CompanyFieldCell field="postcode" />
      <CompanyFieldCell field="city" />
    </$CompanyInfoGrid>
  );
};

export default CompanyInfoGrid;