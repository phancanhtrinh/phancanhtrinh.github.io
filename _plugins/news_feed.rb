# Merges blog posts, press mentions (_data/mediamentions.json), and
# outreach pieces (_data/cv.yml -> outreach) into one array, sorted by
# real date, for the combined /blog/ "News" page. Runs before rendering
# so post.excerpt/content are still handled natively via Liquid on the
# actual Post object (stored under 'post') rather than pre-rendered here.
require 'uri'

module Jekyll
  class NewsFeedGenerator < Generator
    priority :low

    YOUTUBE_EMBED_RE = %r{youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{6,})}.freeze

    def generate(site)
      items = []

      (site.categories['blog'] || []).each do |post|
        items << {
          'type' => 'update',
          'badge' => 'Update',
          'post' => post,
          'date' => post.date,
          'image' => update_image(post),
        }
      end

      papers_by_url = {}
      (site.categories['papers'] || []).each { |p| papers_by_url[p.url] = p }

      mentions = site.data.dig('mediamentions', 'mentions') || []
      mentions = unique_links(mentions)
      # Also clean the standalone press page when building an older archive.
      if site.data['mediamentions']
        site.data['mediamentions']['mentions'] = mentions
        site.data['mediamentions']['count'] = mentions.size
      end
      mentions.each do |m|
        date = parse_date(m['date'])
        next if date.nil?
        items << {
          'type' => 'press',
          'badge' => 'Press',
          'title' => m['title'],
          'url' => m['url'],
          'source' => m['source'],
          'date' => date,
          'display_date' => date,
          'image' => m['image'],
          'vietnamese' => vietnamese?(m['title']) || vietnamese?(m['source']),
        }
      end

      outreach = site.data.dig('cv', 'outreach') || []
      outreach.each do |o|
        date = parse_date(o['date'])
        if date.nil?
          year_match = o['year'].to_s.match(/\d{4}/)
          next if year_match.nil?
          date = Time.new(year_match[0].to_i, 1, 1)
        end
        image = o['image']
        if o['url'].is_a?(String) && papers_by_url.key?(o['url'])
          image ||= papers_by_url[o['url']].data['image']
        end
        items << {
          'type' => 'outreach',
          'badge' => 'Outreach',
          'title' => o['title'],
          'url' => o['url'],
          'source' => o['journal'],
          'date' => date,
          'display_date' => o['date'] ? date : nil,
          'display_year' => o['year'],
          'image' => image,
          'vietnamese' => vietnamese?(o['title']) || vietnamese?(o['journal']),
        }
      end

      items = unique_links(items)
      items.sort_by! { |it| it['date'] }
      items.reverse!

      site.data['news_feed'] = items
    end

    private

    def unique_links(items)
      seen = {}
      items.reject do |item|
        key = canonical_url(item['url'])
        next false if key.empty?
        duplicate = seen.key?(key)
        seen[key] = true
        duplicate
      end
    end

    def canonical_url(url)
      uri = URI.parse(url.to_s.strip)
      uri.fragment = nil
      uri.scheme = uri.scheme.downcase if uri.scheme
      uri.host = uri.host.downcase if uri.host
      uri.path = uri.path.to_s.sub(%r{/+\z}, '')
      if uri.query
        params = URI.decode_www_form(uri.query).reject do |key, _|
          key.downcase.start_with?('utm_') || %w[fbclid gclid mc_cid mc_eid].include?(key.downcase)
        end
        uri.query = params.empty? ? nil : URI.encode_www_form(params.sort)
      end
      uri.to_s
    rescue URI::InvalidURIError, ArgumentError
      url.to_s.strip
    end

    # Matches Vietnamese-only letters/tone marks (not used by German/French/
    # English), so this never false-positives on the site's other non-English
    # sources (e.g. German press mentions from meduniwien.ac.at).
    VIETNAMESE_RE = /[\u{0102}\u{0103}\u{0110}\u{0111}\u{01A0}\u{01A1}\u{01AF}\u{01B0}\u{1EA0}-\u{1EF9}]/.freeze

    def vietnamese?(text)
      !text.to_s.empty? && VIETNAMESE_RE.match?(text)
    end

    def update_image(post)
      image = post.data['image']
      return image if image && !image.to_s.empty?

      m = YOUTUBE_EMBED_RE.match(post.content.to_s)
      m ? "https://img.youtube.com/vi/#{m[1]}/hqdefault.jpg" : nil
    end

    def parse_date(value)
      return nil if value.nil? || value.to_s.empty?
      Date.parse(value.to_s).to_time
    rescue ArgumentError
      nil
    end
  end
end
