# Netnotics - Infrastructure Management SPA

This is one of the largest projects I've taken on solo. A full-stack single page web application to make infrastructure automation and management a breeze for IT administrators.

### Current Stack
- Backend: Python (FastAPI & httpx)
- Frontend: SvelteKit
- Database: Postgres (currently, still determining the right fit and may incorporate Redis in the near future depending upon needs/best practices)

### Current Features
- Session-based user authentication with sessions stored in database
- Protected frontend routes

### Currently Working On:
- [ ] Frontend reactivity for devices
- [ ] Edit inventory/devices (backend & frontend)
- [ ] Programmatically pull device state (will test with Cisco sandboxes)
- [ ] Rewrite tests to meet session-based authentication requirements :O
- [ ] Containerize full-stack environment

### Bold Feature Ideas:
- [ ] Give users the ability to define custom columns using xpath filters (we'll see about this one)
