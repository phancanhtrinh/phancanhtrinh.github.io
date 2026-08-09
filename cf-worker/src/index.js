const ALLOWED_ORIGINS = [
	'https://www.phancanhtrinh.com',
	'https://phancanhtrinh.com',
	'http://localhost:4321',
	'http://127.0.0.1:4321',
];

function corsHeaders(origin) {
	return {
		'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
		'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
		'Access-Control-Allow-Headers': 'Content-Type',
		'Access-Control-Max-Age': '86400',
	};
}

function json(obj, status, headers) {
	return new Response(JSON.stringify(obj), {
		status,
		headers: { 'Content-Type': 'application/json', ...headers },
	});
}

async function getCount(env, storageKey) {
	const raw = await env.LIKES.get(storageKey);
	return raw ? parseInt(raw, 10) : 0;
}

async function bumpCount(env, storageKey, delta) {
	const next = Math.max(0, (await getCount(env, storageKey)) + delta);
	await env.LIKES.put(storageKey, String(next));
	return next;
}

export default {
	async fetch(request, env) {
		const url = new URL(request.url);
		const headers = corsHeaders(request.headers.get('Origin') || '');

		if (request.method === 'OPTIONS') {
			return new Response(null, { headers });
		}

		const ns = url.searchParams.get('ns');
		const key = url.searchParams.get('key');
		if (!ns || !key) {
			return json({ error: 'ns and key query params are required' }, 400, headers);
		}
		const storageKey = `${ns}:${key}`;

		if (url.pathname === '/stats' && request.method === 'GET') {
			return json({ likes: await getCount(env, storageKey) }, 200, headers);
		}

		if (url.pathname === '/like' && request.method === 'POST') {
			return json({ likes: await bumpCount(env, storageKey, 1) }, 200, headers);
		}

		if (url.pathname === '/unlike' && request.method === 'POST') {
			return json({ likes: await bumpCount(env, storageKey, -1) }, 200, headers);
		}

		return json({ error: 'not found' }, 404, headers);
	},
};
