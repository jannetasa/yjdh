import { useRouter } from 'next/router';
import { getFirstValue } from 'shared/utils/array.utils';

const useApplicationIdQueryParam = (): string | undefined => {
  const router = useRouter();
  return getFirstValue(router.query.id);
}
export default useApplicationIdQueryParam;
