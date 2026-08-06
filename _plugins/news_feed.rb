# Merges blog posts, press mentions (_data/mediamentions.json), and
# outreach pieces (_data/cv.yml -> outreach) into one array, sorted by
# real date, for the combined /blog/ "News" page. Runs before rendering
# so post.excerpt/content are still handled natively via Liquid on the
# actual Post object (stored under 'post') rather than pre-rendered here.
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
        }
      end

      outreach = site.data.dig('cv', 'outreach') || []
      outreach.each do |o|
        year_match = o['year'].to_s.match(/\d{4}/)
        next if year_match.nil?
        date = Time.new(year_match[0].to_i, 1, 1)
        image = nil
        if o['url'].is_a?(String) && papers_by_url.key?(o['url'])
          image = papers_by_url[o['url']].data['image']
        end
        items << {
          'type' => 'outreach',
          'badge' => 'Outreach',
          'title' => o['title'],
          'url' => o['url'],
          'source' => o['journal'],
          'date' => date,
          'display_year' => o['year'],
          'image' => image,
        }
      end

      items.sort_by! { |it| it['date'] }
      items.reverse!

      site.data['news_feed'] = items
    end

    private

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
