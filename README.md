# juanjosemunoz.com

Sitio nuevo de Juan José Muñoz, que reemplaza la versión en Webflow. Se va a hospedar en Cloudflare Pages.

## Estado

Fase de estrategia y contenido. Todavía no hay código del sitio.

## Qué hay aquí

- `src/content/blog/`: los 366 artículos exportados de Webflow (2016–2025) en Markdown. El encabezado de cada uno incluye título, fecha, slug original, eje, tema, serie, si es candidato a "Empezá aquí" y, cuando aplica, de qué artículo es duplicado.
- `public/images/blog/`: las 228 imágenes de los artículos, una carpeta por artículo.
- `public/brand/`: logo, favicon y otras imágenes de marca del sitio actual.
- `inventario-blog.csv`: inventario completo del blog con la clasificación.
- `docs/mapa-del-blog.html`: página para revisar la clasificación y la estructura propuesta.
- `tools/`: scripts de la exportación (rastreo, conversión a Markdown, descarga de imágenes), la clasificación en TSV y `imagenes-origen.json` con la URL original de cada imagen.

## Las URLs

Los artículos conservan su slug de Webflow (`/blog/<slug>`), así se pueden mantener las mismas direcciones o redirigirlas con 301.
