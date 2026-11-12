# Browser extension guide

The extension captures only the domain host from a browser tab and sends it to the local monitoring agent or the central backend. It does not collect page contents, keystrokes, form data, or passwords.

## Files

- `manifest.json` declares permissions and service worker registration.
- `content.js` reads the tab hostname and sends a lightweight payload.
- `background.js` forwards the hostname to a local HTTP endpoint.

## Local agent endpoint

Default endpoint:

`http://localhost:9000/api/website-domain`

Configure the agent to accept the payload as JSON:

```json
{
  "computer_name": "PC-01",
  "session_id": 1,
  "domain": "youtube.com"
}
```

## Privacy safeguards

- Only the hostname is recorded.
- No payload content or personal page data is sent.
- Only school-authorized devices should deploy this extension.
