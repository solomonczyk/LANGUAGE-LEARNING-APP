# Known Limitations

## Vertical Slice 003

### Functional Limitations
1. **Auth stub only** — Uses development auth stub, not Supabase Auth (per canon ADR-021, Supabase Auth will be integrated post-MVP)
2. **Mock AI only** — No real AI provider integration (intentionally deferred per task constraints)
3. **No audio** — Audio runtime not implemented (per ADR-022, deferred to Sprint 2+)
4. **No visual lessons** — Only personal_narrative lesson type implemented
5. **No SRS scheduler** — Spaced repetition not implemented
6. **No notifications** — Push notifications not implemented
7. **No reward economy** — XP/achievements not implemented (Gate 8 requires full reward gate)
8. **Limited mastery states** — Only introduced, recognized, guided_use allowed
9. **No payments** — Payment system not implemented
10. **No social features** — No social/sharing functionality

### Technical Limitations
1. **Docker not tested** — Docker Compose setup created but not verified in CI
2. **Mobile not run on device** — Screens built but not tested on physical devices
3. **No CI runs yet** — GitHub Actions workflows created but not executed
4. **Integration tests pending** — Integration tests require running database
5. **Visual QA pending** — Operator visual review not yet completed (Gate 8)
6. **No web/PWA** — Web secondary platform not implemented per ADR-014
7. **Limited test coverage for mobile** — Mobile tests not yet implemented

### Security Limitations
1. **No real authentication** — Auth stub bypasses JWT verification
2. **No rate limiting** — API rate limiting not implemented
3. **No prompt injection defense** — Learner text not scanned for injection markers
4. **No encryption at rest** — Database encryption not configured
5. **No secrets management** — Development .env with placeholder values

### Future Work
All limitations are tracked for post-MVP resolution. Vertical slice 003 is scoped as a functional MVP demonstration, not a production-ready system.
