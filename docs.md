
DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
System Architecture
Relevant source files
This document describes Mem0's three-tier architecture: the client layer (SDKs and APIs), the core memory system (orchestration and factories), and storage backends (vector stores, graph databases, and history tracking).

Architecture Overview
Mem0 employs a modular three-tier architecture that separates client interfaces, memory orchestration, and storage concerns. This design enables flexible deployment models (platform-hosted vs. self-hosted) while maintaining a consistent API surface across multiple programming languages.

The architecture is organized into:

Client Layer: Multiple access methods (Python SDK, TypeScript SDK, REST API, CLI, and framework integrations).
Core Memory System: Central orchestration via the Memory or AsyncMemory classes with factory-based component instantiation.
Storage Backends: Pluggable vector stores, graph databases, and history tracking.
System Components and Code Entities
The following diagram bridges natural language system concepts to their corresponding code entities within the repository.





















Sources: 
mem0/memory/main.py
15-41
 
mem0/utils/factory.py
30-41
 
mem0/configs/base.py
15-16
 
mem0/memory/storage.py
26-27

Client Layer
The client layer provides primary access patterns optimized for different deployment scenarios.

Python SDK
Self-hosted (OSS): The Memory 
mem0/memory/main.py
172-234
 and AsyncMemory 
mem0/memory/main.py
1140-1160
 classes provide full control over infrastructure. Users instantiate them with a MemoryConfig.
Platform API: The MemoryClient class communicates with Mem0's hosted API via REST.
TypeScript SDK and Integrations
The TypeScript SDK (mem0ai npm package) provides platform API access. Integrations like @mem0/vercel-ai-provider allow for memory-enhanced LLM calls by wrapping the memory layer into the Vercel AI SDK 
README.md
111-115

CLI
The mem0-cli package allows users to manage memories directly from the terminal using commands like mem0 add and mem0 search 
README.md
140-148

Sources: 
mem0/memory/main.py
172-234
 
README.md
100-148

Core Memory System
The Memory class is the central entry point for the Open Source version. It orchestrates the flow between LLMs, embedders, and storage backends.

Component Initialization
Upon initialization, the Memory class uses various factories to instantiate providers based on the MemoryConfig 
mem0/memory/main.py
173-234
:

Embedder: EmbedderFactory.create() creates instances like OpenAIEmbedding or HuggingFaceEmbedding 
mem0/utils/factory.py
139-165
Vector Store: VectorStoreFactory.create() initializes providers like Qdrant, Pinecone, or ChromaDB 
mem0/utils/factory.py
167-205
LLM: LlmFactory.create() sets up the language model for fact extraction and memory processing 
mem0/utils/factory.py
30-137
History: SQLiteManager is initialized to track memory changes and versioning 
mem0/memory/main.py
187
Memory Processing Pipeline (v3 Algorithm)
The latest memory algorithm focuses on a token-efficient, single-pass extraction process 
README.md
45-62



Sources: 
mem0/memory/main.py
281-384
 
README.md
56-60
 
mem0/configs/prompts.py
18-22

Component Factories
The factory pattern abstracts the complexity of supporting 60+ providers.

LlmFactory
The LlmFactory maps provider strings to implementation classes and their specific configurations 
mem0/utils/factory.py
37-56
 It supports providers including OpenAI, Anthropic, Groq, Ollama, and AWS Bedrock.

VectorStoreFactory
The VectorStoreFactory manages the instantiation of vector databases. Supported providers are defined in VectorStoreConfig 
mem0/vector_stores/configs.py
13-38

Category    Providers
Cloud/Managed    Pinecone, Upstash, MongoDB, Azure AI Search
Open Source    Qdrant, Chroma, Milvus, PGVector, Weaviate
Local/Embedded    FAISS, SQLite (via extensions)
Sources: 
mem0/utils/factory.py
167-205
 
mem0/vector_stores/configs.py
13-38

Storage Backends
Mem0 uses a multi-level storage approach:

Vector Storage: Stores high-dimensional embeddings of facts for semantic retrieval.
Graph Storage: Stores entities and relationships (e.g., User -- LIKES -- Python) to enable relational reasoning 
README.md
59
Relational Storage (SQLite): The SQLiteManager 
mem0/memory/storage.py
26
 stores the metadata, raw text, and history/audit trails for all memories.
Sources: 
mem0/memory/storage.py
26-100
 
mem0/memory/main.py
187-206

Configuration System
The configuration is managed via Pydantic models in mem0/configs/.

MemoryConfig: The top-level configuration object 
mem0/configs/base.py
15
VectorStoreConfig: Validates provider-specific settings and sets default paths (e.g., /tmp/qdrant) 
mem0/vector_stores/configs.py
6-67
Validation: The system uses model_validator to ensure that provider-specific configuration classes (like QdrantConfig or OpenAIConfig) are correctly instantiated 
mem0/vector_stores/configs.py
40-67
Sources: 
mem0/configs/base.py
15-16
 
mem0/vector_stores/configs.py
6-67

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
System Architecture
Architecture Overview
System Components and Code Entities
Client Layer
Python SDK
TypeScript SDK and Integrations
CLI
Core Memory System
Component Initialization
Memory Processing Pipeline (v3 Algorithm)
Component Factories
LlmFactory
VectorStoreFactory
Storage Backends
Configuration System
Ask Devin about mem0ai/mem0

Fast

System Architecture | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Installation and Setup
Relevant source files
This document covers the installation process and initial configuration for both the Python and TypeScript/JavaScript SDKs. It includes prerequisites, package installation, basic configuration, and quickstart examples to verify your setup.

Prerequisites
Python SDK Requirements
Python 3.10 or higher 
pyproject.toml
15
 
docs/open-source/python-quickstart.mdx
11
OpenAI API key (default provider for OSS mode) 
docs/open-source/python-quickstart.mdx
12
Dependencies: The core package requires qdrant-client, pydantic, openai, posthog, pytz, sqlalchemy, and protobuf 
pyproject.toml
16-24
TypeScript/JavaScript SDK Requirements
Node.js 18 or higher 
mem0-ts/package.json
130
npm, pnpm, or yarn package manager 
docs/llms.txt
17
 
mem0-ts/package.json
135
OpenAI API key (default provider) 
docs/llms.txt
92
Environment Variables
Both SDKs typically use environment variables for API credentials during local development:

export OPENAI_API_KEY="sk-..."  # Required for default OpenAI provider
Sources: 
docs/open-source/python-quickstart.mdx
14-18
 
docs/llms.txt
92

SDK Installation
Python SDK
The Python SDK is distributed as mem0ai on PyPI. It includes the Memory class for self-hosted deployments and MemoryClient for the hosted platform.

pip install mem0ai
For specific backends, you can install optional dependencies defined in pyproject.toml:

pip install "mem0ai[vector_stores]" (e.g., ChromaDB, Pinecone, Milvus) 
pyproject.toml
30-54
pip install "mem0ai[llms]" (e.g., Groq, Anthropic, Ollama) 
pyproject.toml
55-64
pip install "mem0ai[nlp]" (e.g., Spacy) 
pyproject.toml
27-29
Sources: 
pyproject.toml
5-7
 
pyproject.toml
26-74
 
docs/llms.txt
16

TypeScript/JavaScript SDK
The TypeScript SDK is available via npm and supports both CommonJS and ESM.

npm install mem0ai
The package provides distinct entry points:

Platform (Managed): import MemoryClient from "mem0ai" 
mem0-ts/package.json
19-23
 
docs/llms.txt
57
OSS (Self-hosted): import { Memory } from "mem0ai/oss" 
mem0-ts/package.json
24-28
 
docs/llms.txt
114
Sources: 
mem0-ts/package.json
2-7
 
docs/llms.txt
17
 
docs/llms.txt
57
 
docs/llms.txt
114

Installation Architecture
The following diagram bridges the Natural Language concepts to the Code Entities involved during the installation and initialization phase.

Installation and Component Loading Flow

















Sources: 
pyproject.toml
6-7
 
mem0/utils/factory.py
30-167
 
mem0-ts/package.json
2-29
 
docs/llms.txt
16-19

Default Configuration
By default, the Memory() class (OSS) initializes with a specific stack optimized for local development.

Default OSS Stack








Component    Default Implementation    Configuration Key
LLM    OpenAI gpt-4o-mini    llm 
docs/open-source/python-quickstart.mdx
82
Embedder    OpenAI text-embedding-3-small (1536 dim)    embedder 
docs/open-source/python-quickstart.mdx
83
Vector Store    Qdrant (Local path: /tmp/qdrant)    vector_store 
docs/open-source/python-quickstart.mdx
84
 
mem0/vector_stores/configs.py
64
History    SQLite (Path: ~/.mem0/history.db)    history_db_path 
docs/open-source/python-quickstart.mdx
85
Sources: 
docs/open-source/python-quickstart.mdx
80-87
 
mem0/vector_stores/configs.py
7-67

Basic Configuration Examples
Python OSS Mode (Custom Provider)
To use a custom setup (e.g., Ollama), pass a configuration dictionary. The LlmFactory and EmbedderFactory will resolve the providers dynamically.

from mem0 import Memory
 
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "fitness_companion",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "ollama_base_url": "http://localhost:11434",
        },
    },
}
 
memory = Memory.from_config(config)
Sources: 
mem0/utils/factory.py
37-56
 
mem0/vector_stores/configs.py
13-38
 
docs/open-source/python-quickstart.mdx
21-22

Python Platform Mode
The MemoryClient initializes by pinging the API and setting up telemetry identifiers.

from mem0 import MemoryClient
 
client = MemoryClient(api_key="your-api-key")
Sources: 
docs/llms.txt
30-32
 
mem0-ts/src/client/mem0.ts
102-122

Quickstart Examples
Python Quickstart (OSS)
from mem0 import Memory
 
m = Memory()
 
# Add a memory - triggers fact extraction via LLM
m.add("Alex loves basketball.", user_id="alex")
 
# Search memories - performs vector search
results = m.search("What does Alex like?", user_id="alex")
Sources: 
docs/open-source/python-quickstart.mdx
34-57

TypeScript Quickstart (Platform)
import MemoryClient from "mem0ai";
 
const client = new MemoryClient({ apiKey: "your-api-key" });
 
// Add a memory
await client.add(
  [{ role: "user", content: "I love hiking" }],
  { userId: "alice" }
);
Sources: 
docs/llms.txt
60-71
 
mem0-ts/src/client/mem0.ts
251-254

Common Installation Issues
Dimension Mismatch
If using a custom model with dimensions other than 1536 (e.g., 768), you must update the vector store config to avoid alignment errors. Solution: Add "embedding_model_dims": 768 to the vector_store.config.

Sources: 
docs/components/vectordbs/overview.mdx
47-53

Dependency Management
For local development, the repository uses hatch as the build backend.

hatch env create: Sets up the development environment with all features 
Makefile
10-11
hatch run test: Runs the pytest suite 
Makefile
42-43
Sources: 
pyproject.toml
1-3
 
Makefile
1-53

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Installation and Setup
Prerequisites
Python SDK Requirements
TypeScript/JavaScript SDK Requirements
Environment Variables
SDK Installation
Python SDK
TypeScript/JavaScript SDK
Installation Architecture
Installation and Component Loading Flow
Default Configuration
Default OSS Stack
Basic Configuration Examples
Python OSS Mode (Custom Provider)
Python Platform Mode
Quickstart Examples
Python Quickstart (OSS)
TypeScript Quickstart (Platform)
Common Installation Issues
Dimension Mismatch
Dependency Management
Ask Devin about mem0ai/mem0

Fast

Installation and Setup | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Deployment Models
Relevant source files
Mem0 offers two deployment models that serve different operational requirements: Platform (fully managed) and Open Source (self-hosted). This page compares their architectures, trade-offs, and selection criteria to help you choose the appropriate model for your workload.

Architecture Overview
Mem0's dual deployment model separates infrastructure management from memory functionality. Both paths implement the same memory operations but differ in how they provision and scale the underlying services.

Platform Architecture (Managed Service)
The Platform deployment uses MemoryClient to communicate with Mem0's hosted API at api.mem0.ai. Authentication is handled via an API key. The managed infrastructure handles vector storage, graph databases, LLM orchestration, and advanced features like webhooks and custom categories server-side.



















Sources: 
mem0/client/main.py
62-127
 
docs/llms.txt
7-11
 
docs/platform/overview.mdx
7-15
 
docs/core-concepts/memory-operations/add.mdx
57-74

Open Source Architecture (Self-Hosted)
The OSS deployment instantiates the Memory class directly in your process. You are responsible for configuring the LLM, embedder, and vector store. By default, it uses OpenAI for LLM/embeddings and a local Qdrant instance for storage.













Sources: 
docs/open-source/python-quickstart.mdx
80-87
 
docs/llms.txt
85-108
 
docs/open-source/overview.mdx
1-10

Deployment Comparison
Feature Parity Matrix
Capability    Platform (Managed)    Open Source (OSS)    Implementation Details
Fact Extraction    ✅    ✅    Uses LLM to extract facts from messages 
docs/core-concepts/memory-operations/add.mdx
40-42
Conflict Resolution    ✅    ✅    Checks existing memories for duplicates/contradictions 
docs/core-concepts/memory-operations/add.mdx
43-45
Graph Memory    ✅    ✅    Supports Neo4j, Kuzu, Neptune, etc. 
docs/platform/features/platform-overview.mdx
24-25
Async Support    ✅    ✅    AsyncMemoryClient (Platform) vs AsyncMemory (OSS) 
docs/llms.txt
170-171
Webhooks    ✅    ❌    Platform-only event notification system 
docs/llms.txt
103-107
Custom Categories    ✅    ❌    AI-assigned categorization defined at project level 
docs/cookbooks/essentials/building-ai-companion.mdx
185-195
Batch Deletion    ✅    ❌    batch_delete for up to 1000 memories 
docs/core-concepts/memory-operations/delete.mdx
22-23
History Tracking    Managed    Local SQLite    OSS stores history at ~/.mem0/history.db 
docs/open-source/python-quickstart.mdx
85
Sources: 
docs/llms.txt
7-12
 
docs/core-concepts/memory-operations/add.mdx
170-177
 
docs/open-source/python-quickstart.mdx
80-87
 
docs/core-concepts/memory-operations/delete.mdx
10-24

Client Code Comparison
The SDK provides distinct entry points for each model. MemoryClient targets the hosted API, while Memory runs the logic locally.

Platform (Managed):

from mem0 import MemoryClient
 
# Authenticates with api.mem0.ai using API Key
client = MemoryClient(api_key="your-api-key")
client.add([{"role": "user", "content": "I am a vegetarian"}], user_id="user123")
Open Source (Self-Hosted):

from mem0 import Memory
 
# Runs locally; requires provider API keys (e.g., OPENAI_API_KEY)
m = Memory() 
m.add("I am a vegetarian", user_id="user123")
Sources: 
mem0/client/main.py
75-127
 
docs/llms.txt
25-51
 
docs/llms.txt
85-108

Decision Matrix
When to Use Platform (Managed)
Choose Platform if:

Zero Infrastructure: You want to avoid managing vector databases, graph stores, and scaling 
docs/platform/overview.mdx
22-23
Advanced Features: You need managed rerankers, webhooks, or AI-driven custom categories 
docs/llms.txt
7-8
Enterprise Controls: You require SOC 2 Type II compliance, audit logs, and organization-level governance 
docs/platform/overview.mdx
25
Performance: You need sub-50ms retrieval optimized by the Mem0 team 
docs/llms.txt
23
When to Use Open Source (Self-Hosted)
Choose Open Source if:

Data Privacy: You must keep all data within your own infrastructure or VPC 
docs/llms.txt
23
Local Models: You want to use local LLMs (via Ollama) or specific open-source vector stores 
docs/cookbooks/essentials/building-ai-companion.mdx
16-17
Full Customization: You need to modify the extraction prompts or internal memory logic 
docs/open-source/overview.mdx
160-161
Cost Sensitivity: You have extremely high volume where managed API costs exceed self-hosting infrastructure costs.
Sources: 
docs/llms.txt
21-24
 
docs/platform/overview.mdx
20-27
 
docs/cookbooks/essentials/building-ai-companion.mdx
86-120

Technical Implementation Details
Platform Validation Flow
When MemoryClient is initialized, it validates the API key against the /v1/ping/ endpoint to retrieve organization and project context.



Sources: 
mem0/client/main.py
105-154

OSS Component Defaults
The OSS Memory class defaults to a stack that allows immediate usage with an OpenAI API key.

Component    Default Provider    Configuration 
docs/open-source/python-quickstart.mdx
80-87
LLM    OpenAI    gpt-4o-mini for fact extraction
Embedder    OpenAI    text-embedding-3-small (1536 dims)
Vector Store    Qdrant    Local storage at /tmp/qdrant
History    SQLite    Local DB at ~/.mem0/history.db
Sources: 
docs/open-source/python-quickstart.mdx
80-87
 
mem0/client/main.py
29-30

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Deployment Models
Architecture Overview
Platform Architecture (Managed Service)
Open Source Architecture (Self-Hosted)
Deployment Comparison
Feature Parity Matrix
Client Code Comparison
Decision Matrix
When to Use Platform (Managed)
When to Use Open Source (Self-Hosted)
Technical Implementation Details
Platform Validation Flow
OSS Component Defaults
Ask Devin about mem0ai/mem0

Fast

Deployment Models | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Factory Pattern and Component System
Relevant source files
Purpose and Scope
This document describes Mem0's factory pattern implementation, which provides a centralized mechanism for instantiating and configuring AI model providers, vector stores, graph stores, and rerankers. The factory system enables runtime provider selection, type-safe configuration, and extensibility without modifying core code.

For information about the available providers and their capabilities, see Provider Ecosystem. For configuration validation and precedence rules, see Configuration System.

Overview
Mem0's factory pattern addresses the challenge of supporting 60+ provider integrations across five component types (LLMs, embedders, vector stores, graph stores, and rerankers) while maintaining clean separation of concerns. Each factory maintains a registry mapping provider names to implementation classes, enabling dynamic instantiation without tight coupling.

The factory system provides:

Runtime provider selection: Switch providers via configuration without code changes.
Type-safe configuration: Provider-specific config classes with Pydantic validation 
mem0/vector_stores/configs.py
6-67
Dynamic class loading: Lazy import of provider implementations to minimize dependencies 
mem0/utils/factory.py
24-27
Extensibility: Register new providers without modifying factory code 
mem0/utils/factory.py
115-126
Component Architecture: Code Entity Space
This diagram maps the high-level system components to their specific code identifiers and file locations.























Sources: 
mem0/utils/factory.py
1-284
 
mem0/vector_stores/configs.py
6-67

Factory Classes
Mem0 implements five factory classes in Python and equivalent factories in TypeScript for the OSS version.

LlmFactory
The LlmFactory creates Large Language Model instances with provider-specific configurations 
mem0/utils/factory.py
30-56
 It supports both legacy BaseLlmConfig and modern provider-specific config classes.

Provider    Class Path    Config Class
openai    mem0.llms.openai.OpenAILLM    OpenAIConfig
anthropic    mem0.llms.anthropic.AnthropicLLM    AnthropicConfig
azure_openai    mem0.llms.azure_openai.AzureOpenAILLM    AzureOpenAIConfig
ollama    mem0.llms.ollama.OllamaLLM    OllamaConfig
deepseek    mem0.llms.deepseek.DeepSeekLLM    DeepSeekConfig
lmstudio    mem0.llms.lmstudio.LMStudioLLM    LMStudioConfig
vllm    mem0.llms.vllm.VllmLLM    VllmConfig
groq    mem0.llms.groq.GroqLLM    BaseLlmConfig
Key Methods:

create(provider_name, config, **kwargs): Instantiate LLM with configuration 
mem0/utils/factory.py
59-112
register_provider(name, class_path, config_class): Add new LLM provider 
mem0/utils/factory.py
115-126
get_supported_providers(): List available providers 
mem0/utils/factory.py
129-136
Sources: 
mem0/utils/factory.py
30-137
 
mem0-ts/src/oss/src/utils/factory.ts
62-92

EmbedderFactory
The EmbedderFactory creates embedding model instances. It handles a special case for upstash_vector which can use built-in embeddings via MockEmbeddings 
mem0/utils/factory.py
156-157

Provider    Class Path
openai    mem0.embeddings.openai.OpenAIEmbedding
huggingface    mem0.embeddings.huggingface.HuggingFaceEmbedding
fastembed    mem0.embeddings.fastembed.FastEmbedEmbedding
gemini    mem0.embeddings.gemini.GoogleGenAIEmbedding
vertexai    mem0.embeddings.vertexai.VertexAIEmbedding
Sources: 
mem0/utils/factory.py
139-165
 
mem0-ts/src/oss/src/utils/factory.ts
40-60

VectorStoreFactory
The VectorStoreFactory creates vector database clients. In the Python implementation, it uses a dynamic lookup from VectorStoreConfig to validate provider-specific settings 
mem0/vector_stores/configs.py
41-67



Key Providers: qdrant, chroma, pgvector, pinecone, mongodb, milvus, redis, valkey, elasticsearch, opensearch, supabase, weaviate, faiss, azure_ai_search, databricks, upstash_vector 
mem0/vector_stores/configs.py
13-38

Sources: 
mem0/utils/factory.py
167-206
 
mem0/vector_stores/configs.py
6-67
 
mem0-ts/src/oss/src/utils/factory.ts
94-117

GraphStoreFactory and RerankerFactory
GraphStoreFactory: Creates graph clients like MemoryGraph for memgraph, kuzu, or neptune 
mem0/utils/factory.py
208-230
RerankerFactory: Creates rerankers (e.g., CohereReranker, LLMReranker) using a pattern identical to LlmFactory 
mem0/utils/factory.py
232-284
Sources: 
mem0/utils/factory.py
208-284

Dynamic Class Loading
The load_class() function enables lazy loading of provider implementations, which is critical given the extensive list of optional dependencies in pyproject.toml 
pyproject.toml
26-74

def load_class(class_type):
    module_path, class_name = class_type.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
Sources: 
mem0/utils/factory.py
24-27

Configuration Flow and Validation
The system ensures that raw dictionary inputs from users are converted into validated Pydantic models before being passed to component constructors.

Initialization Flow: Natural Language to Code Entity
This diagram illustrates how a user's configuration string or dictionary is transformed into a live code object.











Validation Steps:

Dictionary Merging: If a dictionary is provided, it is merged with **kwargs 
mem0/utils/factory.py
84-87
Type Conversion: If a BaseLlmConfig is provided but the provider requires a specific class (e.g., OpenAIConfig), the factory automatically maps common fields (model, api_key, temperature, etc.) to the new instance 
mem0/utils/factory.py
88-104
Pydantic Enforcement: The final config class (e.g., VectorStoreConfig) validates fields like path, host, and api_key 
mem0/vector_stores/configs.py
41-67
Sources: 
mem0/utils/factory.py
80-112
 
mem0/vector_stores/configs.py
41-67

TypeScript Implementation
The TypeScript OSS implementation (mem0-ts/src/oss) follows a similar factory pattern but uses static switch statements rather than dynamic imports for provider resolution 
mem0-ts/src/oss/src/utils/factory.ts
1-136

Factories in TS:

EmbedderFactory: Supports openai, ollama, google, azure_openai, langchain 
mem0-ts/src/oss/src/utils/factory.ts
40-60
LLMFactory: Supports openai, anthropic, groq, mistral, deepseek, etc 
mem0-ts/src/oss/src/utils/factory.ts
62-92
VectorStoreFactory: Supports memory, qdrant, redis, vectorize, pgvector, etc 
mem0-ts/src/oss/src/utils/factory.ts
94-117
HistoryManagerFactory: Manages SQLiteManager, SupabaseHistoryManager, and MemoryHistoryManager 
mem0-ts/src/oss/src/utils/factory.ts
119-136
Sources: 
mem0-ts/src/oss/src/utils/factory.ts
1-137

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Factory Pattern and Component System
Purpose and Scope
Overview
Component Architecture: Code Entity Space
Factory Classes
LlmFactory
EmbedderFactory
VectorStoreFactory
GraphStoreFactory and RerankerFactory
Dynamic Class Loading
Configuration Flow and Validation
Initialization Flow: Natural Language to Code Entity
TypeScript Implementation
Ask Devin about mem0ai/mem0

Fast

Factory Pattern and Component System | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Provider Ecosystem
Relevant source files
This document catalogs all supported providers across the component types in mem0: LLMs, vector stores, embedders, graph stores, and rerankers. It explains the factory-based selection mechanism and how providers are dynamically instantiated through string identifiers.

For information about the factory pattern implementation, see Factory Pattern and Component System. For configuration details, see Configuration System.

Factory System Overview
Mem0 uses five factory classes to abstract provider selection and instantiation. Each factory maintains a registry mapping string identifiers to implementation classes and their configuration types.

Provider Selection Flow












Sources: 
mem0/utils/factory.py
1-284
 
mem0/llms/openai.py
14-150

The factory system operates in three phases:

Registry Lookup: Maps provider string (e.g., "openai") to tuple of (class_path, config_class) 
mem0/utils/factory.py
37-56
Class Loading: Dynamically imports the provider class using importlib via the load_class helper 
mem0/utils/factory.py
24-27
Instantiation: Validates configuration against provider-specific config class and instantiates the provider instance 
mem0/utils/factory.py
81-112
Factory Classes and Their Registries

Factory Class    Purpose    Method    Registry Location
LlmFactory    LLM provider instantiation    create()    
mem0/utils/factory.py
37-56
EmbedderFactory    Embedding model instantiation    create()    
mem0/utils/factory.py
140-152
VectorStoreFactory    Vector database instantiation    create()    
mem0/utils/factory.py
168-192
GraphStoreFactory    Graph database instantiation    create()    
mem0/utils/factory.py
217-223
RerankerFactory    Reranker instantiation    create()    
mem0/utils/factory.py
242-248
Sources: 
mem0/utils/factory.py
24-284

LLM Providers
The LlmFactory supports 18+ LLM providers through the provider_to_class registry. Each provider maps to an implementation in mem0/llms/ and a configuration class.

LLM Provider Registry
















Sources: 
mem0/utils/factory.py
37-56
 
mem0/llms/openai.py
14-36
 
mem0/llms/ollama.py
15-41
 
mem0/llms/aws_bedrock.py
34-76

Complete LLM Provider List

Provider String    Implementation Class    Config Class    Module Path
openai    OpenAILLM    OpenAIConfig    
mem0/utils/factory.py
39
anthropic    AnthropicLLM    AnthropicConfig    
mem0/utils/factory.py
46
azure_openai    AzureOpenAILLM    AzureOpenAIConfig    
mem0/utils/factory.py
44
ollama    OllamaLLM    OllamaConfig    
mem0/utils/factory.py
38
groq    GroqLLM    BaseLlmConfig    
mem0/utils/factory.py
40
together    TogetherLLM    BaseLlmConfig    
mem0/utils/factory.py
41
aws_bedrock    AWSBedrockLLM    AWSBedrockConfig    
mem0/utils/factory.py
42
litellm    LiteLLM    BaseLlmConfig    
mem0/utils/factory.py
43
openai_structured    OpenAIStructuredLLM    OpenAIConfig    
mem0/utils/factory.py
45
azure_openai_structured    AzureOpenAIStructuredLLM    AzureOpenAIConfig    
mem0/utils/factory.py
47
gemini    GeminiLLM    BaseLlmConfig    
mem0/utils/factory.py
48
deepseek    DeepSeekLLM    DeepSeekConfig    
mem0/utils/factory.py
49
minimax    MiniMaxLLM    MinimaxConfig    
mem0/utils/factory.py
50
xai    XAILLM    BaseLlmConfig    
mem0/utils/factory.py
51
sarvam    SarvamLLM    BaseLlmConfig    
mem0/utils/factory.py
52
lmstudio    LMStudioLLM    LMStudioConfig    
mem0/utils/factory.py
53
vllm    VllmLLM    VllmConfig    
mem0/utils/factory.py
54
langchain    LangchainLLM    BaseLlmConfig    
mem0/utils/factory.py
55
Sources: 
mem0/utils/factory.py
37-56
 
mem0/llms/configs.py
12-32
 
docs/components/llms/overview.mdx
22-39

Vector Store Providers
The VectorStoreFactory supports 24+ vector database providers. The configuration is validated through the VectorStoreConfig Pydantic model.

Vector Store Provider Registry


















Sources: 
mem0/utils/factory.py
168-192
 
mem0/vector_stores/configs.py
13-38

Embedder Providers
The EmbedderFactory supports 11 embedding model providers. Embedders generate vector representations for semantic search.

Complete Embedder Provider List

Provider String    Implementation Class    Default Model    Module Path
openai    OpenAIEmbedding    text-embedding-3-small    
mem0/embeddings/openai.py
11
ollama    OllamaEmbedding    nomic-embed-text    
mem0/utils/factory.py
142
huggingface    HuggingFaceEmbedding    multi-qa-MiniLM-L6-cos-v1    
mem0/embeddings/huggingface.py
15
azure_openai    AzureOpenAIEmbedding    -    
mem0/utils/factory.py
144
gemini    GoogleGenAIEmbedding    models/text-embedding-004    
mem0/utils/factory.py
145
vertexai    VertexAIEmbedding    -    
mem0/utils/factory.py
146
together    TogetherEmbedding    -    
mem0/utils/factory.py
147
lmstudio    LMStudioEmbedding    -    
mem0/utils/factory.py
148
langchain    LangchainEmbedding    -    
mem0/utils/factory.py
149
aws_bedrock    AWSBedrockEmbedding    -    
mem0/utils/factory.py
150
fastembed    FastEmbedEmbedding    -    
mem0/utils/factory.py
151
Sources: 
mem0/utils/factory.py
140-152
 
mem0/embeddings/huggingface.py
15-45
 
mem0/configs/embeddings/base.py
10-111
 
mem0/embeddings/openai.py
11-35

Graph Store Providers
The GraphStoreFactory supports 5 graph database providers for entity-relationship storage.

Provider String    Implementation Class    Graph Technology
default    MemoryGraph    Neo4j
memgraph    MemoryGraph    Memgraph
neptune    MemoryGraph    AWS Neptune (Graph)
neptunedb    MemoryGraph    AWS Neptune (DB)
kuzu    MemoryGraph    Kuzu
Sources: 
mem0/utils/factory.py
214-231

Reranker Providers
The RerankerFactory supports 5 reranking providers for improving search result quality.

Provider String    Implementation Class    Config Class
cohere    CohereReranker    CohereRerankerConfig
sentence_transformer    SentenceTransformerReranker    SentenceTransformerRerankerConfig
zero_entropy    ZeroEntropyReranker    ZeroEntropyRerankerConfig
llm_reranker    LLMReranker    LLMRerankerConfig
huggingface    HuggingFaceReranker    HuggingFaceRerankerConfig
Sources: 
mem0/utils/factory.py
239-284

Optional Dependencies
Provider dependencies are organized into optional groups in pyproject.toml, allowing minimal core installations.

Dependency Group Structure











Sources: 
pyproject.toml
26-74

Dependency Groups Summary

Group    Install Command    Key Providers
vector_stores    pip install mem0ai[vector_stores]    Chroma, Pinecone, Milvus, Redis, Elasticsearch, PGVector, etc. 
pyproject.toml
30-54
llms    pip install mem0ai[llms]    Groq, Together, LiteLLM, Ollama, VertexAI, Gemini 
pyproject.toml
55-64
extras    pip install mem0ai[extras]    Boto3, Langchain, Sentence-Transformers, FastEmbed 
pyproject.toml
65-74
Sources: 
pyproject.toml
26-74
 
Makefile
13-16

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Provider Ecosystem
Factory System Overview
LLM Providers
Vector Store Providers
Embedder Providers
Graph Store Providers
Reranker Providers
Optional Dependencies
Ask Devin about mem0ai/mem0

Fast

Provider Ecosystem | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Configuration System
Relevant source files
The Configuration System in mem0 manages the initialization and validation of component settings across LLMs, embedders, vector stores, graph stores, and rerankers. It implements a provider-based architecture where users specify which provider to use (e.g., "openai", "anthropic") along with provider-specific parameters, and the system validates and instantiates the appropriate implementation.

Configuration Structure
The configuration system is organized hierarchically with a top-level MemoryConfig that contains nested configurations for each component type. Both Python and TypeScript implementations follow similar patterns but with language-specific conventions.

Python Configuration Schema














Python Configuration Classes The Python implementation utilizes Pydantic BaseModel for schema definition and validation.

MemoryConfig: The root configuration class containing all component settings 
mem0/configs/base.py
29-57
LlmConfig: Handles the provider string and a configuration dictionary for the LLM 
mem0/llms/configs.py
6-35
EmbedderConfig: Handles the provider string and a configuration dictionary for the embedder 
mem0/embeddings/configs.py
6-32
VectorStoreConfig: Handles the provider and dynamic loading of provider-specific config classes 
mem0/vector_stores/configs.py
10-67
Sources: 
mem0/configs/base.py
29-57
 
mem0/llms/configs.py
6-35
 
mem0/embeddings/configs.py
6-32
 
mem0/vector_stores/configs.py
10-67

TypeScript Configuration Schema













TypeScript Configuration Types The TypeScript implementation uses Zod for runtime validation and interfaces for type safety.

MemoryConfigSchema: A Zod object used to validate the merged configuration 
mem0-ts/src/oss/src/types/index.ts
101-145
MemoryConfig: Interface defining the structure of the memory configuration 
mem0-ts/src/oss/src/types/index.ts
54-72
LLMConfig: Interface for LLM-specific parameters like apiKey, model, and baseURL 
mem0-ts/src/oss/src/types/index.ts
43-52
VectorStoreConfig: Interface for vector store parameters, allowing passthrough fields for provider-specific options 
mem0-ts/src/oss/src/types/index.ts
24-31
Sources: 
mem0-ts/src/oss/src/types/index.ts
15-145

Configuration Precedence Rules
Configuration values are resolved using a multi-tier precedence system. Values specified explicitly in the configuration object override defaults and environment variables.

Precedence Hierarchy
Priority    Source    Implementation Detail
1 (Highest)    Explicit config dict/object    Passed to constructor or from_config
2 (Medium)    Environment variables    Resolved in provider __init__ or ConfigManager
3 (Lowest)    Default values    Defined in BaseLlmConfig or DEFAULT_MEMORY_CONFIG
Python Precedence Implementation In Python, environment variable resolution typically happens within the provider's __init__ method. For example, in OpenAIStructuredLLM, the API key is resolved by checking the config first, then the environment 
mem0/llms/openai_structured.py
17-18

TypeScript Precedence Implementation The ConfigManager.mergeConfig method explicitly merges user-provided partial configurations with DEFAULT_MEMORY_CONFIG 
mem0-ts/src/oss/src/config/manager.ts
5-163
 It also handles key normalization (e.g., mapping lmstudio_base_url or url to baseURL) to maintain compatibility with Python SDK configs 
mem0-ts/src/oss/src/config/manager.ts
24-29

Sources: 
mem0/llms/openai_structured.py
17-18
 
mem0-ts/src/oss/src/config/manager.ts
5-163
 
mem0-ts/src/oss/src/config/defaults.ts
3-35

Environment Variable Resolution
The system recognizes various environment variables to facilitate zero-config or secret-management-friendly setups.

Component    Environment Variable    File Reference
Telemetry    MEM0_TELEMETRY    
mem0/memory/telemetry.py
14
Telemetry    MEM0_TELEMETRY_SAMPLE_RATE    
mem0/memory/telemetry.py
47
Storage Dir    MEM0_DIR    
mem0/configs/base.py
13
OpenAI LLM    OPENAI_API_KEY    
mem0/llms/openai_structured.py
17
OpenAI Base    OPENAI_API_BASE    
mem0/llms/openai_structured.py
18
Sources: 
mem0/memory/telemetry.py
14-47
 
mem0/configs/base.py
11-13
 
mem0/llms/openai_structured.py
17-18

Configuration Validation and Factories
TypeScript Configuration Merging
The ConfigManager in the TypeScript SDK performs complex merging logic for sub-components:

Vector Store Dimension: It prioritizes user-provided dimensions, then falls back to embedder configuration dimensions, or leaves it undefined for auto-detection during initialization 
mem0-ts/src/oss/src/config/manager.ts
66-69
History Store: Merges top-level historyDbPath with historyStore.config while ensuring SQLite-specific paths are correctly mapped 
mem0-ts/src/oss/src/config/manager.ts
136-155
Validation: Calls MemoryConfigSchema.parse(mergedConfig) as the final step 
mem0-ts/src/oss/src/config/manager.ts
161
Component Factories
Once validated, configurations are passed to factories that instantiate the specific provider classes.













Sources: 
mem0-ts/src/oss/src/config/manager.ts
5-163
 
mem0-ts/src/oss/src/utils/factory.ts
40-136

Base Configuration Classes
BaseLlmConfig (Python)
The BaseLlmConfig class serves as the foundation for all LLM providers, containing parameters common across the ecosystem 
mem0/configs/llms/base.py
7-28

Parameter    Type    Default    Purpose
model    Optional[Union[str, Dict]]    None    Model identifier 
mem0/configs/llms/base.py
18
temperature    float    0.1    Output randomness 
mem0/configs/llms/base.py
19
max_tokens    int    2000    Generation limit 
mem0/configs/llms/base.py
21
top_p    float    0.1    Nucleus sampling 
mem0/configs/llms/base.py
22
reasoning_effort    Optional[str]    None    For models like o1/o3 
mem0/configs/llms/base.py
26
http_client_proxies    Optional[Union[Dict, str]]    None    Proxy settings 
mem0/configs/llms/base.py
27
Vector Store Configuration (Provider-Specific)
Providers often have strict validation for their specific configurations. For example, AzureAISearchConfig uses a @model_validator to prevent unsupported legacy fields like use_compression and ensures compression_type is valid 
mem0/configs/vector_stores/azure_ai_search.py
25-55

Sources: 
mem0/configs/llms/base.py
7-67
 
mem0/configs/vector_stores/azure_ai_search.py
6-57

Telemetry Configuration
Telemetry is a global configuration aspect managed via environment variables and a singleton pattern.

Control: Enabled by default via MEM0_TELEMETRY 
mem0/memory/telemetry.py
14
Sampling: Hot-path events are sampled at a rate defined by MEM0_TELEMETRY_SAMPLE_RATE (default 0.1), while lifecycle events like mem0.init always fire 
mem0/memory/telemetry.py
31-51
User Identification: The system generates or retrieves a unique user_id stored in the local config or vector store to anonymize telemetry data 
mem0/memory/setup.py
35-67
Sources: 
mem0/memory/telemetry.py
14-70
 
mem0/memory/setup.py
12-67

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Configuration System
Configuration Structure
Python Configuration Schema
TypeScript Configuration Schema
Configuration Precedence Rules
Precedence Hierarchy
Environment Variable Resolution
Configuration Validation and Factories
TypeScript Configuration Merging
Component Factories
Base Configuration Classes
BaseLlmConfig (Python)
Vector Store Configuration (Provider-Specific)
Telemetry Configuration
Ask Devin about mem0ai/mem0

Fast

Configuration System | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Memory Class (Open Source)
Relevant source files
Purpose and Scope
The Memory class is the core interface for self-hosted Mem0 deployments. It provides full control over memory operations with configurable LLM providers, vector stores, embedding models, and storage backends. This page documents the Memory and AsyncMemory classes, their initialization, component architecture, and runtime behavior.

For platform-hosted deployments using the Mem0 API, see 
MemoryClient (Platform)
 For detailed memory operation lifecycles (add, search, update, delete), see 
Memory Operations

Sources: 
mem0/memory/main.py
172-234
 
mem0/memory/main.py
1120-1121

Class Overview
The Memory class is defined in 
mem0/memory/main.py
172-234
 and extends MemoryBase. It orchestrates all memory operations by coordinating between:

LLM Provider: Extracts facts and determines memory actions (ADD, UPDATE, DELETE) 
mem0/memory/main.py
38-39
Embedder: Generates vector embeddings for semantic search 
mem0/memory/main.py
37
Vector Store: Stores and retrieves memory embeddings and metadata 
mem0/memory/main.py
40
Graph Store (optional): Maintains entity-relationship graphs for relational memory 
mem0/memory/main.py
41
History Database: Logs all memory modifications for audit trails using SQLiteManager 
mem0/memory/storage.py
11-19
Reranker (optional): Reranks search results for improved relevance 
mem0/memory/main.py
39
Memory Class Component Architecture

















Sources: 
mem0/memory/main.py
172-234
 
mem0/utils/factory.py
36-41

Initialization
Basic Initialization
The simplest way to initialize the Memory class is with default configuration. This requires the OPENAI_API_KEY environment variable by default.

from mem0 import Memory
 
m = Memory()
This creates a Memory instance with default settings:

LLM: OpenAI gpt-4o
Embedder: OpenAI text-embedding-3-small (1536 dimensions)
Vector Store: Qdrant (local storage at ~/.mem0/qdrant)
History: SQLite database at ~/.mem0/history.db
Sources: 
mem0/memory/main.py
173-174
 
mem0/memory/setup.py
25-57

Configuration-Based Initialization
For custom deployments, pass a MemoryConfig object or a dictionary to the from_config method.

from mem0 import Memory
from mem0.configs.base import MemoryConfig
 
config = MemoryConfig(
    llm={"provider": "ollama", "config": {"model": "llama3"}},
    vector_store={"provider": "chroma", "config": {"collection_name": "my_memories"}}
)
m = Memory(config=config)
Sources: 
mem0/memory/main.py
235-243
 
mem0/configs/base.py
15-16

Component Initialization Flow
When a Memory instance is created, components are instantiated via factories. The system also initializes a separate telemetry vector store to track migrations and system events.

Initialization Sequence Diagram


Sources: 
mem0/memory/main.py
173-234
 
mem0/memory/storage.py
11-18

Core Methods
The Memory class provides synchronous methods for CRUD operations.

Method    Description    File Reference
add()    Extracts and stores memories from messages.    
mem0/memory/main.py
281-377
search()    Retrieves memories based on semantic similarity.    
mem0/memory/main.py
643-764
get()    Retrieves a specific memory by ID.    
mem0/memory/main.py
814-842
get_all()    Lists all memories matching filters.    
mem0/memory/main.py
844-908
update()    Updates an existing memory's content or metadata.    
mem0/memory/main.py
910-958
delete()    Removes a specific memory.    
mem0/memory/main.py
985-1014
history()    Retrieves the audit trail for a specific memory ID.    
mem0/memory/main.py
1051-1065
reset()    Clears all data from the vector store and history DB.    
mem0/memory/main.py
1083-1100
Sources: 
mem0/memory/main.py
281-1100

AsyncMemory Class
AsyncMemory provides asynchronous versions of all core methods, suitable for high-concurrency environments like FastAPI or web servers. It inherits from Memory and overrides methods with async implementations 
mem0/memory/main.py
1120-1121

Implementation Pattern
AsyncMemory uses asyncio.to_thread for blocking operations (like SQLite writes) and native async calls for providers that support them.

from mem0 import AsyncMemory
 
async def main():
    m = AsyncMemory()
    await m.add("I love traveling", user_id="user_123")
    results = await m.search("What do I like?", user_id="user_123")
Sources: 
mem0/memory/main.py
1120-1490

Storage and History Management
SQLiteManager
The SQLiteManager class handles persistent storage for two distinct types of data:

History: Audit trails of memory changes (ADD, UPDATE, DELETE) 
mem0/memory/storage.py
102-127
Messages: Raw conversation history used for context during fact extraction 
mem0/memory/storage.py
128-148
Telemetry and Redaction
The Memory class includes a telemetry system that captures events like mem0.init and mem0.add. To ensure security, the _safe_deepcopy_config function redacts sensitive fields (e.g., api_key, access_token, password) before sending configuration data to telemetry 
mem0/memory/main.py
58-88
 
mem0/memory/main.py
187-217

Sources: 
mem0/memory/main.py
58-88
 
mem0/memory/storage.py
11-19

Data Flow: Natural Language to Vector Space
This diagram shows how natural language input is transformed into stored entities within the code.













Sources: 
mem0/memory/main.py
380-450
 
mem0/memory/utils.py
61-70

Validation and Constraints
The Memory class enforces several constraints on identifiers:

No Whitespace: user_id, agent_id, and run_id cannot contain internal spaces 
mem0/memory/main.py
137-141
Non-Empty: Identifiers cannot be empty or whitespace-only strings 
mem0/memory/main.py
133-136
Top-Level Rejection: Entity parameters must be passed in filters, not as top-level keyword arguments in methods like search() or add() 
mem0/memory/main.py
103-110
Sources: 
mem0/memory/main.py
103-141

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Memory Class (Open Source)
Purpose and Scope
Class Overview
Memory Class Component Architecture
Initialization
Basic Initialization
Configuration-Based Initialization
Component Initialization Flow
Initialization Sequence Diagram
Core Methods
AsyncMemory Class
Implementation Pattern
Storage and History Management
SQLiteManager
Telemetry and Redaction
Data Flow: Natural Language to Vector Space
Validation and Constraints
Ask Devin about mem0ai/mem0

Fast

Memory Class (Open Source) | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
MemoryClient (Platform)
Relevant source files
The MemoryClient class provides a Python and TypeScript SDK for interacting with the Mem0 Platform API, a fully managed memory service. This client handles authentication, request formatting, and API communication for memory operations without requiring infrastructure setup.

Scope: This page covers the Platform client (MemoryClient) for hosted deployments. For self-hosted open source deployments, see Memory Class (Open Source). For REST API details, see REST API Reference.

Architecture Overview
Client Position in the System
The MemoryClient sits between your application and the Mem0 Platform API, handling serialization, authentication, and error handling transparently.













Sources: 
mem0/client/main.py
62-135
 
mem0-ts/src/client/mem0.ts
81-122
 
docs/openapi.json
14-18

Key Responsibilities
Responsibility    Implementation
Authentication    API key validation via _validate_api_key() calling /v1/ping/ 
mem0/client/main.py
140-162
 
mem0-ts/src/client/mem0.ts
214-249
Session Management    httpx.Client (Python) or axios (TS) with timeouts 
mem0/client/main.py
119-126
 
mem0-ts/src/client/mem0.ts
113-117
Request Formatting    Automatic payload construction with _prepare_payload() and snake_case conversion 
mem0/client/main.py
186
 
mem0-ts/src/client/mem0.ts
199-206
Error Handling    @api_error_handler (Python) or _fetchWithErrorHandling (TS) 
mem0/client/utils.py
19-50
 
mem0-ts/src/client/mem0.ts
182-197
Telemetry    Event capture via capture_client_event() 
mem0/client/main.py
138
 
mem0-ts/src/client/mem0.ts
124-146
Sources: 
mem0/client/main.py
113-175
 
mem0-ts/src/client/mem0.ts
113-249

Initialization and Authentication
Constructor Signature












Sources: 
mem0/client/main.py
62-135

Authentication Flow


Sources: 
mem0/client/main.py
140-162
 
mem0-ts/src/client/mem0.ts
214-249

Initialization Patterns
Python:

from mem0 import MemoryClient
client = MemoryClient(api_key="your-api-key")
TypeScript:

import MemoryClient from 'mem0ai';
const client = new MemoryClient({ apiKey: 'your-api-key' });
Sources: 
docs/platform/quickstart.mdx
32-43
 
mem0-ts/src/client/mem0.ts
102-122

Core Memory Operations
Add Operation
The add() method stores new memories. In the Platform, this uses an asynchronous pipeline where memories are extracted from messages.

Method Signature:

def add(self, messages, options: Optional[AddMemoryOptions] = None, **kwargs) -> Dict[str, Any]
Message Format Handling: The client normalizes various input formats into a list of message objects.

Input Type    Transformation    Example
str    [{"role": "user", "content": str}]    "Hello" → [{"role": "user", "content": "Hello"}]
dict    [dict]    {"role": "user", "content": "Hi"} → [{"role": "user", "content": "Hi"}]
Sources: 
mem0/client/main.py
188-192
 
mem0-ts/src/client/mem0.ts
251-278

Search Operation
The search() method retrieves relevant memories. For Platform v3, entity IDs (like user_id) must be passed inside the filters object or via options.

# Python Search
results = client.search(
    query="What are my dietary restrictions?",
    filters={"user_id": "user123"}
)
Sources: 
mem0/client/main.py
251-296
 
mem0-ts/src/client/mem0.ts
311-332

Get and List Operations
Operation    Method    API Endpoint
Get Single    get(memory_id)    GET /v1/memories/{memory_id}/ 
mem0/client/main.py
178-204
Get All    get_all(filters=...)    GET /v1/memories/ 
mem0/client/main.py
206-250
History    history(memory_id)    GET /v1/memories/{memory_id}/history/ 
mem0/client/main.py
392-413
Sources: 
mem0/client/main.py
178-413
 
mem0-ts/src/client/mem0.ts
280-310

Entity Management
The MemoryClient provides methods to manage entities (users, agents, apps, runs) that own memories.

Method    Description    API Endpoint
users()    List all user entities    GET /v1/entities/ 
mem0/client/main.py
415-434
delete_users()    Delete user entity and memories    DELETE /v2/entities/user/{id}/ 
mem0/client/main.py
471-490
Sources: 
mem0/client/main.py
415-490
 
docs/openapi.json
89-182

Advanced Platform Features
Webhooks
The TypeScript SDK explicitly supports webhook management for memory events.

import { WebhookEvent } from "mem0ai";
 
await client.createWebhook({
  name: "my-webhook",
  url: "https://example.com/webhook",
  eventTypes: [WebhookEvent.MEMORY_ADDED]
});
Sources: 
mem0-ts/src/client/mem0.ts
503-530
 
mem0-ts/src/client/mem0.types.ts
170-175

Memory Export
Platform users can export memories based on custom schemas and filters.

await client.createMemoryExport({
  schema: { "name": "string", "preference": "string" },
  filters: { "user_id": "user123" }
});
Sources: 
mem0-ts/src/client/mem0.ts
577-593
 
mem0-ts/src/client/mem0.types.ts
208-212

Error Handling
Public methods use structured error handling to map HTTP status codes to specific exceptions.

Exception    HTTP Code    Description
AuthenticationError    401    Invalid API Key 
mem0-ts/src/client/index.ts
38
RateLimitError    429    Request limit exceeded 
mem0-ts/src/client/index.ts
39
MemoryQuotaExceededError    402    Platform storage limit reached 
mem0-ts/src/client/index.ts
44
ValidationError    400    Invalid payload or parameters 
mem0-ts/src/client/index.ts
40
Sources: 
mem0/client/utils.py
19-50
 
mem0-ts/src/client/index.ts
36-46

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
MemoryClient (Platform)
Architecture Overview
Client Position in the System
Key Responsibilities
Initialization and Authentication
Constructor Signature
Authentication Flow
Initialization Patterns
Core Memory Operations
Add Operation
Search Operation
Get and List Operations
Entity Management
Advanced Platform Features
Webhooks
Memory Export
Error Handling
Ask Devin about mem0ai/mem0

Fast

MemoryClient (Platform) | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Memory Operations
Relevant source files
This document details the core operations (add, search, update, delete, get, get_all, and history) that form the foundation of Mem0's memory management system. It covers the implementation details of the V3 additive pipeline, semantic retrieval, and the data structures returned by each operation.

Overview
Mem0 provides two primary classes for memory operations:

Memory (Open Source): Self-hosted memory management with full control over providers. See 
mem0/memory/main.py
172-1242
MemoryClient (Platform): Managed API client for the hosted Mem0 platform.
Both classes implement a consistent API, though the Platform version (V3) emphasizes an "additive-only" extraction pipeline for performance and simplicity 
docs/api-reference/memory/add-memories.mdx
7-15

Core Operations
Add Operation
The add() method stores new memories from conversation messages. In the Open Source version, it supports two modes: intelligent inference (default) or raw storage.

Add Operation Flow (OSS)














Sources: 
mem0/memory/main.py
281-384
 
mem0/memory/main.py
386-597

Inference vs Raw Mode
When infer=True, the system performs extraction using USER_MEMORY_EXTRACTION_PROMPT or AGENT_MEMORY_EXTRACTION_PROMPT 
mem0/configs/prompts.py
63-114
 It then resolves conflicts by comparing new facts against existing memories retrieved from the VectorStore 
mem0/memory/main.py
465-475

When infer=False, messages are stored verbatim. Each message becomes a separate entry in the vector store with associated metadata 
mem0/memory/main.py
392-421

Search Operation
The search() method retrieves relevant memories using semantic similarity. It can optionally use a hybrid approach combining vector search with BM25 keyword matching and reranking.

Search Implementation Details
The search function calculates a combined score if both vector and keyword search are enabled. It uses score_and_rank to merge results 
mem0/memory/main.py
825-835










Sources: 
mem0/memory/main.py
758-867
 
mem0/utils/scoring.py
43-48

Parameters
Parameter    Location    Description
query    
mem0/memory/main.py
759
Natural language string to search for
filters    
mem0/memory/main.py
765
Dictionary for metadata filtering (user_id, agent_id, etc.)
threshold    
mem0/memory/main.py
766
Minimum similarity score (0.0 to 1.0)
limit    
mem0/memory/main.py
764
Maximum number of results to return
Update and Delete Operations
Update
The update() method modifies an existing memory entry. It re-generates embeddings for the new text and updates the record in the VectorStore 
mem0/memory/main.py
869-901

Implementation: It calls _update_memory(), which calculates an MD5 hash of the new data to prevent redundant updates 
mem0/memory/main.py
1004-1041
Delete
Mem0 provides three ways to remove data:

delete(memory_id): Removes a specific record 
mem0/memory/main.py
903-931
 In OSS, this now fetches the memory first to log it to history before deletion 
tests/test_main.py
164-174
delete_all(filters): Removes all memories matching criteria (e.g., all for a specific user_id) 
mem0/memory/main.py
933-1002
reset(): Completely clears the vector store and history database 
mem0/memory/main.py
1145-1173
History Operation
The history() method tracks the lifecycle of a memory. It queries the SQLiteManager to return a chronological list of events (ADD, UPDATE, DELETE) associated with a specific memory_id.

Sources: 
mem0/memory/main.py
1118-1143
 
mem0/memory/storage.py
221-255

History Schema
The history is stored in a local SQLite table managed by SQLiteManager 
mem0/memory/storage.py
11

memory_id: The ID of the memory record 
mem0/memory/storage.py
68-81
old_memory: The content before an update.
new_memory: The content after an update or addition.
event: The action type (ADD/UPDATE/DELETE).
Get and Get All Operations
get(memory_id): Retrieves a single memory by ID. It maps the raw vector store payload into a structured MemoryItem 
mem0/memory/main.py
610-651
get_all(filters): Lists memories based on filters. It supports pagination via limit and offset 
mem0/memory/main.py
653-709
 In Platform V3, entity IDs like user_id must be passed inside the filters object 
docs/api-reference/memory/get-memories.mdx
7-10
Code Entity Summary
Primary Classes
Entity    File    Role
Memory    
mem0/memory/main.py
172
Main entry point for OSS memory operations.
AsyncMemory    
mem0/memory/main.py
1244
Asynchronous implementation of the Memory class.
SQLiteManager    
mem0/memory/storage.py
11
Manages local history and message persistence.
MemoryItem    
mem0/configs/base.py
15
Pydantic model defining the structure of a memory record.
Key Utility Functions
Function    File    Role
_build_filters_and_metadata    
mem0/memory/main.py
87
Normalizes session IDs into storage-compatible filters.
parse_messages    
mem0/memory/utils.py
61
Converts list of message dicts into a flat string for LLM processing.
extract_json    
mem0/memory/utils.py
125
Robustly extracts JSON from LLM responses containing markdown.
normalize_facts    
mem0/memory/utils.py
84
Normalizes LLM-extracted facts from objects to plain strings.
Sources: 
mem0/memory/main.py
 
mem0/memory/storage.py
 
mem0/memory/utils.py

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Memory Operations
Overview
Core Operations
Add Operation
Add Operation Flow (OSS)
Inference vs Raw Mode
Search Operation
Search Implementation Details
Parameters
Update and Delete Operations
Update
Delete
History Operation
History Schema
Get and Get All Operations
Code Entity Summary
Primary Classes
Key Utility Functions
Ask Devin about mem0ai/mem0

Fast

Memory Operations | mem0ai/mem0 | DeepWiki
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Session Scoping and Filters
Relevant source files
Session scoping and filters control memory isolation and retrieval precision in Mem0. Session identifiers (user_id, agent_id, app_id, run_id) partition memories into non-overlapping namespaces, while metadata filters enable fine-grained queries within those partitions. This system prevents data leakage between users, organizes multi-agent workflows, and supports ephemeral session contexts.

Core Session Identifiers
Mem0 enforces memory isolation through hierarchical session identifiers. In the Open Source SDK, these are validated to ensure at least one identifier is present for any operation that interacts with the memory store.

Identifier    Scope    Typical Lifespan    Example Use Case
user_id    Individual user/account    Weeks to years    Persistent user preferences, profile data
agent_id    Specific agent/assistant    Days to months    Agent-specific learning, tool usage patterns
run_id    Single conversation/session    Minutes to hours    Temporary context within a workflow
app_id    Application context    Weeks to months    Multi-app deployments, service isolation
Validation Logic: The Memory class rejects operations if no entity parameters are provided. This is enforced by ENTITY_PARAMS checking in _reject_top_level_entity_params 
mem0/memory/main.py
100-111
 and identifier normalization in _validate_and_trim_entity_id 
mem0/memory/main.py
113-141

Sources: 
mem0/memory/main.py
100-141
 
docs/llms.txt
34-51
 
docs/platform/features/v2-memory-filters.mdx
32-41
 
docs/cookbooks/essentials/entity-partitioning-playbook.mdx
22-39

Session Scoping Architecture
Identifier Validation and Processing
The system ensures that identifiers are valid strings without internal whitespace to prevent query injection or formatting errors in vector/graph store backends.

Diagram: Entity ID Validation Flow

Sources: 
mem0/memory/main.py
103-111
 
mem0/memory/main.py
113-141

Data Flow in Scoped Operations
When a memory is added or searched, the session identifiers flow through the Memory class into the VectorStore and GraphMemory components.

Diagram: Scoped Memory Data Flow

Sources: 
mem0/memory/main.py
236-267
 
mem0/memory/main.py
758-856
 
mem0/memory/graph_memory.py
65-94

Metadata Filtering
Beyond core session identifiers, Mem0 supports arbitrary metadata filtering. Metadata is stored as part of the payload in vector stores and can be queried using simple equality or advanced operators.

Implementation in Vector Stores
During a search, the filters dictionary is passed directly to the vector_store.search method 
mem0/memory/main.py
875-880

OSS: Filters are typically handled by the underlying vector database (e.g., Qdrant, Chroma).
Platform: Supports a rich JSON-based filter structure including logical operators 
docs/platform/features/v2-memory-filters.mdx
18-30
Filter Operators (Platform)
Operator    Description    Example
eq    Equal to    {"user_id": "user_1"}
ne    Not equal to    {"status": {"ne": "archived"}}
in    In a list of values    {"app_id": {"in": ["app1", "app2"]}}
contains    Case-sensitive substring    {"metadata": {"key": "value"}}
gt / lt    Comparison (Time/Numeric)    {"created_at": {"gt": "2024-01-01"}}
Sources: 
docs/platform/features/v2-memory-filters.mdx
32-60
 
mem0/memory/main.py
810-815

Multi-Agent Isolation
In multi-agent systems, isolation is achieved by combining user_id with agent_id. This prevents an agent from accessing memories belonging to another agent, even if they share the same user.

Partitioning Strategy
User-level Partition: Memories where agent_id is null. Stores global user preferences.
Agent-level Partition: Memories where both user_id and agent_id are set. Stores interaction history specific to that agent.
Common Pitfall: A search with {"AND": [{"user_id": "alice"}, {"agent_id": "bot"}]} will only return memories where both fields were explicitly set during add(). If a memory was added with only user_id, it will not appear in a search that filters for a non-null agent_id 
docs/platform/features/v2-memory-filters.mdx
61-63

Sources: 
docs/platform/features/v2-memory-filters.mdx
32-63
 
docs/cookbooks/essentials/entity-partitioning-playbook.mdx
76-93

Graph Memory Scoping
Graph memory utilizes the same filters to constrain entity and relationship extraction and retrieval.

Scoped Extraction
When graph.add() is called, the session filters (e.g., user_id, agent_id) are attached to every node and relationship created in the graph 
mem0/memory/graph_memory.py
86-94
 This ensures that the graph structure is partitioned by the same boundaries as the vector store.

Scoped Retrieval
The GraphMemory.search() method uses the provided filters to narrow the search space before performing entity matching or relationship traversal 
mem0/memory/graph_memory.py
96-130

Sources: 
mem0/memory/graph_memory.py
86-130
 
mem0/memory/main.py
835-843

Technical Implementation Details
The Memory Class and Filters
In mem0/memory/main.py, the search and get_all methods are the primary entry points for filtered retrieval.

search(query, filters, ...): Combines semantic vector search with metadata filtering 
mem0/memory/main.py
758-856
get_all(filters, ...): Retrieves all memories matching the filter criteria without a query string 
mem0/memory/main.py
653-709
delete_all(filters, ...): Performs bulk deletion based on filter matches 
mem0/memory/main.py
911-948
History and Scoping
The SQLiteManager tracks the history of memory changes. While history is primarily tracked by memory_id, the actor_id (often a name or identifier for the specific participant) can be used to filter historical records 
mem0/memory/storage.py
150-191

Sources: 
mem0/memory/main.py
653-709
 
mem0/memory/main.py
911-948
 
mem0/memory/storage.py
150-191

Summary of Usage Patterns
Operation    Usage of Filters    Requirement
add    Used to find existing memories for deduplication/update    At least one ID 
mem0/memory/main.py
281-329
search    Narrows vector/graph search space    At least one ID 
mem0/memory/main.py
758-800
get_all    Filters the list of returned memories    At least one ID 
mem0/memory/main.py
653-680
delete_all    Targets specific memories for removal    At least one ID 
mem0/memory/main.py
911-923
Sources: 
mem0/memory/main.py
281-948
 
docs/platform/features/v2-memory-filters.mdx
69-102
 
docs/platform/features/async-client.mdx
78-81

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Session Scoping and Filters
Core Session Identifiers
Session Scoping Architecture
Identifier Validation and Processing
Data Flow in Scoped Operations
Metadata Filtering
Implementation in Vector Stores
Filter Operators (Platform)
Multi-Agent Isolation
Partitioning Strategy
Graph Memory Scoping
Scoped Extraction
Scoped Retrieval
Technical Implementation Details
The `Memory` Class and Filters
History and Scoping
Summary of Usage Patterns
Ask Devin about mem0ai/mem0

Fast

Session Scoping and Filters | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Asynchronous Operations
Relevant source files
This document covers Mem0's support for non-blocking asynchronous operations across Python and TypeScript SDKs. Asynchronous operations enable concurrent memory management, improved throughput, and better resource utilization in I/O-bound applications.

Overview
Mem0 provides asynchronous APIs that allow applications to perform memory operations without blocking the main execution thread. This is particularly valuable for:

Web servers and APIs: Handle multiple memory operations concurrently.
Batch processing: Process large volumes of memory operations in parallel.
Real-time applications: Maintain responsiveness while managing memories.
High-throughput systems: Maximize I/O utilization with concurrent requests.
The async support is implemented differently across platforms:

Python: AsyncMemory and AsyncMemoryClient classes with async/await syntax.
TypeScript: All client methods are asynchronous by default using Promises.
Sources: 
mem0/__init__.py
5-7
 
mem0/memory/main.py
1-41
 
mem0/client/main.py
1-25

Python Async Architecture
The diagram below bridges the natural language space of "Memory Operations" to the code entities that implement them asynchronously.

Memory Class to Code Entity Mapping













Sources: 
mem0/memory/main.py
24-41
 
mem0/client/main.py
10-135
 
mem0/memory/storage.py
11-19
 
mem0/__init__.py
5-7

AsyncMemory Class (Self-Hosted)
The AsyncMemory class provides async/await versions of all core memory operations for self-hosted deployments. It inherits from MemoryBase and mirrors the Memory class API but with coroutines.

Initialization
from mem0 import AsyncMemory
from mem0.configs.base import MemoryConfig
 
# Initialize with configuration
config = MemoryConfig(
    vector_store={
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    }
)
 
memory = AsyncMemory(config=config)
Key Methods
All methods from the synchronous Memory class have async equivalents in AsyncMemory:

Synchronous Method    Async Method    Description
add()    await add()    Add memories from messages (uses LLM for extraction)
search()    await search()    Search memories by query (semantic + keyword)
get()    await get()    Retrieve memory by ID
get_all()    await get_all()    List all memories with filters
update()    await update()    Update existing memory
delete()    await delete()    Delete memory by ID
delete_all()    await delete_all()    Bulk delete based on filters
history()    await history()    Retrieve history for a specific memory ID
Sources: 
mem0/memory/main.py
118-124
 
tests/memory/test_main.py
120-124
 
tests/test_memory.py
25-31

AsyncMemoryClient Class (Platform)
The AsyncMemoryClient class provides async operations for the hosted Mem0 Platform API.

Initialization
from mem0 import AsyncMemoryClient
 
client = AsyncMemoryClient(
    api_key="your-api-key"
)
Concurrent Operations Example
Using asyncio.gather allows for high-concurrency memory ingestion.

import asyncio
from mem0 import AsyncMemory
 
async def batch_operations():
    memory = AsyncMemory()
 
    tasks = [
        memory.add(
            messages=[{"role": "user", "content": f"Message {i}"}],
            user_id=f"user_{i}"
        )
        for i in range(5)
    ]
 
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
Sources: 
mem0/client/main.py
108-135
 
mem0/client/main.py
164-185

Platform Async Patterns
The async_mode parameter controls whether memory operations execute synchronously or asynchronously on the platform side.

Platform Execution Flow








async_mode=True (default): Platform processes the request asynchronously and returns immediately with an event ID.
async_mode=False: Platform processes the request synchronously and waits for completion before returning final results.
Sources: 
mem0/client/main.py
164-186
 
docs/openapi.json
123-144

Performance Considerations
Concurrency vs. Blocking
Asynchronous operations significantly reduce the total time for batch tasks by overlapping I/O wait times.













Internal Implementation Details
The synchronous Memory class internally uses concurrent.futures.ThreadPoolExecutor to parallelize certain operations while maintaining a blocking external API. For example, during the add operation, fact extraction and graph updates can be triggered in parallel.

In contrast, AsyncMemory uses native asyncio patterns for these tasks to avoid blocking the event loop.

Sources: 
mem0/memory/main.py
1-11
 
tests/memory/test_main.py
126-153

Best Practices
Lifecycle Management: Wrap AsyncMemory in an async context manager or FastAPI startup/shutdown hooks to ensure vector store connections and database handles in SQLiteManager are managed correctly.
Resilience: Implement retries for network-bound async operations when using AsyncMemoryClient.
Event Loop Awareness: Never call AsyncMemory methods outside of an async def function to avoid RuntimeError: no running event loop.
Metadata Preservation: When using update(), ensure metadata is passed correctly to preserve contextual information.
# Example of robust async update
# From tests/memory/test_main.py:141-153
async def robust_update(memory_instance, mem_id, text, metadata):
    result = await memory_instance.update(
        memory_id=mem_id, 
        data=text, 
        metadata=metadata
    )
    return result
Sources: 
mem0/memory/storage.py
11-19
 
tests/memory/test_main.py
141-153
 
mem0/client/main.py
164-186

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Asynchronous Operations
Overview
Python Async Architecture
Memory Class to Code Entity Mapping
AsyncMemory Class (Self-Hosted)
Initialization
Key Methods
AsyncMemoryClient Class (Platform)
Initialization
Concurrent Operations Example
Platform Async Patterns
Platform Execution Flow
Performance Considerations
Concurrency vs. Blocking
Internal Implementation Details
Best Practices
Ask Devin about mem0ai/mem0

Fast

Asynchronous Operations | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Proxy Integration
Relevant source files
Purpose and Scope
The Mem0 proxy provides transparent memory integration into LLM chat completions through LiteLLM. This proxy intercepts chat completion requests, automatically searches for relevant memories, injects them into the conversation context, and stores new information for future retrieval. The proxy mimics the OpenAI chat completions API while adding memory capabilities.

The proxy is implemented in mem0/proxy/main.py 
mem0/proxy/main.py
1-191
 and supports both the open-source Memory class and the hosted MemoryClient.

Architecture Overview
The proxy architecture consists of three primary classes that wrap memory operations around LiteLLM completion calls:















Sources: 
mem0/proxy/main.py
28-50
 
tests/test_proxy.py
1-101

Core Components
Mem0 Class
The Mem0 class 
mem0/proxy/main.py
28-40
 serves as the entry point for proxy initialization and supports two initialization modes:

Platform Mode: Initializes with MemoryClient if an api_key is provided 
mem0/proxy/main.py
35-36
OSS Mode: Initializes with a local Memory instance using a configuration dictionary or default settings 
mem0/proxy/main.py
38
The class exposes a chat attribute that provides the chat completions interface via the Chat class 
mem0/proxy/main.py
40

Chat and Completions Classes
The Chat class 
mem0/proxy/main.py
43-45
 provides a namespace similar to the OpenAI client structure. It initializes a Completions instance 
mem0/proxy/main.py
48-191
 that handles the actual completion logic.

Key Methods in Completions:

Method    Parameters    Returns    Description
create()    model, messages, user_id, agent_id, run_id, **kwargs    litellm.ModelResponse    Intercepts the request, manages memory, and calls LiteLLM.
_prepare_messages()    messages    List[dict]    Ensures a system prompt is present, prepending MEMORY_ANSWER_PROMPT 
mem0/configs/prompts.py
4-13
 if missing.
_async_add_to_memory()    messages, IDs, metadata    None    Spawns a daemon thread to store the conversation in memory without blocking.
_fetch_relevant_memories()    messages, IDs, filters    List    Queries the memory backend using the last 6 messages as context.
Sources: 
mem0/proxy/main.py
48-177
 
mem0/configs/prompts.py
4-13

Data Flow and Memory Injection
The following sequence diagram illustrates the complete request lifecycle when using the proxy:



Sources: 
mem0/proxy/main.py
95-145
 
mem0/proxy/main.py
152-177

Memory Retrieval and Formatting
When a user message is detected as the last item in the messages list, the proxy performs memory injection 
mem0/proxy/main.py
104-108
:

Search Context: The proxy extracts the last 6 messages to form a search query 
mem0/proxy/main.py
168
Search Execution: It calls self.mem0_client.search() with the generated query and provided filters 
mem0/proxy/main.py
170-177
Context Formatting: The _format_query_with_memories method 
mem0/proxy/main.py
179-191
 joins the retrieved facts into a single string. If using the OSS Memory class 
mem0/memory/main.py
7
 it also includes extracted entities/relations if available 
mem0/proxy/main.py
184-186
Content Update: The retrieved facts are prepended to the content of the final user message 
mem0/proxy/main.py
108
Asynchronous Storage
To prevent memory storage from increasing latency for the end-user, the proxy uses threading.Thread with daemon=True to call self.mem0_client.add() in the background 
mem0/proxy/main.py
153-164

Configuration and Usage
Initialization
The proxy can be initialized to use either the local memory engine or the Mem0 platform.

from mem0.proxy.main import Mem0
 
# Mode 1: Platform (MemoryClient)
mem0_platform = Mem0(api_key="m0-xxx")
 
# Mode 2: OSS (Memory)
config = {
    "vector_store": {"provider": "chroma", "config": {"path": "./db"}},
    "llm": {"provider": "openai", "config": {"model": "gpt-4o"}}
}
mem0_oss = Mem0(config=config)
Sources: 
mem0/proxy/main.py
29-40

LiteLLM Integration
The proxy utilizes LiteLLM's unified interface to support over 100+ LLM providers. It validates that the selected model supports function calling before proceeding 
mem0/proxy/main.py
98-101
 All standard OpenAI-compatible parameters (e.g., temperature, tools, response_format) are forwarded directly to litellm.completion() 
mem0/proxy/main.py
110-140

Telemetry and Tracking
Every successful completion through the proxy triggers a telemetry event via capture_event (for OSS) or capture_client_event (for Platform) with the event name mem0.chat.create 
mem0/proxy/main.py
141-144

Sources: 
mem0/proxy/main.py
141-144
 
mem0/memory/telemetry.py
23

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Proxy Integration
Purpose and Scope
Architecture Overview
Core Components
Mem0 Class
Chat and Completions Classes
Data Flow and Memory Injection
Memory Retrieval and Formatting
Asynchronous Storage
Configuration and Usage
Initialization
LiteLLM Integration
Telemetry and Tracking
Ask Devin about mem0ai/mem0

Fast

Proxy Integration | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Intelligent Memory Processing
Relevant source files
Purpose and Scope
This document explains Mem0's intelligent memory processing system, which uses Large Language Models (LLMs) to extract structured facts from conversations, deduplicate information, and automatically maintain memory consistency. This process represents the core "intelligence" layer that distinguishes Mem0 from traditional vector databases.

For basic memory operations, see Memory Operations. For information about multi-level memory architecture, see Session Scoping and Filters. For graph-based relationship extraction, see Graph Memory.

Overview
Mem0 supports two memory processing modes controlled by the infer parameter in the add() method of the Memory class:

Mode    Parameter    Behavior    Use Case
Direct Mode    infer=False    Messages stored as-is without processing    Raw conversation logging, minimal latency
Intelligent Mode    infer=True (default)    LLM extracts facts, deduplicates, and manages consistency    Personalized AI applications, knowledge management
In intelligent mode, Mem0 performs a multi-stage LLM-driven pipeline to transform conversational data into structured, deduplicated memory entries.

Sources: 
mem0/memory/main.py
386-421
 
mem0/memory/main.py
423-597

Architecture
High-Level Processing Pipeline





















Sources: 
mem0/memory/main.py
386-597
 
mem0/memory/utils.py
15-29

Component Interaction (Code Entity Space)























Sources: 
mem0/memory/main.py
423-589
 
mem0/memory/utils.py
15-29
 
mem0/memory/utils.py
109-142
 
mem0/configs/prompts.py
63-173

Fact Extraction
User vs Agent Memory Extraction
Mem0 uses different extraction strategies based on whether the memory is for a user or an agent. This is determined by the presence of agent_id and assistant messages.
















Sources: 
mem0/memory/main.py
260-279
 
mem0/memory/utils.py
15-29

Extraction Process
The fact extraction process within _add_to_vector_store() involves:

Message Parsing: parse_messages() converts the input message list into a string format for the LLM. 
mem0/memory/utils.py
61-70
Prompt Selection: get_fact_retrieval_messages() selects the appropriate prompt. 
mem0/memory/utils.py
15-29
LLM Invocation: The system calls llm.generate_response() with response_format={"type": "json_object"} to ensure structured output. 
mem0/memory/main.py
434-440
Response Cleaning: remove_code_blocks() and extract_json() handle cases where the LLM includes markdown or <think> tags (stripping them via regex). 
mem0/memory/utils.py
109-142
Normalization: normalize_facts() ensures facts are a flat list of strings, even if smaller LLMs return objects like {"fact": "..."}. 
mem0/memory/utils.py
84-106
Sources: 
mem0/memory/main.py
423-456
 
mem0/memory/utils.py
84-106
 
mem0/memory/utils.py
121

Memory Deduplication
Similarity Search Phase
Before adding new facts, Mem0 searches for similar existing memories to identify potential duplicates or contradictions.











Sources: 
mem0/memory/main.py
461-494

UUID Mapping Strategy
To prevent LLM hallucinations when referencing complex UUIDs, Mem0 maps them to simple integers (e.g., "0", "1") before passing them to the action determination prompt. This mapping is reversed during execution to ensure the correct memory_id is updated or deleted in the VectorStore. 
mem0/memory/main.py
490-494
 
mem0/memory/main.py
541-564

Memory Actions
Action Determination
The LLM compares extracted facts against retrieved existing memories and assigns one of four actions based on the MemoryUpdateSchema:

Action    Meaning    Code Execution
ADD    Completely new information.    _create_memory()
UPDATE    Refines or changes an existing memory.    _update_memory()
DELETE    Contradicts an existing memory (which should be removed).    _delete_memory()
NONE    Information already exists or is irrelevant.    Updates metadata only
Sources: 
mem0/memory/main.py
524-585
 
mem0/configs/prompts.py
175-323
 
mem0-ts/src/oss/src/prompts/index.ts
20-43

Action Execution Logic
The implementation in _add_to_vector_store() handles the state transitions:

ADD: Creates a new entry in the VectorStore and records the event in SQLiteManager. 
mem0/memory/main.py
534-540
UPDATE: Re-embeds the updated text and replaces the existing vector and payload in the vector database. 
mem0/memory/main.py
541-555
DELETE: Removes the vector from the store and marks the history as deleted in the metadata database. 
mem0/memory/main.py
556-564
NONE: Updates the updated_at timestamp and ensures agent_id or run_id are associated with the memory if they were provided in the current call. 
mem0/memory/main.py
565-585
Sources: 
mem0/memory/main.py
524-585
 
mem0/memory/storage.py
150-192

Custom Prompts
Users can override the intelligent processing logic by providing custom prompts in MemoryConfig.

custom_fact_extraction_prompt: Overrides the default fact extraction system prompt. 
mem0/configs/base.py
59-66
custom_update_memory_prompt: Overrides the logic for determining ADD/UPDATE/DELETE/NONE actions. 
mem0/configs/base.py
59-66
If a prompt argument is passed directly to the add() method, it takes precedence over the custom_instructions defined at the config level for that specific call. 
tests/memory/test_main.py
93-104

Sources: 
mem0/configs/base.py
59-66
 
mem0/memory/main.py
405-408
 
mem0/memory/main.py
425-427

Summary of Key Functions
Function    File    Role
_add_to_vector_store    mem0/memory/main.py    Orchestrates the entire intelligent processing pipeline.
get_fact_retrieval_messages    mem0/memory/utils.py    Generates prompts for fact extraction.
get_update_memory_messages    mem0/configs/prompts.py    Generates prompts for ADD/UPDATE/DELETE determination.
remove_code_blocks    mem0/memory/utils.py    Cleans LLM output (removes markdown and thinking tags).
normalize_facts    mem0/memory/utils.py    Ensures LLM output matches expected JSON schema.
Sources: 
mem0/memory/main.py
386-597
 
mem0/memory/utils.py
15-106

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Intelligent Memory Processing
Purpose and Scope
Overview
Architecture
High-Level Processing Pipeline
Component Interaction (Code Entity Space)
Fact Extraction
User vs Agent Memory Extraction
Extraction Process
Memory Deduplication
Similarity Search Phase
UUID Mapping Strategy
Memory Actions
Action Determination
Action Execution Logic
Custom Prompts
Summary of Key Functions
Ask Devin about mem0ai/mem0

Fast

Intelligent Memory Processing | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Graph Memory Overview
Relevant source files
Graph memory is an optional extension to Mem0's core vector-based memory system that represents knowledge as a graph of entities (nodes) and their relationships (edges). This enables structured knowledge representation, complex relational queries, and semantic understanding of how different pieces of information connect.

For details on configuring graph store providers (Neo4j, Kuzu, Memgraph, Neptune), see 4.2 Graph Store Providers. For implementation details of entity extraction and relationship establishment, see 4.3 Entity and Relationship Extraction.

What is Graph Memory
Graph memory complements Mem0's vector-based memory by storing information in a graph database structure. While vector memory excels at semantic similarity search, graph memory captures explicit relationships between entities, enabling queries like "who knows whom" or "what product did user X purchase."

The system uses an LLM to automatically extract entities (people, places, things) and their relationships from conversational text, then stores them as nodes and edges in a graph database. Each entity node contains a vector embedding for similarity matching and deduplication.

Key Characteristics:

Entity-centric: Stores discrete entities (people, places, concepts) as nodes.
Relationship-aware: Captures explicit relationships (knows, works_at, likes) as edges.
Hybrid storage: Combines graph structure with vector embeddings for node matching.
Automatic extraction: LLM-powered entity and relationship identification using tool calling.
Optional: Requires graph extra dependencies and specific configuration.
Sources: 
docs/core-concepts/memory-operations/add.mdx
46-48
 
docs/platform/advanced-memory-operations.mdx
67-68
 
examples/graph-db-demo/neptune-example.ipynb
11-13

Graph Memory vs Vector Memory
The following diagram illustrates the different processing paths for a single piece of information.

Comparison: Natural Language to Code Entity Space












Aspect    Vector Memory    Graph Memory
Structure    Flat embeddings    Nodes and edges
Queries    Semantic Similarity search    Relationship traversal
Deduplication    Text similarity / Conflict Resolution    Entity matching by embedding
Relationships    Implicit (via embeddings)    Explicit (via edges)
Use Case    "Find similar memories"    "Find all relationships for entity X"
Storage    Vector database (Qdrant, Pinecone, etc.)    Graph database (Neo4j, Neptune, etc.)
Sources: 
docs/core-concepts/memory-operations/add.mdx
40-49
 
docs/core-concepts/memory-operations/search.mdx
32-45
 
examples/graph-db-demo/neptune-example.ipynb
11-13

Architecture and Integration
System Components
The Memory class acts as the orchestrator. When graph features are enabled in the configuration, it coordinates between vector and graph storage backends.

















Sources: 
docs/open-source/overview.mdx
66-85
 
docs/open-source/configuration.mdx
59-83
 
examples/graph-db-demo/neptune-example.ipynb
131-160

Parallel Execution Model
When a user calls add(), Mem0 processes both vector and graph updates.

Vector Path: Extracts facts from messages and stores them in the configured VectorStore.
Graph Path: Passes the same messages to the graph subsystem for entity/relationship extraction.
Merging: The final response returns both vector memory results and graph relations.
Sources: 
docs/core-concepts/memory-operations/add.mdx
40-49
 
docs/platform/advanced-memory-operations.mdx
111-113

Entity and Relationship Model
Node Properties
Each entity node in the graph contains properties used for scoping and retrieval.

Property    Description
name    The unique identifier for the node (e.g., "Alice").
user_id    Used to isolate graphs between different users.
agent_id    Used to isolate graphs between different agents.
embedding    Vector representation of the entity name for deduplication.
Sources: 
docs/core-concepts/memory-operations/add.mdx
19-25
 
docs/core-concepts/memory-operations/search.mdx
19-24
 
examples/graph-db-demo/neptune-example.ipynb
11-13

Relationship Format
Relationships are typically extracted in a triple format: source -- RELATIONSHIP -- destination. For example, Alice -- WORKS_AT -- Google.

Sources: 
docs/platform/advanced-memory-operations.mdx
111-113
 
examples/graph-db-demo/neptune-example.ipynb
11-13

Basic Usage
Initialization
Graph memory is enabled via configuration providers.

# Example using Amazon Neptune as Graph Memory
config = {
    "graph_store": {
        "provider": "neptune",
        "config": {
            "endpoint": "neptune-graph://my-graph-identifier",
        },
    },
    "llm": {
        "provider": "aws_bedrock",
        "config": {"model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"}
    }
}
from mem0 import Memory
m = Memory.from_config(config)
Sources: 
examples/graph-db-demo/neptune-example.ipynb
131-160
 
docs/open-source/configuration.mdx
59-83

Adding and Searching
# Adding memory triggers both vector and graph extraction
m.add("I prefer boutique hotels in Tokyo", user_id="morgan")
 
# Search retrieves semantically similar facts AND graph relationships
results = m.search("What are Morgan's hotel preferences?", user_id="morgan")
Sources: 
docs/platform/advanced-memory-operations.mdx
73-86
 
docs/platform/advanced-memory-operations.mdx
122-129

Data Flow: Extraction and Storage
The extraction process utilizes LLMs to identify facts, which are then further processed into entities and relationships.



Sources: 
docs/core-concepts/memory-operations/add.mdx
40-49
 
docs/platform/advanced-memory-operations.mdx
111-113
 
examples/graph-db-demo/neptune-example.ipynb
11-13

Session Scoping and Isolation
Graph memory respects the same scoping rules as vector memory. Filters like user_id, agent_id, and run_id are used to ensure that a search for "Alice" in one user's context does not return "Alice" from another user's context.

Sources: 
docs/core-concepts/memory-operations/search.mdx
62-64
 
docs/core-concepts/memory-operations/search.mdx
159-175
 
docs/core-concepts/memory-types.mdx
50-57

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Graph Memory Overview
What is Graph Memory
Graph Memory vs Vector Memory
Comparison: Natural Language to Code Entity Space
Architecture and Integration
System Components
Parallel Execution Model
Entity and Relationship Model
Node Properties
Relationship Format
Basic Usage
Initialization
Adding and Searching
Data Flow: Extraction and Storage
Session Scoping and Isolation
Ask Devin about mem0ai/mem0

Fast

Graph Memory Overview | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Graph Store Providers
Relevant source files
Graph store providers enable Mem0 to capture and query entity-relationship structures extracted from conversations. This page documents the supported graph database providers, their configuration, and the factory pattern used to instantiate them.

For information about graph memory operations and search, see Graph Search and Retrieval. For similarity threshold configuration, see Similarity Thresholds. For general graph memory architecture, see Graph Memory Overview.

Supported Providers
Mem0 supports several graph database providers through a factory-based architecture. These providers allow the system to store and retrieve knowledge as a network of entities and relationships.

Provider    Backend    Module Path    Primary Use Case
default (Neo4j)    Neo4j    mem0.memory.graph_memory.MemoryGraph    Production deployments with enterprise features
memgraph    Memgraph    mem0.memory.memgraph_memory.MemoryGraph    High-performance in-memory graph operations
neptune    AWS Neptune Graph    mem0.graphs.neptune.neptunegraph.MemoryGraph    AWS-native graph database (serverless)
neptunedb    AWS Neptune DB    mem0.graphs.neptune.neptunedb.MemoryGraph    AWS Neptune with persistent storage
kuzu    Kuzu    mem0.memory.kuzu_memory.MemoryGraph    Embedded graph database for local deployments
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/utils/factory.py#L214-L220" min=214 max=220 file-path="mem0/utils/factory.py">Hii</FileRef>

Factory Architecture
GraphStoreFactory Implementation
The GraphStoreFactory class manages the dynamic instantiation of graph store providers. It maps provider names to their respective class paths and configuration requirements.

The following diagram illustrates the relationship between configuration, the factory, and the underlying code entities.

Graph Store Code Entity Mapping



























Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/utils/factory.py#L208-L230" min=208 max=230 file-path="mem0/utils/factory.py">Hii</FileRef>, <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/configs/base.py#L29-L58" min=29 max=58 file-path="mem0/configs/base.py">Hii</FileRef>, <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/memory/main.py#L199-L206" min=199 max=206 file-path="mem0/memory/main.py">Hii</FileRef>

Provider Configuration
Neo4j (Default)
Neo4j is the default graph store provider. It utilizes the langchain_neo4j.Neo4jGraph client for database interaction and rank_bm25 for reranking search results.

Configuration Parameters:

config = {
    "graph_store": {
        "provider": "default", 
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "your-password",
            "database": "neo4j"
        },
        "threshold": 0.7
    }
}
Index Management: The Neo4j implementation creates specific indexes for performance:

entity_single: A single property index on user_id.
entity_composite: A composite index on (name, user_id) (requires Neo4j Enterprise).
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/utils/factory.py#L214-L214" min=214 file-path="mem0/utils/factory.py">Hii</FileRef>

AWS Neptune
Mem0 provides deep integration with AWS Neptune, supporting both the Analytics (serverless) and Database (persistent) engines.

Neptune Analytics (Serverless): Used via the neptune provider. It is often paired with AWS Bedrock for embeddings and LLM operations. The endpoint must follow the neptune-graph:// protocol for Analytics.

config = {
    "embedder": {
        "provider": "aws_bedrock",
        "config": {
            "model": "amazon.titan-embed-text-v2:0",
            "embedding_dims": 1024
        }
    },
    "graph_store": {
        "provider": "neptune",
        "config": {
            "endpoint": "neptune-graph://my-graph-identifier",
            "region": "us-east-1"
        }
    }
}
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/examples/graph-db-demo/neptune-example.ipynb#L65-L71" min=65 max=71 file-path="examples/graph-db-demo/neptune-example.ipynb">Hii</FileRef>, <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/configs/vector_stores/neptune.py#L11-L23" min=11 max=23 file-path="mem0/configs/vector_stores/neptune.py">Hii</FileRef>, <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/utils/factory.py#L216-L217" min=216 max=217 file-path="mem0/utils/factory.py">Hii</FileRef>

Memgraph and Kuzu
Memgraph: An in-memory graph database. Configuration requires standard connection parameters like url, username, and password.
Kuzu: An embedded graph database. Configuration primarily requires a path for local storage, making it suitable for local-first applications.
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/utils/factory.py#L215-L218" min=215 max=218 file-path="mem0/utils/factory.py">Hii</FileRef>

Enabling Graph Memory
Graph memory is activated within the Memory class based on the presence of a graph store configuration. If graph_store is provided in the configuration, the Memory class initializes the component and sets the internal flag enable_graph.

Memory Component Initialization Flow













Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/memory/main.py#L199-L206" min=199 max=206 file-path="mem0/memory/main.py">Hii</FileRef>

Installation
Graph store dependencies are optional to keep the core package lightweight. They can be installed using the graph extra. For AWS-specific graph stores like Neptune, the extras tag is also recommended.

# Install all graph dependencies
pip install "mem0ai[graph]"
 
# Install graph and AWS dependencies (for Neptune/Bedrock)
pip install "mem0ai[graph,extras]"
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/examples/graph-db-demo/neptune-example.ipynb#L27-L30" min=27 max=30 file-path="examples/graph-db-demo/neptune-example.ipynb">Hii</FileRef>

Entity Extraction and Search
The Extraction Pipeline
When m.add() is called with graph memory enabled, the system follows a specific sequence to update the graph.

Extraction: The LLM identifies entities and their types from the provided messages.
Relationship Building: The LLM establishes triples (Source -> Relation -> Destination).
Deduplication: The system uses vector similarity (controlled by threshold) to match new entities with existing ones in the graph.
Update: Obsolete relationships are identified and deleted before new ones are added.
BM25 Reranking
During m.search(), the graph store retrieves potential matches. To improve relevance, the system applies BM25 reranking (using the rank_bm25 library) to ensure the most relevant relationships are returned as context to the LLM.

Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/proxy/main.py#L182-L189" min=182 max=189 file-path="mem0/proxy/main.py">Hii</FileRef>

Configuration Precedence
Graph operations can be configured to use a different LLM than the rest of the memory system. This is useful for using a more powerful model (like GPT-4 or Claude 3.7 Sonnet) for complex extraction while using a cheaper model for standard vector memory.

Graph-Specific LLM: config["graph_store"]["llm"]
Global LLM: config["llm"] (Defined in MemoryConfig)
Default: OpenAI
Sources: <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/configs/base.py#L29-L58" min=29 max=58 file-path="mem0/configs/base.py">Hii</FileRef>, <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/examples/graph-db-demo/neptune-example.ipynb#L65-L71" min=65 max=71 file-path="examples/graph-db-demo/neptune-example.ipynb">Hii</FileRef>

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Graph Store Providers
Supported Providers
Factory Architecture
GraphStoreFactory Implementation
Provider Configuration
Neo4j (Default)
AWS Neptune
Memgraph and Kuzu
Enabling Graph Memory
Installation
Entity Extraction and Search
The Extraction Pipeline
BM25 Reranking
Configuration Precedence
Ask Devin about mem0ai/mem0

Fast

Graph Store Providers | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Entity and Relationship Extraction
Relevant source files
This page documents how Mem0 extracts entities and relationships from natural language text and transforms them into structured graph data. Entity and relationship extraction is powered by LLM tool calling and occurs when graph memory is enabled.

For information about configuring graph stores and enabling graph memory, see 4.2 Graph Store Providers. For information about querying the extracted graph data, see 4.4 Graph Search and Retrieval.

Purpose and Scope
Entity and relationship extraction is the process of transforming unstructured conversation text into structured knowledge graphs. The system:

Identifies named entities (people, places, concepts) and their types.
Establishes directional relationships between entities.
Sanitizes text for safe Cypher query construction.
Maintains session scoping with user_id, agent_id, and run_id.
This extraction happens automatically during Memory.add() operations when graph_store.config is configured in the MemoryConfig 
mem0/memory/main.py
199-206

Extraction Pipeline Overview
The extraction pipeline consists of several stages that transform raw text into graph nodes and edges. In the MemoryGraph class (or its provider-specific implementations), the add() method orchestrates the flow 
mem0/memory/graph_memory.py
76-94












Entity and Relationship Extraction Flow

Sources: 
mem0/memory/graph_memory.py
76-94

Entity Extraction
Entity extraction identifies all entities mentioned in the input text and assigns them semantic types. The _retrieve_nodes_from_data() method uses LLM tool calling to perform this extraction 
mem0/memory/graph_memory.py
196-227

Entity Extraction Process








Entity Extraction Using LLM Tool Calling

Sources: 
mem0/memory/graph_memory.py
196-227

Entity Types and Self-References
The system automatically handles self-references in user messages. When the text contains "I", "me", "my", etc., the LLM is instructed to use the user_id from filters as the source entity 
mem0/memory/graph_memory.py
205

Example:

Input: "I love playing chess"
filters = {"user_id": "alice"}
Extracted entities: {"alice": "person", "chess": "game"}
The system prompt explicitly instructs the LLM:

"If user message contains self reference such as 'I', 'me', 'my' etc. then use {filters['user_id']} as the source entity." 
mem0/memory/graph_memory.py
205

Entity Normalization
All extracted entities undergo normalization before storage to ensure consistency across the graph 
mem0/memory/graph_memory.py
225
:

Original Entity    Normalized Entity
"Alice Smith"    "alice_smith"
"New York"    "new_york"
"Machine Learning"    "machine_learning"
Sources: 
mem0/memory/graph_memory.py
225

Relationship Extraction
After entities are identified, the system establishes directional relationships between them. The _establish_nodes_relations_from_data() method performs this extraction 
mem0/memory/graph_memory.py
229-269

Relationship Extraction Process








Relationship Extraction Process

Sources: 
mem0/memory/graph_memory.py
229-269

User Identity Composition
The system builds a user identity string that includes available session identifiers to ensure extracted relationships are properly scoped 
mem0/memory/graph_memory.py
232-237
:

user_identity = f"user_id: {filters['user_id']}"
if filters.get("agent_id"):
    user_identity += f", agent_id: {filters['agent_id']}"
if filters.get("run_id"):
    user_identity += f", run_id: {filters['run_id']}"
Sources: 
mem0/memory/graph_memory.py
232-237

Custom Prompts
If config.graph_store.custom_prompt is configured, it is inserted into the extraction prompt as an additional instruction 
mem0/memory/graph_memory.py
239-242
:

if self.config.graph_store.custom_prompt:
    system_content = EXTRACT_RELATIONS_PROMPT.replace("USER_ID", user_identity)
    system_content = system_content.replace("CUSTOM_PROMPT", 
                                           f"4. {self.config.graph_store.custom_prompt}")
Sources: 
mem0/memory/graph_memory.py
239-242

LLM Tools for Extraction
The extraction process uses LLM function calling with predefined tools. Different tool schemas are used depending on whether the LLM provider supports structured outputs.

Entity Extraction Tools
Tool Name    Provider    Definition
EXTRACT_ENTITIES_TOOL    Standard providers    
mem0/graphs/tools.py
124-150
EXTRACT_ENTITIES_STRUCT_TOOL    azure_openai_structured, openai_structured    
mem0/graphs/tools.py
281-308
Sources: 
mem0/graphs/tools.py
124-150
 
mem0/graphs/tools.py
281-308

Relationship Extraction Tools
Tool Name    Provider    Definition
RELATIONS_TOOL    Standard providers    
mem0/graphs/tools.py
85-121
RELATIONS_STRUCT_TOOL    azure_openai_structured, openai_structured    
mem0/graphs/tools.py
238-278
Sources: 
mem0/graphs/tools.py
85-121
 
mem0/graphs/tools.py
238-278

Data Sanitization
Before storing relationships in graph databases like Neo4j, the system sanitizes text to prevent Cypher syntax errors using sanitize_relationship_for_cypher() 
mem0/memory/utils.py
159-207

Character Mapping








Character Sanitization Process

Sources: 
mem0/memory/utils.py
159-207

Sanitization Character Map
The function maps problematic characters to safe alternatives 
mem0/memory/utils.py
161-207
:

Character    Replacement    Reason
...    _ellipsis_    Cypher syntax conflict
/    _slash_    Path separator
\    _backslash_    Escape character
&    _ampersand_    Operator
*    _asterisk_    Wildcard
(, )    _lparen_, _rparen_    Expression delimiters
Sources: 
mem0/memory/utils.py
161-207

Integration with Memory System
Entity and relationship extraction integrates into the main memory addition flow, typically running in parallel with vector store operations.

Parallel Execution


Parallel Vector and Graph Memory Operations

Sources: 
mem0/memory/main.py
369-384
 
mem0/memory/graph_memory.py
76-94

_add_to_graph Method
The _add_to_graph() method in the Memory class serves as the entry point 
mem0/memory/main.py
599-608
:

def _add_to_graph(self, messages, filters):
    added_entities = []
    if self.enable_graph:
        if filters.get("user_id") is None:
            filters["user_id"] = "user"
        
        data = "\n".join([msg["content"] for msg in messages 
                         if "content" in msg and msg["role"] != "system"])
        added_entities = self.graph.add(data, filters)
    
    return added_entities
Sources: 
mem0/memory/main.py
599-608

Graph Memory Initialization
Graph memory is initialized when graph_store.config is present in MemoryConfig 
mem0/memory/main.py
199-206
 The GraphStoreFactory is used to create the appropriate provider instance 
mem0/utils/factory.py
112-132

self.enable_graph = False
 
if self.config.graph_store.config:
    provider = self.config.graph_store.provider
    self.graph = GraphStoreFactory.create(provider, self.config)
    self.enable_graph = True
Sources: 
mem0/memory/main.py
199-206
 
mem0/utils/factory.py
112-132

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Entity and Relationship Extraction
Purpose and Scope
Extraction Pipeline Overview
Entity Extraction
Entity Extraction Process
Entity Types and Self-References
Entity Normalization
Relationship Extraction
Relationship Extraction Process
User Identity Composition
Custom Prompts
LLM Tools for Extraction
Entity Extraction Tools
Relationship Extraction Tools
Data Sanitization
Character Mapping
Sanitization Character Map
Integration with Memory System
Parallel Execution
_add_to_graph Method
Graph Memory Initialization
Ask Devin about mem0ai/mem0

Fast

Entity and Relationship Extraction | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Graph Search and Retrieval
Relevant source files
This page documents the graph search and retrieval system in Mem0, which enables querying relational knowledge stored in graph databases. Graph search complements vector-based semantic search by traversing entity relationships and ranking results based on graph structure and lexical relevance.

Overview
Graph search in Mem0 executes a multi-stage pipeline:

Entity Extraction: LLM extracts entities from the search query.
Vector Similarity: Each entity is embedded and matched against graph nodes using cosine similarity.
Relationship Retrieval: Cypher queries fetch relationships connected to matching nodes.
BM25 Reranking: Results are reranked using BM25 scoring for relevance.
The search system is implemented within the MemoryGraph class and is integrated into the hybrid search pipeline of the main Memory class.

Graph Search Pipeline











Sources: 
mem0/memory/main.py
832-856
 
mem0/utils/scoring.py
43-48

Search Method
The search functionality is triggered within the Memory.search() method. When a graph store is configured, the system performs a hybrid retrieval by combining results from the vector store and the graph store.

Implementation Flow:

The Memory.search() method validates parameters using _validate_search_params() 
mem0/memory/main.py
144-170
It identifies entities in the query using extract_entities() 
mem0/memory/main.py
35
The system performs semantic search via the vector store 
mem0/memory/main.py
806-810
Concurrently, if self.graph is present, it queries the graph store for related entities and relationships 
mem0/memory/main.py
832-843
Results are reranked using the score_and_rank() utility 
mem0/utils/scoring.py
47-48
The system enforces strict scoping for multi-tenant applications by rejecting top-level entity parameters like user_id or agent_id, requiring them to be passed within the filters dictionary 
mem0/memory/main.py
103-110

Sources: 
mem0/memory/main.py
103-110
 
mem0/memory/main.py
144-170
 
mem0/memory/main.py
832-843

Entity Extraction from Query
The system uses LLM tool calling to extract entities and their types from the search query. This process ensures that natural language references are mapped correctly to identifiers.

Entity Extraction Process








Post-processing: Entity IDs are validated and trimmed using _validate_and_trim_entity_id(), which rejects empty strings or identifiers containing internal whitespace 
mem0/memory/main.py
113-141

Sources: 
mem0/utils/entity_extraction.py
1-35
 
mem0/memory/main.py
113-141

Hybrid Search and BM25 Reranking
Mem0 implements a hybrid search approach that combines semantic (vector) similarity with keyword (BM25) relevance.

BM25 Reranking
The system utilizes lemmatize_for_bm25 to improve matching accuracy by reducing words to their base forms before scoring 
mem0/utils/lemmatization.py
1-20
 The score_and_rank function then combines the vector similarity score with the BM25 score.

BM25 Reranking Process








Sources: 
mem0/utils/lemmatization.py
1-20
 
mem0/utils/scoring.py
43-48
 
mem0/memory/main.py
42-48

Similarity Thresholds
The similarity threshold determines which entities or memories are considered matches. _validate_search_params ensures thresholds are between 0 and 1 (inclusive) and that top_k is a non-negative integer 
mem0/memory/main.py
144-170

Sources: 
mem0/memory/main.py
144-170

Integration with Vector Store Search
The Memory.search() method handles the orchestration between the vector store and graph store. For providers like Qdrant or Milvus, the vector store search includes a keyword component if the collection schema supports it (e.g., the bm25 sparse vector slot in Qdrant 
mem0/vector_stores/qdrant.py
81-86
 or the sparse field in Milvus 
mem0/vector_stores/milvus.py
89-92
).

Concurrent Search Execution







Sources: 
mem0/memory/main.py
832-843
 
mem0/vector_stores/qdrant.py
81-86
 
mem0/vector_stores/milvus.py
89-92

Search Parameters
The search operations utilize a consistent set of parameters:

Parameter    Type    Description
query    str    The natural language query string.
filters    dict    Scoping filters (user_id, agent_id, run_id).
limit    int    Maximum number of results to return.
threshold    float    Similarity threshold (0.0 to 1.0).
Sources: 
mem0/memory/main.py
787-810
 
mem0/memory/main.py
144-170

Utility Functions
format_entities
The format_entities function in mem0/memory/utils.py converts extracted relationship objects into a simplified string format: source -- relationship -- destination.

Sources: 
mem0/memory/utils.py
73-82

lemmatize_for_bm25
Used to preprocess queries and memory text for keyword search, ensuring that variations of words match the same base token.

Sources: 
mem0/utils/lemmatization.py
1-20

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Graph Search and Retrieval
Overview
Search Method
Entity Extraction from Query
Hybrid Search and BM25 Reranking
BM25 Reranking
Similarity Thresholds
Integration with Vector Store Search
Search Parameters
Utility Functions
format_entities
lemmatize_for_bm25
Ask Devin about mem0ai/mem0

Fast

Graph Search and Retrieval | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Similarity Thresholds
Relevant source files
Similarity thresholds control how Mem0's graph memory system determines whether two entities are similar enough to be considered the same node. This threshold-based matching prevents duplicate entities in the knowledge graph while allowing legitimate variations to exist as separate nodes.

Scope: This page covers vector similarity thresholds used specifically in graph memory for entity deduplication and node matching. For information about vector search thresholds in memory retrieval, see Memory Operations. For graph memory architecture overview, see Graph Memory Overview.

Overview
When adding entities to the graph, Mem0 embeds each entity name and compares it against existing nodes using cosine similarity. The similarity threshold determines whether a new entity should reuse an existing node or create a new one. This prevents the graph from filling with near-duplicate nodes like "john_smith", "john_s", and "j_smith" that all refer to the same person.

Default threshold: 0.7 (configurable via graph_store.threshold)

Sources: 
mem0/memory/main.py
155-161
 
mem0/utils/scoring.py
57-65

How Similarity Thresholds Work
The threshold operates on normalized cosine similarity scores between entity embeddings. The system calculates scores in the range [0, 1] (or [-1, 1] depending on the backend) where higher values indicate greater similarity.














Validation Logic

The _validate_search_params function in mem0/memory/main.py ensures that any user-provided threshold is a valid numeric value between 0 and 1.

Sources: 
mem0/memory/main.py
144-161

Threshold Values and Trade-offs
Different threshold values create different behaviors in the memory system:

Threshold    Behavior    Use Case
0.9-1.0    Very strict matching - only near-identical entities merge    High precision needed, entities have strict definitions
0.7-0.9    Balanced matching - similar entities merge    Default - general purpose graph building
0.5-0.7    Lenient matching - loosely similar entities merge    Aggressive deduplication, informal entity names
< 0.5    Very lenient - risk of incorrect merges    Not recommended
Sources: 
mem0/memory/main.py
158-161
 
mem0/utils/scoring.py
60-70

Hybrid Retrieval Scoring
Beyond graph entity matching, Mem0 utilizes thresholds and additive scoring for hybrid retrieval in its vector store layer. This involves combining semantic scores, BM25 scores, and entity boosts.

Additive Scoring Logic
The score_and_rank function in mem0/utils/scoring.py implements the final ranking logic. It applies a threshold to the semantic score before combining it with other signals.
















Adaptive Divisor

The scoring system adapts the divisor based on active signals to keep scores in the [0, 1] range:

Semantic only: max_possible = 1.0
Semantic + BM25: max_possible = 2.0
Semantic + BM25 + Entity: max_possible = 2.5 (Entity boost weight ENTITY_BOOST_WEIGHT is 0.5)
Sources: 
mem0/utils/scoring.py
44-48
 
mem0/utils/scoring.py
57-93
 
mem0/utils/scoring.py
101-110

BM25 Normalization
BM25 scores are raw and unbounded. Mem0 normalizes them to a [0, 1] range using a logistic sigmoid function in normalize_bm25. The parameters for this sigmoid (midpoint and steepness) are dynamically adjusted based on the number of terms in the query.

Query Terms    Midpoint    Steepness
<= 3    5.0    0.7
4 - 6    7.0    0.6
7 - 9    9.0    0.5
10 - 15    10.0    0.5
> 15    12.0    0.5
Sources: 
mem0/utils/scoring.py
16-40
 
mem0/utils/scoring.py
43-54

Implementation in Vector Stores
Different vector stores implement filtering and thresholding using their native query languages.

Qdrant Implementation
Qdrant.search in mem0/vector_stores/qdrant.py uses query_points and constructs a Filter object from the provided metadata filters.

Sources: 
mem0/vector_stores/qdrant.py
214-235
 
mem0/vector_stores/qdrant.py
273-300

Milvus Implementation
MilvusDB.search in mem0/vector_stores/milvus.py converts filters into a string expression (e.g., (metadata["user_id"] == "alice")) and passes it to the MilvusClient.search method.

Sources: 
mem0/vector_stores/milvus.py
139-155
 
mem0/vector_stores/milvus.py
186-218

ChromaDB Implementation
ChromaDB.search in mem0/vector_stores/chroma.py utilizes the where clause for filtering and parses the output using _parse_output to ensure a consistent OutputData format.

Sources: 
mem0/vector_stores/chroma.py
76-107
 
mem0/vector_stores/chroma.py
143-161

Related Pages:

Graph Memory Overview - Graph-based memory concepts
Entity and Relationship Extraction - How entities are extracted
Graph Search and Retrieval - Using BM25 reranking for graph search
Vector Stores Overview - Base interfaces for vector operations
Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Similarity Thresholds
Overview
How Similarity Thresholds Work
Threshold Values and Trade-offs
Hybrid Retrieval Scoring
Additive Scoring Logic
BM25 Normalization
Implementation in Vector Stores
Qdrant Implementation
Milvus Implementation
ChromaDB Implementation
Ask Devin about mem0ai/mem0

Fast

Similarity Thresholds | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Vector Stores Overview
Relevant source files
Vector stores are the primary storage layer for semantic memory in Mem0. They enable fast similarity search over embedding vectors, allowing the memory system to retrieve relevant memories based on semantic meaning rather than exact keyword matches. This page covers the vector store abstraction, factory pattern, and common operations.

For detailed configuration of specific vector store providers, see Vector Store Providers (5.2). For configuration schema and validation, see Vector Store Configuration (5.3).

Purpose in the Memory System
Vector stores in Mem0 serve two critical functions:

Embedding Storage: Store vector embeddings generated from memory content alongside metadata.
Semantic Retrieval: Perform approximate nearest neighbor (ANN) search to find memories similar to a query.
The vector store layer is decoupled from the rest of the memory system through the VectorStoreBase interface 
mem0/vector_stores/base.py
24
 allowing users to choose from over 20 supported providers 
mem0/vector_stores/configs.py
13-38
 based on their deployment requirements, scale, and performance needs.

Sources: 
mem0/vector_stores/base.py
1-24
 
docs/components/vectordbs/overview.mdx
1-37
 
mem0/vector_stores/configs.py
13-38

Architecture Overview
The following diagram illustrates the relationship between the core memory system and the vector store abstraction layer.

System Architecture to Code Entity Mapping
Workflow:

The memory system initializes with a VectorStoreConfig specifying provider and connection details 
mem0/vector_stores/configs.py
6-11
VectorStoreFactory.create() dynamically loads the appropriate provider class using importlib 
mem0/utils/factory.py
1-27
The provider instance implements the VectorStoreBase interface for standardized operations.
Embedders generate vectors which are then passed to the store for insertion or search.
Sources: 
mem0/utils/factory.py
167-206
 
mem0/vector_stores/configs.py
6-68
 
mem0/utils/factory.py
24-27

VectorStoreBase Interface
All vector store implementations inherit from VectorStoreBase 
mem0/vector_stores/base.py
24
 and implement a standard set of operations.

Common Operations
Operation    Description    Implementation Example
create_col    Creates a new collection or index with specific dimensions and metrics.    
mem0/vector_stores/qdrant.py
120-157
insert    Inserts vectors, payloads, and IDs into the store.    
mem0/vector_stores/milvus.py
118-137
search    Performs similarity search with optional metadata filtering.    
mem0/vector_stores/qdrant.py
196-224
delete    Removes a specific vector by its ID.    
mem0/vector_stores/qdrant.py
246-250
update    Updates the vector or payload for an existing ID.    
mem0/vector_stores/qdrant.py
234-244
list_cols    Lists all existing collections in the database.    
mem0/vector_stores/qdrant.py
252-254
Sources: 
mem0/vector_stores/qdrant.py
29-271
 
mem0/vector_stores/milvus.py
25-180
 
mem0/vector_stores/base.py
24

VectorStoreFactory
The VectorStoreFactory implements the factory pattern to dynamically instantiate vector store providers.

Provider Registry
The factory maintains a provider_to_class mapping that associates string identifiers with the full module path of the implementation:

provider_to_class = {
    "qdrant": "mem0.vector_stores.qdrant.Qdrant",
    "chroma": "mem0.vector_stores.chroma.ChromaDB",
    "milvus": "mem0.vector_stores.milvus.MilvusDB",
    # ... over 20 other providers
}
mem0/utils/factory.py
168-192

Creation Logic
When create() is called, the factory:

Resolves the class path from the provider name 
mem0/utils/factory.py
194
Loads the class using importlib.import_module via the load_class helper 
mem0/utils/factory.py
24-27
Converts the configuration (if provided as a dict) into the provider-specific config object 
mem0/utils/factory.py
195-197
Sources: 
mem0/utils/factory.py
167-206
 
mem0/utils/factory.py
24-27

VectorStoreConfig System
The configuration system uses Pydantic for validation and type safety.

Configuration Flow














Key Features:

Dynamic Validation: The validate_and_create_config method imports the specific provider config (e.g., QdrantConfig) and validates the config field against it 
mem0/vector_stores/configs.py
41-67
Default Injection: If no path is provided for local stores, it defaults to /tmp/{provider} 
mem0/vector_stores/configs.py
63-64
Sources: 
mem0/vector_stores/configs.py
6-68
 
mem0/configs/vector_stores/qdrant.py
6-48
 
mem0/configs/vector_stores/chroma.py
6-58

Hybrid Search Support (v3)
Recent implementations like Qdrant and Milvus support hybrid search combining dense semantic vectors with BM25 sparse vectors.

Implementation Details:
Qdrant: Uses fastembed for BM25 encoding 
mem0/vector_stores/qdrant.py
88-101
 and creates a named sparse vector slot bm25 in the collection 
mem0/vector_stores/qdrant.py
146-154
Milvus: Uses a Function of type BM25 to automatically generate sparse vectors from a text field 
mem0/vector_stores/milvus.py
97-103
 It also adds a SPARSE_INVERTED_INDEX for efficient retrieval 
mem0/vector_stores/milvus.py
109-114
Sources: 
mem0/vector_stores/qdrant.py
88-154
 
mem0/vector_stores/milvus.py
84-116

Standard Operation Patterns
Insert Operation
Insertion typically involves preparing data structures specific to the backend (e.g., Qdrant PointStruct or Milvus dictionaries).

Qdrant: insert iterates through vectors and payloads, creating PointStruct objects 
mem0/vector_stores/qdrant.py
178-194
Milvus: insert builds a list of dictionaries, including a text field for BM25 if the schema supports it 
mem0/vector_stores/milvus.py
129-137
Search and Filtering
All search operations support metadata filtering.

Filtering: Filters for user_id, agent_id, and run_id are translated into provider-specific syntax. Qdrant uses Filter and FieldCondition objects 
mem0/vector_stores/qdrant.py
226-244
 Milvus uses boolean expression strings 
mem0/vector_stores/milvus.py
139-155
Scoring: Results are returned as a list of OutputData or similar objects containing the id, score, and payload 
mem0/vector_stores/milvus.py
157-180
 
mem0/vector_stores/chroma.py
17-21
Sources: 
mem0/vector_stores/qdrant.py
178-244
 
mem0/vector_stores/milvus.py
118-180
 
mem0/vector_stores/chroma.py
143-161

Embedding Dimensions
A common configuration point is embedding_model_dims. While many models default to 1536 (OpenAI), users must match this to their specific embedding provider to avoid alignment errors 
docs/components/vectordbs/overview.mdx
47-54
 This is typically passed during initialization of the vector store class 
mem0/vector_stores/qdrant.py
33
 
mem0/vector_stores/milvus.py
31

Sources: 
mem0/configs/vector_stores/qdrant.py
12
 
mem0/vector_stores/milvus.py
41
 
docs/components/vectordbs/overview.mdx
47-54

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Vector Stores Overview
Purpose in the Memory System
Architecture Overview
System Architecture to Code Entity Mapping
VectorStoreBase Interface
Common Operations
VectorStoreFactory
Provider Registry
Creation Logic
VectorStoreConfig System
Configuration Flow
Hybrid Search Support (v3)
Implementation Details:
Standard Operation Patterns
Insert Operation
Search and Filtering
Embedding Dimensions
Ask Devin about mem0ai/mem0

Fast

Vector Stores Overview | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Vector Store Providers
Relevant source files
This document catalogs the supported vector store providers in Mem0's open-source implementation. Vector stores serve as the primary storage backend for embedding vectors, enabling semantic memory search through similarity matching. Mem0 currently supports over 24 implementations, ranging from local lightweight databases to enterprise-grade cloud solutions.

Provider Architecture
Mem0 utilizes a factory pattern to dynamically instantiate vector store implementations. The VectorStoreFactory class maps provider strings to their respective implementation classes, facilitating runtime provider selection based on user configuration.

Factory Pattern and Data Flow
The factory maintains a registry of supported providers. When a Memory instance is initialized, it uses the VectorStoreFactory to load the appropriate class and pass the configuration parameters.


























Sources: 
mem0/utils/factory.py
164-200
 
mem0/vector_stores/base.py
1-20
 
mem0/vector_stores/qdrant.py
29-30
 
mem0/vector_stores/pgvector.py
41-42
 
mem0/vector_stores/faiss.py
127-128

Provider Registry
The VectorStoreFactory.provider_to_class dictionary defines the mapping between configuration strings and implementation modules.

Category    Provider Key    Implementation Class    File Path
Cloud/Remote    qdrant    Qdrant    
mem0/vector_stores/qdrant.py
29
pinecone    PineconeDB    
mem0/vector_stores/pinecone.py
22
mongodb    MongoDB    
mem0/vector_stores/mongodb.py
28
azure_ai_search    AzureAISearch    
mem0/vector_stores/azure_ai_search.py
21
Self-Hosted    pgvector    PGVector    
mem0/vector_stores/pgvector.py
41
milvus    MilvusDB    
mem0/vector_stores/milvus.py
25
chroma    ChromaDB    
mem0/vector_stores/chroma.py
23
elasticsearch    ElasticsearchDB    
mem0/vector_stores/elasticsearch.py
24
opensearch    OpenSearchDB    
mem0/vector_stores/opensearch.py
24
Local/Other    faiss    FAISS    
mem0/vector_stores/faiss.py
127
valkey    ValkeyDB    
mem0/vector_stores/valkey.py
25
databricks    Databricks    
mem0/vector_stores/databricks.py
24
Sources: 
mem0/utils/factory.py
165-189

Implementation Deep Dive
Qdrant (qdrant)
The Qdrant implementation supports both local (on-disk) and remote server modes. It features a sophisticated hybrid search capability using BM25 for keyword matching alongside semantic vector search.

Hybrid Search: It lazy-loads the fastembed library to encode text into sparse vectors for the bm25 slot 
mem0/vector_stores/qdrant.py
88-101
Indexing: Automatically creates payload indexes for user_id, agent_id, run_id, and actor_id to optimize filtering 
mem0/vector_stores/qdrant.py
158-177
Initialization: The __init__ method handles client setup via URL, host/port, or local path 
mem0/vector_stores/qdrant.py
30-76
Persistent Storage: The on_disk flag enables persistent storage for vectors 
mem0/vector_stores/qdrant.py
54-55
Sources: 
mem0/vector_stores/qdrant.py
29-177

PGVector (pgvector)
The PGVector provider utilizes PostgreSQL with the vector extension. It is designed for robustness with connection pooling support.

Driver Support: Dynamically switches between psycopg (v3) with ConnectionPool and psycopg2 with ThreadedConnectionPool 
mem0/vector_stores/pgvector.py
9-26
Indexing Strategies: Supports both HNSW and DiskANN (via vectorscale extension) for high-performance approximate nearest neighbor search 
mem0/vector_stores/pgvector.py
169-181
Context Management: Uses _get_cursor context manager to handle pool check-outs and automatic commits/rollbacks 
mem0/vector_stores/pgvector.py
116-148
Schema: Creates a table with UUID primary key, vector column, and JSONB payload 
mem0/vector_stores/pgvector.py
159-168
Sources: 
mem0/vector_stores/pgvector.py
41-181

Milvus (milvus)
Milvus is used for large-scale vector data. Mem0's implementation leverages Milvus's internal functions for BM25.

BM25 Integration: It defines a Function of type BM25 within the Milvus schema to auto-generate sparse vectors from a text field 
mem0/vector_stores/milvus.py
97-103
Schema: Uses FLOAT_VECTOR for dense embeddings and SPARSE_FLOAT_VECTOR for keyword search 
mem0/vector_stores/milvus.py
84-92
Dynamic Fields: Enables enable_dynamic_field=True for flexible metadata storage 
mem0/vector_stores/milvus.py
94
Sources: 
mem0/vector_stores/milvus.py
25-117

ChromaDB (chroma)
ChromaDB is a popular choice for local development and embedded use cases.

Cloud Support: Includes a dedicated initialization path for chromadb.CloudClient using API keys and tenants 
mem0/vector_stores/chroma.py
48-55
Output Parsing: The _parse_output method flattens Chroma's nested list response into OutputData objects 
mem0/vector_stores/chroma.py
76-107
Persistence: Defaults to a persistent directory at db if no path is provided 
mem0/vector_stores/chroma.py
65-69
Sources: 
mem0/vector_stores/chroma.py
23-107

MongoDB (mongodb)
The MongoDB provider utilizes Atlas Vector Search for high-performance retrieval.

Search Indexes: Automatically creates a vectorSearch index and an Atlas Search text index for keyword matching 
mem0/vector_stores/mongodb.py
65-121
Driver Metadata: Includes Mem0 specific driver information for telemetry 
mem0/vector_stores/mongodb.py
20
Metric Support: Hardcoded to use cosine similarity 
mem0/vector_stores/mongodb.py
30
Sources: 
mem0/vector_stores/mongodb.py
28-126

FAISS (faiss)
FAISS is a library for efficient similarity search and clustering of dense vectors.

Security: Implements a SafeUnpickler to prevent arbitrary code execution during legacy .pkl docstore loading 
mem0/vector_stores/faiss.py
34-61
Migration: Automatically migrates legacy pickle docstores to JSON format for better security and portability 
mem0/vector_stores/faiss.py
168-170
Strategies: Supports euclidean, inner_product, and cosine distance strategies 
mem0/vector_stores/faiss.py
142-143
Sources: 
mem0/vector_stores/faiss.py
127-173

Key Functions and Data Flow
The following diagram illustrates the internal logic for searching memories across different providers, bridging the configuration to the specific class methods.


















Sources: 
mem0/vector_stores/qdrant.py
199-231
 
mem0/vector_stores/pgvector.py
214-263
 
mem0/vector_stores/chroma.py
143-161
 
mem0/vector_stores/mongodb.py
151-180
 
mem0/vector_stores/elasticsearch.py
140-168

Configuration and Validation
Each provider has a specific configuration model (Pydantic) located in mem0/configs/vector_stores/. These models validate input parameters before the factory instantiates the provider.

Config Class    Notable Fields    File Path
ChromaDbConfig    path, host, port, api_key, tenant    
mem0/configs/vector_stores/chroma.py
6
ElasticsearchConfig    cloud_id, api_key, host, port, user, password    
mem0/configs/vector_stores/elasticsearch.py
12
OpenSearchConfig    use_ssl, verify_certs, http_auth, user, password    
mem0/configs/vector_stores/opensearch.py
12
PGVectorConfig    dbname, user, password, diskann, hnsw, sslmode    
mem0/configs/vector_stores/pgvector.py
5
MilvusConfig    url, token, db_name, metric_type    
mem0/configs/vector_stores/milvus.py
16
Sources: 
mem0/configs/vector_stores/chroma.py
6-20
 
mem0/configs/vector_stores/elasticsearch.py
12-40
 
mem0/configs/vector_stores/opensearch.py
12-25
 
mem0/configs/vector_stores/pgvector.py
5-20
 
mem0/configs/vector_stores/milvus.py
16-25

Summary Table of Key Methods
All providers inherit from VectorStoreBase and implement the following interface:

Method    Purpose    Implementation Pattern
insert()    Batch insert vectors and metadata.    Usually involves converting payloads to JSON and calling provider upsert, bulk, or insert_many.
search()    Vector similarity search.    Takes a vector and optional filters; returns OutputData objects with id, score, and payload.
delete()    Remove a specific memory.    Deletes by primary ID or vector ID.
update()    Modify existing memory.    Updates the vector and/or metadata for a specific ID.
create_col()    Setup storage.    Creates tables, collections, or indexes with the correct dimensions and distance metrics.
list_cols()    Audit existing storage.    Lists all available collections or indexes in the database.
Sources: 
mem0/vector_stores/base.py
1-20
 
mem0/vector_stores/qdrant.py
178-231
 
mem0/vector_stores/pgvector.py
183-263
 
mem0/vector_stores/chroma.py
126-141

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Vector Store Providers
Provider Architecture
Factory Pattern and Data Flow
Provider Registry
Implementation Deep Dive
Qdrant (`qdrant`)
PGVector (`pgvector`)
Milvus (`milvus`)
ChromaDB (`chroma`)
MongoDB (`mongodb`)
FAISS (`faiss`)
Key Functions and Data Flow
Configuration and Validation
Summary Table of Key Methods
Ask Devin about mem0ai/mem0

Fast

Vector Store Providers | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Vector Store Configuration
Relevant source files
Purpose and Scope
This document details the configuration system for vector stores in Mem0, including Pydantic-based validation, provider-specific configuration options, connection management strategies, and indexing configurations. For information about available vector store providers and their capabilities, see Vector Store Providers. For details on vector store operations (insert, search, update, delete), see Vector Stores Overview.

Configuration System Overview
Mem0 uses a two-tier configuration system for vector stores:

VectorStoreConfig: A top-level configuration wrapper at 
mem0/vector_stores/configs.py
6-67
 that validates the provider name and delegates to provider-specific configs.
Provider-specific config classes: Pydantic BaseModel classes (e.g., QdrantConfig, ChromaDbConfig, MilvusDBConfig) that enforce provider-specific parameters.
Configuration Flow

















Configuration Flow with VectorStoreConfig

Sources: 
mem0/vector_stores/configs.py
6-67
 
mem0/utils/factory.py
167-201

VectorStoreConfig Class
The VectorStoreConfig class at 
mem0/vector_stores/configs.py
6-67
 serves as the entry point for all vector store configurations:

class VectorStoreConfig(BaseModel):
    provider: str = Field(
        description="Provider of the vector store (e.g., 'qdrant', 'chroma', 'upstash_vector')",
        default="qdrant",
    )
    config: Optional[Dict] = Field(description="Configuration for the specific vector store", default=None)
It maintains a mapping of all 24+ supported providers to their config classes:

Provider    Config Class    File
qdrant    QdrantConfig    
mem0/configs/vector_stores/qdrant.py
chroma    ChromaDbConfig    
mem0/configs/vector_stores/chroma.py
milvus    MilvusDBConfig    
mem0/configs/vector_stores/milvus.py
pgvector    PGVectorConfig    
mem0/configs/vector_stores/pgvector.py
pinecone    PineconeConfig    
mem0/configs/vector_stores/pinecone.py
upstash_vector    UpstashVectorConfig    
mem0/configs/vector_stores/upstash_vector.py
redis    RedisDBConfig    
mem0/configs/vector_stores/redis.py
valkey    ValkeyConfig    
mem0/configs/vector_stores/valkey.py
And 16+ more...        See 
mem0/vector_stores/configs.py
13-38
The validate_and_create_config validator at 
mem0/vector_stores/configs.py
40-67
 dynamically imports and instantiates the appropriate config class based on the provider name.

Sources: 
mem0/vector_stores/configs.py
6-67

VectorStoreFactory
The VectorStoreFactory at 
mem0/utils/factory.py
167-201
 instantiates vector store implementations based on the validated configuration:

class VectorStoreFactory:
    provider_to_class = {
        "qdrant": "mem0.vector_stores.qdrant.Qdrant",
        "chroma": "mem0.vector_stores.chroma.ChromaDB",
        "milvus": "mem0.vector_stores.milvus.MilvusDB",
        # ... 21 more providers
    }
    
    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            vector_store_instance = load_class(class_type)
            return vector_store_instance(**config)
        else:
            raise ValueError(f"Unsupported VectorStore provider: {provider_name}")
Sources: 
mem0/utils/factory.py
167-201

Common Configuration Patterns
Required Fields Validation
All configuration classes enforce required fields and reject extra fields to prevent misconfigurations using a standard validator pattern:

@model_validator(mode="before")
@classmethod
def validate_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = set(cls.model_fields.keys())
    input_fields = set(values.keys())
    extra_fields = input_fields - allowed_fields
    if extra_fields:
        raise ValueError(
            f"Extra fields not allowed: {', '.join(extra_fields)}. Please input only the following fields: {', '.join(allowed_fields)}"
        )
    return values
Sources: 
mem0/configs/vector_stores/qdrant.py
35-46
 
mem0/configs/vector_stores/chroma.py
46-57

Default Values
Configuration classes provide sensible defaults for common parameters:

Parameter    Default Value    Used By
collection_name    "mem0"    All providers
embedding_model_dims    1536    Qdrant, Milvus, PGVector
path    Provider-specific    Qdrant (/tmp/qdrant), ChromaDB (None)
on_disk    False    Qdrant
Sources: 
mem0/configs/vector_stores/qdrant.py
11-19
 
mem0/configs/vector_stores/chroma.py
13-20
 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
31-40

Provider-Specific Configurations
Qdrant Configuration
QdrantConfig supports local, remote server, and cloud deployments. In the TypeScript implementation, QdrantConfig also supports passing a pre-configured QdrantClient instance 
mem0-ts/src/oss/src/vector_stores/qdrant.ts
6-31

Configuration Parameters
Parameter    Type    Description    Default
collection_name    str    Name of the collection    "mem0"
embedding_model_dims    int    Vector dimensions    1536
client    QdrantClient    Existing client instance    None
host    str    Server host address    None
port    int    Server port    None
path    str    Local database path    "/tmp/qdrant"
url    str    Full server URL    None
api_key    str    API key for authentication    None
on_disk    bool    Enable persistent storage    False
The validator check_host_port_or_path at 
mem0/configs/vector_stores/qdrant.py
21-33
 ensures that either path, or host+port, or url+api_key are provided.

Sources: 
mem0/configs/vector_stores/qdrant.py
6-48
 
mem0/vector_stores/qdrant.py
30-41
 
mem0-ts/src/oss/src/vector_stores/qdrant.ts
6-31

PGVector Configuration (TypeScript)
The TypeScript implementation of PGVector provides detailed connection parameters and support for advanced indexing like diskann and hnsw 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
31-40

Parameter    Type    Description
user    string    Database user
password    string    Database password
host    string    Database host
port    number    Database port
dbname    string    Database name (defaults to vector_store)
diskann    boolean    Enable DiskANN indexing
hnsw    boolean    Enable HNSW indexing
Sources: 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
31-40

Supabase Configuration (TypeScript)
SupabaseDB in TypeScript requires a supabaseUrl and supabaseKey, and allows customizing the table and column names 
mem0-ts/src/oss/src/vector_stores/supabase.ts
25-31

Parameter    Type    Description    Default
supabaseUrl    string    Supabase Project URL    Required
supabaseKey    string    Supabase API Key    Required
tableName    string    Table for memories    Required
embeddingColumnName    string    Column for vectors    "embedding"
metadataColumnName    string    Column for metadata    "metadata"
Sources: 
mem0-ts/src/oss/src/vector_stores/supabase.ts
25-31

Hybrid Search and Schema Migration
Qdrant Hybrid Search (v3)
In Mem0 v3, Qdrant implementations automatically attempt to enable hybrid search (Dense + BM25) by creating a bm25 sparse vector slot at 
mem0/vector_stores/qdrant.py
146-154

Migration Handling
For existing collections created prior to v3, the system checks for the presence of the bm25 slot. If missing, it logs a warning and falls back to semantic-only search to maintain compatibility without requiring manual migration 
mem0/vector_stores/qdrant.py
134-142

Milvus Hybrid Search (v3)
Similarly, MilvusDB creates a schema with a text field and a sparse vector field populated via a BM25 Function at 
mem0/vector_stores/milvus.py
84-116

Migration Handling
If an existing collection lacks the text or sparse fields, MilvusDB sets _has_bm25_schema = False and disables hybrid scoring for that specific collection 
mem0/vector_stores/milvus.py
72-82

Sources: 
mem0/vector_stores/qdrant.py
120-157
 
mem0/vector_stores/milvus.py
58-116

Connection Management
PGVector Initialization (TypeScript)
The PGVector implementation follows a two-stage connection strategy: first connecting to the default postgres database to check/create the target database, then reconnecting to the target database to initialize the vector extension and tables 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
82-125













PGVector Initialization Flow (TypeScript)

Sources: 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
82-125

Qdrant Client Initialization Flow
Qdrant.__init__() implements a flexible priority system for client setup:
















Qdrant Client Initialization Flow

Sources: 
mem0/vector_stores/qdrant.py
57-76

Validation and Error Handling
Default Path Assignment
VectorStoreConfig automatically assigns a default temporary path if a provider requires a path parameter but none was provided by the user (e.g., /tmp/qdrant) 
mem0/vector_stores/configs.py
62-64

Custom Dimensions Error
A common configuration issue occurs when using embedding models with dimensions other than the default (1536). This results in a ValueError during search or insert: ValueError: shapes (0,1536) and (768,) not aligned. Resolution: Explicitly set embedding_model_dims (Python) or embeddingModelDims (TypeScript) in the vector store config 
docs/components/vectordbs/overview.mdx
47-54

Sources: 
mem0/vector_stores/configs.py
62-67
 
docs/components/vectordbs/overview.mdx
47-54
 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
31-40

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Vector Store Configuration
Purpose and Scope
Configuration System Overview
Configuration Flow
VectorStoreConfig Class
VectorStoreFactory
Common Configuration Patterns
Required Fields Validation
Default Values
Provider-Specific Configurations
Qdrant Configuration
Configuration Parameters
PGVector Configuration (TypeScript)
Supabase Configuration (TypeScript)
Hybrid Search and Schema Migration
Qdrant Hybrid Search (v3)
Migration Handling
Milvus Hybrid Search (v3)
Migration Handling
Connection Management
PGVector Initialization (TypeScript)
Qdrant Client Initialization Flow
Validation and Error Handling
Default Path Assignment
Custom Dimensions Error
Ask Devin about mem0ai/mem0

Fast

Vector Store Configuration | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
History and Audit Trails
Relevant source files
This document describes Mem0's history and audit trail system, which provides a complete, immutable log of all memory modifications. The history system tracks every add, update, and delete operation performed on memories, enabling auditability, debugging, and temporal analysis of memory changes.

For information about vector store backends, see 
Vector Stores Overview
 For details on memory operations that generate history records, see 
Memory Operations

Purpose and Architecture
The history system is implemented through the SQLiteManager class in 
mem0/memory/storage.py
11-219
 which maintains an SQLite database containing an immutable audit trail of all memory modifications. Every write operation (ADD, UPDATE, DELETE) to the memory system automatically generates a corresponding history record with full metadata about the change.

In the TypeScript implementation, this role is fulfilled by the HistoryManager interface and its concrete implementations like SQLiteHistoryManager (aliased or used via HistoryManagerFactory) 
mem0-ts/src/oss/src/memory/index.ts
16-28

System Data Flow
The following diagram bridges the Natural Language operations (adding/updating memories) to the Code Entities responsible for persistence.

















Sources: 
mem0/memory/storage.py
11-219
 
mem0/memory/main.py
26
 
mem0-ts/src/oss/src/memory/index.ts
168-175

SQLiteManager Class
The SQLiteManager class provides thread-safe access to the history database. It is initialized with a database path and creates the necessary schema on startup 
mem0/memory/storage.py
11-19

Initialization and Thread Safety
The SQLiteManager constructor accepts a db_path parameter, defaulting to ":memory:" 
mem0/memory/storage.py
12-13
 It initializes a threading.Lock to handle concurrent access from multiple threads 
mem0/memory/storage.py
15



All database operations acquire self._lock before executing, preventing race conditions in multi-threaded environments 
mem0/memory/storage.py
163-187

Sources: 
mem0/memory/storage.py
12-187

Schema Definitions
History Table
The history table uses the following schema 
mem0/memory/storage.py
108-119
:

Column    Type    Description
id    TEXT PRIMARY KEY    Unique identifier for the history record (UUID)
memory_id    TEXT    ID of the memory that was modified
old_memory    TEXT    Previous content of the memory (NULL for ADD)
new_memory    TEXT    New content of the memory (NULL for DELETE)
event    TEXT    Type of operation: "ADD", "UPDATE", "DELETE"
created_at    DATETIME    Timestamp when the record was created
updated_at    DATETIME    Timestamp when the record was updated
is_deleted    INTEGER    Flag (0 or 1) indicating deletion status
actor_id    TEXT    ID of the entity performing the operation
role    TEXT    Role of the actor (user/agent/system)
Messages Table
The messages table tracks the conversation context used for fact extraction 
mem0/memory/storage.py
128-148

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_scope TEXT,
    role TEXT,
    content TEXT,
    name TEXT,
    created_at DATETIME
)
Sources: 
mem0/memory/storage.py
108-142

Temporal Queries and Operations
Adding Records
The add_history() method creates new audit trail entries. It is called by memory operations when memories are added, updated, or deleted 
mem0/memory/storage.py
150-191

# Called by Memory.update() in main.py
self.db.add_history(
    memory_id=memory_id,
    old_memory=old_text,
    new_memory=new_text,
    event="UPDATE",
    actor_id=user_id,
    # ...
)
Retrieving History
The get_history() method retrieves the complete history for a specific memory, ordered chronologically 
mem0/memory/storage.py
224-244

SELECT id, memory_id, old_memory, new_memory, event,
       created_at, updated_at, is_deleted, actor_id, role
FROM history
WHERE memory_id = ?
ORDER BY created_at ASC, DATETIME(updated_at) ASC
Sources: 
mem0/memory/storage.py
150-232

Migration System
The SQLiteManager includes automatic schema migration to handle upgrades. The _migrate_history_table() method detects if a pre-existing table has old "group-chat" columns and migrates the data to the new schema 
mem0/memory/storage.py
20-100













Sources: 
mem0/memory/storage.py
20-100

Integration in TypeScript (OSS)
The TypeScript SDK follows a similar pattern but uses a factory for the history manager 
mem0-ts/src/oss/src/memory/index.ts
16-28
 If disableHistory is set in the config, a DummyHistoryManager is used instead of the standard SQLite-backed store 
mem0-ts/src/oss/src/memory/index.ts
168-175

In MemoryVectorStore (SQLite-based vector store), a separate memory_migrations table is maintained to track schema versions for the vector payloads themselves 
mem0-ts/src/oss/src/vector_stores/memory.ts
69-73

TypeScript Implementation Mapping













Sources: 
mem0-ts/src/oss/src/memory/index.ts
168-175
 
mem0-ts/src/oss/src/vector_stores/memory.ts
69-73

Summary of Key Classes
Class    Language    Responsibility
SQLiteManager    Python    Manages history and message tables in SQLite 
mem0/memory/storage.py
11
HistoryManagerFactory    TS    Instantiates the appropriate history provider 
mem0-ts/src/oss/src/memory/index.ts
171
DummyHistoryManager    TS    No-op history manager for disabled tracking 
mem0-ts/src/oss/src/memory/index.ts
169
MemoryVectorStore    TS    SQLite-based vector storage with its own migration table 
mem0-ts/src/oss/src/vector_stores/memory.ts
17
Sources: 
mem0/memory/storage.py
11
 
mem0-ts/src/oss/src/memory/index.ts
168-175
 
mem0-ts/src/oss/src/vector_stores/memory.ts
17

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
History and Audit Trails
Purpose and Architecture
System Data Flow
SQLiteManager Class
Initialization and Thread Safety
Schema Definitions
History Table
Messages Table
Temporal Queries and Operations
Adding Records
Retrieving History
Migration System
Integration in TypeScript (OSS)
TypeScript Implementation Mapping
Summary of Key Classes
Ask Devin about mem0ai/mem0

Fast

History and Audit Trails | mem0ai/mem0 | DeepWiki
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
Syntax error in text
mermaid version 11.12.3
1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
LLM Providers
Relevant source files
This page documents the Large Language Model (LLM) provider integrations in Mem0's open source deployment. LLM providers are used by the Memory class to extract facts from messages, determine memory update operations (ADD, UPDATE, DELETE), and perform intelligent memory consolidation. Mem0 supports 18+ LLM providers through a unified abstraction layer based on the factory pattern.

For information about embedding model providers, see Embedding Providers. For general LLM configuration guidelines, see LLM Configuration.

Architecture Overview
LLM providers in Mem0 follow a factory-based architecture where LlmFactory dynamically instantiates provider-specific implementations based on configuration. All providers inherit from LLMBase and implement a standard generate_response() method.

Diagram: LLM Provider Factory Architecture
























Sources: 
mem0/llms/base.py
11-18
 
mem0/llms/openai.py
14-36
 
mem0/llms/aws_bedrock.py
34-64
 
mem0/llms/ollama.py
15-36

Base Abstractions
LLMBase Class
All LLM providers inherit from LLMBase 
mem0/llms/base.py
11-14
 It defines the core interface:

generate_response(): The primary method for text generation and tool calling 
mem0/llms/base.py
36-47
_get_supported_params(): Filters valid parameters for the specific model to prevent API errors by inspecting the provider's generate_response signature 
mem0/llms/base.py
49-65
BaseLlmConfig Class
BaseLlmConfig provides common parameters like model, temperature, api_key, max_tokens, top_p, and top_k 
mem0/configs/llms/base.py
7-34

Key Provider Implementations
OpenAI & OpenRouter
The OpenAILLM class supports native OpenAI, Azure OpenAI (via separate class), and OpenRouter 
mem0/llms/openai.py
14-15

OpenRouter: If OPENROUTER_API_KEY is present in the environment, the client is initialized with the OpenRouter base URL 
mem0/llms/openai.py
41-47
Reasoning Models: Supports reasoning_effort for models like o3-mini 
mem0/llms/openai.py
32
 
tests/llms/test_openai.py
173-175
Tool Parsing: Implements _parse_response to extract content and tool calls from the OpenAI choice structure 
mem0/llms/openai.py
54-82
Diagram: OpenAI Request Flow



Sources: 
mem0/llms/openai.py
84-149
 
mem0/llms/openai.py
54-82

AWS Bedrock
AWSBedrockLLM supports a wide range of providers including Anthropic, Meta, Mistral, and Cohere 
mem0/llms/aws_bedrock.py
19-23

Initialization: Initializes a bedrock-runtime client using boto3 
mem0/llms/aws_bedrock.py
77-83
Provider Detection: Automatically detects the underlying provider from the model ID string 
mem0/llms/aws_bedrock.py
26-31
Capability Mapping: Determines if the model supports tools, vision, or streaming based on the provider 
mem0/llms/aws_bedrock.py
120-129
Sources: 
mem0/llms/aws_bedrock.py
34-75
 
mem0/llms/aws_bedrock.py
120-144

Azure OpenAI
AzureOpenAILLM handles integration with Azure's OpenAI service 
mem0/llms/azure_openai.py
16

Authentication: Supports both API Keys and DefaultAzureCredential for Entra ID (formerly Azure AD) authentication 
mem0/llms/azure_openai.py
51-59
Structured Outputs: AzureOpenAIStructuredLLM uses the .parse() method for guaranteed JSON schemas 
mem0/llms/azure_openai_structured.py
15-57
Reasoning Support: Supports reasoning_effort for Azure deployments of reasoning models 
mem0/llms/azure_openai.py
34
 
tests/llms/test_azure_openai.py
138-141
Sources: 
mem0/llms/azure_openai.py
16-69
 
mem0/llms/azure_openai_structured.py
15-57

Ollama (Local)
OllamaLLM provides integration for locally hosted models 
mem0/llms/ollama.py
15

Configuration: Maps standard parameters like max_tokens to Ollama's num_predict 
mem0/llms/ollama.py
129-133
JSON Format: When response_format is set to json_object, it passes format="json" to the Ollama client and appends a fallback instruction to the user prompt 
mem0/llms/ollama.py
120-126
Sources: 
mem0/llms/ollama.py
15-41
 
mem0/llms/ollama.py
113-143

vLLM
VllmLLM uses the OpenAI-compatible server provided by vLLM 
mem0/llms/vllm.py
13

Client: Uses the standard openai.OpenAI client pointing to the vLLM base URL 
mem0/llms/vllm.py
41
Default Model: Defaults to Qwen/Qwen2.5-32B-Instruct 
mem0/llms/vllm.py
37
Sources: 
mem0/llms/vllm.py
13-41
 
mem0/llms/vllm.py
94-109

Supported Providers List
Provider    Class    Default Model    Source
OpenAI    OpenAILLM    gpt-5-mini    
mem0/llms/openai.py
39
Anthropic    AnthropicLLM    claude-3-5-sonnet-20240620    
mem0/llms/anthropic.py
AWS Bedrock    AWSBedrockLLM    Config Dependent    
mem0/llms/aws_bedrock.py
34
Ollama    OllamaLLM    llama3.1:70b    
mem0/llms/ollama.py
39
Groq    GroqLLM    llama-3-3-70b-versatile    
mem0/llms/groq.py
20
Azure OpenAI    AzureOpenAILLM    gpt-5-mini    
mem0/llms/azure_openai.py
42
Together    TogetherLLM    mistralai/Mixtral-8x7B-Instruct-v0.1    
mem0/llms/together.py
20
vLLM    VllmLLM    Qwen/Qwen2.5-32B-Instruct    
mem0/llms/vllm.py
37
Response Callbacks
The OpenAI provider (and others using its base) supports a response_callback 
mem0/llms/openai.py
142
 This allows developers to hook into the generation process to capture raw responses, token usage, or latency metrics 
mem0/llms/openai.py
144
 
tests/llms/test_openai.py
109-124

Sources: 
mem0/llms/openai.py
142-149
 
tests/llms/test_openai.py
109-131

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
LLM Providers
Architecture Overview
Base Abstractions
LLMBase Class
BaseLlmConfig Class
Key Provider Implementations
OpenAI & OpenRouter
AWS Bedrock
Azure OpenAI
Ollama (Local)
vLLM
Supported Providers List
Response Callbacks
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

https://deepwiki.com/mem0ai/mem0/6.2-llm-configuration

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
LLM Configuration
Relevant source files
This document covers the LLM configuration system in Mem0, including the base configuration class, provider-specific settings, tool calling, and response handling. It focuses on how to configure and customize Large Language Model providers for use within the Mem0 memory system.

Configuration Architecture
The LLM configuration system in Mem0 follows a hierarchical structure with a base configuration class that defines common parameters, while provider-specific implementations extend this for specialized settings.

Configuration Class Hierarchy











































Sources: 
mem0/configs/llms/base.py
7-68
 
mem0/configs/llms/openai.py
6-88
 
mem0/llms/configs.py
6-36
 
mem0/llms/base.py
7-142
 
mem0/llms/openai.py
14-150
 
mem0/llms/xai.py
10-53

Base LLM Configuration Parameters
The BaseLlmConfig class provides common parameters that apply across all LLM providers. These parameters control fundamental aspects of model behavior and connection settings.

Core Parameters
Parameter    Type    Default    Description
model    str    None    Model identifier (e.g., "gpt-4o-mini", "claude-3-5-sonnet-20240620")
temperature    float    0.1    Controls randomness (0.0-2.0)
api_key    str    None    API key for the provider
max_tokens    int    2000    Maximum tokens to generate (1-4096)
top_p    float    0.1    Nucleus sampling parameter (0.0-1.0)
top_k    int    1    Top-k sampling parameter (1-40)
enable_vision    bool    False    Enable vision capabilities
vision_details    str    "auto"    Vision processing level ("low", "high", "auto")
reasoning_effort    str    None    Effort level for reasoning models ("low", "medium", "high")
http_client_proxies    dict/str    None    Proxy settings for the internal httpx.Client
The BaseLlmConfig initializes an httpx.Client if http_client_proxies are provided 
mem0/configs/llms/base.py
67

Sources: 
mem0/configs/llms/base.py
16-68

Provider Configuration System
The LlmConfig class validates and manages provider-specific configurations using Pydantic.

Configuration Structure





















Sources: 
mem0/llms/configs.py
6-36

Provider-Specific Configuration Parameters
OpenAI and OpenRouter Configuration
The OpenAIConfig class extends BaseLlmConfig with specialized parameters for OpenAI, OpenRouter, and monitoring.

Parameter    Type    Default    Description
openai_base_url    str    None    Custom OpenAI API base URL
models    List[str]    None    List of models for OpenRouter routing
route    str    "fallback"    OpenRouter routing strategy
openrouter_base_url    str    None    OpenRouter API base URL
site_url    str    None    Site URL for OpenRouter headers
app_name    str    None    Application name for OpenRouter headers
store    bool    None    Whether to store conversation on OpenAI's server (Opt-in)
response_callback    Callable    None    Function to monitor LLM responses
The store parameter is explicitly handled to avoid leaking unknown fields into OpenAI-compatible backends like Gemini or Groq 
mem0/llms/openai.py
129-133

Sources: 
mem0/configs/llms/openai.py
12-87
 
mem0/llms/openai.py
112-133

Tool Calling and Response Handling
Mem0 implements a standardized way to handle LLM responses, especially when tool calling (function calling) is involved.

Response Data Flow


Tool Call Parsing
In OpenAILLM._parse_response, if tools are present, the response is structured into a dictionary containing content and a list of tool_calls. Each tool call includes the function name and parsed arguments 
mem0/llms/openai.py
65-80

Reasoning Models Support
The LLMBase class includes logic to filter parameters for reasoning models (e.g., o1, o3, gpt-5). These models often do not support parameters like temperature or top_p 
mem0/llms/base.py
43-102

_is_reasoning_model: Detects models by name prefix (e.g., o1-, o3-) 
mem0/llms/base.py
43-70
_get_supported_params: Filters out common parameters for reasoning models, keeping only messages, response_format, tools, tool_choice, and reasoning_effort 
mem0/llms/base.py
85-102
Sources: 
mem0/llms/openai.py
54-82
 
mem0/llms/base.py
43-105
 
mem0/llms/openai.py
141-149

Configuration Validation and Precedence
Value Precedence Rules
Config values are resolved in the following order:

Explicit values: Set in the config dictionary passed to the constructor 
docs/components/llms/config.mdx
30
Environment variables: e.g., OPENAI_API_KEY or OPENAI_BASE_URL 
docs/components/llms/config.mdx
31
Defaults: Defined within the specific LLM implementation (e.g., OpenAILLM defaults to gpt-5-mini if no model is provided) 
mem0/llms/openai.py
38-39
Implementation Example: OpenAI
The OpenAILLM class handles complex initialization logic, checking for OpenRouter specific keys before falling back to standard OpenAI variables 
mem0/llms/openai.py
41-52

# From mem0/llms/openai.py:41-52
if os.environ.get("OPENROUTER_API_KEY"):  # Use OpenRouter
    self.client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url=self.config.openrouter_base_url
        or os.getenv("OPENROUTER_API_BASE")
        or "https://openrouter.ai/api/v1",
    )
else:
    api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
    base_url = self.config.openai_base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    self.client = OpenAI(api_key=api_key, base_url=base_url)
Sources: 
docs/components/llms/config.mdx
26-34
 
mem0/llms/openai.py
15-52
 
mem0/configs/llms/base.py
16-68

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
LLM Configuration
Configuration Architecture
Configuration Class Hierarchy
Base LLM Configuration Parameters
Core Parameters
Provider Configuration System
Configuration Structure
Provider-Specific Configuration Parameters
OpenAI and OpenRouter Configuration
Tool Calling and Response Handling
Response Data Flow
Tool Call Parsing
Reasoning Models Support
Configuration Validation and Precedence
Value Precedence Rules
Implementation Example: OpenAI
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.


DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Embedding Providers
Relevant source files
This page documents the embedding providers supported by Mem0, their architecture, and how they integrate into the memory system. Embedding providers convert text into high-dimensional vectors that enable semantic search capabilities.

Architecture Overview
Mem0's embedding system uses a factory pattern to support multiple embedding providers through a common interface. All embedders inherit from EmbeddingBase and implement the embed() method.

Base Classes and Factory
Sources: 
mem0/embeddings/base.py
1-32
 
mem0/configs/embeddings/base.py
10-111
 
mem0/embeddings/openai.py
11-12
 
mem0/embeddings/huggingface.py
15-16

EmbeddingBase Abstract Class
All embedding providers inherit from EmbeddingBase, which defines the contract for embedding implementations:

class EmbeddingBase(ABC):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None)
    
    @abstractmethod
    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]])
The embed() method accepts a memory_action parameter that allows providers to use different embedding strategies for different operations (add, search, or update).

Sources: 
mem0/embeddings/base.py
7-32

Supported Providers
Cloud-Based Providers
OpenAI
Default Model: text-embedding-3-small 
mem0/embeddings/openai.py
15
Default Dimensions: 1536 
mem0/embeddings/openai.py
19
Key Features: Supports Matryoshka embeddings via customizable dimensions. Dimensions are only passed to the API if explicitly set by the user to maintain compatibility with non-matryoshka backends 
mem0/embeddings/openai.py
16-18
API Key: OPENAI_API_KEY environment variable or config parameter 
mem0/embeddings/openai.py
21
The implementation automatically chunks batch requests into groups of 100 to stay within API limits 
mem0/embeddings/openai.py
62-66

Sources: 
mem0/embeddings/openai.py
11-76
 
tests/embeddings/test_openai_embeddings.py
112-125

Google Gemini (Google AI)
Default Model: models/gemini-embedding-001 
mem0/embeddings/gemini.py
15
Default Dimensions: 768 
mem0/embeddings/gemini.py
16
Client: Uses google.genai.Client 
mem0/embeddings/gemini.py
20
Special Parameters: Supports output_dimensionality via types.EmbedContentConfig 
mem0/embeddings/gemini.py
34-37
Sources: 
mem0/embeddings/gemini.py
11-40

Vertex AI
Default Model: gemini-embedding-001 
mem0/embeddings/vertexai.py
15
Authentication: Uses GCPAuthenticator for centralized Google Cloud authentication 
mem0/embeddings/vertexai.py
27-31
Task-Specific Embeddings: Supports specialized embedding types based on the memory operation:
add/update: RETRIEVAL_DOCUMENT 
mem0/embeddings/vertexai.py
19-20
search: RETRIEVAL_QUERY 
mem0/embeddings/vertexai.py
21
Task Type Mapping: Maps memory_action to task_type in TextEmbeddingInput 
mem0/embeddings/vertexai.py
54-61
Sources: 
mem0/embeddings/vertexai.py
11-64
 
tests/embeddings/test_vertexai_embeddings.py
91-115

Local and Self-Hosted Providers
Ollama
Default Model: nomic-embed-text 
mem0/embeddings/ollama.py
28
Default Dimensions: 512 
mem0/embeddings/ollama.py
29
Automatic Management: Checks if the model exists locally via self.client.list() and pulls it if missing via self.client.pull() 
mem0/embeddings/ollama.py
38-49
TypeScript Implementation: Includes a defensive check to ensure input is a string before calling the Ollama client 
mem0-ts/src/oss/src/embeddings/ollama.ts
31-35
Sources: 
mem0/embeddings/ollama.py
24-66
 
mem0-ts/src/oss/src/embeddings/ollama.ts
6-70

Hugging Face
Modes: Supports both local execution via sentence_transformers and remote TEI (Text Embeddings Inference) via an OpenAI-compatible client 
mem0/embeddings/huggingface.py
19-25
Local Mode: Uses SentenceTransformer with a default of multi-qa-MiniLM-L6-cos-v1. It automatically sets embedding_dims by querying the model dimension 
mem0/embeddings/huggingface.py
23-27
TEI Mode: Triggered by setting huggingface_base_url, uses openai.OpenAI client 
mem0/embeddings/huggingface.py
19-21
Sources: 
mem0/embeddings/huggingface.py
15-44
 
tests/embeddings/test_huggingface_embeddings.py
75-103

Implementation Details
Data Flow: Text to Vector Space
The following diagram illustrates how natural language input flows through the code entities to produce a vector.



Sources: 
mem0/embeddings/openai.py
37-55
 
mem0/embeddings/base.py
21-32
 
tests/embeddings/test_openai_embeddings.py
17-30

Dual-Mode Support (HuggingFace)
The HuggingFace provider dynamically switches between local library calls and network API calls based on the presence of a huggingface_base_url.
















Sources: 
mem0/embeddings/huggingface.py
16-44
 
tests/embeddings/test_huggingface_embeddings.py
18-27
 
tests/embeddings/test_huggingface_embeddings.py
75-103

Batch Processing
OpenAI and Ollama (TypeScript) providers support batch operations to optimize network overhead.

Feature    Implementation    File
Batch Size    100 texts per chunk    
mem0/embeddings/openai.py
62
Normalization    Replaces \n with space    
mem0/embeddings/openai.py
63
Ordering    Sorted by response index    
mem0/embeddings/openai.py
75
TS Batching    Uses Promise.all for mapping    
mem0-ts/src/oss/src/embeddings/ollama.ts
44-47
Sources: 
mem0/embeddings/openai.py
57-76
 
mem0-ts/src/oss/src/embeddings/openai.ts
30-49

Configuration Parameters
Configuration is managed via BaseEmbedderConfig, which centralizes parameters for all providers.

Parameter    Purpose    Provider
model    Model identifier    All
api_key    Authentication token    Cloud providers
embedding_dims    Vector size    OpenAI, Vertex, Gemini, HF
ollama_base_url    Local server address    Ollama
huggingface_base_url    TEI endpoint address    HuggingFace
vertex_credentials_json    Path to GCP service account    VertexAI
http_client_proxies    Routing via corporate proxy    Azure/General
Sources: 
mem0/configs/embeddings/base.py
10-111
 
mem0/embeddings/openai.py
18-27

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Embedding Providers
Architecture Overview
Base Classes and Factory
EmbeddingBase Abstract Class
Supported Providers
Cloud-Based Providers
OpenAI
Google Gemini (Google AI)
Vertex AI
Local and Self-Hosted Providers
Ollama
Hugging Face
Implementation Details
Data Flow: Text to Vector Space
Dual-Mode Support (HuggingFace)
Batch Processing
Configuration Parameters
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.
Syntax error in text
mermaid version 11.12.3

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Embeddings Configuration
Relevant source files
This document covers configuration options for embedding models in Mem0, focusing on the BaseEmbedderConfig class and provider-specific parameters. For information about available embedding providers and the EmbeddingBase interface, see Embedding Providers. For LLM configuration, see LLM Configuration.

Overview
Embedding configuration in Mem0 is managed through the BaseEmbedderConfig class, which provides a unified configuration interface for all embedding providers. The configuration system supports 11+ embedding providers with provider-specific parameters while maintaining a consistent API surface.

The configuration is passed to embedding implementations through the EmbeddingBase constructor and determines model selection, API authentication, embedding dimensions, and provider-specific behaviors.

Sources: 
mem0/configs/embeddings/base.py
10-111
 
mem0/embeddings/base.py
1-32

BaseEmbedderConfig Class
Configuration Class Diagram














































Sources: 
mem0/configs/embeddings/base.py
10-111
 
mem0/embeddings/base.py
7-32
 
mem0/embeddings/openai.py
11-35
 
mem0/embeddings/huggingface.py
15-28
 
mem0/embeddings/ollama.py
24-32
 
mem0/embeddings/gemini.py
11-20

Constructor Parameters
The BaseEmbedderConfig constructor initializes a configuration instance with the following parameters:

Parameter    Type    Default    Description
model    Optional[str]    None    Embedding model identifier
api_key    Optional[str]    None    API key for authentication
embedding_dims    Optional[int]    None    Vector dimensionality
ollama_base_url    Optional[str]    None    URL for Ollama API
openai_base_url    Optional[str]    None    URL for OpenAI-compatible API
model_kwargs    Optional[dict]    {}    Arguments for HuggingFace SentenceTransformer
huggingface_base_url    Optional[str]    None    URL for HuggingFace TEI
azure_kwargs    Optional[AzureConfig]    {}    Azure OpenAI specific configuration
http_client_proxies    Optional[Union[Dict, str]]    None    Proxy settings for httpx.Client
vertex_credentials_json    Optional[str]    None    Vertex AI credentials path
memory_add_embedding_type    Optional[str]    None    Task type for memory addition
memory_update_embedding_type    Optional[str]    None    Task type for memory updates
memory_search_embedding_type    Optional[str]    None    Task type for memory search
output_dimensionality    Optional[str]    None    Dimensionality for Gemini models
lmstudio_base_url    Optional[str]    "http://localhost:1234/v1"    URL for LM Studio
aws_access_key_id    Optional[str]    None    AWS Access Key (Bedrock)
aws_secret_access_key    Optional[str]    None    AWS Secret Key (Bedrock)
aws_region    Optional[str]    None    AWS Region (defaults to env or "us-west-2")
Sources: 
mem0/configs/embeddings/base.py
15-110

Common Configuration Parameters
Model Selection
Providers assign default models if the model parameter is None during initialization:

# OpenAI default [mem0/embeddings/openai.py:15]
self.config.model = self.config.model or "text-embedding-3-small"
 
# HuggingFace default (local) [mem0/embeddings/huggingface.py:23]
self.config.model = self.config.model or "multi-qa-MiniLM-L6-cos-v1"
 
# Ollama default [mem0/embeddings/ollama.py:28]
self.config.model = self.config.model or "nomic-embed-text"
 
# Gemini default [mem0/embeddings/gemini.py:15]
self.config.model = self.config.model or "models/gemini-embedding-001"
Sources: 
mem0/embeddings/openai.py
15
 
mem0/embeddings/huggingface.py
23
 
mem0/embeddings/ollama.py
28
 
mem0/embeddings/gemini.py
15

API Key Management
API keys are resolved with the following precedence:

Explicit api_key in BaseEmbedderConfig
Environment variables (e.g., OPENAI_API_KEY, GOOGLE_API_KEY, AWS_REGION)
Sources: 
mem0/embeddings/openai.py
21
 
mem0/embeddings/gemini.py
18
 
mem0/configs/embeddings/base.py
109

Embedding Dimensions
The embedding_dims parameter controls vector size. Implementation varies by provider:

OpenAI: Passes dimensions to the API if set by user. Defaults to 1536 
mem0/embeddings/openai.py
18-19
HuggingFace: Auto-detected from model.get_sentence_embedding_dimension() if not specified 
mem0/embeddings/huggingface.py
27
Gemini: Uses output_dimensionality if provided, otherwise defaults to 768 
mem0/embeddings/gemini.py
16
Ollama: Defaults to 512 
mem0/embeddings/ollama.py
29
Sources: 
mem0/embeddings/openai.py
18-19
 
mem0/embeddings/huggingface.py
27
 
mem0/embeddings/gemini.py
16
 
mem0/embeddings/ollama.py
29

Configuration Flow
Configuration to Provider Instantiation












Sources: 
mem0/embeddings/configs.py
6-32
 
mem0/embeddings/base.py
14-18
 
mem0/embeddings/openai.py
12-35
 
mem0/embeddings/huggingface.py
16-28

Provider-Specific Configuration
OpenAI Configuration
OpenAI embeddings support custom base URLs and batch processing.

openai_base_url: Resolves from config, then OPENAI_API_BASE (deprecated), then OPENAI_BASE_URL, defaulting to "https://api.openai.com/v1" 
mem0/embeddings/openai.py
22-27
Batching: embed_batch automatically chunks input into batches of 100 to stay within API limits 
mem0/embeddings/openai.py
62
Matryoshka Support: The dimensions parameter is only passed to the API if embedding_dims was explicitly set in config 
mem0/embeddings/openai.py
18
Sources: 
mem0/embeddings/openai.py
11-77

HuggingFace Configuration
Supports two operational modes:

Remote Mode: Uses huggingface_base_url to connect to a Text Embeddings Inference (TEI) endpoint via the OpenAI client 
mem0/embeddings/huggingface.py
19-21
Local Mode: Uses SentenceTransformer to load models locally 
mem0/embeddings/huggingface.py
25
Sources: 
mem0/embeddings/huggingface.py
15-44

Ollama Configuration
Ollama implementation ensures the model exists locally before use:

ollama_base_url: Passed as host to ollama.Client 
mem0/embeddings/ollama.py
31
Auto-Pull: _ensure_model_exists() checks the local model list and pulls the model if missing 
mem0/embeddings/ollama.py
38-49
Sources: 
mem0/embeddings/ollama.py
24-66

Gemini Configuration
Gemini embeddings use the google-genai SDK:

output_dimensionality: Maps to types.EmbedContentConfig 
mem0/embeddings/gemini.py
34
Model Default: models/gemini-embedding-001 
mem0/embeddings/gemini.py
15
Sources: 
mem0/embeddings/gemini.py
11-39

Task-Specific Embeddings
Mem0 supports task-specific embedding types for different memory actions. This is particularly useful for providers like Vertex AI that distinguish between retrieval and storage tasks.

memory_add_embedding_type: Used when adding a memory.
memory_update_embedding_type: Used when updating a memory.
memory_search_embedding_type: Used when searching for memories.
The embed function signature includes a memory_action parameter to facilitate this logic: def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None) 
mem0/embeddings/base.py
21

Sources: 
mem0/configs/embeddings/base.py
32-98
 
mem0/embeddings/base.py
21-31

Validation and Pydantic Schema
The EmbedderConfig class provides high-level validation for the embedding provider using Pydantic's field_validator:

class EmbedderConfig(BaseModel):
    provider: str = Field(
        description="Provider of the embedding model (e.g., 'ollama', 'openai')",
        default="openai",
    )
    config: Optional[dict] = Field(description="Configuration for the specific embedding model", default={})
 
    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in [
            "openai", "ollama", "huggingface", "azure_openai", "gemini",
            "vertexai", "together", "lmstudio", "langchain", "aws_bedrock", "fastembed",
        ]:
            return v
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
Sources: 
mem0/embeddings/configs.py
6-32

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Embeddings Configuration
Overview
BaseEmbedderConfig Class
Configuration Class Diagram
Constructor Parameters
Common Configuration Parameters
Model Selection
API Key Management
Embedding Dimensions
Configuration Flow
Configuration to Provider Instantiation
Provider-Specific Configuration
OpenAI Configuration
HuggingFace Configuration
Ollama Configuration
Gemini Configuration
Task-Specific Embeddings
Validation and Pydantic Schema
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Reranking
Relevant source files
Purpose and Scope
Reranking improves search result quality by re-ordering memories retrieved from vector or graph stores based on relevance to the query. While vector similarity search provides initial results, rerankers apply more sophisticated models (such as cross-encoders or LLMs) to refine the ranking and surface the most relevant memories.

This page covers reranker configuration, supported providers (Cohere, Zero Entropy, Sentence Transformers, LLM-based, and HuggingFace), and integration with the retrieval pipeline.

Sources: 
mem0/reranker/llm_reranker.py
10-11
 
docs/components/rerankers/models/llm_reranker.mdx
6-9
 
mem0/configs/rerankers/llm.py
8-10

Reranker Architecture
Factory Pattern and Provider Registration
Mem0 uses a factory pattern to instantiate rerankers dynamically. This maps provider strings (e.g., "cohere") to specific implementation classes and their corresponding configuration models.

















Sources: 
mem0/utils/factory.py
232-245
 
mem0/reranker/llm_reranker.py
4-7
 
mem0/configs/rerankers/llm.py
8-20

Supported Reranker Providers
Provider    Implementation Class    Configuration Class    Primary Use Case
cohere    CohereReranker    CohereRerankerConfig    Production-grade managed reranking API.
sentence_transformer    SentenceTransformerReranker    SentenceTransformerRerankerConfig    Local reranking using cross-encoder models.
zero_entropy    ZeroEntropyReranker    ZeroEntropyRerankerConfig    High-performance specialized reranking service.
llm_reranker    LLMReranker    LLMRerankerConfig    Using an LLM (OpenAI, Anthropic, etc.) to score relevance.
huggingface    HuggingFaceReranker    HuggingFaceRerankerConfig    Reranking via HuggingFace Inference API.
Sources: 
mem0/utils/factory.py
239-245
 
docs/components/rerankers/models/llm_reranker.mdx
71-150

LLM-Based Reranking
The LLMReranker is a specialized implementation that allows using any supported language model as a reranker. It leverages the LlmFactory to create an underlying LLM instance 
mem0/reranker/llm_reranker.py
59

Data Flow for LLM Reranking
The rerank method iterates through candidate documents, truncating inputs to _MAX_INPUT_LEN (4000 characters) to prevent prompt flooding, and extracts a numerical score from the LLM response 
mem0/reranker/llm_reranker.py
89-102



Implementation Details:

Prompting: Uses a default _SYSTEM_PROMPT that defines a scale from 0.0 (not relevant) to 1.0 (perfectly relevant) 
mem0/reranker/llm_reranker.py
75-86
Score Extraction: Uses regex r'\b(<FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/01" undefined file-path="01">Hii</FileRef>?)\b' to find decimal numbers in the LLM's text response, clamping results between 0.0 and 1.0 
mem0/reranker/llm_reranker.py
91-102
Fallback: If scoring fails, a neutral fallback score of 0.5 is assigned 
mem0/reranker/llm_reranker.py
102
Configuration Parameters (LLMRerankerConfig)
Parameter    Type    Default    Description
provider    str    "openai"    LLM provider (openai, anthropic, etc.) 
mem0/configs/rerankers/llm.py
30-33
model    str    "gpt-4o-mini"    LLM model to use for reranking 
mem0/configs/rerankers/llm.py
22-25
scoring_prompt    str    None    Custom prompt template for scoring (Deprecated) 
mem0/configs/rerankers/llm.py
46-49
top_k    int    None    Number of top documents to return after reranking 
mem0/configs/rerankers/llm.py
34-37
llm    dict    None    Nested LLM configuration for provider-specific fields (e.g., ollama_base_url) 
mem0/configs/rerankers/llm.py
50-54
Sources: 
mem0/reranker/llm_reranker.py
10-169
 
mem0/configs/rerankers/llm.py
8-54
 
docs/components/rerankers/models/llm_reranker.mdx
31-43

Integration and Usage
Retrieval Pipeline
The reranking step occurs after initial retrieval from a storage backend (like PGVector or CassandraDB).












Keyword and Vector Search Context
While rerankers typically operate on vector search results, providers like PGVector also support keywordSearch using PostgreSQL full-text search capabilities (to_tsvector, plainto_tsquery), which can serve as the candidate source for the reranker 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
200-231

Sources: 
mem0/reranker/llm_reranker.py
104-115
 
mem0-ts/src/oss/src/vector_stores/pgvector.ts
200-231
 
mem0/vector_stores/cassandra.py
146-160

Custom Prompts
You can provide a custom prompt template using the scoring_prompt parameter in LLMRerankerConfig. The prompt is now used as the system message 
mem0/reranker/llm_reranker.py
61-71

Required Variables:

{query}: The search query.
{document}: The memory entry being scored.
Example Configuration:

config = {
    "reranker": {
        "provider": "llm_reranker",
        "config": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "scoring_prompt": "Score relevance of {document} to {query} from 0.0 to 1.0."
        }
    }
}
Sources: 
docs/components/rerankers/custom-prompts.mdx
30-74
 
mem0/reranker/llm_reranker.py
61-73

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Reranking
Purpose and Scope
Reranker Architecture
Factory Pattern and Provider Registration
Supported Reranker Providers
LLM-Based Reranking
Data Flow for LLM Reranking
Configuration Parameters (`LLMRerankerConfig`)
Integration and Usage
Retrieval Pipeline
Keyword and Vector Search Context
Custom Prompts
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Hosted Platform Overview
Relevant source files
The Mem0 Platform is a fully managed cloud service that provides a production-ready memory layer for AI applications. It eliminates the need for managing infrastructure like vector databases, graph stores, or LLM-based extraction pipelines. The platform is accessible via a high-performance REST API at https://api.mem0.ai and provides advanced features like multi-tenancy, webhooks, and automated memory decay.

Platform Architecture
The platform follows a managed client-server model. Applications use the MemoryClient or AsyncMemoryClient to communicate with the hosted API, which orchestrates the memory lifecycle across distributed storage and processing layers.

System Components and Data Flow























Sources: 
mem0/client/main.py
36-109
 
docs/platform/overview.mdx
7-15
 
docs/platform/features/memory-decay.mdx
37-45

Natural Language to Code Mapping: Platform Operations
The following diagram maps high-level platform concepts to the specific code entities and API endpoints that implement them.













Sources: 
mem0/client/main.py
137-175
 
mem0/client/main.py
251-295
 
mem0/client/main.py
448-489
 
docs/platform/features/memory-decay.mdx
61-75

Authentication and Initialization
The platform uses API key-based authentication. During initialization, the MemoryClient performs a validation check to retrieve project context.

Initialization Sequence
API Key Resolution: The client looks for an api_key argument, falling back to the MEM0_API_KEY environment variable 
mem0/client/main.py
70
User ID Generation: An MD5 hash of the API key is created as a unique user_id for telemetry 
mem0/client/main.py
80
HTTP Client Setup: An httpx.Client is initialized with the Authorization token and Mem0-User-ID headers 
mem0/client/main.py
93-100
Key Validation: The client calls _validate_api_key(), which hits the /v1/ping/ endpoint 
mem0/client/main.py
113-117
Context Injection: The org_id and project_id returned are stored on the client instance for scoped requests 
mem0/client/main.py
122-124
Sources: 
mem0/client/main.py
49-111
 
mem0/client/main.py
113-135

Multi-Tenancy and Scoping
The platform enforces a strict hierarchy: Organization > Project > Entity.

Scoping Parameters
All memory operations can be scoped using entity types defined in ENTITY_PARAMS 
mem0/client/main.py
33
:

user_id: Ties memory to a specific human user 
docs/core-concepts/memory-types.mdx
23
agent_id: Ties memory to a specific AI agent 
docs/core-concepts/memory-types.mdx
24
app_id: Scopes memory to a specific application instance.
run_id: Scopes memory to a specific session or execution run 
docs/core-concepts/memory-types.mdx
80
Filter Logic
Platform searches support complex logical operators (AND, OR) and field-level comparisons (in, gte, contains) 
docs/core-concepts/memory-operations/search.mdx
92-97

Filter Example    Code Implementation
Simple    client.search(query, filters={"user_id": "alice"})
Complex    client.search(query, filters={"OR": [{"user_id": "alice"}, {"agent_id": "bot"}]})
Sources: 
mem0/client/main.py
33
 
docs/core-concepts/memory-operations/search.mdx
159-207

Advanced Platform Features
1. Memory Decay
Memory Decay is an opt-in ranking bias that reinforces recently-accessed memories and dampens stale ones 
docs/platform/features/memory-decay.mdx
8

Mechanism: Applies a scaling factor from 0.3x to 1.5x to the relevance score 
docs/platform/features/memory-decay.mdx
25
Reinforcement: Every time a memory is returned in search, its access history is updated, boosting its future rank 
docs/platform/features/memory-decay.mdx
44
Activation: Enabled via client.project.update(decay=True) 
docs/platform/features/memory-decay.mdx
63
2. Async Client
For high-concurrency agents, the AsyncMemoryClient provides non-blocking operations 
docs/platform/features/platform-overview.mdx
20

Usage: await client.add(messages, user_id="...") 
docs/platform/advanced-memory-operations.mdx
80
Performance: Offloads memory extraction and storage to background workers on the platform 
docs/platform/overview.mdx
23
3. Managed Graph Memory
The platform provides a managed graph layer for entity relationship extraction.

Extraction: Automatically extracts entities and establishes links during the add operation 
docs/changelog/highlights.mdx
34
Integration: Seamlessly combines vector search with graph traversal for complex queries 
docs/platform/features/platform-overview.mdx
28
4. Enterprise Governance
Audit Logs: Tracks activity and latency across the workspace 
docs/platform/overview.mdx
15
Compliance: Supports GDPR/CCPA through granular deletion methods 
docs/core-concepts/memory-operations/delete.mdx
14
Wildcard Deletes: Explicitly wipe projects by setting all filters to "*" 
docs/core-concepts/memory-operations/delete.mdx
156
Sources: 
docs/platform/features/memory-decay.mdx
7-46
 
docs/platform/advanced-memory-operations.mdx
35-41
 
docs/core-concepts/memory-operations/delete.mdx
139-179
 
docs/api-reference/organizations-projects.mdx
80-110

API Versioning and Normalization
The platform manages multiple API versions to ensure backward compatibility.

Version    Primary Use Case    Response Structure
v1    Project & Org Management    Often raw lists or specific objects 
mem0/client/main.py
774
v2    Entity & Metadata Ops    Standardized results wrapper 
mem0/client/main.py
441
v3    Advanced Memory Search    Standardized with confidence scores 
docs/changelog/highlights.mdx
16
The MemoryClient normalizes responses, ensuring that if an endpoint returns a raw list, it is wrapped in a {"results": ...} dictionary for consistency 
mem0/client/main.py
247-249

Sources: 
mem0/client/main.py
169-171
 
mem0/client/main.py
291-295
 
docs/changelog/highlights.mdx
10-16

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Hosted Platform Overview
Platform Architecture
System Components and Data Flow
Natural Language to Code Mapping: Platform Operations
Authentication and Initialization
Initialization Sequence
Multi-Tenancy and Scoping
Scoping Parameters
Filter Logic
Advanced Platform Features
1. Memory Decay
2. Async Client
3. Managed Graph Memory
4. Enterprise Governance
API Versioning and Normalization
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
REST API Reference
Relevant source files
This page provides comprehensive documentation for the Mem0 Platform REST API, covering all available endpoints, request/response formats, authentication, and versioning. The REST API enables programmatic access to Mem0's memory management capabilities through HTTP requests.

For information about client SDKs that wrap these endpoints, see Python SDK and TypeScript/JavaScript SDK. For platform-specific features like webhooks and organizations, see Hosted Platform Overview.

API Architecture
The Mem0 REST API follows RESTful principles with JSON request/response payloads and token-based authentication. The current production base URL is https://api.mem0.ai.

API Structure Diagram
Sources: 
docs/openapi.json
14-18
 
mem0/client/main.py
97
 
docs/api-reference/memory/add-memories.mdx
4
 
docs/api-reference/memory/search-memories.mdx
4

Authentication
All API requests require token-based authentication using an API key obtained from the Mem0 Platform dashboard.

Authentication Header
Authorization: Token <your-api-key>
The MemoryClient handles authentication by setting the authorization header and a custom Mem0-User-ID header derived from the MD5 hash of the API key 
mem0/client/main.py
106-126

Authentication Flow


Sources: 
mem0/client/main.py
96-106
 
mem0/client/main.py
113-134
 
mem0/client/main.py
140-153
 
docs/openapi.json
19-23

API Versioning
Mem0 uses versioned paths to differentiate between processing paradigms and entity management models.

Version    Base Path    Primary Use Case    Key Features
v1    /v1/*    Legacy & Audit    Basic entity listing, history tracking, and event monitoring.
v2    /v2/*    Entity Management    Granular CRUD for Users, Agents, Apps, and Runs.
**v3    /v3/*    Modern Memory    Additive extraction (ADD-only), Hybrid Search, and Complex Filtering.
Sources: 
docs/api-reference/memory/add-memories.mdx
4-7
 
docs/api-reference/memory/search-memories.mdx
4-7
 
docs/api-reference/entities/delete-user.mdx
4

Memory Endpoints (V3)
The V3 API is the current standard for high-performance memory operations, utilizing an asynchronous additive pipeline.

Add Memories
Endpoint: POST /v3/memories/add/

Extracts facts from conversation messages. V3 uses a single-pass extraction where memories are strictly added and never overwritten or deleted during the process 
docs/api-reference/memory/add-memories.mdx
7-15

Infer Mode: Setting infer: false allows "Direct Import," bypassing LLM extraction to store text as-is 
docs/platform/features/direct-import.mdx
7-9
Async Nature: Returns an event_id. Use GET /v1/event/{event_id}/ to poll for SUCCEEDED or FAILED status 
docs/api-reference/memory/add-memories.mdx
60-85
Search Memories
Endpoint: POST /v3/memories/search/

Performs hybrid retrieval combining semantic similarity, BM25 keyword matching, and entity matching 
docs/api-reference/memory/search-memories.mdx
7

Filters: Entity IDs (user_id, agent_id, etc.) must be inside the filters object 
docs/api-reference/memory/search-memories.mdx
9
Reranking: Optional deep semantic reordering (adds ~150-200ms latency) 
docs/platform/features/advanced-retrieval.mdx
12-44
Get Memories
Endpoint: POST /v3/memories/

Retrieves a paginated list of memories. Requires filters to be specified 
docs/api-reference/memory/get-memories.mdx
7-20

Sources: 
docs/api-reference/memory/add-memories.mdx
1-85
 
docs/api-reference/memory/search-memories.mdx
1-117
 
docs/api-reference/memory/get-memories.mdx
1-68
 
mem0/client/main.py
164-249

Entity and Event Endpoints
Entity Management (V1/V2)
List Entities: GET /v1/entities/ retrieves all entities with associated memory counts 
docs/openapi.json
89-181
Delete Entity: DELETE /v2/entities/{entity_type}/{entity_id}/ removes the entity and all its memories 
docs/api-reference/entities/delete-user.mdx
1-5
Events and History (V1)
Get Events: GET /v1/events/ tracks the status of background tasks 
docs/api-reference/events/get-events.mdx
1-13
Memory History: GET /v1/memories/{memory_id}/history/ provides an audit trail of a specific memory's lifecycle 
docs/api-reference/memory/history-memory.mdx
1-5
Implementation Flow
This diagram bridges the SDK methods to the internal REST routes and background processing logic.



Sources: 
mem0/client/main.py
164-186
 
docs/api-reference/memory/add-memories.mdx
15-16
 
docs/api-reference/memory/search-memories.mdx
7-9
 
docs/platform/features/async-client.mdx
32-56

Error Handling
The API uses standard HTTP status codes to communicate success or failure.

Code    Meaning    Common Cause in Mem0
400    Bad Request    Passing user_id at top-level in V3 Search/Get instead of inside filters 
docs/api-reference/memory/get-memories.mdx
7
401    Unauthorized    Missing or invalid API Key in the Authorization header 
mem0/client/main.py
155-161
404    Not Found    Attempting to access a memory_id or event_id that does not exist.
429    Rate Limit    Exceeding the request quota for the current project 
mem0/client/main.py
181
Sources: 
mem0/client/utils.py
19
 
docs/api-reference/memory/add-memories.mdx
73-80
 
docs/api-reference/memory/get-memories.mdx
7-8

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
REST API Reference
API Architecture
API Structure Diagram
Authentication
Authentication Header
Authentication Flow
API Versioning
Memory Endpoints (V3)
Add Memories
Search Memories
Get Memories
Entity and Event Endpoints
Entity Management (V1/V2)
Events and History (V1)
Implementation Flow
Error Handling
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.
Syntax error in text
mermaid version 11.12.3

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
API Versioning
Relevant source files
This page documents the versioning strategy used in the Mem0 Platform API, including API endpoint versioning (v1, v2, and v3) and output format versioning (v1.0 vs v1.1). It covers how to specify versions in client SDKs and migrate between versions.

Overview
Mem0 Platform implements two independent versioning dimensions:

API Endpoint Versioning: URL path-based versioning (/v1/, /v2/, and /v3/) that determines the endpoint structure and request/response handling.
Output Format Versioning: Response format versioning (v1.0 vs v1.1) that controls the structure of returned data.
The Platform automatically defaults to the latest stable format (v1.1) for most operations. For add operations, the SDK explicitly forces the v1.1 output format 
mem0/client/main.py
202

Sources: 
mem0/client/main.py
202
 
docs/platform/quickstart.mdx
75

API Endpoint Versioning
Version Comparison
Feature    v1 Endpoints    v2 Endpoints    v3 Endpoints
Get All Memories    GET /v1/memories/    POST /v2/memories/    N/A
Search Memories    POST /v1/memories/search/    POST /v2/memories/search/    POST /v3/memories/search/
Add Memories    POST /v1/memories/    N/A    POST /v3/memories/add/
Entity Management    GET /v1/entities/    DELETE /v2/entities/{type}/{id}/    N/A
Filtering    Query parameters    JSON body nested filters    Enhanced body filters
Version Selection Flow:



















Sources: 
mem0/client/main.py
203
 
mem0/client/main.py
276-304
 
mem0/client/main.py
330-353
 
docs/platform/quickstart.mdx
75

v1 Endpoints
Used primarily for standard retrieval, metadata filtering, and legacy compatibility. Filters are typically passed as query strings in GET requests 
docs/openapi.json
95-112

Usage in Python:

# Uses /v1/ping/ for validation
client = MemoryClient(api_key="your-api-key")
Sources: 
mem0/client/main.py
144
 
docs/openapi.json
89-112

v2 Endpoints
Introduced to handle complex filtering and specific entity management.

Entity Deletion: Supports deleting specific entities by type (user, agent, app, run) 
docs/api-reference/entities/delete-user.mdx
4
Memory Retrieval: Uses POST to allow for complex JSON-based filtering in the request body 
mem0/client/main.py
299
Sources: 
docs/openapi.json
225-245
 
mem0/client/main.py
299

v3 Endpoints
The current standard for core memory operations in the Platform.

Add Memory: POST /v3/memories/add/ 
docs/platform/quickstart.mdx
75
Search Memory: POST /v3/memories/search/ 
docs/platform/quickstart.mdx
107
Sources: 
docs/platform/quickstart.mdx
75
 
docs/platform/quickstart.mdx
107
 
mem0/client/main.py
203

Output Format Versioning
Output format versioning controls the structure of API responses independent of the endpoint version.

Format Comparison
v1.0 Format (Legacy): Returns a flat list of memory objects.

[
    {
        "id": "mem_1",
        "memory": "Loves coffee"
    }
]
v1.1 Format (Current): Returns a dictionary with a results key.

{
    "results": [
        {
            "id": "mem_1",
            "memory": "Loves coffee"
        }
    ]
}
SDK Normalization Logic
The MemoryClient includes logic to ensure consistent output formats for the user, regardless of the raw API response.















Sources: 
mem0/client/main.py
202
 
mem0/client/main.py
300-304
 
mem0/client/main.py
348-353

Migration Guide
Migrating from Open Source to Platform
When moving from OSS to Platform, the retrieval calls require significant updates because Platform uses nested filtering.

Method    Open Source (OSS)    Platform (MemoryClient)
search()    m.search(query, user_id="alex")    client.search(query, filters={"user_id": "alex"})
get_all()    m.get_all(user_id="alex")    client.get_all(filters={"user_id": "alex"})
limit param    limit=10    top_k=10
Sources: 
docs/migration/oss-to-platform.mdx
80-95

Critical Changes in Platform API
Filters Required: get_all() now requires filters to be specified; it no longer returns the entire database without a scope 
docs/platform/features/direct-import.mdx
70
Top_k: The limit parameter is replaced by top_k across all Platform SDKs 
docs/migration/oss-to-platform.mdx
84-86
Nested Filters: Platform supports logical operators like AND, OR, and NOT within the filters dictionary 
docs/migration/oss-to-platform.mdx
114-119
Example Migration (Search):

# OSS (Old)
results = m.search("preferences", user_id="user123")
 
# Platform (New)
results = client.search("preferences", filters={"user_id": "user123"})
Sources: 
docs/migration/oss-to-platform.mdx
101-121

API Category Reference
Category    Version    Key Endpoint
Memories    v3    /v3/memories/add/, /v3/memories/search/
Entities    v1/v2    /v1/entities/, /v2/entities/{type}/{id}/
Events    v1    /v1/events/
Projects    v1    /v1/projects/
Sources: 
docs/openapi.json
25-89
 
docs/openapi.json
225
 
docs/api-reference/events/get-events.mdx
4
 
docs/platform/quickstart.mdx
75

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
API Versioning
Overview
API Endpoint Versioning
Version Comparison
v1 Endpoints
v2 Endpoints
v3 Endpoints
Output Format Versioning
Format Comparison
SDK Normalization Logic
Migration Guide
Migrating from Open Source to Platform
Critical Changes in Platform API
API Category Reference
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Organizations and Projects
Relevant source files
Organizations and Projects provide a multi-tenancy model for the Mem0 Platform, enabling logical isolation of memories, configuration, and entities across different organizational units and use cases. This page documents the organization/project hierarchy, initialization, configuration, and project management capabilities.

Multi-Tenancy Model
The Mem0 Platform implements a two-level hierarchy for organizing memories and configuration:

Hierarchy Diagram










Sources: 
mem0/client/main.py
98-100
 
mem0/client/main.py
149-153
 
mem0/client/project.py
16-25
 
docs/api-reference/organizations-projects.mdx
7-21

Organization Level
Organizations represent the top-level tenant boundary. Each organization:

Has a unique org_id identifier 
mem0/client/main.py
98
Provides billing and access control boundaries 
docs/api-reference/organizations-projects.mdx
17-20
Isolates data and configuration from other organizations.
Project Level
Projects are logical subdivisions within an organization. Each project:

Has a unique project_id identifier 
mem0/client/main.py
99
Maintains independent configuration settings including custom_instructions, custom_categories, and multilingual support 
mem0/client/project.py
176-181
 
docs/api-reference/organizations-projects.mdx
80-110
Supports Memory Decay, a search-time ranking bias enabled via the decay field 
docs/platform/features/memory-decay.mdx
8-10
Sources: 
mem0/client/main.py
98-99
 
mem0/client/project.py
176-181
 
docs/platform/features/memory-decay.mdx
55-60

Client Initialization
The MemoryClient can be initialized with an API key, which triggers an automatic discovery of the default organization and project.

Automatic Discovery Flow
When a MemoryClient is instantiated, it calls _validate_api_key() to retrieve tenant context 
mem0/client/main.py
127



Sources: 
mem0/client/main.py
105-106
 
mem0/client/main.py
127-135
 
mem0/client/main.py
140-153

Project Configuration and Memory Decay
Projects maintain settings that control how memories are extracted and retrieved. A significant recent addition is Memory Decay.

Configuration Parameters
Parameter    Type    Description    Reference
custom_instructions    str    Custom prompts for the fact extraction pipeline.    
mem0/client/project.py
178
custom_categories    list    Specific labels used for memory classification.    
mem0/client/project.py
179
multilingual    bool    Enables memory storage/retrieval in the input language.    
docs/api-reference/organizations-projects.mdx
98-99
decay    bool    Opt-in search-time ranking bias (0.3x to 1.5x scaling).    
docs/platform/features/memory-decay.mdx
25-33
Memory Decay Implementation
Memory Decay is a "soft bias" applied at search time. It does not filter memories but reorders them based on access history 
docs/platform/features/memory-decay.mdx
8-10

Scaling Factor: Ranges from 0.3x (stale) to 1.5x (fresh/just accessed) 
docs/platform/features/memory-decay.mdx
27-33
Reinforcement: Every time a memory is returned in a search, its access history is updated 
docs/platform/features/memory-decay.mdx
44-46
Clamping: The final public score remains clamped to [0, 1] for API consistency 
docs/platform/features/memory-decay.mdx
42
Sources: 
docs/platform/features/memory-decay.mdx
8-46
 
docs/api-reference/organizations-projects.mdx
112-123

Project Management Interface
The MemoryClient delegates project-level operations to the Project (sync) or AsyncProject (async) classes 
mem0/client/project.py
243
 
mem0/client/project.py
346

Key Operations
Method    API Endpoint    Description
client.project.get()    GET /v1/projects/{id}/    Retrieve project metadata and config.
client.project.create()    POST /v1/projects/    Create a new project in the organization.
client.project.update()    PATCH /v1/projects/{id}/    Update instructions, categories, or decay.
client.project.delete()    DELETE /v1/projects/{id}/    Irreversibly delete project and all memories.
Sources: 
mem0/client/project.py
274-343
 
docs/api-reference/organizations-projects.mdx
52-136

Member Management
Projects also support role-based access control for team members 
docs/api-reference/organizations-projects.mdx
140-169
:

READER: Can view/search memories.
OWNER: Full access to settings and member management.
Methods: add_member(), update_member(), remove_member(), and get_members() 
docs/api-reference/organizations-projects.mdx
145-161

Entity and Event Scoping
All data entities and audit logs are scoped to the organization and project.

Entities
Entities (Users, Agents, Apps, Runs) are filtered by org_id and project_id during retrieval 
docs/openapi.json
95-112

List Entities: GET /v1/entities/ accepts org_id and project_id as query parameters.
Delete Entity: DELETE /v2/entities/{entity_type}/{entity_id}/ allows targeted removal of users or agents 
docs/openapi.json
225-246
Events
The events system provides an audit trail for organization and project activities 
docs/api-reference/events/get-events.mdx
1-12

Endpoint: GET /v1/events/
Usage: Used for dashboards, alerting on FAILED operations, and compliance logging 
docs/api-reference/events/get-events.mdx
9-12
Sources: 
docs/openapi.json
89-112
 
docs/api-reference/entities/delete-user.mdx
1-4
 
docs/api-reference/events/get-events.mdx
1-12

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Organizations and Projects
Multi-Tenancy Model
Hierarchy Diagram
Organization Level
Project Level
Client Initialization
Automatic Discovery Flow
Project Configuration and Memory Decay
Configuration Parameters
Memory Decay Implementation
Project Management Interface
Key Operations
Member Management
Entity and Event Scoping
Entities
Events
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Webhooks and Events
Relevant source files
This page documents the webhook system and event tracking capabilities of the Mem0 managed platform. Webhooks enable real-time notifications when memory operations occur, allowing your application to react to memory changes asynchronously. Event tracking provides visibility into the processing lifecycle of memory operations.

This page covers the Platform API's webhook and event systems. For information about memory operations themselves, see 
Memory Operations
 For general Platform API features, see 
Hosted Platform Overview

Overview
The Mem0 Platform provides two complementary systems for monitoring and reacting to memory operations:

Webhooks - HTTP callbacks that push notifications to your application when specified events occur.
Events - A queryable log of all memory operations with status tracking and performance metrics.
Both systems are project-scoped: webhooks are configured per-project and only receive events from that project, while event queries are filtered by project context.

Key Characteristics:

Asynchronous Processing: Memory operations run in the background (v3 API), with events tracking their lifecycle 
docs/openapi.json
75-85
Stateful Tracking: Events maintain status through PENDING, RUNNING, FAILED, and SUCCEEDED states 
docs/openapi.json
399-409
Real-time Notifications: Webhooks deliver event notifications via HTTP POST within seconds.
Project Isolation: All webhook and event data respects organization/project boundaries 
mem0/client/main.py
776-781
Implementation:

Webhook management via MemoryClient methods: create_webhook(), get_webhooks(), update_webhook(), delete_webhook() 
mem0/client/main.py
773-835
Event querying via REST endpoints: GET /v1/events/ and GET /v1/event/{event_id}/ 
docs/openapi.json
357-568
Sources: 
mem0/client/main.py
773-835
 
docs/openapi.json
357-568
 
docs/openapi.json
75-85

System Architecture
Webhook Registration and Event Flow

Title: Webhook Registration and Event Flow




























The diagram shows three primary flows:

Webhook Configuration: Applications call client.create_webhook() which sends POST /api/v1/webhooks/ to register webhook endpoints with specific event_types 
mem0/client/main.py
791-809
Memory Operation: When client.add() is called, it triggers POST /v3/memories/add/ which creates an event record with status: PENDING and returns an event_id 
docs/openapi.json
75-85
Event Processing & Notification: The event transitions through states, and upon completion, the webhook dispatcher filters by configured event_types and sends POST requests to matching webhook URLs.
Sources: 
mem0/client/main.py
164-186
 
mem0/client/main.py
791-809
 
docs/openapi.json
357-461
 
docs/openapi.json
75-85

Event Processing Architecture

Title: Event Processing Architecture






















Each memory operation creates an event record with comprehensive tracking data. In the TypeScript SDK, the WebhookEvent enum defines these triggers 
mem0-ts/src/client/mem0.types.ts
170-175

Field    Type    Description
id    UUID    Unique event identifier 
docs/openapi.json
391
event_type    string    Operation type (ADD, UPDATE, DELETE, CATEGORIZE) 
docs/openapi.json
397
status    enum    Processing state (PENDING, RUNNING, FAILED, SUCCEEDED) 
docs/openapi.json
399
payload    object    Original request data that triggered the event 
docs/openapi.json
411
metadata    object    Additional context (user_id, agent_id, etc.) 
docs/openapi.json
423
results    array    Operation results (memories created/updated/deleted) 
docs/openapi.json
427
created_at    datetime    Event creation timestamp (ISO 8601) 
docs/openapi.json
445
latency    number    Processing duration in milliseconds 
docs/openapi.json
446
Sources: 
docs/openapi.json
387-447
 
mem0/client/main.py
791-809
 
mem0-ts/src/client/mem0.types.ts
170-175

Event Types and Lifecycle
Supported Event Types

The Platform supports the following event types, defined in the SDKs:

Event Type (Code)    Enum Name    Description
memory_add    MEMORY_ADDED    Memory creation via client.add() 
mem0-ts/src/client/mem0.types.ts
171
memory_update    MEMORY_UPDATED    Memory modification via client.update() 
mem0-ts/src/client/mem0.types.ts
172
memory_delete    MEMORY_DELETED    Memory removal via client.delete() 
mem0-ts/src/client/mem0.types.ts
173
memory_categorize    MEMORY_CATEGORIZED    Async categorization process 
mem0-ts/src/client/mem0.types.ts
174
Sources: 
mem0-ts/src/client/mem0.types.ts
170-175
 
docs/openapi.json
397-409

Event Lifecycle States
Events transition through a defined lifecycle with status tracking. The status field in event records follows this progression 
docs/openapi.json
399-409
:

PENDING: Event created and queued for processing.
RUNNING: Processing has begun (e.g., LLM fact extraction).
SUCCEEDED: Operation completed successfully. results array is populated with memory objects 
docs/openapi.json
427-444
FAILED: Operation encountered an error.
Latency Tracking: The latency field provides operation performance metrics in milliseconds, measuring the time from start to completion 
docs/openapi.json
446-447

Sources: 
docs/openapi.json
399-447
 
docs/openapi.json
489-545

Webhook Management
Creating Webhooks
Webhooks are created via the MemoryClient.create_webhook() method. Each webhook is scoped to a specific project and organization 
mem0/client/main.py
791-809

Python Example:

webhook = client.create_webhook(
    url="https://your-app.com/webhook",
    name="Memory Logger",
    event_types=["memory_add", "memory_categorize"]
)
TypeScript Example:

const webhook = await client.createWebhook({
  name: "My Webhook",
  url: "https://example.com/webhook",
  eventTypes: [WebhookEvent.MEMORY_ADDED]
});
The payload for creation is defined by the WebhookCreatePayload interface 
mem0-ts/src/client/mem0.types.ts
188-192

Sources: 
mem0/client/main.py
791-809
 
mem0-ts/src/client/mem0.types.ts
188-192

Retrieving and Updating Webhooks
Operation    Python Method    TypeScript Method    API Endpoint
List All    get_webhooks()    getWebhooks()    GET /v1/webhooks/ 
mem0/client/main.py
773-789
Update    update_webhook()    updateWebhook()    PUT /v1/webhooks/{id}/ 
mem0/client/main.py
811-825
Delete    delete_webhook()    deleteWebhook()    DELETE /v1/webhooks/{id}/ 
mem0/client/main.py
827-835
Update Payload: Uses WebhookUpdatePayload, allowing modification of name, url, and eventTypes 
mem0-ts/src/client/mem0.types.ts
194-199

Sources: 
mem0/client/main.py
773-835
 
mem0-ts/src/client/mem0.types.ts
194-199

Event Querying and Monitoring
Listing Recent Events
Retrieve events for the current organization and project to monitor system health or audit changes 
docs/api-reference/events/get-events.mdx
1-13

API Endpoint: GET /v1/events/ 
docs/openapi.json
357

Response Fields:

Field    Type    Description
count    integer    Total number of events 
docs/openapi.json
374
results    array    List of event objects including status, latency, and payload 
docs/openapi.json
387-447
Use Cases:

Dashboards: Summarize operations over time 
docs/api-reference/events/get-events.mdx
11
Alerting: Poll for FAILED events to trigger recovery workflows 
docs/api-reference/events/get-events.mdx
12
Audit: Store payloads for compliance logs 
docs/api-reference/events/get-events.mdx
13
Sources: 
docs/openapi.json
357-461
 
docs/api-reference/events/get-events.mdx
1-13

Retrieving a Specific Event
Query a single event by its ID to get full processing details, including LLM extraction results 
docs/api-reference/events/get-event.mdx
1-5

API Endpoint: GET /v1/event/{event_id}/ 
docs/openapi.json
463

Sources: 
docs/openapi.json
463-567
 
docs/api-reference/events/get-event.mdx
1-5

Webhook Payload Formats
When an operation completes, the Platform sends a POST request to your URL.

Memory Operation Payloads
For memory_add, memory_update, and memory_delete, the payload includes the resulting memory state.

{
  "event_details": {
    "id": "mem_uuid",
    "data": {
      "memory": "The extracted fact text"
    },
    "event": "ADD"
  }
}
Webhook Security and Best Practices
HTTPS Enforcement: Only https:// URLs are accepted for webhook endpoints.
Asynchronous Processing: Webhook handlers should return a 2xx status code immediately (within 10 seconds) and process the payload in a background queue 
mem0/client/main.py
791-809
Idempotency: Use the id field in the payload to detect and ignore duplicate notifications.
Validation: Verify requests using the Authorization header if your endpoint is protected.
Sources: 
mem0/client/main.py
791-809
 
docs/openapi.json
357-567

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Webhooks and Events
Overview
System Architecture
Event Types and Lifecycle
Event Lifecycle States
Webhook Management
Creating Webhooks
Retrieving and Updating Webhooks
Event Querying and Monitoring
Listing Recent Events
Retrieving a Specific Event
Webhook Payload Formats
Memory Operation Payloads
Webhook Security and Best Practices
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Memory Export
Relevant source files
Memory Export is a structured data extraction system that transforms unstructured memories into typed, schema-conformant data structures. This feature allows applications to retrieve memories in a format defined by JSON schemas (typically generated from Pydantic), enabling type-safe integration with downstream systems and data portability.

Overview
The Memory Export system operates as an asynchronous job-based service that:

Accepts a JSON schema definition.
Retrieves memories matching optional filters.
Transforms and structures data conforming to the schema using LLM-based extraction.
Returns typed results via a polling-based retrieval mechanism.
This enables applications to convert conversational memory data into structured formats like customer profiles, professional resumes, or domain-specific entities.

Sources: 
docs/docs.json
95
 
mem0/client/main.py
563-606

Export Workflow
The following diagram illustrates the interaction between the SDK and the Platform API during an export lifecycle.



Diagram: Memory Export request and retrieval lifecycle showing asynchronous processing.

Sources: 
mem0/client/main.py
563-606
 
docs/openapi.json
24-210

Creating an Export
Endpoint: POST /v1/memories/export/
The export creation endpoint accepts a schema, filters, and optional instructions.

Request Structure:

Field    Type    Required    Description
schema    object    Yes    JSON schema defining export structure (Pydantic-compatible).
filters    object    No    Entity filters (user_id, agent_id, app_id, run_id).
export_instructions    string    No    Custom natural language instructions for the extraction process.
Client Method: create_memory_export
The MemoryClient.create_memory_export() method wraps the export creation API.

# Example Usage
filters = {"user_id": "alice"}
export_instructions = "Create a comprehensive profile. Prioritize recent info."
 
response = client.create_memory_export(
    schema=json_schema,
    filters=filters,
    export_instructions=export_instructions
)
print(response["id"])
Implementation Details:

Located at <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/client/main.py#L563-L587" min=563 max=587 file-path="mem0/client/main.py">Hii</FileRef>.
Accepts schema (dict) and optional export_instructions.
Uses _prepare_params() to inject org_id and project_id into the request context <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/client/main.py#L143-L154" min=143 max=154 file-path="mem0/client/main.py">Hii</FileRef>.
Captures telemetry event client.create_memory_export <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/client/main.py#L587-L587" min=587 file-path="mem0/client/main.py">Hii</FileRef>.
Sources: 
mem0/client/main.py
563-587
 
mem0/client/main.py
143-154

Schema and Instructions
Schema Definition
The schema drives the structure of the output. It supports nested objects, enums, and basic types. Common structures include ProfessionalProfile or UserPreferences.

Export Instructions
Users can provide export_instructions to guide the LLM during extraction. Common use cases include:

Conflict Resolution: Prioritizing recent information over historical records.
Detail Level: Specifying the depth of extraction for specific fields.
Factualness: Distinguishing between confirmed facts and speculative user statements.
Sources: 
mem0/client/main.py
563-568
 
docs/platform/features/v2-memory-filters.mdx
6-16

Retrieving Export Results
Endpoint: GET /v1/memories/export/{id}/
Once an export job is created, results are retrieved by export ID.

Client Method: get_memory_export

# Retrieve using export ID
response = client.get_memory_export(memory_export_id="550e8400-e29b-41d4-a716-446655440000")
Alternative: Retrieve by Filters The SDK also allows fetching the latest export associated with specific filters.

filters = {"user_id": "alex"}
response = client.get_memory_export(filters=filters)
Implementation Details:

Located at <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/client/main.py#L590-L606" min=590 max=606 file-path="mem0/client/main.py">Hii</FileRef>.
If memory_export_id is provided, it calls the specific ID endpoint.
If filters are provided, it calls the filter-based retrieval endpoint.
Captures telemetry event client.get_memory_export <FileRef file-url="https://github.com/mem0ai/mem0/blob/54a03cc7/mem0/client/main.py#L606-L606" min=606 file-path="mem0/client/main.py">Hii</FileRef>.
Sources: 
mem0/client/main.py
590-606

Code Entity Mapping
The following diagram maps SDK methods to their corresponding API endpoints and internal utility functions.














Diagram: Association of SDK methods with API endpoints and internal logic.

Sources: 
mem0/client/main.py
563-622
 
mem0/client/utils.py
1-20

Filtering Exports
Exports can be scoped using the same filtering logic as standard memory searches.

Filter    Purpose    Example
user_id    Isolate memories for a specific user.    {"user_id": "user_123"}
agent_id    Filter by a specific agent persona.    {"agent_id": "agent_456"}
app_id    Scope to a specific application instance.    {"app_id": "app_789"}
run_id    Limit to a specific session or thread.    {"run_id": "run_000"}
created_at    Time-based export using operators.    {"created_at": {"gte": "2024-01-01"}}
Sources: 
docs/platform/features/v2-memory-filters.mdx
32-60
 
mem0/client/main.py
32-34

Summary and Metadata
The Platform API provides a /v1/summary/ endpoint to get a high-level overview of memories without performing a full structured export.

Client Method: get_summary

# mem0/client/main.py:609-622
def get_summary(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get the summary of a memory export."""
    params = self._prepare_params({"filters": filters})
    response = self.client.post("/v1/summary/", json=params)
    return response.json()
Sources: 
mem0/client/main.py
609-622

Error Handling
Status Code    Reason    Resolution
401    Unauthorized    Verify MEM0_API_KEY is set correctly.
404    Not Found    The export ID does not exist or has expired.
422    Validation Error    The provided JSON schema or filter is invalid.
The SDK uses the @api_error_handler decorator to translate these HTTP errors into Python exceptions like ValidationError or AuthenticationError.

Sources: 
mem0/client/main.py
163
 
mem0/client/utils.py
1-20

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Memory Export
Overview
Export Workflow
Creating an Export
Endpoint: `POST /v1/memories/export/`
Client Method: `create_memory_export`
Schema and Instructions
Schema Definition
Export Instructions
Retrieving Export Results
Endpoint: `GET /v1/memories/export/{id}/`
Code Entity Mapping
Filtering Exports
Summary and Metadata
Error Handling
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Telemetry and Analytics
Relevant source files
This document describes Mem0's telemetry and analytics system, which collects usage metrics via PostHog to improve the product. For configuration options related to API clients, see Client SDKs. For self-hosted deployment configuration, see Deployment Models.

Purpose and Scope
Mem0's telemetry system captures anonymized usage metrics from SDK clients (both platform API clients and self-hosted instances) to understand feature adoption, identify issues, and improve the developer experience. The system is opt-out by default and integrates with PostHog for event processing and analytics.

Architecture Overview
The telemetry architecture consists of a core AnonymousTelemetry class in Python and a UnifiedTelemetry class in TypeScript. These classes interface with PostHog to transmit event data.

Python Telemetry Architecture






















Sources: 
mem0/memory/telemetry.py
73-132
 
mem0/memory/telemetry.py
186-210
 
mem0-ts/src/client/telemetry.ts
26-75

PostHog Integration
Mem0 uses PostHog as its analytics backend. In Python, it uses the posthog library, while in TypeScript, it uses a direct API integration via fetch.

Configuration Constants (Python)
Constant    Value    File Location
PROJECT_API_KEY    phc_hgJkUVJFYtmaJqrvf6CYN67TIQ8yhXAkWzUn9AMU4yX    
mem0/memory/telemetry.py
15
HOST    https://us.i.posthog.com    
mem0/memory/telemetry.py
16
MEM0_TELEMETRY    True (default)    
mem0/memory/telemetry.py
14
The MEM0_TELEMETRY environment variable controls whether telemetry is enabled. It accepts boolean-like strings: "true", "1", "yes". 
mem0/memory/telemetry.py
18-22

Configuration Constants (TypeScript)
Constant    Value    File Location
POSTHOG_API_KEY    phc_hgJkUVJFYtmaJqrvf6CYN67TIQ8yhXAkWzUn9AMU4yX    
mem0-ts/src/client/telemetry.ts
15
POSTHOG_HOST    https://us.i.posthog.com/i/v0/e/    
mem0-ts/src/client/telemetry.ts
16
Sources: 
mem0/memory/telemetry.py
14-22
 
mem0-ts/src/client/telemetry.ts
11-16

Telemetry System Components
AnonymousTelemetry Class (Python)
The AnonymousTelemetry class handles the lifecycle of the PostHog client. It includes a capture_event method that enriches data with system information (OS, Python version, processor) before sending. 
mem0/memory/telemetry.py
98-110

Identity Stitching (Aliasing)
Both Python and TypeScript SDKs support identity stitching to merge anonymous local IDs with platform user identities (emails). This ensures that usage from the CLI or local OSS instances can be associated with a platform account when a MemoryClient is initialized with an API key.

Mechanism: The SDK fires a $identify event with $anon_distinct_id set to the local anonymous ID. 
mem0/memory/telemetry.py
116-131
 
mem0-ts/src/client/telemetry.ts
77-113
Persistence: To avoid redundant identification calls, markers are stored in ~/.mem0/config.json. 
mem0/memory/setup.py
100-119
 
mem0-ts/src/client/config.ts
140-165
Sampling Mechanism (Python OSS)
To reduce noise and costs, Mem0 implements a sampling mechanism for "hot-path" events in the OSS Python SDK.

Default Rate: 0.1 (10% of events). 
mem0/memory/telemetry.py
31
Configuration: Controlled via MEM0_TELEMETRY_SAMPLE_RATE environment variable. 
mem0/memory/telemetry.py
47
Lifecycle Events: Certain events bypass sampling and always fire at 100%. These include mem0.init, mem0.reset, mem0._create_procedural_memory, and $identify. 
mem0/memory/telemetry.py
52


Sources: 
mem0/memory/telemetry.py
31-70

Event Properties
Captured Metadata (Python)
The Python SDK captures extensive system metadata:

Property    Source
client_source    Hardcoded "python"
client_version    mem0.__version__
python_version    sys.version
os    sys.platform
os_version    platform.version()
processor    platform.processor()
Sources: 
mem0/memory/telemetry.py
99-110

Captured Metadata (TypeScript Client)
When capturing events for the MemoryClient, the system logs:

function: The constructor name of the instance (e.g., MemoryClient).
method: The specific method being called (e.g., add).
api_host: The target host for the API call.
client_version: Injected at build time.
Sources: 
mem0-ts/src/client/telemetry.ts
136-150

Event Naming Convention
Events follow naming patterns depending on the SDK and deployment:

Platform Client (Python/TS): client.{method_name} (e.g., client.init, client.add) 
mem0-ts/src/client/telemetry.ts
148
OSS SDK (Python): mem0.{method_name} (e.g., mem0.init, mem0.add) 
mem0/memory/telemetry.py
186
Privacy and Opt-Out
Disabling Telemetry
Telemetry can be disabled by setting the MEM0_TELEMETRY environment variable to False (Python) or false (TS).

Python: Handled in AnonymousTelemetry.__init__ and capture_event. 
mem0/memory/telemetry.py
14-22
 
mem0/memory/telemetry.py
75-78
TypeScript: Handled in UnifiedTelemetry.captureEvent and isTelemetryEnabled. 
mem0-ts/src/client/telemetry.ts
11-14
 
mem0-ts/src/client/telemetry.ts
40
User Identification
The user_id used for telemetry is managed by get_or_create_user_id in Python and getOrCreateMem0UserId in TypeScript.

It first checks a local config.json in the MEM0_DIR (defaults to ~/.mem0). 
mem0/memory/setup.py
9-11
 
mem0-ts/src/client/config.ts
37
In Python, if a vector_store is provided, it attempts to retrieve or persist a user_identity vector to maintain a stable ID across different environments using the same database. 
mem0/memory/setup.py
122-154
Sources: 
mem0/memory/setup.py
122-154
 
mem0-ts/src/client/config.ts
81-96

Implementation Details
Thread-Safe Singleton (Python)
The OSS telemetry uses a thread-safe lazy singleton pattern to ensure only one PostHog client exists per process. It uses threading.Lock() for instantiation and atexit.register() to ensure the background worker threads are shut down cleanly on process exit.

Sources: 
mem0/memory/telemetry.py
139-168

TypeScript Build-Time Versioning
The TypeScript SDK injects the version number at build time. In unbundled environments like tests, it falls back to "dev".

Sources: 
mem0-ts/src/client/telemetry.ts
7-8

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Telemetry and Analytics
Purpose and Scope
Architecture Overview
Python Telemetry Architecture
PostHog Integration
Configuration Constants (Python)
Configuration Constants (TypeScript)
Telemetry System Components
AnonymousTelemetry Class (Python)
Identity Stitching (Aliasing)
Sampling Mechanism (Python OSS)
Event Properties
Captured Metadata (Python)
Captured Metadata (TypeScript Client)
Event Naming Convention
Privacy and Opt-Out
Disabling Telemetry
User Identification
Implementation Details
Thread-Safe Singleton (Python)
TypeScript Build-Time Versioning
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.

DeepWiki
mem0ai/mem0


Index your code with
Devin
Edit Wiki

Share

Last indexed: 12 May 2026 (54a03c)
Overview
System Architecture
Installation and Setup
Deployment Models
Core Architecture
Factory Pattern and Component System
Provider Ecosystem
Configuration System
Memory System
Memory Class (Open Source)
MemoryClient (Platform)
Memory Operations
Session Scoping and Filters
Asynchronous Operations
Proxy Integration
Intelligent Memory Processing
Graph Memory
Graph Memory Overview
Graph Store Providers
Entity and Relationship Extraction
Graph Search and Retrieval
Similarity Thresholds
Storage Backends
Vector Stores Overview
Vector Store Providers
Vector Store Configuration
History and Audit Trails
AI Model Integrations
LLM Providers
LLM Configuration
Embedding Providers
Embeddings Configuration
Reranking
Platform and API
Hosted Platform Overview
REST API Reference
API Versioning
Organizations and Projects
Webhooks and Events
Memory Export
Client SDKs
Python SDK
TypeScript/JavaScript SDK
Vercel AI SDK Provider
Framework Integrations
Agent Frameworks
OpenClaw Plugin
Voice and Multimodal
Development Tools
MCP Server and AI Coding Agents
Usage Patterns
Basic Usage
Advanced Patterns
Domain-Specific Examples
Advanced Features
Custom Prompts
Telemetry and Analytics
Performance Optimization
Advanced Filtering
Batch Operations
Self-Hosted Server
Server Setup and Deployment
Server Authentication and Security
Server Dashboard
CLI
CLI Installation and Commands
CLI Configuration and Agent Mode
Development
Development Setup
Testing
CI/CD Pipeline
Contributing Guidelines
Documentation System
Evaluation Framework
OpenMemory (Deprecated)
OpenMemory Overview and Migration
OpenMemory MCP Server
Legacy: Embedchain
Embedchain Overview
Embedchain Configuration
Embedchain Data Sources
Glossary
Evaluation Framework
Relevant source files
The Mem0 evaluation framework is a research-grade benchmarking suite designed to assess the performance of the Mem0 memory layer against existing long-term memory solutions, RAG architectures, and proprietary systems using the LOCOMO dataset 
evaluation/README.md
1-19
 It provides standardized metrics for accuracy, latency, and token consumption to validate the efficacy of Mem0's hierarchical memory approach 
evaluation/README.md
164-173

Overview and Purpose
The framework is structured to compare Mem0 against several baselines:

Literature Benchmarks: LoCoMo, ReadAgent, MemoryBank, MemGPT, and A-Mem 
evaluation/README.md
10-12
Open Source & Third-Party: LangMem and Zep 
evaluation/README.md
13-17
Commercial Solutions: OpenAI's built-in memory 
evaluation/README.md
15-16
Retrieval Baselines: Standard RAG (varying chunk sizes) and Full-Context processing 
evaluation/README.md
14-15
Data Flow for Benchmarking
The evaluation process follows a structured pipeline from data ingestion to metric generation.




















Sources: 
evaluation/README.md
21-50
 
evaluation/metrics/llm_judge.py
58-130

Key Components and Implementation
Experiment Execution (run_experiments.py)
This script acts as the entry point for running benchmarks. It supports various techniques through the --technique_type parameter (e.g., mem0, rag, langmem) and methods like add or search 
evaluation/README.md
106-120

LLM Judge (evaluation/metrics/llm_judge.py)
To overcome the limitations of exact matching, the framework employs an LLM-based evaluator.

Class/Function: evaluate_llm_judge(question, gold_answer, generated_answer) 
evaluation/metrics/llm_judge.py
39-55
Model: Uses gpt-4o-mini with a specific ACCURACY_PROMPT to determine if a generated answer is "CORRECT" or "WRONG" compared to the gold answer 
evaluation/metrics/llm_judge.py
12-55
Logic: It extracts the label using extract_json 
mem0/memory/utils.py
15
 and returns a binary score (1 for CORRECT, 0 for WRONG) 
evaluation/metrics/llm_judge.py
54-55
Score Generation (generate_scores.py)
This utility aggregates the results from the results/ directory to calculate:

Mean Scores per Category: Breaks down performance by question complexity levels 
evaluation/README.md
143-156
Overall Mean Scores: Provides a global average for BLEU, F1, and LLM scores 
evaluation/README.md
158-162
Code Entity Mapping
The following diagrams map the conceptual evaluation steps and infrastructure to the specific code entities and providers used during the research process.

Memory Technique to Code Mapping
This diagram bridges the natural language "Techniques" to the run_experiments.py parameters and specific implementation files.












Sources: 
evaluation/README.md
37-42
 
evaluation/README.md
84-93
 
evaluation/README.md
106-120

LLM Provider Integration
This diagram maps the various LLM backends supported by Mem0 that can be utilized during evaluation runs.
















Sources: 
mem0/llms/aws_bedrock.py
34-41
 
mem0/llms/groq.py
15-23
 
mem0/llms/ollama.py
15-34
 
mem0/llms/together.py
15-23
 
mem0/llms/litellm.py
14-20
 
tests/llms/test_aws_bedrock.py
122-125

Evaluation Metrics
The framework captures five primary metrics to provide a multi-dimensional view of memory system performance:

Metric    Description    Implementation Source
BLEU Score    Similarity between response and ground truth.    evals.py 
evaluation/README.md
168
F1 Score    Harmonic mean of precision and recall.    evals.py 
evaluation/README.md
169
LLM Score    Binary correctness judged by gpt-4o-mini.    llm_judge.py 
evaluation/metrics/llm_judge.py
39-55
Token Consumption    Total tokens used for the final answer.    run_experiments.py 
evaluation/README.md
171
Latency    Time taken for search and generation.    run_experiments.py 
evaluation/README.md
172
Dataset Structure (LOCOMO)
The dataset is partitioned for different experimental setups:

locomo10.json: The standard conversational dataset for memory recall 
evaluation/README.md
30
locomo10_rag.json: Formatted specifically for RAG-based chunking and retrieval tests 
evaluation/README.md
31
Questions are categorized by type (Category 1-5), allowing the generate_scores.py script to report performance across different cognitive loads 
evaluation/metrics/llm_judge.py
80-90

Sources: 
evaluation/README.md
21-32
 
evaluation/metrics/llm_judge.py
111-115

Dismiss
Refresh this wiki

This wiki was recently refreshed. Please wait 2 days to refresh again.

On this page
Evaluation Framework
Overview and Purpose
Data Flow for Benchmarking
Key Components and Implementation
Experiment Execution (`run_experiments.py`)
LLM Judge (`evaluation/metrics/llm_judge.py`)
Score Generation (`generate_scores.py`)
Code Entity Mapping
Memory Technique to Code Mapping
LLM Provider Integration
Evaluation Metrics
Dataset Structure (LOCOMO)
Ask Devin about mem0ai/mem0

Fast

1Password menu is available. Press down arrow to select.
