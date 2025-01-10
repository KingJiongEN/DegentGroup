# Degent Group Documentation

Welcome to the Degent Group documentation. Degent Group is an AI-powered chat system that integrates with Telegram and provides NFT creation, bargaining, and artwork generation capabilities.

## System Overview

```mermaid
graph TB
    subgraph Frontend
    TW[Twitter API]
    TG[Telegram Bot]
    BC[Blockchain API]
    end
    
    subgraph Application Layer
    AS[Agent Service]
    DS[Dialog Service]
    NS[NFT Service]
    WS[Wallet Service]
    MS[Memory Service]
    end
    
    subgraph AI Engine
    LLM[GPT-4]
    IM[Image Generator]
    end
    
    subgraph Storage
    DB[(Database)]
    Cache[(Redis)]
    IPFS[(IPFS)]
    Chain[Blockchain]
    end
    
    TW --> AS
    TG --> AS
    BC --> WS
    
    AS --> DS
    AS --> NS
    AS --> WS
    AS --> MS
    
    DS --> LLM
    NS --> IM
    NS --> IPFS
    
    DS --> Cache
    MS --> DB
    WS --> Chain
    NS --> Chain
```

## Key Features

- 🤖 Telegram Bot Integration
- 🎨 AI Artwork Generation
- 💰 NFT Creation and Trading
- 🤝 Automated Bargaining System
- 👥 Group Chat Management

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Basic Bot Tutorial](tutorials/basic-bot.md)
- [API Reference](api/telegram.md)
- [Examples](examples/basic.md)

## Support

For support, please [open an issue](https://github.com/KingJiongEN/DegentGroup/issues) on our GitHub repository. 