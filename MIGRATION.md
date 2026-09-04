# Migrating from 1.x to 2.0

2.0.0 resyncs the SDK with the Aircall API after roughly eight months of drift, and
fixes a set of bugs that made much of 1.2.0 unusable.

**If you are on 1.2.0, upgrading is strongly recommended regardless of the breaking
changes below.** In 1.2.0 every method returning a `User`, `Call`, `Team`, `Message`
or `Integration` raised `` `User` is not fully defined `` on the first call — ten of
the sixteen core read paths were broken.

Most code needs no changes at all. The list below is ordered by how likely you are
to be affected.

---

## 1. `list_*` methods return a `Page`, not a plain list

Previously the pagination metadata Aircall sends was discarded, so there was no way
to page without hand-rolling requests.

`Page` subclasses `list`, so **iteration, indexing, `len()`, slicing, comparison and
`isinstance(x, list)` all keep working**. Most code needs no change.

```python
page = client.call.list_calls()

# unchanged
for call in page: ...
first = page[0]
count = len(page)

# new
page.meta.total          # total matching calls across all pages
page.meta.current_page
page.meta.next_page_link
page.has_next
page.total               # shorthand for page.meta.total
```

`page.meta` is `None` when an endpoint returns no metadata, so guard it if you are
not sure: `page.meta.total if page.meta else None`, or just use `page.total`.

**Action:** none, unless you relied on `type(result) is list` (an exact type check
rather than `isinstance`).

### `per_page` is now validated

Values outside the range Aircall accepts raise `ValueError` before the request is
sent, instead of returning a 400.

```python
client.call.list_calls(per_page=100)   # ValueError: per_page must be between 1 and 50
```

Most endpoints allow 1-50. `list_sms_templates()` allows 1-100.

---

## 2. Message send methods renamed

The old names described the wrong thing. `send()` skipped the agent inbox, while
`send_native()` was the agent-visible one — the opposite of what most people
assumed, and `send_native()`'s docstring wrongly called it a WhatsApp template
endpoint. Getting these the wrong way round sends customer traffic down the wrong
channel.

| 1.x | 2.0 | What it does |
|---|---|---|
| `send()` | `send_skipping_inbox()` | Bypasses the Aircall inbox. High-volume/automated. |
| `send_native()` | `send_in_conversation()` | Stored in the agent conversation, visible to agents. |

The old names still work and emit a `DeprecationWarning`, routing to the same
endpoint they always did. **Check which one you actually wanted before renaming.**

`media_url` is now a named parameter and is serialised as `mediaUrl`:

```python
client.message.send_skipping_inbox(number_id, to="+1555", body="hi",
                                   media_url=["https://example.com/a.png"])
```

### Message send responses now parse

`send()` previously did `Message(**response["message"])`, but Aircall returns the
message object at the top level with no envelope — so every send raised `KeyError`.
Fixed. `Message.media_url` was added, and `Message.external_number` became optional
because send responses do not include it.

---

## 3. User V1 is deprecated

Aircall removes the V1 list, retrieve, create and update endpoints on **2026-09-30**.
Those four methods now emit a `DeprecationWarning`.

```python
# before
client.user.list_users()
client.user.get(456)

# after
client.userv2.list_users()
client.userv2.get(456)
```

`client.user.delete()`, `get_availability()`, `get_availabilities()`, `start_call()`
and `dial()` are **not** deprecated — they have no V2 equivalent and remain where
they are.

### `client.userv2` actually reaches `/v2` now

In 1.2.0 `AircallClient` defined a `base_url_v2` but `_request` hardcoded the v1 URL,
so every `userv2` call silently hit `/v1`. `client.userv2.get()` was an exact
duplicate of `client.user.get()`, and `client.userv2.get_numbers()` returned a 404.

`UserV2Resource` now returns `UserV2` objects rather than `User`:

```python
user = client.userv2.get(456)      # UserV2, not User
```

`UserV2` has no `numbers` field — Aircall's V2 user object omits it. Use
`get_numbers()`.

### `userv2.get_numbers()` returns Numbers, not IDs

It read a `number_ids` key the API never sends, so it raised `KeyError`.

```python
# before (never worked)
number_ids = client.userv2.get_numbers(456)   # list[int]

# after
page = client.userv2.get_numbers(456)         # Page of Number objects
ids = [n.id for n in page]
```

---

## 4. `UserAvailability` changed shape

The model declared five booleans (`available`, `offline`, `do_not_disturb`,
`in_call`, `after_call_work`), but Aircall returns a single string. Every field
parsed as `None` — silently wrong rather than failing.

```python
# before (always None)
client.user.get_availability(456).available

# after
client.user.get_availability(456).availability     # "after_call_work"
```

`get_availabilities()` is now paginated and returns a `Page` of `UserAvailability`,
each carrying `id` and `availability`:

```python
for entry in client.user.get_availabilities():
    print(entry.id, entry.availability)
```

The documented values are `available`, `offline`, `do_not_disturb`, `in_call` and
`after_call_work`. It is typed as a plain `str` so a value Aircall adds later cannot
break parsing.

---

## 5. `dialer_campaign.get_phone_numbers()` returns data now

It read a `phone_numbers` key; Aircall sends `numbers`. It returned an empty list on
every call, with no error.

```python
# before: always []
# after: Page of DialerCampaignPhoneNumber
for entry in client.dialer_campaign.get_phone_numbers(456):
    print(entry.number, entry.called)
```

---

## 6. Model fields that became optional

Aircall abridges objects when they are nested inside other objects, so several
required fields could not stay required. These are now `Optional` and default to
`None`:

- `User.substatus`, `User.wrap_up_time`, `User.time_zone`, `User.language`
- `UserV2.substatus`
- `Message.external_number`

If you read these, add a `None` check. This is what made `call.get()` fail on
Aircall's own documented response payload.

---

## 7. Authentication signature

`api_id` and `api_token` are now optional keyword arguments so OAuth can be used
instead. **Existing positional and keyword calls are unaffected.**

```python
AircallClient("id", "token")                       # still works
AircallClient(api_id="id", api_token="token")      # still works
AircallClient(access_token="oauth_token")          # new
```

Supplying neither, or both schemes, now raises `ValueError` rather than building a
broken `Authorization` header.

---

## New in 2.0

Nothing here breaks existing code.

**Endpoints** — all 94 documented endpoints are now covered:

- `call.get_predicted_csat()`, `call.get_custom_summary_result()`
- Query params on `call.list_calls()`, `call.search()` and `call.get()`:
  `from`, `to`, `order`, `fetch_contact`, `fetch_short_urls`,
  `fetch_call_timeline`, `fetch_aiva_conv`
- `call.get_transcription(id, mode="realtime")` — replaces the deprecated
  `get_realtime_transcription()`, whose removal date has already passed
- `call.get_playbook_result(id, fetch_playbook=True)`
- `message.send_group_in_conversation()`, `message.send_group_skipping_inbox()`
- `message.send_whatsapp_in_conversation()`, `message.send_whatsapp_skipping_inbox()`
- `message.list_sms_templates()`, `message.list_whatsapp_templates()`,
  `message.get_whatsapp_status()`
- `client.ai_voice_agent.trigger_outbound_call()`
- `client.analytics.create_export()`, `client.analytics.get_export()`
- `client.ping()`

**Models** — `GroupMessage`, `SmsTemplate`, `WhatsAppLineStatus`, `AnalyticsExport`,
`OutboundCallRequest`, `CallAIVoiceAgent`. `Call` gained `ai_voice_agents` and
`automatic_callback_call_id`; `Number` gained `flow_editor_enabled`; `Playbook` is no
longer an empty stub.

All models are now importable from the top-level package:

```python
from aircall import Call, Page, AnalyticsExport   # previously aircall.models
```

---

## Surfacing the warnings

`DeprecationWarning` is hidden by default in Python. To see what you are still using:

```bash
python -W default::DeprecationWarning your_script.py
```

Or in pytest, add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
filterwarnings = ["default::DeprecationWarning"]
```
