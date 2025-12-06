import axios from 'axios';

export type ApiError = Error & { status?: number };

export const getError = (err: unknown): ApiError => {
  const error = new Error('An unknown error occurred') as ApiError;

  if (axios.isAxiosError(err)) {
    const status = err.response?.status;
    const data = err.response?.data as { detail?: unknown } | undefined;
    let detail: string | undefined;

    if (Array.isArray(data?.detail)) {
      detail = data?.detail
        .map((item: any) => item?.msg || item?.message || JSON.stringify(item))
        .join('; ');
    } else if (typeof data?.detail === 'string') {
      detail = data.detail;
    } else if (data?.detail !== undefined) {
      detail = JSON.stringify(data.detail);
    }

    error.message = detail ?? err.message ?? error.message;
    error.status = status;
    return error;
  }

  return error;
};
