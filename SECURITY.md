# 🔒 Security Policy

## Reporting Security Vulnerabilities

The security of this project is taken seriously. If you discover a security vulnerability, please follow these guidelines:

### ⚠️ DO NOT

- Open a public GitHub issue for security vulnerabilities
- Discuss the vulnerability publicly before it's fixed
- Exploit the vulnerability maliciously

### ✅ DO

1. **Email the maintainer** at: [security contact - update this]
2. **Include detailed information**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Wait for acknowledgment** before public disclosure
4. **Allow reasonable time** for fix implementation

## 🎯 Scope

### In Scope

This security policy covers:

- The web application (`src/main.py`)
- Docker configuration
- Dependencies and third-party libraries
- Deployment configurations
- Authentication/session management (if applicable)

### Out of Scope

The following are **intentionally insecure by design** (this is a CTF challenge):

- MD5 hash collision exploitation (this is the challenge!)
- Brainfuck code injection
- The flag reveal mechanism

**Note**: While these are intentionally vulnerable for educational purposes, please report if:
- They affect systems beyond the challenge scope
- They pose risk to infrastructure
- They enable unintended access

## 🛡️ Security Measures

### Current Protections

1. **Input Validation**
   - File size limits (1MB)
   - File type restrictions
   - Code validation before execution

2. **Resource Limits**
   - Memory allocation caps (30,000 cells)
   - Execution timeout protection
   - Request rate limiting (recommended in production)

3. **Container Isolation**
   - Docker containerization
   - Non-root user execution
   - Limited network access

4. **Dependency Management**
   - Regular dependency updates
   - Vulnerability scanning with `pip-audit`

### Recommended Production Settings

```python
# Rate limiting
@limiter.limit("10 per minute")
def upload_files():
    pass

# Secure headers
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-Frame-Options'] = 'DENY'
response.headers['Content-Security-Policy'] = "default-src 'self'"

# HTTPS enforcement
if not app.debug:
    Talisman(app, force_https=True)
```

## 🔍 Known Security Considerations

### 1. Brainfuck Interpreter

**Risk**: Potentially infinite loops
**Mitigation**: 
- Implement timeout mechanism
- Monitor resource usage
- Use Docker resource limits

```yaml
# compose.yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### 2. File Uploads

**Risk**: Malicious file uploads
**Mitigation**:
- Strict file size limits
- File type validation
- Content scanning
- Temporary file cleanup

### 3. MD5 Collisions (By Design)

**Risk**: This is the challenge!
**Note**: MD5 collision exploitation is the intended mechanic. This demonstrates real-world cryptographic vulnerabilities for educational purposes.

**Production Recommendation**: Never use MD5 for security purposes. Use SHA-256 or SHA-3 instead.

### 4. Flask Secret Key

**Risk**: Session hijacking if weak/default key
**Mitigation**:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
```

**Production**: Always use a strong, randomly generated secret key stored securely.

### 5. Information Disclosure

**Risk**: `/source` endpoint reveals implementation
**Mitigation**: This is intentional for transparency, but consider:
- Removing in production if not needed
- Ensuring no sensitive data in source
- Using environment variables for secrets

## 🔄 Update Policy

### Dependency Updates

We monitor and update dependencies regularly:

```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
uv lock --upgrade

# Test after updates
pytest
```

### Security Patches

- **Critical**: Patched within 24 hours
- **High**: Patched within 1 week
- **Medium**: Patched within 1 month
- **Low**: Addressed in next release

## 📋 Security Checklist for Deployment

Before deploying to production:

- [ ] Change default FLAG value
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS with valid certificate
- [ ] Configure rate limiting
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable security headers
- [ ] Configure proper CORS policies
- [ ] Set up monitoring and alerts
- [ ] Review and restrict file upload limits
- [ ] Implement proper logging (without sensitive data)
- [ ] Configure backup strategy
- [ ] Set up intrusion detection
- [ ] Review Docker security best practices
- [ ] Scan container images for vulnerabilities

## 🛠️ Security Tools

### Recommended Tools

1. **Dependency Scanning**
   ```bash
   pip-audit
   safety check
   ```

2. **Container Scanning**
   ```bash
   docker scan bf-md5-collision:latest
   trivy image bf-md5-collision:latest
   ```

3. **Web Security Testing**
   ```bash
   # OWASP ZAP
   docker run -t owasp/zap2docker-stable zap-baseline.py \
     -t https://collision.hacknroll.academy

   # Nikto
   nikto -h https://collision.hacknroll.academy
   ```

4. **Static Analysis**
   ```bash
   bandit -r src/
   ```

### Automated Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r src/
      
      - name: Scan Docker image
        run: |
          docker build -t bf-collision .
          docker scan bf-collision
```

## 🎓 Educational Context

This project is designed for security education and demonstrates:

- Real-world cryptographic vulnerabilities (MD5 collisions)
- Secure coding practices (despite the intentional vulnerability)
- Proper input validation
- Resource management
- Container security

**Important**: This challenge should only be deployed in controlled environments for educational purposes.

## 📞 Contact

For security concerns:
- **Email**: [Your security contact email]
- **PGP Key**: [Your PGP key fingerprint]
- **Response Time**: Within 48 hours

## 🏆 Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

| Date | Researcher | Vulnerability | Severity |
|------|-----------|---------------|----------|
| - | - | - | - |

*Your name could be here!*

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)

---

**Thank you for helping keep this project secure!** 🛡️

*Last Updated: December 2024*