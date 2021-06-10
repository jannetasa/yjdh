import ApplicationFormStep1 from 'benefit/applicant/components/applications/forms/application/step1/ApplicationFormStep1';
import ApplicationFormStep2 from 'benefit/applicant/components/applications/forms/application/step2/ApplicationFormStep2';
import ApplicationFormStep3 from 'benefit/applicant/components/applications/forms/application/step3/ApplicationFormStep3';
import ApplicationFormStep4 from 'benefit/applicant/components/applications/forms/application/step4/ApplicationFormStep4';
import ApplicationFormStep5 from 'benefit/applicant/components/applications/forms/application/step5/ApplicationFormStep5';
import ApplicationFormStep6 from 'benefit/applicant/components/applications/forms/application/step6/ApplicationFormStep6';
import StepperActions from 'benefit/applicant/components/applications/forms/application/stepperActions/StepperActions';
import {
  StyledHeaderItem,
  StyledPageHeader,
  StyledPageHeading,
} from 'benefit/applicant/components/applications/styled';
import React from 'react';
import Container from 'shared/components/container/Container';
import Stepper from 'shared/components/stepper/Stepper';

import { useComponent } from './extended';

const PageContent: React.FC = () => {
  const {
    handleSubmit,
    handleBack,
    t,
    steps,
    currentStep,
    hasBack,
    hasNext,
  } = useComponent();

  const actions = (
    <StepperActions
      hasBack={hasBack}
      hasNext={hasNext}
      handleSubmit={handleSubmit}
      handleBack={handleBack}
    />
  );

  return (
    <Container>
      <StyledPageHeader>
        <StyledHeaderItem>
          <StyledPageHeading>
            {t('common:applications.pageHeaders.new')}
          </StyledPageHeading>
        </StyledHeaderItem>
        <StyledHeaderItem>
          <Stepper steps={steps} activeStep={currentStep} />
        </StyledHeaderItem>
      </StyledPageHeader>
      {currentStep === 1 && <ApplicationFormStep1 actions={actions} />}
      {currentStep === 2 && <ApplicationFormStep2 actions={actions} />}
      {currentStep === 3 && <ApplicationFormStep3 actions={actions} />}
      {currentStep === 4 && <ApplicationFormStep4 actions={actions} />}
      {currentStep === 5 && <ApplicationFormStep5 actions={actions} />}
      {currentStep === 6 && <ApplicationFormStep6 actions={actions} />}
    </Container>
  );
};

export default PageContent;