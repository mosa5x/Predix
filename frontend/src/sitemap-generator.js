const fs = require('fs');
const path = require('path');

const baseUrl = 'https://predix.site';

// Define your routes here
const routes = [
  '/',
  '/stock/:stockId',
  '/commodities',
  '/commodity/:commodityId',
  '/cryptocurrencies',
  '/cryptocurrency/:cryptoId'
];

// Generate sitemap content
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${routes.map(route => {
    // Replace dynamic parts with wildcards
    const path = route.replace(/:[^/]+/g, '*');
    return `
  <url>
    <loc>${baseUrl}${path}</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>`;
  }).join('')}
</urlset>`;

// Write sitemap to file
fs.writeFileSync(path.join(__dirname, '../public/sitemap.xml'), sitemap);

console.log('Sitemap generated successfully');