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

async function answerResearch(request, env, headers) {
	if (!env.ANTHROPIC_API_KEY) return json({ error: 'research service is not configured' }, 503, headers);
	let body;
	try { body = await request.json(); } catch (_) { return json({ error: 'invalid JSON' }, 400, headers); }
	const question = typeof body.question === 'string' ? body.question.trim().slice(0, 1200) : '';
	if (!question) return json({ error: 'question is required' }, 400, headers);
	const prompt = `You are the public research assistant for Trinh Phan-Canh. Answer the visitor's question clearly and accurately. Use the supplied website context when relevant, distinguish verified facts from reasonable interpretation, and say when information is unavailable. You may explain broader scientific concepts, but do not invent personal facts, publications, awards, or clinical advice. Format the answer for a compact chat card: use only ## headings for major sections (at most three sections), use **bold** for emphasis, use '-' bullet lines for supporting points, never use numbers or numbered headings, and do not add blank lines between bullets. Put labels such as Email on their own line. Keep the answer concise but useful and include source URLs from the context when available.\n\nWebsite context:\n${JSON.stringify(body.context || {}).slice(0, 90000)}\n\nVisitor question:\n${question}`;
	const response = await fetch('https://api.anthropic.com/v1/messages', {
		method: 'POST',
		headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
		body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 900, messages: [{ role: 'user', content: prompt }] }),
	});
	if (!response.ok) return json({ error: 'upstream research service unavailable' }, 502, headers);
	const result = await response.json();
	const text = (result.content || []).filter((part) => part.type === 'text').map((part) => part.text).join('\n').trim();
	return json({ answer: text }, 200, headers);
}

export default {
	async fetch(request, env) {
		const url = new URL(request.url);
		const headers = corsHeaders(request.headers.get('Origin') || '');

		if (request.method === 'OPTIONS') {
			return new Response(null, { headers });
		}
		if (url.pathname === '/research' && request.method === 'POST') {
			return answerResearch(request, env, headers);
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
