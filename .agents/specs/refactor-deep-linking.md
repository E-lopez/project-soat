## 1. User Stories

---

### GENERIC TEMPLATE

**As a** user  
**I want** to add a book with title, author, and status  
**So that** I can track my reading list

**Acceptance Criteria:**

- Title is required (1-500 chars)
- Author is required (1-200 chars)
- Status is optional, defaults to "unread"
- Valid statuses: unread, reading, completed
- System assigns unique ID and timestamp

---

### SACS-3646: AI Search | POC | Foundation | Gladly Bar Deep Routing Replacement

**As a** customer arriving from an external deep link  
**I want** article deep linking to be handled directly by the customer support site  
**So that** article URLs continue to work even after Gladly Bar routing logic is removed

**Acceptance Criteria:**

- When the current page URL contains a Gladly-style `?a=...--id-...` query string whose trailing identifier matches an entry in `src/main/js/common/hcLinks.js`, the site redirects the browser to that entry's `target`
- The redirect match is performed using the trailing identifier segment currently used by the frontend redirect logic, not by requiring the full source URL string to match exactly
- Existing externally indexed or shared Gladly-style article URLs that are represented in `hcLinks.js` remain valid through redirect behavior owned by the site
- A direct deep-link request can reach the site and resolve without requiring Gladly Bar to render the article route first
- When the current deep link does not match any `hcLinks.js` entry, the site does not perform an `hcLinks.js` redirect and control passes to the site-owned article rendering or not-found path
- If an article is not found because it is deprecated or its identifier changed, the system first checks for a matching redirect in `src/main/js/common/hcLinks.js`; if no redirect match exists, control falls back to the parent site, which displays its standard 404 not found page

**Notes:**

- Preserving existing URLs is critical because they are already used by search engines and external links
- In the current frontend implementation, `hcLinks.js` acts as a browser-side redirect map and `useGladlyHcLinks` performs immediate redirect behavior on mount when the trailing Gladly identifier matches
- This story establishes the routing foundation needed for later article rendering work

---

### SACS-3888: AI Search | Deep Linking Article Component

**As a** customer opening a deep-linked help article  
**I want** the article to render in a site-owned article page component  
**So that** I can read the linked help content directly without depending on the previous Gladly Bar rendering path

**Acceptance Criteria:**

- A new article page component is created under `src/main/js/pages/helpCenter/components`, following the existing help-center folder structure and component conventions
- The new component uses the same article data source and rendering pattern as `src/main/js/pages/helpCenter/components/columns/ColumnsMainComponent.vue` unless a documented spec update states otherwise
- When a valid deep-linked article identifier is provided and no `hcLinks.js` redirect applies, the requested article renders in the new page component
- Every deep-linked article identifier supported by the existing article retrieval flow renders in the new component
- The article page preserves the intended article-view context by displaying the requested article while not rendering a competing in-page article selection state
- When the requested article cannot be retrieved and no `hcLinks.js` redirect applies, the deep-link flow falls back to the parent site, which displays its standard 404 not found page

**Notes:**

- The goal is not to redesign article rendering, but to relocate deep-linked article display into a page flow owned by the site
- The new component should align with existing help-center conventions for reactive rendering and data retrieval

---

### SACS-3889: AI Search | Deep Linking Cleanup

**As a** customer using deep-linked support content  
**I want** the final deep-linking experience to behave the same as before from a tracking and navigation perspective  
**So that** the routing refactor does not change analytics behavior or leave obsolete Gladly search dependencies behind

**Acceptance Criteria:**

- Obsolete Gladly Search Bar dependencies that are no longer required by the final deep-linking flow are removed or isolated from the article page path
- The final deep-linking flow no longer depends on removed Gladly Search Bar behavior to function correctly
- A successful deep-linked article view triggers a `metrics.link` analytics event with `pageName: ''` and `linkName` formatted as `${adobeName}_${camelCase(articleName)}`, matching the current article flow implemented in `useArticleContent`
- A markdown document is produced at the project root summarizing the implemented deep-linking flow, including redirect behavior, article rendering behavior, and not-found behavior

**Notes:**

- This cleanup story should happen after the site-owned routing and article rendering path is working
- Analytics parity applies to externally visible tracking behavior even if internal implementation details change

## 3. Business Rules

### BR-001: Correct Deep Linking

**Given** the site is online  
**When** a user opens an external Gladly-style deep link  
**Then** the site must either redirect the request using the configured `hcLinks.js` mapping or render the requested article in the site-owned article page  
**And** if neither a redirect target nor a retrievable article exists, the deep-link flow must fall back to the parent site, which displays its standard 404 not found page  
**And** a successful deep-linked article view must emit a `metrics.link` event with `pageName: ''` and `linkName` formatted as `${adobeName}_${camelCase(articleName)}`, matching the current article flow implemented in `useArticleContent`

## 4. Data Model

## 5. API Contract

### GET /customer-support/help/all-articles

**Purpose:** Retrieve article data used by the help-center article-rendering experience when a deep link resolves to an article instead of an `hcLinks.js` redirect target.

**Query Parameters:**

- `articleIds` (optional): list of article IDs to retrieve when the client already knows the target article

**Success Response (200):**

```json
[
  {
    "bodyHtml": "<div>...</div>",
    "id": "string",
    "name": "string"
  }
]
```

**Behavior Notes:**

- The deep-linking refactor should reuse the existing article retrieval contract where possible rather than introduce a parallel article API without need
- The exact request shape should remain aligned with the endpoint family already used by the help-center article experience
- If `articleIds` is provided and a matching article is returned, the article page renders that article and emits the defined article-view analytics event
- If no matching article is returned, the deep-link flow must fall back to the parent site's standard 404 not found page unless an `hcLinks.js` redirect already matched earlier in the flow

## 6. Out of Scope (Phase 1)

- Redesigning the help-center information architecture or article taxonomy
- Changing externally visible article URLs
- Reworking analytics semantics beyond preserving existing deep-link behavior
- Replacing the broader Gladly content source as part of this refactor
- Rebuilding unrelated help-center browsing experiences that do not participate in deep linking

## 7. Decision Log

### DEC-001: Duplicate Handling

**Date:** [11/03/2026]
**Decision:** Add a not-found article
**Rationale:** There might be outdated articles around the web

### DEC-001: Analytics BAseline

**Date:** [11/03/2026]
**Decision:** Adds analytics references
**Rationale:** The spec does not provide context of the current prod analytics behaviour
