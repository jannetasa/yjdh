export const getFirstValue = <T>(value: T[] | T | undefined): T | undefined =>
  Array.isArray(value) ? (value.length > 0 ? value[0] : undefined) : value;

export const getLastValue = <T>(value: T[] | T | undefined): T | undefined =>
  Array.isArray(value)
    ? value.length > 0
      ? value.slice(-1)[0]
      : undefined
    : value;

export const isEmpty = (arr?: Array<unknown>): boolean =>
  arr?.length === 0 ?? true;

export type ArrayType<A> = A extends (infer I)[] ? I : never;
