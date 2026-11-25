import axios, { AxiosError, type AxiosResponse } from 'axios';

export const api = axios.create({
	baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1',
	timeout: 10_000,
	headers: { 'Content-Type': 'application/json' },
	// The refresh token travels in an HttpOnly cookie set by the API.
	withCredentials: true,
});

export type ApiErrorResponse = {
	error: {
		code: string;
		message: string;
		details?: Record<string, unknown>;
	};
};

export type ApiErrorEnvelope = AxiosError<ApiErrorResponse> & {
	response: AxiosResponse<ApiErrorResponse>;
};

export function isApiError(error: unknown): error is ApiErrorEnvelope {
	return axios.isAxiosError(error) && !!error.response?.data?.error;
}

/** Best-effort human message from the API error envelope. */
export function apiErrorMessage(error: unknown, fallback = 'Something went wrong.'): string {
	if (isApiError(error)) return error.response.data.error.message;
	if (axios.isAxiosError(error) && !error.response) return 'Cannot reach the server. Check your connection.';
	return fallback;
}

/** Field-level validation details from the API error envelope, if any. */
export function apiErrorDetails(error: unknown): Record<string, unknown> | undefined {
	return isApiError(error) ? error.response.data.error.details : undefined;
}

// --- In-memory access token -------------------------------------------------
// The access token never touches localStorage or cookies; it lives only in this
// module's memory (docs/sacs.md section 3.4). A page reload starts from the
// refresh cookie through the /auth/token/refresh/ endpoint.

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
	accessToken = token;
}

export function getAccessToken() {
	return accessToken;
}

// --- Coordinated silent refresh --------------------------------------------

let refreshInFlight: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
	const response = await api.post<{ access: string }>('/auth/token/refresh/');
	return response.data.access;
}

export function refreshSession(): Promise<string> {
	// Concurrent 401s share one refresh round trip instead of racing.
	refreshInFlight ??= refreshAccessToken()
		.then((token) => {
			setAccessToken(token);
			return token;
		})
		.finally(() => {
			refreshInFlight = null;
		});
	return refreshInFlight;
}

api.interceptors.request.use((config) => {
	if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
	return config;
});

api.interceptors.response.use(
	(response) => response,
	async (error: AxiosError) => {
		const original = error.config as (typeof error.config & { _retried?: boolean }) | undefined;
		const status = error.response?.status;
		const isAuthCall = original?.url?.includes('/auth/');

		if (status === 401 && original && !original._retried && !isAuthCall) {
			original._retried = true;
			try {
				// The request interceptor re-attaches the refreshed in-memory token.
				await refreshSession();
				return api.request(original);
			} catch {
				setAccessToken(null);
			}
		}
		return Promise.reject(error);
	},
);