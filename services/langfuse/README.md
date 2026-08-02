# Langfuse Deployment

## Starting up Langfuse service

- copy the .env.template to .env and provide the variables there
- compose up the compose file

## Langfuse Environment Variables

In the service you want to connect from you have to provide these variables

```.env
LANGFUSE_SECRET_KEY = "sk-lf-..."
LANGFUSE_PUBLIC_KEY = "pk-lf-..."
LANGFUSE_BASE_URL = "http://host.docker.internal:3001"
```

The keys you will get from a langfuse project.

## Connect to langfuse MCP server

The vscode config for langfuse MCP is

```json
{
    "servers": {
        "langfuse": {
            "type": "http",
            "url": "http://host.docker.internal:3001/api/public/mcp",
            "headers": {
                "Authorization": "Basic cGstbGYtNTM0MzRhO............DEtYzMwYS00NG"
            }
        }
    }
}
```

> Be aware...
>
> ...that the key for basic authentication is a base64 encoded public and secret key. You will get this also during generation of a new key for a langfuse project.

## Langfuse Skill

You can install also a langfuse skill in your project you are using langfuse

```bash
npx skills add langfuse/skills --skill "langfuse" --agent universal
```
