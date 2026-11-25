import { NextResponse, type NextRequest } from 'next/server';

/**
 * Optimistic route protection (Next.js 16 calls middleware "proxy").
 *
 * It only inspects the presence of the refresh cookie to redirect obvious
 * cases early. It is NOT a security boundary: the cookie can be stale or
 * forged at this layer, so the Django API independently verifies every
 * authenticated request (docs/sacs.md section 4.1). See docs/fis.md section 5.2.
 */

const SESSION_COOKIE = 'sp_refresh';
const PROTECTED_PREFIXES = ['/dashboard'];
const AUTH_PAGES = ['/login', '/register', '/forgot-password', '/reset-password'];

function matches(path: string, entries: string[]): boolean {
	return entries.some((entry) => path === entry || path.startsWith(`${entry}/`));
}

export function proxy(request: NextRequest) {
	const path = request.nextUrl.pathname;
	const hasSession = request.cookies.has(SESSION_COOKIE);

	if (matches(path, PROTECTED_PREFIXES) && !hasSession) {
		const loginUrl = new URL('/login', request.url);
		loginUrl.searchParams.set('next', path);
		return NextResponse.redirect(loginUrl);
	}

	if (matches(path, AUTH_PAGES) && hasSession) {
		return NextResponse.redirect(new URL('/dashboard', request.url));
	}

	return NextResponse.next();
}

export const config = {
	matcher: ['/((?!api|_next/static|_next/image|.*\\.(?:png|svg|ico|txt)$).*)'],
};