# InkMerge Shopify Custom Theme

## Overview
InkMerge is a custom Shopify theme tailored for a DTF transfer business. Its primary purpose is to offer transparent square-inch pricing ($0.02/sq inch) for DTF transfers, featuring a gang sheet builder, product upload functionality, and robust SEO optimization. The project aims for high conversion rates, seamless user experience, and strong organic search performance through Google 2025 compliant content.

## User Preferences
- Design inspired by Ninja Transfers but uniquely InkMerge-branded
- Fast, secure, mobile/desktop optimized
- Conversion-focused features
- Low stock alerts only for 3-15 items
- **CRITICAL**: Upload Center app uses natural form submissions - no JavaScript preventDefault()
- Variant selection uses normalized Unicode character matching
- All dynamic content properly escaped to prevent injection
- Structured data uses proper JSON-LD format with numeric values (not strings)
- Schema validated for Google Rich Results

## System Architecture

### UI/UX Decisions
- Clean, professional design with a focus on product clarity and ease of use.
- Gang sheet builder products display only the builder button, while regular DTF transfers show standard product pages.
- Standardized box structure for product pages across all templates.
- Mobile-responsive design implemented throughout, including card layouts for SEO content and testimonial sections.
- Purple gradient and interactive styling for blog articles.
- Visual breadcrumb navigation implemented with matching UI and schema.

### Technical Implementations
- **Product Templates**: Converted to modern JSON template architecture (`templates/product.json`) to support app blocks via the theme customizer. `product.liquid` content moved to `sections/main-product.liquid`.
- **Gang Sheet Builder**: Uses a dedicated `product.gang-sheet.json` template. CSS (`.gang-sheet-hide-controls`) dynamically hides size, quantity, and add-to-cart elements for gang sheet products, focusing the user on the builder.
- **Performance Optimization**: Eliminated forced reflows, reduced Total Blocking Time, and ensured cross-browser compatibility through JavaScript optimizations (e.g., `IntersectionObserver`, throttled scroll, `requestAnimationFrame`, `localStorage` checks) for scripts like `sticky-cart.js`, `recently-bought.js`, and `gdpr-cookie-bar.js`.
- **SEO Enhancements**:
    - **Schema Markup**: Extensive use of JSON-LD for Article, Organization, AboutPage, FAQPage, CollectionPage, and BreadcrumbList schemas, including dynamic Liquid dates and numerical values.
    - **Content Strategy**: Implemented a 6-week content strategy focusing on keyword-rich product descriptions, collection page SEO content (300-500 words below products), and 99 unique, customer-focused blog articles.
    - **Google 2025 Compliance**: Blog articles are optimized with specific phrases for first-hand experience (6-8 per article) to avoid scaled content abuse detection.
    - **Internal Linking**: Automated visual breadcrumbs and contextual help links on product pages.
    - **OpenGraph & Twitter Cards**: Product-specific social media meta tags with image fallbacks.
- **Lead Magnet Funnel**: A standalone Replit-hosted system for email list building, comprising a landing page, Python backend API (handling form submissions and Acumbamail integration), and a thank-you page. Shopify simply redirects to the Replit-hosted landing page.
- **Blog Article Management**: Cleanup of 198 duplicate and 31 seller-focused articles, replaced with 31 new customer-focused topics, resulting in 99 unique, 800+ word articles promoting InkMerge pricing.
- **Link Management**: Fixed 5 broken links and ensured proper `link` title attributes across 469 pages.
- **Critical Variant Pricing Fix**: Implemented `normalizeOption()` to handle Unicode character mismatches in variant selection.
- **AI Compatibility**: Enhanced Organization Schema with AggregateRating, geo coordinates, business hours, and `knowsAbout` array.

### Feature Specifications
- **Gang Sheet Builder**: Dedicated product template and CSS rules to streamline the builder experience.
- **Order Tracking**: Functionality integrated via `templates/page.track-your-order.liquid`.
- **SEO-Optimized Blog**: 99 unique articles with structured data, author profiles, and Google 2025 compliance.
- **Lead Magnet**: Fully operational funnel including a 50+ page DTF Application Guide.
- **Testimonials & Reviews Section**: `sections/testimonials-reviews.liquid` displaying customer cards and trust badges.
- **Rich About Us Page**: `templates/page.about-us.liquid` providing brand story, expertise, and CTAs.
- **FAQ Page**: `templates/page.faq.liquid` with 12 Q&A pairs and FAQPage schema.

## External Dependencies

- **Acumbamail**: Used for email list management and sending welcome emails for the lead magnet funnel (List ID: 1188198).
- **IndexPlease App**: Shopify app installed for IndexNow instant indexing with Bing, Yandex, Naver, Baidu, DuckDuckGo, and Seznam.
- **Shopify CDN**: Used for hosting verification files and other assets.
- **Google Rich Results Test**: External tool used for validating schema markup.
- **Replit**: Hosts the lead magnet landing page, backend API, guide, and thank-you page.
- **Trustpilot & Google Reviews**: Integrated for displaying testimonials and linking to external review platforms.