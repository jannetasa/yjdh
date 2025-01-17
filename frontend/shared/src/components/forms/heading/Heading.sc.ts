import styled, { DefaultTheme } from 'styled-components';

export type HeadingProps = {
  size?: keyof DefaultTheme['fontSize']['heading'];
  header?: string;
  loading?: boolean;
  loadingText?: string;
  loadingFinishedText?: string;
  tooltip?: string;
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'div';
};

export const $Header = styled.h1<HeadingProps>`
  ${(props) =>
    props.size ? `font-size: ${props.theme.fontSize.heading[props.size]};` : ''}
  display: flex;
  align-items: center;
  gap: ${(props) => props.theme.spacing.s};
  font-weight: 500;
`;
