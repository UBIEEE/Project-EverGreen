/**
 * Check if this request is affected by rate limit rules
 * 
 * Rules:
 * - Block IP on 50 req/10 sec
 * - Return 429 if blocked
 * - IP is blocked for 30 seconds
 * 
 * @param {HTTPRequest} r nginx HTTP Request object
 * @see https://nginx.org/en/docs/njs/reference.html#http
 */
function check(r) {


    r.return(429)
}

export default { check }
