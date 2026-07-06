# landing/ — Workshop Landing + Conversion Funnel

The trackable top-of-funnel that hands off to Luma registration.

## Purpose

- Mirror the event, drive the CTA to https://luma.com/7ango3wp.
- Instrument the funnel: page view -> "Request to Join" click -> registered -> attended.
- Deploy as **Cloudflare Worker Assets**; use **GSAP** for interactivity (house standard).

## Tracking layer (`landing/tracking/`)

| Layer | Tool | Events |
|-------|------|--------|
| Tag manager | Google Tag Manager | `page_view`, `cta_click_join`, `outbound_luma` |
| Paid social | Meta Pixel | `ViewContent`, `Lead`, `CompleteRegistration` |
| Paid social | TikTok Pixel | `ViewContent`, `ClickButton`, `CompleteRegistration` |
| Analytics | GA4 | funnel + livestream `watch_start` / `watch_25/50/75/100` |
| Server (optional) | Stape / CF server-side GTM | dedup + CAPI for Meta/TikTok |

> Luma is the registration system of record. The landing page is the trackable entry point
> that hands off to it. GTM MCP is connected on the build machine for container work.
> Google Ads / Shopify hooks are left commented for later if paid or ticketed.

IDs come from `.env` / `.dev.vars`: `GTM_CONTAINER_ID`, `META_PIXEL_ID`, `TIKTOK_PIXEL_ID`,
`GA4_MEASUREMENT_ID`.
