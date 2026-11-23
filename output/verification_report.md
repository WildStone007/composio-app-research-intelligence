# Verification report

- Sample size: 6
- Authentication signal overlaps: 3
- Non-overlaps: 3
- Signal overlap rate: 50.0%
- This is NOT an overall accuracy score.
- Six records were cross-checked against official documentation.

## Google Ads
- Expected authentication: OAuth2
- Agent authentication: unknown
- Signal overlap: No
- Finding: OAuth 2.0 plus a developer access model undergoing transition.
- Official source: https://developers.google.com/google-ads/api/rest/auth
- Secondary source: https://developers.google.com/google-ads/api/docs/api-policy/developer-token

## Zendesk
- Expected authentication: OAuth2, Basic, API token
- Agent authentication: OAuth2, API key, Basic, Bearer/token
- Signal overlap: Yes
- Finding: OAuth is recommended; legacy API-token and Basic authentication have migration considerations.
- Official source: https://developer.zendesk.com/api-reference/introduction/security-and-auth/
- Secondary source: https://developer.zendesk.com/documentation/authentication/api-tokens-to-oauth/

## Shopify
- Expected authentication: Access token
- Agent authentication: unknown
- Signal overlap: No
- Finding: Scoped access tokens authenticate API requests. REST Admin API is legacy; GraphQL is the preferred direction.
- Official source: https://shopify.dev/docs/api/usage/authentication
- Secondary source: https://shopify.dev/docs/api/admin-graphql

## Apify
- Expected authentication: API token
- Agent authentication: OAuth2, API key, Bearer/token
- Signal overlap: Yes
- Finding: Public REST API with secret API-token authentication.
- Official source: https://docs.apify.com/integrations/api
- Secondary source: https://docs.apify.com/api/v2

## Notion
- Expected authentication: API token, OAuth2
- Agent authentication: unknown
- Signal overlap: No
- Finding: Internal connections use API tokens; external integrations can use OAuth. Workspace permissions affect access.
- Official source: https://www.notion.com/help/create-integrations-with-the-notion-api
- Secondary source: https://developers.notion.com/reference/intro

## Plaid
- Expected authentication: Client ID, Secret, Access token
- Agent authentication: OAuth2, API key, Bearer/token
- Signal overlap: Yes
- Finding: Client ID and secret identify the developer application; access tokens authorize access to linked Items.
- Official source: https://plaid.com/docs/quickstart/
- Secondary source: https://plaid.com/docs/api/
