import styled from 'styled-components';

type Props = { backgroundColor?: string };

export const $Section = styled.div`
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid ${(props) => props.theme.colors.black20};
  padding-bottom: ${(props) => props.theme.spacing.m};
  margin-bottom: ${(props) => props.theme.spacing.s};
`;

export const $SubHeader = styled.h3`
  font-size: ${(props) => props.theme.fontSize.heading.xxs};
  font-weight: 600;
`;

export const $Content = styled.div`
  display: flex;
  flex-direction: column;
  font-size: ${(props) => props.theme.fontSize.heading.s};
  font-weight: normal;
  line-height: ${(props) => props.theme.lineHeight.l};
`;

export const $FormGroup = styled.div<Props>`
  display: flex;
  align-items: center;
  font-size: ${(props) => props.theme.fontSize.body.m};
  margin-bottom: ${(props) => props.theme.spacing.xs};
  gap: ${(props) => props.theme.spacing.s};
  background-color: ${(props) => props.backgroundColor};
`;

export const $FieldsContainerWithPadding = styled.div`
  display: flex;
  height: 130px;
  padding-left: var(--spacing-m);
  padding-right: var(--spacing-xs);
  padding-top: ${(props) => props.theme.spacingLayout.xs2};
  margin-right: 0 !important;
  gap: ${(props) => props.theme.spacing.xs};

  & > div {
    width: 236px;
  }
`;

export const $ViewFieldsContainer = styled.div`
  font-size: ${(props) => props.theme.fontSize.body.m};
  display: flex;
  align-items: center;
  padding: ${(props) => props.theme.spacing.xs};
  margin-right: 0 !important;
  padding-right: 0;
  & > div {
    width: 240px;
    margin-left: ${(props) => props.theme.spacing.xs};
  }
  & > div > div {
    margin-right: ${(props) => props.theme.spacing.xs};
  }
  width: 100%;
`;

export const $ViewField = styled.div``;
