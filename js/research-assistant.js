(function () {
  'use strict';

  var dataNode = document.getElementById('research-assistant-data');
  var messagesNode = document.getElementById('research-assistant-messages');
  var form = document.getElementById('research-assistant-form');
  var input = document.getElementById('research-assistant-input');
  if (!dataNode || !messagesNode || !form || !input) return;

  var data;
  try {
    data = JSON.parse(dataNode.textContent);
  } catch (error) {
    return;
  }

  var stopWords = {
    a: 1, about: 1, an: 1, and: 1, are: 1, as: 1, at: 1, be: 1, by: 1,
    can: 1, did: 1, do: 1, does: 1, for: 1, from: 1, has: 1, have: 1,
    he: 1, his: 1, how: 1, i: 1, in: 1, is: 1, it: 1, me: 1, of: 1,
    on: 1, or: 1, please: 1, tell: 1, that: 1, the: 1, their: 1, them: 1,
    they: 1, this: 1, to: 1, trinh: 1, was: 1, what: 1, when: 1, where: 1,
    which: 1, who: 1, why: 1, with: 1, you: 1, your: 1
  };

  var synonymGroups = [
    ['candida', 'auris', 'fungal', 'fungus', 'mycology', 'pathogen'],
    ['antifungal', 'drug', 'resistance', 'tolerance', 'azole', 'amphotericin'],
    ['skin', 'cutaneous', 'keratinocyte', 'fibroblast', 'colonization', 'tropism'],
    ['spatial', 'multiomics', 'multi-omics', 'omics', 'transcriptomics', 'proteomics'],
    ['switching', 'plasticity', 'morphogenesis', 'morphotype', 'white', 'brown'],
    ['career', 'position', 'role', 'job', 'work', 'experience'],
    ['award', 'prize', 'honor', 'recognition'],
    ['paper', 'publication', 'article', 'study', 'research'],
    ['education', 'degree', 'phd', 'pharmacy', 'training'],
    ['news', 'media', 'coverage', 'press'],
    ['diary', 'blog', 'story', 'memoir', 'village', 'vienna', 'saigon', 'student', 'teaching']
  ];

  var synonymMap = {};
  synonymGroups.forEach(function (group) {
    group.forEach(function (word) {
      synonymMap[word] = group;
    });
  });

  function plain(value) {
    var div = document.createElement('div');
    div.innerHTML = value == null ? '' : String(value);
    return (div.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function normalize(value) {
    return plain(value).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function tokens(value) {
    var seen = {};
    normalize(value).split(/\s+/).forEach(function (token) {
      if (token.length < 2 || stopWords[token]) return;
      seen[token] = 1;
      (synonymMap[token] || []).forEach(function (related) { seen[related] = 0.35; });
    });
    return seen;
  }

  function compact(text, limit) {
    text = plain(text).replace(/^(summary|abstract|highlights|importance)\s*/i, '');
    if (text.length <= limit) return text;
    var clipped = text.slice(0, limit);
    var sentence = clipped.lastIndexOf('. ');
    if (sentence > limit * 0.55) clipped = clipped.slice(0, sentence + 1);
    return clipped.replace(/[\s,;:]+$/, '') + '…';
  }

  function paperBy(fragment) {
    fragment = normalize(fragment);
    return data.papers.find(function (paper) {
      return normalize(paper.title).indexOf(fragment) !== -1;
    });
  }

  function source(label, url) {
    return { label: label, url: url };
  }

  function safeUrl(value) {
    try {
      var parsed = new URL(value, window.location.origin);
      return parsed.protocol === 'http:' || parsed.protocol === 'https:' ? parsed.href : null;
    } catch (error) {
      return null;
    }
  }

  var documents = [];
  data.papers.forEach(function (paper) {
    documents.push({
      kind: 'paper',
      title: plain(paper.title),
      text: [paper.title, paper.authors, paper.journal, paper.year, paper.summary].join(' '),
      summary: compact(paper.summary, 440),
      url: paper.url,
      meta: [plain(paper.journal), paper.year].filter(Boolean).join(' · ')
    });
  });
  (data.news || []).forEach(function (item) {
    documents.push({
      kind: 'news',
      title: plain(item.title),
      text: [item.title, item.source, item.date].join(' '),
      summary: 'Public coverage from ' + plain(item.source) + (item.date ? ', dated ' + item.date : '') + '.',
      url: item.url,
      meta: [plain(item.source), item.date].filter(Boolean).join(' · ')
    });
  });
  (data.diary || []).forEach(function (item) {
    documents.push({
      kind: 'diary',
      title: plain(item.title),
      text: [item.title, item.date, item.text].join(' '),
      summary: compact(item.text, 520),
      url: item.url,
      meta: item.date || ''
    });
  });
  documents.forEach(function (doc) { doc.terms = tokens(doc.text); });

  function rank(query, kind) {
    var queryTerms = tokens(query);
    var queryNorm = normalize(query);
    return documents.filter(function (doc) { return !kind || doc.kind === kind; }).map(function (doc) {
      var score = 0;
      Object.keys(queryTerms).forEach(function (term) {
        if (doc.terms[term] !== undefined) score += 2.2 + queryTerms[term];
        if (normalize(doc.title).indexOf(term) !== -1) score += 2.5;
      });
      if (queryNorm.length > 5 && normalize(doc.text).indexOf(queryNorm) !== -1) score += 8;
      if (doc.kind === 'paper') score += 0.15;
      return { doc: doc, score: score };
    }).filter(function (entry) { return entry.score > 1.2; })
      .sort(function (a, b) { return b.score - a.score; });
  }

  function list(items) {
    var ul = document.createElement('ul');
    items.forEach(function (item) {
      var li = document.createElement('li');
      li.textContent = item;
      ul.appendChild(li);
    });
    return ul;
  }

  function response(paragraphs, sources, bullets) {
    return { paragraphs: paragraphs || [], sources: sources || [], bullets: bullets || [] };
  }

  function contributionResponse() {
    var nce = paperBy('carbonic anhydrase nce103');
    var switching = paperBy('white brown switching');
    var rip1 = paperBy('rip1 modulates antifungal tolerance');
    var skin = paperBy('keratinocytes and fibroblasts');
    return response(
      ['Trinh Phan-Canh’s work connects fungal genetics, host–pathogen biology, and translational antifungal research. His main scientific contributions are:'],
      [
        nce && source('Nce103 and skin tropism', nce.url),
        switching && source('White–Brown switching', switching.url),
        rip1 && source('Rip1 and drug tolerance', rip1.url),
        skin && source('Human skin immunity', skin.url),
        source('Complete publication list', data.papersUrl)
      ].filter(Boolean),
      [
        'Identifying a carbon-sensing pathway centered on Nce103 that supports Candida auris skin fitness and amphotericin B resistance.',
        'Defining reversible White–Brown switching as a mechanism of phenotypic plasticity, host adaptation, immune interaction, and virulence.',
        'Clarifying multiple routes to antifungal resistance and tolerance, including 5-fluorocytosine adaptation, PDR16 gene dosage, and mitochondrial Rip1.',
        'Advancing human-skin models of fungal infection, epithelial immunity, and practical strategies to reduce C. auris colonization.',
        'Extending this foundation into spatial multi-omics for host–disease interactions at BIDMC and Harvard Medical School.'
      ]
    );
  }

  function currentResearchResponse() {
    var current = (data.profile.experience || [])[0] || {};
    return response([
      'Trinh is a postdoctoral researcher at BIDMC and Harvard Medical School. His current focus is the development of spatial multi-omics technologies to study host–disease interactions.',
      'This builds on his earlier work in fungal pathogenesis, drug resistance, host immunity, genetic engineering, and integrated transcriptomic/proteomic analysis.'
    ], [source('Curriculum vitae', data.profile.cvUrl), source('Publication record', data.papersUrl)]);
  }

  function educationResponse() {
    var entries = (data.profile.education || []).slice(0, 4).map(function (item) {
      return plain(item.degree) + ' — ' + plain(item.place) + ' (' + plain(item.date) + ')';
    });
    return response(['His training spans molecular genetics and immunology, pharmacy, and information technology:'], [source('Curriculum vitae', data.profile.cvUrl)], entries);
  }

  function awardsResponse() {
    var awards = (data.profile.awards || []).slice(0, 7).map(plain);
    return response(['Selected recent awards and recognitions include:'], [source('Curriculum vitae', data.profile.cvUrl), source('Verified media coverage', data.newsUrl)], awards);
  }

  function paperSearchResponse(question) {
    var results = rank(question, 'paper').slice(0, 4);
    if (!results.length) return null;
    var sources = results.map(function (entry) { return source(entry.doc.title, entry.doc.url); });
    var bullets = results.map(function (entry) {
      return entry.doc.title + (entry.doc.meta ? ' (' + entry.doc.meta + ')' : '') + ': ' + compact(entry.doc.summary, 240);
    });
    return response(['These publications are the closest matches in Trinh’s paper archive:'], sources, bullets);
  }

  function newsResponse(question) {
    var results = rank(question, 'news').slice(0, 5);
    if (!results.length) {
      return response(['I could not find a matching verified media item. The complete News page is checked daily across public outlets.'], [source('Browse verified coverage', data.newsUrl)]);
    }
    return response(['These verified public items are the closest matches:'], results.map(function (entry) {
      return source(entry.doc.title, entry.doc.url);
    }), results.map(function (entry) { return entry.doc.title + ' — ' + entry.doc.meta; }));
  }

  function diaryResponse(question) {
    var results = rank(question, 'diary').slice(0, 5);
    if (!results.length) return null;
    return response(['These diary entries are the closest matches in the archive:'], results.map(function (entry) {
      return source(entry.doc.title, entry.doc.url);
    }), results.map(function (entry) {
      return entry.doc.title + (entry.doc.meta ? ' (' + entry.doc.meta + ')' : '') + ': ' + compact(entry.doc.summary, 300);
    }));
  }

  function answer(question) {
    var q = normalize(question);

    if (/^(hi|hello|hey|xin chao|chao)\b/.test(q)) {
      return response(['Hello! I can help you explore Trinh Phan-Canh’s scientific contributions, papers, current research, training, awards, and verified public coverage. Try one of the suggested questions above.']);
    }
    if (/\b(contact|email|reach|collaborat|talk to|message)\b/.test(q)) {
      return response(['You can contact Trinh at cphan4@bidmc.harvard.edu. For collaboration or detailed scientific questions, email is the best route.'], [source('Contact information', data.profile.contactUrl)]);
    }
    if (/\b(diagnos|patient|medical advice|treat me|my symptoms|prescri)\b/.test(q)) {
      return response(['I can explain Trinh’s published research, but I cannot provide diagnosis, treatment recommendations, or individual medical advice. Please consult a qualified healthcare professional for personal health questions.'], [source('Browse the research papers', data.papersUrl)]);
    }
    if (/\b(main|major|key|important|overall|summary|summarize|contribution|impact)\b/.test(q) && /\b(science|scientific|research|work|contribution|impact)\b/.test(q)) {
      return contributionResponse();
    }
    if (/\b(current|currently|now|harvard|bidmc|postdoc|position|role|employed)\b/.test(q) || /\bwhere\b.*\b(work|based)\b/.test(q)) {
      return currentResearchResponse();
    }
    if (/\b(education|degree|studied|study|training|phd|pharmacy)\b/.test(q)) {
      return educationResponse();
    }
    if (/\b(award|prize|honor|recognition)\b/.test(q)) {
      return awardsResponse();
    }
    if (/\b(news|media|press|coverage|internet)\b/.test(q)) {
      return newsResponse(question);
    }
    if (/\b(diary|blog|story|memoir|village|vienna|saigon|student|teaching|teacher|life)\b/.test(q)) {
      var diaryAnswer = diaryResponse(question);
      if (diaryAnswer) return diaryAnswer;
    }
    if (/\b(who is|about trinh|biography|background)\b/.test(q)) {
      return response([
        'Trinh Phan-Canh is a pharmacist and molecular biologist working at the intersection of fungal pathogenesis, antifungal resistance, host immunity, and spatial multi-omics. He earned his PhD at the Medical University of Vienna and Max Perutz Labs, and is now a postdoctoral researcher at BIDMC and Harvard Medical School.'
      ], [source('Curriculum vitae', data.profile.cvUrl), source('Publications', data.papersUrl)]);
    }

    var paperAnswer = paperSearchResponse(question);
    if (paperAnswer) return paperAnswer;

    var diaryAnswer = diaryResponse(question);
    if (diaryAnswer) return diaryAnswer;

    return response([
      'I could not verify a specific answer from the available biography, publication archive, or public coverage. Try asking about Candida auris, antifungal resistance, skin tropism, White–Brown switching, spatial multi-omics, education, awards, or a paper title.',
      'For questions requiring unpublished information or personal interpretation, please contact Trinh directly.'
    ], [source('Contact Trinh', data.profile.contactUrl)]);
  }

  function addMessage(role, content) {
    var row = document.createElement('div');
    row.className = 'research-assistant-message ' + (role === 'user' ? 'is-user' : 'is-assistant');
    var bubble = document.createElement('div');
    bubble.className = 'research-assistant-bubble';

    if (role === 'user') {
      bubble.textContent = content;
    } else {
      content.paragraphs.forEach(function (paragraph) {
        var p = document.createElement('p');
        p.textContent = paragraph;
        bubble.appendChild(p);
      });
      if (content.bullets && content.bullets.length) bubble.appendChild(list(content.bullets));
      if (content.sources && content.sources.length) {
        var sourceBox = document.createElement('div');
        sourceBox.className = 'research-assistant-sources';
        var label = document.createElement('span');
        label.className = 'research-assistant-sources-label';
        label.textContent = 'Sources';
        sourceBox.appendChild(label);
        content.sources.slice(0, 6).forEach(function (item) {
          var href = safeUrl(item.url);
          if (!href) return;
          var link = document.createElement('a');
          link.href = href;
          link.target = '_blank';
          link.rel = 'noopener';
          link.textContent = item.label;
          sourceBox.appendChild(link);
        });
        bubble.appendChild(sourceBox);
      }
    }

    row.appendChild(bubble);
    messagesNode.appendChild(row);
    messagesNode.scrollTop = messagesNode.scrollHeight;
  }

  function ask(question) {
    question = String(question || '').trim();
    if (!question) return;
    addMessage('user', question);
    input.value = '';
    window.setTimeout(function () { addMessage('assistant', answer(question)); }, 140);
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    ask(input.value);
  });
  document.querySelectorAll('[data-assistant-question]').forEach(function (button) {
    button.addEventListener('click', function () { ask(button.getAttribute('data-assistant-question')); });
  });

  addMessage('assistant', response([
    'Hello — I’m Trinh’s website-grounded research guide. Ask me about his scientific contributions, papers, current work, training, awards, verified coverage, or diary entries. I will link the sources behind my answer.'
  ]));
}());
