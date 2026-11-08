// While the site is being built, the public domain shows a "coming soon" page.
// The full site stays viewable on the workers.dev preview address.
// To launch: set PUBLIC_LAUNCH to true (or delete this file and "main" from wrangler.jsonc).
const PUBLIC_LAUNCH = false;
const PUBLIC_HOSTS = new Set(["sarcomahub.com", "www.sarcomahub.com"]);
const SHARED = ["/assets/logo-sh.svg", "/assets/logo-800.webp", "/assets/logo-800.jpg", "/assets/letter-s.svg", "/assets/letter-h.svg", "/assets/favicon-32.png", "/assets/apple-touch-icon.png", "/assets/og-image.jpg"];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (PUBLIC_LAUNCH || !PUBLIC_HOSTS.has(url.hostname)) return env.ASSETS.fetch(request);
    if (SHARED.includes(url.pathname)) return env.ASSETS.fetch(request);
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain" } });
    }
    const page = await env.ASSETS.fetch(new Request(new URL("/coming-soon/", url), request));
    return new Response(page.body, {
      status: 200,
      headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" },
    });
  },
};
