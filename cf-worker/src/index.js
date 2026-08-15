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

function researchPrompt(question, context) {
	return `You are the public research assistant for Trinh Phan-Canh. Answer as a careful research colleague, not as a generic website chatbot. First identify what the visitor is actually asking; then investigate before writing. You MUST use Google Search for questions about current role, institution, awards, external coverage, employment, publications, citations, scientific claims, or any fact that could be independently verified. Search specific names, paper titles, institutions, PubMed/DOI records, and primary institutional pages; do not rely on search snippets alone. Use the supplied website context as an important lead and primary record of personal material, but never let it be the whole answer where independent sources can answer the question.\n\nGive the answer first, then explain the evidence and uncertainty. Do not pad with phrases such as "based on the supplied profile," "I can only find," or generic descriptions of research interests. If evidence is weak or conflicting, say precisely what is known, what is inferred, and what cannot be verified. Never invent personal facts, publications, awards, or clinical advice. Match the visitor's language. For scientific questions, explain mechanism, evidence, limitations, and significance when relevant.\n\nFormat for a compact chat card: at most three ## headings; short, substantive paragraphs; **bold** only for important terms; and '-' bullets only where they clarify a comparison or several distinct points. Never use numbered lists or numbered headings. Do not add blank lines between bullets. Always include 2–5 concise source URLs after a web search.\n\nWebsite context:\n${JSON.stringify(context || {}).slice(0, 90000)}\n\nVisitor question:\n${question}`;
}

function sourceList(urls) {
	const unique = [...new Set(urls.filter(Boolean))].slice(0, 5);
	return unique.length ? `\n\n## Sources\n${unique.map((url) => `- ${url}`).join('\n')}` : '';
}

async function answerWithGemini(prompt, env) {
	const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent', {
		method: 'POST',
		headers: { 'content-type': 'application/json', 'x-goog-api-key': env.GEMINI_API_KEY },
		body: JSON.stringify({
			contents: [{ role: 'user', parts: [{ text: prompt }] }],
			tools: [{ google_search: {} }],
			generationConfig: { maxOutputTokens: 1300, temperature: 0.35 },
		}),
	});
	if (!response.ok) throw new Error(`Gemini upstream status ${response.status}`);
	const result = await response.json();
	const candidate = result.candidates && result.candidates[0];
	const text = (candidate && candidate.content && candidate.content.parts || []).map((part) => part.text || '').join('\n').trim();
	if (!text) throw new Error('Gemini returned no answer');
	const chunks = candidate && candidate.groundingMetadata && candidate.groundingMetadata.groundingChunks || [];
	const sources = chunks.map((chunk) => chunk.web && chunk.web.uri).filter(Boolean);
	return { answer: text + sourceList(sources), searchedWeb: sources.length > 0, provider: 'gemini' };
}

async function answerWithClaude(prompt, env) {
	const apiHeaders = { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'anthropic-beta': 'web-search-2025-03-05' };
	const tools = [{ type: 'web_search_20250305', name: 'web_search', max_uses: 3 }];
	let messages = [{ role: 'user', content: prompt }];
	let result;

	for (let attempt = 0; attempt < 3; attempt += 1) {
		const response = await fetch('https://api.anthropic.com/v1/messages', {
			method: 'POST',
			headers: apiHeaders,
			body: JSON.stringify({ model: 'claude-sonnet-4-5-20250929', max_tokens: 1300, tools, messages }),
		});
		if (!response.ok) throw new Error(`Claude upstream status ${response.status}`);
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
	return { answer: text + sourceList(sources), searchedWeb: sources.length > 0, provider: 'claude' };
}

async function answerResearch(request, env, headers) {
	if (!env.GEMINI_API_KEY && !env.ANTHROPIC_API_KEY) return json({ error: 'research service is not configured' }, 503, headers);
	let body;
	try { body = await request.json(); } catch (_) { return json({ error: 'invalid JSON' }, 400, headers); }
	const question = typeof body.question === 'string' ? body.question.trim().slice(0, 1200) : '';
	if (!question) return json({ error: 'question is required' }, 400, headers);
	const prompt = researchPrompt(question, body.context);

	try {
		if (env.GEMINI_API_KEY) return json(await answerWithGemini(prompt, env), 200, headers);
		return json(await answerWithClaude(prompt, env), 200, headers);
	} catch (geminiError) {
		// Keep the public widget available if Gemini reaches a rate or billing limit.
		if (env.GEMINI_API_KEY && env.ANTHROPIC_API_KEY) {
			try { return json(await answerWithClaude(prompt, env), 200, headers); } catch (_) { /* handled below */ }
		}
		return json({ error: 'upstream research service unavailable' }, 502, headers);
	}
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
