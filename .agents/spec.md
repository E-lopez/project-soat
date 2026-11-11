# Product Specification

## 1. Overview

**Problem Statement:** REI customers need a fast, self-service support experience that helps them resolve common questions and tasks without calling customer support. The current support journey spans help-center content, search, guided forms, order assistance, and AI-assisted answers, so the product must reduce friction across all of those paths while keeping the experience consistent, accurate, and trustworthy.

**Target Users:** REI customers seeking support online, including shoppers with general help-center questions, customers managing active orders, members requesting account-related updates, and users who prefer self-service before contacting an agent.

**Success Metrics:**
- Increase call deflection by resolving more support needs on the site without agent contact
- Reduce time-to-answer for common support questions through search, quick links, and AI-assisted retrieval
- Improve completion rates for guided support flows such as delivery issues, membership name changes, refund-status questions, and email/contact forms
- Maintain a reliable support experience with low error rates across SSR page loads, API-backed widgets, and form submissions

## 2. Product Context

The customer support site is an REI microsite built on Spring Boot and Vue. It combines server-rendered support pages with client-side interactive components, JSON endpoints, guided forms, and AI-assisted search experiences.

The product brings together several support journeys in one place:
- Help-center landing and category pages
- Gladly-backed article discovery and content retrieval
- AI/RAG-assisted question answering for self-service support
- Contact and escalation pathways such as chat, email, and delivery-issue reporting
- Logged-in order-help experiences, including active order visibility and tracking-oriented assistance
- Quick tools and curated support shortcuts for common customer needs

Gladly currently supplies help-center content and parts of the support-search/chat experience. The repo also contains newer AI and RAG-oriented functionality, including custom chat and retrieval-driven support features, which indicates an ongoing transition toward newer support-answering capabilities.

## 3. Core User Needs

### 3.1 Find trustworthy help content quickly
Customers should be able to find relevant help-center content with minimal effort, whether they start from the landing page, browse by help center or category, use quick tools, or search directly for an answer.

### 3.2 Resolve common issues without contacting support
The product should help users complete common support tasks on their own, including understanding order status, finding related articles, checking delivery-related guidance, and submitting structured requests when self-service content alone is not enough.

### 3.3 Escalate smoothly when self-service is insufficient
When the site cannot fully solve the issue, customers should have clear next steps such as chat, email, forms, or phone-based help. Escalation paths should feel connected to the self-service journey instead of forcing users to restart.

### 3.4 Support personalized and contextual experiences
For authenticated or context-aware journeys, the site should show relevant help options, order-related tools, page-specific analytics context, and feature-flagged content without exposing internal complexity to the user.

## 4. Primary Product Areas

### 4.1 Help Center Content Experience
This area includes the landing pages, category and article navigation, related links, popular topics, quick tools, and support-page layouts that help customers browse or drill down into answers.

### 4.2 AI and Search Experience
This area includes retrieval-augmented answers, custom chat/search behaviors, article search, and answer-ranking or source-preview experiences intended to shorten the path from question to answer.

### 4.3 Guided Support Forms
This area includes structured support flows such as delivery issues, price adjustments, membership name changes, refund-status workflows, and subscription/contact-related forms. These flows should collect only the information needed, validate input clearly, and support successful completion with minimal confusion.

### 4.4 Order Help and Account-Adjacent Support
This area includes active-order assistance, tracking-related information, order-help options, and member-facing support widgets or cards that depend on account/session context.

### 4.5 Support Channel Handoffs
This area includes chat, email, contact-us paths, and other escalation mechanisms that connect customers to human support when content, search, or forms do not fully resolve the issue.

## 5. Functional Expectations

- The site must support both server-rendered page delivery and client-side enhancement for interactive support experiences.
- Customers must be able to browse help content through landing pages, categories, and article relationships.
- The site must expose API-backed experiences for newer support widgets and JSON consumers where appropriate.
- Guided forms must validate user input clearly and provide actionable error feedback.
- Authenticated order-help experiences must remain scoped to the user's available session and account context.
- Analytics and metrics must capture meaningful page, click, and support-flow interactions so the team can measure call deflection and usage behavior.
- AI-assisted responses must remain connected to support content and should help users move toward resolution rather than generate unsupported answers in isolation.

## 6. Non-Functional Expectations

- The experience must feel fast and dependable for high-intent support traffic.
- Content, quick tools, forms, and support widgets must remain consistent across SSR and hydrated client behavior.
- The product should tolerate failures in external dependencies by degrading gracefully where possible, especially around article retrieval, AI dependencies, and third-party support integrations.
- Sensitive customer and operational data must be protected throughout support workflows.
- The architecture should allow support experiences to evolve incrementally without requiring a full rewrite of legacy and newer frontend patterns.

## 7. Constraints and Integration Notes

- The product is implemented as a Spring Boot + Vue microsite with page-based SSR entrypoints and client-side enhancement.
- The codebase contains both legacy Vue component patterns and newer typed composable-driven patterns, so new work must align with the surrounding feature area.
- Gladly is a key content and support integration today, but parts of the user experience are evolving toward newer AI-driven and custom-chat capabilities.
- Operational success depends not only on correctness, but also on customer containment and efficient routing away from unnecessary support contacts.

## 8. Product Intent Summary

The customer support site exists to help REI customers solve support needs quickly, confidently, and with as little human intervention as necessary. It should combine strong content discovery, guided self-service flows, personalized order-help experiences, and carefully integrated AI assistance to reduce support costs while improving the customer experience.

## 9. Project Commands

- Compile main sources: `mvn generate-sources compiler:compile -q`
- Compile test sources: `mvn resources:resources resources:testResources compiler:testCompile -q`
- Run Java unit tests: `mvn surefire:test -q`
- Run a specific Java test class: `mvn surefire:test -Dtest=<ClassName> -q`

**Notes:**
- Use `nvm use 20.15.0` before running any npm commands.
- `npm run lint` uses `eslint --ext .js --ext .vue --ext .mjs ./src/main/js` and may skip pure `.ts` files.
