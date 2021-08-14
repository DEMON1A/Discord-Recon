# Security Policy

## Supported Versions
- Just to keep you updated even if there's something wrong with the policy. only the latest two versions on discord-recon or supported here. if you're reporting security issues to versions lower than the latest two version it will only be accepted on rare cases.

- The current latest version is: 0.0.5, then only V0.0.4 and V0.0.5 are in-scope

## Reporting a Vulnerability
- If you think you have found a security issue on discord-recon. you can contact me via email about it: mdaif1332@gmail.com. or you can submit the issue on huntr platform, Don't submit security issues on public issue tracker like github again.

- After reporting any valid security issue, I will be creating an advisory for it and request a CVE via github, Make sure to accept the credits for the issue when you see an email.

## Known issues ( don't report ):
- Subjack errors discloses the server IP address - No impact, Not an issue
- Full path disclosure via dirsearch output - Low/None impact, Could be fixed later
- Denial of service by using subdomains command over again when it's done - I'm working on a rate limiting system
