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
	const prompt = `You are the public research assistant for Trinh Phan-Canh. Give a direct, specific, intellectually serious answer to the visitor's question. Treat the supplied website context as primary evidence for biographical facts, publications, awards, and research. For questions about current information, independent recognition, external publications, science beyond the supplied context, or when the context is insufficient, use web search before answering. Never say that you only have a name or ask the visitor to provide a URL when web search can resolve the question. Distinguish verified facts from interpretation and do not invent personal facts, publications, awards, or clinical advice. Format for a compact chat card: use at most three ## headings, short paragraphs, **bold** only for key terms (never insert line breaks inside bold markers), and '-' bullets only when they make a comparison or list clearer. Never use numbered lists or numbered headings. Do not add blank lines between bullet lines. Include concise sources when web search was used.\n\nWebsite context:\n${JSON.stringify(body.context || {}).slice(0, 90000)}\n\nVisitor question:\n${question}`;
	const apiHeaders = { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' };
	const tools = [{ type: 'web_search_20250305', name: 'web_search', max_uses: 3 }];
	let messages = [{ role: 'user', content: prompt }];
	let result;

	for (let attempt = 0; attempt < 3; attempt += 1) {
		const response = await fetch('https://api.anthropic.com/v1/messages', {
			method: 'POST',
			headers: apiHeaders,
			body: JSON.stringify({ model: 'claude-sonnet-4-5-20250929', max_tokens: 1300, tools, messages }),
		});
		if (!response.ok) return json({ error: 'upstream research service unavailable', upstreamStatus: response.status }, 502, headers);
		result = await response.json();
		if (result.stop_reason !== 'pause_turn') break;
		messages = messages.concat([{ role: 'assistant', content: result.content }]);
	}

	const textBlocks = (result.content || []).filter((part) => part.type === 'text');
	let text = textBlocks.map((part) => part.text).join('\n').trim();
	const sources = [];
	textBlocks.forEach((part) => (part.citations || []).forEach((citation) => {
		if (citation.url && !sources.includes(citation.url)) sources.push(citation.url);
	}));
	if (sources.length) text += `\n\n## Sources\n${sources.slice(0, 5).map((url) => `- ${url}`).join('\n')}`;
	return json({ answer: text, searchedWeb: sources.length > 0 }, 200, headers);
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
