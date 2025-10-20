# OAuth2 Shield

A lightweight FastAPI-based reverse proxy that protects static content behind OAuth2/OIDC authentication. Perfect for securing documentation sites, internal dashboards, or any static content that needs access control.

## Features

- 🔒 **OAuth2/OIDC Authentication** - Secure your static content with industry-standard authentication
- 🌐 **Domain-based Authorization** - Restrict access to specific email domains
- 📁 **Static File Serving** - Seamlessly serve static content after authentication
- 🔄 **Session Management** - Persistent login sessions with secure session handling
- 🐳 **Docker Ready** - Containerized deployment with Poetry dependency management
- ⚡ **FastAPI Powered** - High-performance async web framework
- 🎨 **Customizable Templates** - Branded login and error pages [**WIP**]

## How It Works

OAuth2 Shield acts as a protective layer in front of your static content:

1. **Unauthenticated users** are redirected to the OAuth2 login flow
2. **Authentication** happens with your OAuth2 provider (Google, GitHub, etc.) 
3. **Domain validation** (optional) ensures only authorized email domains can access
4. **Authenticated users** can access the protected static content
5. **Session management** keeps users logged in across requests

## Quick Start

### Using Docker

```bash
# Clone the repository
git clone https://github.com/debonzi/oauth2-shield.git
cd oauth2-shield

# Set up your environment variables
cp .env.example .env  # Edit with your OAuth2 credentials

# Run with Docker
docker build -t oauth2-shield .
docker run -p 8000:8000 --env-file .env oauth2-shield
```

### Local Development

```bash
# Install dependencies with Poetry
poetry install

# Set up environment variables
export CLIENT_ID="your-oauth2-client-id"
export CLIENT_SECRET="your-oauth2-client-secret"
export SECRET_KEY="your-secret-key"
# ... other required variables

# Run the development server
poetry run fastapi dev oauth_shield/main.py
```

## Configuration

OAuth2 Shield is configured through environment variables:

### Required Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `CLIENT_ID` | OAuth2 client ID | `your-client-id.apps.googleusercontent.com` |
| `CLIENT_SECRET` | OAuth2 client secret | `your-client-secret` |
| `SECRET_KEY` | Session encryption key | `your-secure-random-key` |
| `AUTHORIZATION_BASE_URL` | OAuth2 authorization endpoint | `https://accounts.google.com/o/oauth2/auth` |
| `TOKEN_URL` | OAuth2 token endpoint | `https://oauth2.googleapis.com/token` |
| `KEYS_URL` | JWKS endpoint for token verification | `https://www.googleapis.com/oauth2/v3/certs` |

### Optional Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVICE_NAME` | Display name for your service | `OAuth Shield` |
| `DOMAIN` | Your domain name | `localhost:8000` |
| `ENVIRONMENT` | Deployment environment | `local` |
| `STATIC_PATH` | Path to static files directory | `site` |
| `AUTHORIZED_DOMAINS` | Comma-separated list of allowed email domains | (none - allows all) |
| `SCOPES` | OAuth2 scopes to request | `[]` |

### Domain Authorization

To restrict access to specific email domains:

```bash
export AUTHORIZED_DOMAINS="company.com,partner.org"
```

Only users with email addresses from these domains will be granted access.

## Project Structure

```
oauth2-shield/
├── oauth_shield/
│   ├── main.py          # FastAPI application entry point
│   ├── oauth2.py        # OAuth2 authentication logic
│   └── config.py        # Configuration settings
├── templates/
│   ├── login.html       # Custom login page
│   └── invalid_domain.html  # Domain restriction error page
├── site/                # Your static content goes here
│   └── index.html       # Example static file
├── Dockerfile           # Container configuration
└── pyproject.toml       # Python dependencies
```

## Customization

### Static Content

Place your static files in the `site/` directory. They will be served after authentication:

```
site/
├── index.html
├── assets/
│   ├── css/
│   └── js/
└── docs/
```

### Templates

Customize the login experience by editing templates in the `templates/` directory:

- `login.html` - OAuth2 login page
- `invalid_domain.html` - Shown when user's domain is not authorized

## OAuth2 Provider Setup

### Google OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth2 credentials
5. Set authorized redirect URI to: `https://yourdomain.com/__oauth/callback`

### GitHub OAuth2

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL to: `https://yourdomain.com/__oauth/callback`

## Deployment

### Production Considerations

- Use HTTPS in production (automatic when `ENVIRONMENT != "local"`)
- Set a strong `SECRET_KEY` for session encryption
- Configure `AUTHORIZED_DOMAINS` for access control
- Use environment-specific configuration files

### Environment Variables Example

```bash
# Production environment
export ENVIRONMENT="production"
export DOMAIN="myapp.company.com"
export CLIENT_ID="your-production-client-id"
export CLIENT_SECRET="your-production-client-secret"
export SECRET_KEY="your-production-secret-key"
export AUTHORIZED_DOMAINS="company.com"
```

## API Endpoints

OAuth2 Shield provides several internal endpoints:

- `/__oauth/login` - Initiate OAuth2 login flow
- `/__oauth/callback` - OAuth2 callback endpoint
- `/__oauth/logout` - End user session
- `/__oauth/invalid_domain` - Domain restriction error page
- `/` - Serves your protected static content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Daniel Debonzi** - [debonzi@gmail.com](mailto:debonzi@gmail.com)

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/debonzi/oauth2-shield/issues) on GitHub.