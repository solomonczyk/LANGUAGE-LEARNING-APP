# Audio and Media Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-022

---

## 1. Supported Formats

| Operation | Format | Codec | Sample Rate | Bitrate |
|-----------|--------|-------|-------------|---------|
| Recording | AAC (`.m4a`) | AAC-LC | 44.1kHz | 128kbps |
| Upload | Same as recording | Same | Same | Same |
| Playback (content) | MP3, AAC | MP3/AAC-LC | 44.1kHz | V0–320kbps |
| Playback (AI generation) | — | — | — | Post-MVP |

---

## 2. Recording Limits

| Parameter | Limit | Enforcement |
|-----------|-------|-------------|
| Max duration per recording | 120 seconds | Timer on client + server check |
| Max file size | 5 MB | Server check, reject with 422 |
| Min duration | 1 second (debounce) | Client-side guard |

---

## 3. Microphone Permission

| Flow | Detail |
|------|--------|
| Request timing | At point of need (user taps record button, first time) |
| Denied? | Show explanation screen → "Open Settings" → `Linking.openSettings()` |
| Never prompt | After one denial without explanation screen |

---

## 4. Recording Interruption Handling

| Interruption | Behaviour |
|-------------|-----------|
| Phone call | Pause recording, save draft (URI + position), show "Recording paused" |
| App background | Pause recording, save draft to local storage |
| Alarm (iOS/Android) | Pause recording, same as phone call |
| Audio focus loss (Android) | Pause recording |

On resume: user sees paused state, may continue recording (from where paused) or discard.

---

## 5. Upload Flow

```
Record → Local file → Validate (format, size, duration) → Checksum → Upload → Storage
```

| Step | Detail |
|------|--------|
| Checksum | SHA-256 of file content, computed client-side |
| Upload | Multipart POST to `/api/v1/submissions/audio` |
| Idempotency | `Idempotency-Key` header prevents duplicate upload |
| Resume | Post-MVP (simple retry for MVP) |
| Success | Server returns `storage_key` and `transcript` (post-MVP) |

---

## 6. Duplicate Upload Prevention

| Mechanism | Detail |
|-----------|--------|
| Idempotency Key | Same key = same upload ignored (409) |
| Checksum | Same checksum within 5 minutes = potential duplicate, flagged |
| Server side | UNIQUE constraint on `(lesson_session_id, checksum)` |

---

## 7. Storage

| Environment | Storage | Bucket |
|-------------|---------|--------|
| Local | MinIO (`localhost:9000`) | `audio-submissions` |
| Test | MinIO (Docker) | `audio-submissions-test` |
| Staging | Cloudflare R2 | `audio-submissions` |

Storage path: `{user_id}/{lesson_session_id}/{uuid}.m4a`

---

## 8. Transcript Lifecycle

| Stage | Action |
|-------|--------|
| Upload complete | Transcript generation queued (AI Gateway → `analyze_transcript()`) |
| In progress | Submission status: `analyzing` |
| Complete | Transcript stored in `submissions.transcript` |
| Failed | Transcript null; submission status: `failed` |
| Deletion | Transcript deleted with user account deletion |

---

## 9. Audio Playback

| Feature | Detail |
|---------|--------|
| Library | `expo-av` (Audio.Sound) |
| Controls | Play/pause, progress bar (seek), elapsed/total time |
| Speed | 0.5×, 1.0×, 1.5×, 2.0× |
| Audio session | `AVAudioSessionCategory.playback` (iOS), background mode |

---

## 10. Audio for MVP Sprint 1

**Audio runtime remains out of scope for Sprint 1 (vertical slice 003).** However, the contract is fixed as above.

What is in Sprint 1:
- Audio recording UI component (stub — disabled with "Coming soon" label)
- Audio player UI component (stub — disabled)
- Backend audio endpoint contracts (API exists, returns 501 Not Implemented)

What is NOT in Sprint 1:
- Real recording
- Real upload
- Real playback
- Transcript generation

Audio implementation is Sprint 2+.

---

## 11. Forbidden

| Action | Reason |
|--------|--------|
| Store audio files in PostgreSQL | LOB storage is inefficient; use object storage |
| Client-side transcript generation | Requires real LLM call; backend only |
| Upload without MIME validation | Security — file type spoofing |
| Unlimited recording duration | Storage and processing cost |
