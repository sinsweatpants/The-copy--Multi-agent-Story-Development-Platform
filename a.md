# 🚀 كود النظام الكامل - Jules Narrative Development Platform
# 🚀 السياق الهندسي الشامل: نظام Jules - نسخة Node.js/TypeScript

## 📋 نظرة عامة على المشروع

### الهدف الرئيسي
تطوير تطبيق ويب إنتاجي متكامل بـ **Node.js/TypeScript** يحول نظام "Jules" - المنظم الرئيسي لتطوير القصص - إلى منصة تفاعلية تدير 11 وكيلاً متخصصاً (AI Agents) باستخدام **Gemini 2.5 Pro API**.

---

## 🏗️ البنية المعمارية

### نموذج المعمارية: Modern Microservices-Ready Monolith

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │   React SPA (TypeScript + Vite)                  │  │
│  │   - State: Zustand + TanStack Query              │  │
│  │   - UI: Tailwind CSS + shadcn/ui                 │  │
│  │   - WebSocket: Socket.io-client                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTPS/WSS
┌─────────────────────────────────────────────────────────┐
│                   API GATEWAY LAYER                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Fastify API Gateway                            │  │
│  │   - JWT Authentication (jsonwebtoken)            │  │
│  │   - Rate Limiting (@fastify/rate-limit)          │  │
│  │   - Request Validation (Zod)                     │  │
│  │   - CORS (@fastify/cors)                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               APPLICATION SERVICES LAYER                │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────┐ │
│  │ Orchestrator   │  │ Agent Manager  │  │ Session  │ │
│  │ Service        │  │ Service        │  │ Service  │ │
│  └────────────────┘  └────────────────┘  └──────────┘ │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────┐ │
│  │ Idea Generator │  │ Review Engine  │  │ Decision │ │
│  │ Service        │  │ Service        │  │ Service  │ │
│  └────────────────┘  └────────────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  INTEGRATION LAYER                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Gemini AI Integration (@google/generative-ai)  │  │
│  │   - Connection Pool Management                   │  │
│  │   - Retry with Exponential Backoff (p-retry)     │  │
│  │   - Response Streaming                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────┐ │
│  │ PostgreSQL  │  │   Redis     │  │  File Storage  │ │
│  │ (Prisma ORM)│  │  (ioredis)  │  │  (S3/Local)    │ │
│  └─────────────┘  └─────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Backend Stack - Node.js/TypeScript

### بنية المشروع الكاملة

```
backend/
├── src/
│   ├── config/
│   │   ├── database.config.ts      # Prisma configuration
│   │   ├── redis.config.ts         # Redis configuration
│   │   ├── gemini.config.ts        # Gemini API config
│   │   └── app.config.ts           # App settings
│   │
│   ├── types/
│   │   ├── agent.types.ts          # Agent type definitions
│   │   ├── session.types.ts        # Session types
│   │   ├── idea.types.ts           # Idea types
│   │   ├── tournament.types.ts     # Tournament types
│   │   └── index.ts                # Export all types
│   │
│   ├── schemas/                    # Zod validation schemas
│   │   ├── auth.schema.ts
│   │   ├── session.schema.ts
│   │   ├── agent.schema.ts
│   │   ├── idea.schema.ts
│   │   ├── tournament.schema.ts
│   │   └── index.ts
│   │
│   ├── services/
│   │   ├── orchestrator.service.ts      # Master orchestrator
│   │   ├── agent-manager.service.ts     # 11 Agents manager
│   │   ├── session.service.ts           # Session lifecycle
│   │   ├── idea-generator.service.ts    # Idea generation
│   │   ├── review-engine.service.ts     # Review system
│   │   ├── tournament-manager.service.ts # Tournament logic
│   │   ├── decision-maker.service.ts    # Final decision
│   │   └── index.ts
│   │
│   ├── integrations/
│   │   ├── gemini/
│   │   │   ├── gemini-client.ts         # Gemini API client
│   │   │   ├── prompt-builder.ts        # Prompt engineering
│   │   │   ├── streaming-handler.ts     # Stream responses
│   │   │   ├── retry-handler.ts         # Retry logic
│   │   │   └── index.ts
│   │   └── storage/
│   │       ├── file-storage.service.ts  # File uploads
│   │       └── index.ts
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.routes.ts           # Auth endpoints
│   │   │   ├── session.routes.ts        # Session CRUD
│   │   │   ├── agent.routes.ts          # Agent management
│   │   │   ├── idea.routes.ts           # Idea generation
│   │   │   ├── tournament.routes.ts     # Tournament
│   │   │   ├── decision.routes.ts       # Decisions
│   │   │   └── index.ts
│   │   │
│   │   ├── middlewares/
│   │   │   ├── auth.middleware.ts       # JWT verification
│   │   │   ├── error.middleware.ts      # Error handling
│   │   │   ├── validate.middleware.ts   # Zod validation
│   │   │   ├── rate-limit.middleware.ts # Rate limiting
│   │   │   └── index.ts
│   │   │
│   │   └── websocket/
│   │       ├── connection-manager.ts    # WS connections
│   │       ├── event-handlers.ts        # WS events
│   │       └── index.ts
│   │
│   ├── utils/
│   │   ├── logger.ts                    # Winston logger
│   │   ├── encryption.ts                # Crypto utilities
│   │   ├── jwt.ts                       # JWT helpers
│   │   ├── errors.ts                    # Custom errors
│   │   └── index.ts
│   │
│   ├── app.ts                           # Fastify app setup
│   └── server.ts                        # Server entry point
│
├── prisma/
│   ├── schema.prisma                    # Database schema
│   ├── migrations/                      # DB migrations
│   └── seed.ts                          # Seed data
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env.example
├── package.json
├── tsconfig.json
├── Dockerfile
└── README.md
```

---

## 📝 package.json الكامل

```json
{
  "name": "jules-backend",
  "version": "1.0.0",
  "description": "Jules Narrative Development Platform - Backend API",
  "main": "dist/server.js",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc && tsc-alias",
    "start": "node dist/server.js",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:studio": "prisma studio",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    "format": "prettier --write \"src/**/*.ts\"",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@fastify/cors": "^9.0.1",
    "@fastify/helmet": "^11.1.1",
    "@fastify/jwt": "^8.0.0",
    "@fastify/multipart": "^8.1.0",
    "@fastify/rate-limit": "^9.1.0",
    "@fastify/static": "^7.0.1",
    "@fastify/websocket": "^10.0.1",
    "@google/generative-ai": "^0.21.0",
    "@prisma/client": "^5.19.0",
    "bcrypt": "^5.1.1",
    "dotenv": "^16.4.5",
    "fastify": "^4.28.1",
    "ioredis": "^5.4.1",
    "jsonwebtoken": "^9.0.2",
    "p-retry": "^6.2.0",
    "pino": "^9.3.2",
    "pino-pretty": "^11.2.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/bcrypt": "^5.0.2",
    "@types/jest": "^29.5.12",
    "@types/jsonwebtoken": "^9.0.6",
    "@types/node": "^22.5.0",
    "@typescript-eslint/eslint-plugin": "^8.2.0",
    "@typescript-eslint/parser": "^8.2.0",
    "eslint": "^9.9.0",
    "jest": "^29.7.0",
    "prettier": "^3.3.3",
    "prisma": "^5.19.0",
    "ts-jest": "^29.2.4",
    "tsc-alias": "^1.8.10",
    "tsx": "^4.17.0",
    "typescript": "^5.5.4"
  },
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  }
}
```

---

## 🗄️ Prisma Schema الكامل

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ============================================
// User Management
// ============================================

model User {
  id            String    @id @default(uuid())
  email         String    @unique
  hashedPassword String   @map("hashed_password")
  fullName      String?   @map("full_name")
  isActive      Boolean   @default(true) @map("is_active")
  isVerified    Boolean   @default(false) @map("is_verified")
  
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")
  lastLogin     DateTime? @map("last_login")
  
  // Relations
  apiKeys       ApiKey[]
  sessions      Session[]
  activityLogs  ActivityLog[]
  
  @@map("users")
  @@index([email])
  @@index([createdAt])
}

// ============================================
// API Key Management
// ============================================

model ApiKey {
  id            String    @id @default(uuid())
  userId        String    @map("user_id")
  encryptedKey  String    @map("encrypted_key")
  keyName       String?   @map("key_name")
  isActive      Boolean   @default(true) @map("is_active")
  quotaLimit    Int?      @map("quota_limit")
  quotaUsed     Int       @default(0) @map("quota_used")
  
  lastUsedAt    DateTime? @map("last_used_at")
  expiresAt     DateTime? @map("expires_at")
  createdAt     DateTime  @default(now()) @map("created_at")
  
  // Relations
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  sessions      Session[]
  
  @@map("api_keys")
  @@index([userId])
  @@index([isActive])
}

// ============================================
// Session Management
// ============================================

enum SessionStatus {
  INITIALIZED
  BRIEF_SUBMITTED
  IDEAS_GENERATING
  IDEAS_GENERATED
  REVIEWING
  TOURNAMENT_ACTIVE
  DECISION_MADE
  COMPLETED
  FAILED
}

enum SessionPhase {
  BRIEF
  IDEA_GENERATION
  INDEPENDENT_REVIEW
  TOURNAMENT
  FINAL_DECISION
}

model Session {
  id            String        @id @default(uuid())
  userId        String        @map("user_id")
  apiKeyId      String        @map("api_key_id")
  
  status        SessionStatus @default(INITIALIZED)
  currentPhase  SessionPhase  @default(BRIEF) @map("current_phase")
  
  sessionData   Json          @default("{}") @map("session_data")
  metadata      Json          @default("{}") @map("metadata")
  
  createdAt     DateTime      @default(now()) @map("created_at")
  updatedAt     DateTime      @updatedAt @map("updated_at")
  completedAt   DateTime?     @map("completed_at")
  
  // Relations
  user          User          @relation(fields: [userId], references: [id], onDelete: Cascade)
  apiKey        ApiKey        @relation(fields: [apiKeyId], references: [id])
  agents        Agent[]
  creativeBrief CreativeBrief?
  ideas         Idea[]
  reviews       Review[]
  tournament    Tournament?
  finalDecision FinalDecision?
  activityLogs  ActivityLog[]
  
  @@map("sessions")
  @@index([userId])
  @@index([status])
  @@index([createdAt])
}

// ============================================
// Agent Management
// ============================================

enum AgentType {
  STORY_ARCHITECT
  REALISM_CRITIC
  STRATEGIC_ANALYST
  CHARACTER_DEVELOPMENT
  CHARACTER_EXPANSION
  WORLD_BUILDING
  DIALOGUE_VOICE
  THEME
  GENRE_TONE
  PACING
  CONFLICT_TENSION
}

model Agent {
  id            String     @id @default(uuid())
  sessionId     String     @map("session_id")
  
  agentType     AgentType  @map("agent_type")
  agentName     String     @map("agent_name")
  guideContent  String?    @map("guide_content") @db.Text
  
  modelName     String     @default("gemini-2.5-pro") @map("model_name")
  temperature   Float      @default(0.7)
  maxTokens     Int        @default(6000) @map("max_tokens")
  
  status        String     @default("initialized")
  isActive      Boolean    @default(true) @map("is_active")
  
  config        Json       @default("{}")
  statistics    Json       @default("{}")
  
  createdAt     DateTime   @default(now()) @map("created_at")
  
  // Relations
  session       Session    @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  reviews       Review[]
  
  @@map("agents")
  @@index([sessionId])
  @@index([agentType])
}

// ============================================
// Creative Brief
// ============================================

model CreativeBrief {
  id              String   @id @default(uuid())
  sessionId       String   @unique @map("session_id")
  
  coreIdea        String   @map("core_idea") @db.Text
  genre           String
  targetAudience  String?  @map("target_audience") @db.Text
  
  mainCharacters  Json     @default("[]") @map("main_characters")
  themes          Json     @default("[]")
  constraints     Json     @default("{}")
  preferences     Json     @default("{}")
  
  createdAt       DateTime @default(now()) @map("created_at")
  updatedAt       DateTime @updatedAt @map("updated_at")
  
  // Relations
  session         Session  @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  
  @@map("creative_briefs")
  @@index([sessionId])
}

// ============================================
// Ideas
// ============================================

model Idea {
  id                  String   @id @default(uuid())
  sessionId           String   @map("session_id")
  ideaNumber          Int      @map("idea_number")
  
  title               String
  logline             String   @db.Text
  synopsis            String   @db.Text
  
  threeActStructure   Json     @map("three_act_structure")
  mainCharacters      Json     @default("[]") @map("main_characters")
  keyScenes           Json     @default("[]") @map("key_scenes")
  thematicElements    Json     @default("[]") @map("thematic_elements")
  uniqueSellingPoints Json     @default("[]") @map("unique_selling_points")
  
  generatedByAgents   Json     @map("generated_by_agents")
  generationMetadata  Json     @default("{}") @map("generation_metadata")
  
  generatedAt         DateTime @default(now()) @map("generated_at")
  
  // Relations
  session             Session  @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  reviews             Review[]
  winningDecisions    FinalDecision[] @relation("WinningIdea")
  losingDecisions     FinalDecision[] @relation("LosingIdea")
  
  @@unique([sessionId, ideaNumber])
  @@map("ideas")
  @@index([sessionId])
}

// ============================================
// Reviews
// ============================================

model Review {
  id                String   @id @default(uuid())
  sessionId         String   @map("session_id")
  agentId           String   @map("agent_id")
  ideaId            String   @map("idea_id")
  
  qualityScore      Float    @map("quality_score")
  noveltyScore      Float    @map("novelty_score")
  impactScore       Float    @map("impact_score")
  
  qualityAnalysis   String   @map("quality_analysis") @db.Text
  noveltyAnalysis   String   @map("novelty_analysis") @db.Text
  impactAnalysis    String   @map("impact_analysis") @db.Text
  
  strengths         Json     @default("[]")
  weaknesses        Json     @default("[]")
  recommendations   Json     @default("[]")
  
  overallVerdict    String   @map("overall_verdict") @db.Text
  reviewMetadata    Json     @default("{}") @map("review_metadata")
  
  createdAt         DateTime @default(now()) @map("created_at")
  
  // Relations
  session           Session  @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  agent             Agent    @relation(fields: [agentId], references: [id], onDelete: Cascade)
  idea              Idea     @relation(fields: [ideaId], references: [id], onDelete: Cascade)
  
  @@unique([agentId, ideaId])
  @@map("reviews")
  @@index([sessionId])
  @@index([agentId])
  @@index([ideaId])
}

// ============================================
// Tournament
// ============================================

enum TournamentStatus {
  ACTIVE
  COMPLETED
  CANCELLED
}

model Tournament {
  id              String           @id @default(uuid())
  sessionId       String           @unique @map("session_id")
  
  status          TournamentStatus @default(ACTIVE)
  currentTurn     Int              @default(0) @map("current_turn")
  maxTurns        Int              @default(8) @map("max_turns")
  
  tournamentData  Json             @default("{}") @map("tournament_data")
  
  startedAt       DateTime         @default(now()) @map("started_at")
  endedAt         DateTime?        @map("ended_at")
  
  // Relations
  session         Session          @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  turns           TournamentTurn[]
  finalDecision   FinalDecision?
  
  @@map("tournaments")
  @@index([sessionId])
}

// ============================================
// Tournament Turns
// ============================================

model TournamentTurn {
  id                  String     @id @default(uuid())
  tournamentId        String     @map("tournament_id")
  turnNumber          Int        @map("turn_number")
  
  participatingAgents Json       @map("participating_agents")
  arguments           Json       @default("[]")
  
  turnMetadata        Json       @default("{}") @map("turn_metadata")
  
  createdAt           DateTime   @default(now()) @map("created_at")
  
  // Relations
  tournament          Tournament @relation(fields: [tournamentId], references: [id], onDelete: Cascade)
  
  @@unique([tournamentId, turnNumber])
  @@map("tournament_turns")
  @@index([tournamentId])
  @@index([turnNumber])
}

// ============================================
// Final Decision
// ============================================

model FinalDecision {
  id                          String     @id @default(uuid())
  sessionId                   String     @unique @map("session_id")
  tournamentId                String     @map("tournament_id")
  
  winningIdeaId               String     @map("winning_idea_id")
  losingIdeaId                String     @map("losing_idea_id")
  
  decisionRationale           String     @map("decision_rationale") @db.Text
  keyStrengths                Json       @default("[]") @map("key_strengths")
  addressedWeaknesses         Json       @default("[]") @map("addressed_weaknesses")
  
  voteBreakdown               Json       @map("vote_breakdown")
  unanimous                   Boolean
  confidenceScore             Float      @map("confidence_score")
  
  implementationRecommendations Json     @default("[]") @map("implementation_recommendations")
  nextSteps                   Json       @default("[]") @map("next_steps")
  
  decisionMetadata            Json       @default("{}") @map("decision_metadata")
  
  createdAt                   DateTime   @default(now()) @map("created_at")
  
  // Relations
  session                     Session    @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  tournament                  Tournament @relation(fields: [tournamentId], references: [id])
  winningIdea                 Idea       @relation("WinningIdea", fields: [winningIdeaId], references: [id])
  losingIdea                  Idea       @relation("LosingIdea", fields: [losingIdeaId], references: [id])
  
  @@map("final_decisions")
  @@index([sessionId])
  @@index([winningIdeaId])
}

// ============================================
// Activity Logs
// ============================================

model ActivityLog {
  id                  String    @id @default(uuid())
  sessionId           String?   @map("session_id")
  userId              String?   @map("user_id")
  
  activityType        String    @map("activity_type")
  activityDescription String?   @map("activity_description") @db.Text
  
  activityData        Json      @default("{}") @map("activity_data")
  
  ipAddress           String?   @map("ip_address")
  userAgent           String?   @map("user_agent") @db.Text
  
  createdAt           DateTime  @default(now()) @map("created_at")
  
  // Relations
  session             Session?  @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  user                User?     @relation(fields: [userId], references: [id], onDelete: SetNull)
  
  @@map("activity_logs")
  @@index([sessionId])
  @@index([userId])
  @@index([activityType])
  @@index([createdAt])
}
```

---

## 🔧 ملفات التكوين الأساسية

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@config/*": ["./config/*"],
      "@services/*": ["./services/*"],
      "@utils/*": ["./utils/*"],
      "@types/*": ["./types/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### .env.example

```bash
# ============================================
# Application Configuration
# ============================================
NODE_ENV=development
PORT=8000
HOST=0.0.0.0

# ============================================
# Database Configuration
# ============================================
DATABASE_URL="postgresql://jules_user:password@localhost:5432/jules_db?schema=public"

# ============================================
# Redis Configuration
# ============================================
REDIS_URL="redis://localhost:6379"
REDIS_PASSWORD=
REDIS_DB=0

# ============================================
# JWT Configuration
# ============================================
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=30m
REFRESH_TOKEN_SECRET=your-refresh-token-secret
REFRESH_TOKEN_EXPIRES_IN=7d

# ============================================
# Encryption
# ============================================
ENCRYPTION_KEY=your-32-character-encryption-key-here

# ============================================
# Google Gemini API
# ============================================
GEMINI_API_KEY=your-gemini-api-key-here

# ============================================
# CORS Configuration
# ============================================
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# ============================================
# Rate Limiting
# ============================================
RATE_LIMIT_MAX=100
RATE_LIMIT_TIMEWINDOW=60000

# ============================================
# File Upload
# ============================================
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# ============================================
# Logging
# ============================================
LOG_LEVEL=info
```

---

## 💻 أمثلة الكود Production-Ready

### 1. Gemini Client Integration

```typescript
// src/integrations/gemini/gemini-client.ts

import { GoogleGenerativeAI, GenerativeModel } from '@google/generative-ai';
import pRetry from 'p-retry';
import { logger } from '@/utils/logger';
import { GeminiAPIError, RateLimitError } from '@/utils/errors';

interface GeminiClientConfig {
  apiKey: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
}

interface GenerateContentOptions {
  prompt: string;
  systemInstruction?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

export class GeminiClient {
  private genAI: GoogleGenerativeAI;
  private model: GenerativeModel;
  private config: Required<GeminiClientConfig>;

  constructor(config: GeminiClientConfig) {
    this.config = {
      model: config.model || 'gemini-2.5-pro',
      temperature: config.temperature || 0.7,
      maxTokens: config.maxTokens || 8000,
      apiKey: config.apiKey,
    };

    this.genAI = new GoogleGenerativeAI(this.config.apiKey);
    this.model = this.genAI.getGenerativeModel({
      model: this.config.model,
    });

    logger.info('Gemini client initialized', {
      model: this.config.model,
    });
  }

  /**
   * Generate content with retry logic
   */
  async generateContent(
    options: GenerateContentOptions
  ): Promise<string> {
    const { prompt, systemInstruction, temperature, maxTokens } = options;

    try {
      const result = await pRetry(
        async () => {
          const response = await this.model.generateContent({
            contents: [
              {
                role: 'user',
                parts: [
                  {
                    text: systemInstruction
                      ? `${systemInstruction}\n\n${prompt}`
                      : prompt,
                  },
                ],
              },
            ],
            generationConfig: {
              temperature: temperature || this.config.temperature,
              maxOutputTokens: maxTokens || this.config.maxTokens,
            },
          });

          const text = response.response.text();
          
          if (!text) {
            throw new GeminiAPIError('Empty response from Gemini API');
          }

          return text;
        },
        {
          retries: 3,
          factor: 2,
          minTimeout: 1000,
          maxTimeout: 10000,
          onFailedAttempt: (error) => {
            logger.warn('Gemini API retry attempt', {
              attemptNumber: error.attemptNumber,
              retriesLeft: error.retriesLeft,
              error: error.message,
            });

            // Check for rate limiting
            if (error.message.includes('429') || error.message.includes('quota')) {
              throw new RateLimitError('Gemini API rate limit exceeded');
            }
          },
        }
      );

      logger.info('Content generated successfully', {
        promptLength: prompt.length,
        responseLength: result.length,
      });

      return result;
    } catch (error) {
      logger.error('Failed to generate content', {
        error: error instanceof Error ? error.message : String(error),
        prompt: prompt.substring(0, 100),
      });

      if (error instanceof RateLimitError) {
        throw error;
      }

      throw new GeminiAPIError(
        `Failed to generate content: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  /**
   * Generate content with streaming
   */
  async *generateContentStream(
    options: GenerateContentOptions
  ): AsyncGenerator<string, void, unknown> {
    const { prompt, systemInstruction, temperature, maxTokens } = options;

    try {
      const result = await this.model.generateContentStream({
        contents: [
          {
            role: 'user',
            parts: [
              {
                text: systemInstruction
                  ? `${systemInstruction}\n\n${prompt}`
                  : prompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: temperature || this.config.temperature,
          maxOutputTokens: maxTokens || this.config.maxTokens,
        },
      });

      for await (const chunk of result.stream) {
        const text = chunk.text();
        if (text) {
          yield text;
        }
      }

      logger.info('Streaming content generation completed');
    } catch (error) {
      logger.error('Failed to stream content', {
        error: error instanceof Error ? error.message : String(error),
      });

      throw new GeminiAPIError(
        `Failed to stream content: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  /**
   * Count tokens in a prompt
   */
  async countTokens(text: string): Promise<number> {
    try {
      const result = await this.model.countTokens(text);
      return result.totalTokens;
    } catch (error) {
      logger.error('Failed to count tokens', {
        error: error instanceof Error ? error.message : String(error),
      });
      throw new GeminiAPIError('Failed to count tokens');
    }
  }
}

// Connection Pool Manager
export class GeminiClientPool {
  private clients: Map<string, GeminiClient> = new Map();
  private maxPoolSize: number;

  constructor(maxPoolSize: number = 5) {
    this.maxPoolSize = maxPoolSize;
  }

  getClient(apiKey: string, config?: Partial<GeminiClientConfig>): GeminiClient {
    const clientKey = `${apiKey}-${config?.model || 'default'}`;

    if (!this.clients.has(clientKey)) {
      if (this.clients.size >= this.maxPoolSize) {
        // Remove oldest client
        const firstKey = this.clients.keys().next().value;
        this.clients.delete(firstKey);
        logger.info('Removed oldest client from pool', { clientKey: firstKey });
      }

      const client = new GeminiClient({
        apiKey,
        ...config,
      });

      this.clients.set(clientKey, client);
      logger.info('Created new Gemini client', { clientKey });
    }

    return this.clients.get(clientKey)!;
  }

  clearPool(): void {
    this.clients.clear();
    logger.info('Cleared Gemini client pool');
  }

  getPoolSize(): number {
    return this.clients.size;
  }
}

export const geminiClientPool = new GeminiClientPool();

// src/types/agent.types.ts

export enum AgentType {
  STORY_ARCHITECT = 'STORY_ARCHITECT',
  REALISM_CRITIC = 'REALISM_CRITIC',
  STRATEGIC_ANALYST = 'STRATEGIC_ANALYST',
  CHARACTER_DEVELOPMENT = 'CHARACTER_DEVELOPMENT',
  CHARACTER_EXPANSION = 'CHARACTER_EXPANSION',
  WORLD_BUILDING = 'WORLD_BUILDING',
  DIALOGUE_VOICE = 'DIALOGUE_VOICE',
  THEME = 'THEME',
  GENRE_TONE = 'GENRE_TONE',
  PACING = 'PACING',
  CONFLICT_TENSION = 'CONFLICT_TENSION',
}

export interface AgentConfig {
  id: string;
  type: AgentType;
  name: string;
  guideFilePath: string;
  systemInstruction: string;
  temperature: number;
  maxTokens: number;
}

export interface AgentInstance {
  id: string;
  sessionId: string;
  type: AgentType;
  name: string;
  guideContent: string;
  config: AgentConfig;
  status: 'initialized' | 'active' | 'completed' | 'error';
  statistics: {
    totalCalls: number;
    totalTokensUsed: number;
    averageResponseTime: number;
  };
}

export interface AgentResponse {
  agentId: string;
  agentType: AgentType;
  content: string;
  metadata: {
    tokensUsed: number;
    responseTime: number;
    timestamp: Date;
  };
}

export interface ReviewOutput {
  agentId: string;
  agentType: AgentType;
  ideaId: string;
  scores: {
    quality: number;
    novelty: number;
    impact: number;
  };
  analysis: {
    quality: string;
    novelty: string;
    impact: string;
  };
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  overallVerdict: string;
}

export const AGENT_CONFIGS: Record<AgentType, Omit<AgentConfig, 'id'>> = {
  [AgentType.STORY_ARCHITECT]: {
    type: AgentType.STORY_ARCHITECT,
    name: 'مهندس القصة',
    guideFilePath: '/mnt/user-data/uploads/story_architect_agent.md',
    systemInstruction: 'أنت وكيل مهندس القصة المتخصص في البنية السردية والتطوير الدرامي.',
    temperature: 0.7,
    maxTokens: 6000,
  },
  [AgentType.REALISM_CRITIC]: {
    type: AgentType.REALISM_CRITIC,
    name: 'ناقد الواقعية',
    guideFilePath: '/mnt/user-data/uploads/realism_critic_guide.md',
    systemInstruction: 'أنت وكيل ناقد الواقعية المتخصص في التحقق من أصالة ومنطقية القصص.',
    temperature: 0.6,
    maxTokens: 6000,
  },
  [AgentType.STRATEGIC_ANALYST]: {
    type: AgentType.STRATEGIC_ANALYST,
    name: 'المحلل الاستراتيجي',
    guideFilePath: '/mnt/user-data/uploads/strategic_analyst_agent_guide.md',
    systemInstruction: 'أنت وكيل المحلل الاستراتيجي المتخصص في تحليل السوق والجدوى التجارية.',
    temperature: 0.5,
    maxTokens: 6000,
  },
  [AgentType.CHARACTER_DEVELOPMENT]: {
    type: AgentType.CHARACTER_DEVELOPMENT,
    name: 'تطوير الشخصيات',
    guideFilePath: '/mnt/user-data/uploads/character_development_agent.md',
    systemInstruction: 'أنت وكيل تطوير الشخصيات المتخصص في بناء الشخصيات المعقدة والنفسية.',
    temperature: 0.8,
    maxTokens: 6000,
  },
  [AgentType.CHARACTER_EXPANSION]: {
    type: AgentType.CHARACTER_EXPANSION,
    name: 'توسيع الشخصيات',
    guideFilePath: '/mnt/user-data/uploads/character_expansion_agent_guide.md',
    systemInstruction: 'أنت وكيل توسيع الشخصيات المتخصص في تطوير الشخصيات الثانوية والنظام البيئي للشخصيات.',
    temperature: 0.75,
    maxTokens: 6000,
  },
  [AgentType.WORLD_BUILDING]: {
    type: AgentType.WORLD_BUILDING,
    name: 'بناء العالم',
    guideFilePath: '/mnt/user-data/uploads/world_building_agent.md',
    systemInstruction: 'أنت وكيل بناء العالم المتخصص في إنشاء عوالم موثوقة وغامرة.',
    temperature: 0.7,
    maxTokens: 6000,
  },
  [AgentType.DIALOGUE_VOICE]: {
    type: AgentType.DIALOGUE_VOICE,
    name: 'الحوار والصوت',
    guideFilePath: '/mnt/user-data/uploads/dialogue_voice_agent.md',
    systemInstruction: 'أنت وكيل الحوار والصوت المتخصص في صياغة حوارات أصيلة ومميزة.',
    temperature: 0.8,
    maxTokens: 6000,
  },
  [AgentType.THEME]: {
    type: AgentType.THEME,
    name: 'الموضوع',
    guideFilePath: '/mnt/user-data/uploads/theme_agent_guide.md',
    systemInstruction: 'أنت وكيل الموضوع المتخصص في استكشاف الحقائق الفلسفية والإنسانية.',
    temperature: 0.7,
    maxTokens: 6000,
  },
  [AgentType.GENRE_TONE]: {
    type: AgentType.GENRE_TONE,
    name: 'النوع والنبرة',
    guideFilePath: '/mnt/user-data/uploads/genre_tone_agent.md',
    systemInstruction: 'أنت وكيل النوع والنبرة المتخصص في التناسق الجوي والتوقعات الأدبية.',
    temperature: 0.6,
    maxTokens: 6000,
  },
  [AgentType.PACING]: {
    type: AgentType.PACING,
    name: 'السرعة والإيقاع',
    guideFilePath: '/mnt/user-data/uploads/pacing_agent_guide.md',
    systemInstruction: 'أنت وكيل السرعة والإيقاع المتخصص في التحكم في تدفق السرد والتوتر.',
    temperature: 0.65,
    maxTokens: 6000,
  },
  [AgentType.CONFLICT_TENSION]: {
    type: AgentType.CONFLICT_TENSION,
    name: 'الصراع والتوتر',
    guideFilePath: '/mnt/user-data/uploads/conflict_tension_guide.md',
    systemInstruction: 'أنت وكيل الصراع والتوتر المتخصص في تصعيد المخاطر وتصميم العقبات.',
    temperature: 0.7,
    maxTokens: 6000,
  },
};
```

---

### `src/types/session.types.ts`

```typescript
// src/types/session.types.ts

export enum SessionStatus {
  INITIALIZED = 'INITIALIZED',
  BRIEF_SUBMITTED = 'BRIEF_SUBMITTED',
  IDEAS_GENERATING = 'IDEAS_GENERATING',
  IDEAS_GENERATED = 'IDEAS_GENERATED',
  REVIEWING = 'REVIEWING',
  TOURNAMENT_ACTIVE = 'TOURNAMENT_ACTIVE',
  DECISION_MADE = 'DECISION_MADE',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
}

export enum SessionPhase {
  BRIEF = 'BRIEF',
  IDEA_GENERATION = 'IDEA_GENERATION',
  INDEPENDENT_REVIEW = 'INDEPENDENT_REVIEW',
  TOURNAMENT = 'TOURNAMENT',
  FINAL_DECISION = 'FINAL_DECISION',
}

export interface CreativeBrief {
  coreIdea: string;
  genre: string;
  targetAudience?: string;
  mainCharacters: Array<{
    name: string;
    role: string;
    description: string;
  }>;
  themes: string[];
  constraints?: Record<string, any>;
  preferences?: Record<string, any>;
}

export interface SessionData {
  brief?: CreativeBrief;
  ideas?: any[];
  reviews?: any[];
  tournament?: any;
  finalDecision?: any;
  metadata: {
    totalTokensUsed: number;
    totalDuration: number;
    phaseTimings: Record<SessionPhase, number>;
  };
}

export interface SessionProgress {
  sessionId: string;
  status: SessionStatus;
  currentPhase: SessionPhase;
  progress: {
    completed: string[];
    current: string;
    remaining: string[];
    percentage: number;
  };
  estimatedTimeRemaining?: number;
}
```

---

### `src/types/idea.types.ts`

```typescript
// src/types/idea.types.ts

export interface ThreeActStructure {
  actOne: {
    setup: string;
    incitingIncident: string;
    plotPoint1: string;
  };
  actTwo: {
    risingAction: string;
    midpoint: string;
    complications: string;
    plotPoint2: string;
  };
  actThree: {
    climax: string;
    resolution: string;
    newEquilibrium: string;
  };
}

export interface Character {
  name: string;
  role: string;
  description: string;
  arc?: string;
  motivation?: string;
  conflict?: string;
}

export interface KeyScene {
  sceneNumber: number;
  title: string;
  description: string;
  purpose: string;
  emotionalBeat: string;
}

export interface Idea {
  id: string;
  sessionId: string;
  ideaNumber: 1 | 2;
  title: string;
  logline: string;
  synopsis: string;
  threeActStructure: ThreeActStructure;
  mainCharacters: Character[];
  keyScenes: KeyScene[];
  thematicElements: string[];
  uniqueSellingPoints: string[];
  generatedBy: {
    storyArchitect: string;
    characterDevelopment: string;
  };
  metadata: {
    generatedAt: Date;
    tokensUsed: number;
    generationTime: number;
  };
}

export interface IdeaGenerationRequest {
  sessionId: string;
  brief: CreativeBrief;
  ideaNumber: 1 | 2;
}

export interface IdeaGenerationResponse {
  idea: Idea;
  success: boolean;
  error?: string;
}
```

---

### `src/types/tournament.types.ts`

```typescript
// src/types/tournament.types.ts

import { AgentType } from './agent.types';

export enum TournamentStatus {
  ACTIVE = 'ACTIVE',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
}

export interface TournamentArgument {
  agentId: string;
  agentType: AgentType;
  agentName: string;
  position: 'supporting_idea_1' | 'supporting_idea_2' | 'neutral';
  argument: string;
  keyPoints: string[];
  rebuttal?: string;
  timestamp: Date;
}

export interface TournamentTurn {
  turnNumber: number;
  participatingAgents: Array<{
    agentId: string;
    agentType: AgentType;
    agentName: string;
  }>;
  arguments: TournamentArgument[];
  summary: string;
  shiftInMomentum?: {
    before: { idea1Support: number; idea2Support: number };
    after: { idea1Support: number; idea2Support: number };
  };
}

export interface TournamentData {
  sessionId: string;
  idea1Id: string;
  idea2Id: string;
  turns: TournamentTurn[];
  currentTurn: number;
  maxTurns: number;
  status: TournamentStatus;
  startedAt: Date;
  endedAt?: Date;
}

export interface TournamentProgress {
  tournamentId: string;
  status: TournamentStatus;
  currentTurn: number;
  maxTurns: number;
  idea1Support: number;
  idea2Support: number;
  neutralAgents: number;
}
```

---

## 📁 **2. Validation Schemas (Zod)**

### `src/schemas/auth.schema.ts`

```typescript
// src/schemas/auth.schema.ts

import { z } from 'zod';

export const registerSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
      'Password must contain uppercase, lowercase, number and special character'
    ),
  fullName: z.string().min(2, 'Full name must be at least 2 characters').optional(),
});

export const loginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(1, 'Password is required'),
});

export const apiKeySchema = z.object({
  geminiApiKey: z
    .string()
    .min(20, 'Invalid API key format')
    .startsWith('AIza', 'Invalid Gemini API key format'),
  keyName: z.string().min(1, 'Key name is required').optional(),
  quotaLimit: z.number().positive().optional(),
});

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput = z.infer<typeof loginSchema>;
export type ApiKeyInput = z.infer<typeof apiKeySchema>;
```

---

### `src/schemas/session.schema.ts`

```typescript
// src/schemas/session.schema.ts

import { z } from 'zod';

const characterSchema = z.object({
  name: z.string().min(1, 'Character name is required'),
  role: z.string().min(1, 'Character role is required'),
  description: z.string().min(10, 'Character description must be at least 10 characters'),
});

export const creativeBriefSchema = z.object({
  coreIdea: z.string().min(50, 'Core idea must be at least 50 characters'),
  genre: z.string().min(3, 'Genre is required'),
  targetAudience: z.string().optional(),
  mainCharacters: z.array(characterSchema).min(1, 'At least one main character is required'),
  themes: z.array(z.string()).min(1, 'At least one theme is required'),
  constraints: z.record(z.any()).optional(),
  preferences: z.record(z.any()).optional(),
});

export const createSessionSchema = z.object({
  apiKeyId: z.string().uuid('Invalid API key ID'),
});

export const updateSessionStatusSchema = z.object({
  status: z.enum([
    'INITIALIZED',
    'BRIEF_SUBMITTED',
    'IDEAS_GENERATING',
    'IDEAS_GENERATED',
    'REVIEWING',
    'TOURNAMENT_ACTIVE',
    'DECISION_MADE',
    'COMPLETED',
    'FAILED',
  ]),
});

export type CreativeBriefInput = z.infer<typeof creativeBriefSchema>;
export type CreateSessionInput = z.infer<typeof createSessionSchema>;
export type UpdateSessionStatusInput = z.infer<typeof updateSessionStatusSchema>;
```

---

## 📁 **3. Core Services**

### `src/services/agent-manager.service.ts`

```typescript
// src/services/agent-manager.service.ts

import { PrismaClient } from '@prisma/client';
import { readFile } from 'fs/promises';
import { AgentType, AgentInstance, AGENT_CONFIGS, AgentResponse } from '@/types/agent.types';
import { GeminiClient, geminiClientPool } from '@/integrations/gemini/gemini-client';
import { logger } from '@/utils/logger';
import { ServiceError } from '@/utils/errors';

export class AgentManagerService {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  /**
   * Initialize all 11 agents for a session
   */
  async initializeAgents(sessionId: string, apiKey: string): Promise<AgentInstance[]> {
    try {
      logger.info('Initializing agents for session', { sessionId });

      const agentInstances: AgentInstance[] = [];

      for (const [agentType, config] of Object.entries(AGENT_CONFIGS)) {
        // Read guide content from file
        const guideContent = await this.loadGuideContent(config.guideFilePath);

        // Create agent in database
        const agent = await this.prisma.agent.create({
          data: {
            sessionId,
            agentType: agentType as AgentType,
            agentName: config.name,
            guideContent,
            modelName: 'gemini-2.5-pro',
            temperature: config.temperature,
            maxTokens: config.maxTokens,
            status: 'initialized',
            config: config as any,
            statistics: {
              totalCalls: 0,
              totalTokensUsed: 0,
              averageResponseTime: 0,
            },
          },
        });

        agentInstances.push({
          id: agent.id,
          sessionId: agent.sessionId,
          type: agent.agentType as AgentType,
          name: agent.agentName,
          guideContent: agent.guideContent || '',
          config: agent.config as any,
          status: 'initialized',
          statistics: agent.statistics as any,
        });
      }

      logger.info('All agents initialized successfully', {
        sessionId,
        agentCount: agentInstances.length,
      });

      return agentInstances;
    } catch (error) {
      logger.error('Failed to initialize agents', {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to initialize agents', 500);
    }
  }

  /**
   * Load guide content from file
   */
  private async loadGuideContent(filePath: string): Promise<string> {
    try {
      const content = await readFile(filePath, 'utf-8');
      return content;
    } catch (error) {
      logger.warn('Failed to load guide content from file', {
        filePath,
        error: error instanceof Error ? error.message : String(error),
      });
      // Return default instruction if file not found
      return 'أنت وكيل متخصص في تطوير القصص. اتبع التعليمات بدقة.';
    }
  }

  /**
   * Execute agent with prompt
   */
  async executeAgent(
    agentId: string,
    prompt: string,
    apiKey: string,
    stream: boolean = false
  ): Promise<AgentResponse> {
    const startTime = Date.now();

    try {
      // Get agent from database
      const agent = await this.prisma.agent.findUnique({
        where: { id: agentId },
      });

      if (!agent) {
        throw new ServiceError('Agent not found', 404);
      }

      // Get Gemini client
      const geminiClient = geminiClientPool.getClient(apiKey, {
        model: agent.modelName,
        temperature: agent.temperature,
        maxTokens: agent.maxTokens,
      });

      // Build full prompt with guide content
      const systemInstruction = agent.guideContent || '';

      // Generate content
      const content = await geminiClient.generateContent({
        prompt,
        systemInstruction,
        temperature: agent.temperature,
        maxTokens: agent.maxTokens,
      });

      const responseTime = Date.now() - startTime;

      // Update agent statistics
      const currentStats = agent.statistics as any;
      const newStats = {
        totalCalls: (currentStats.totalCalls || 0) + 1,
        totalTokensUsed: (currentStats.totalTokensUsed || 0) + content.length / 4, // Rough estimate
        averageResponseTime:
          ((currentStats.averageResponseTime || 0) * (currentStats.totalCalls || 0) + responseTime) /
          ((currentStats.totalCalls || 0) + 1),
      };

      await this.prisma.agent.update({
        where: { id: agentId },
        data: {
          statistics: newStats,
          status: 'active',
        },
      });

      logger.info('Agent executed successfully', {
        agentId,
        agentType: agent.agentType,
        responseTime,
        contentLength: content.length,
      });

      return {
        agentId: agent.id,
        agentType: agent.agentType as AgentType,
        content,
        metadata: {
          tokensUsed: content.length / 4,
          responseTime,
          timestamp: new Date(),
        },
      };
    } catch (error) {
      logger.error('Failed to execute agent', {
        agentId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw error;
    }
  }

  /**
   * Get all agents for a session
   */
  async getSessionAgents(sessionId: string): Promise<AgentInstance[]> {
    try {
      const agents = await this.prisma.agent.findMany({
        where: { sessionId },
        orderBy: { createdAt: 'asc' },
      });

      return agents.map((agent) => ({
        id: agent.id,
        sessionId: agent.sessionId,
        type: agent.agentType as AgentType,
        name: agent.agentName,
        guideContent: agent.guideContent || '',
        config: agent.config as any,
        status: agent.status as any,
        statistics: agent.statistics as any,
      }));
    } catch (error) {
      logger.error('Failed to get session agents', {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to get session agents', 500);
    }
  }

  /**
   * Get agent by type
   */
  async getAgentByType(sessionId: string, agentType: AgentType): Promise<AgentInstance | null> {
    try {
      const agent = await this.prisma.agent.findFirst({
        where: {
          sessionId,
          agentType,
        },
      });

      if (!agent) {
        return null;
      }

      return {
        id: agent.id,
        sessionId: agent.sessionId,
        type: agent.agentType as AgentType,
        name: agent.agentName,
        guideContent: agent.guideContent || '',
        config: agent.config as any,
        status: agent.status as any,
        statistics: agent.statistics as any,
      };
    } catch (error) {
      logger.error('Failed to get agent by type', {
        sessionId,
        agentType,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to get agent by type', 500);
    }
  }
}



// src/services/orchestrator.service.ts

import { PrismaClient } from '@prisma/client';
import { SessionStatus, SessionPhase, SessionProgress } from '@/types/session.types';
import { AgentManagerService } from './agent-manager.service';
import { SessionService } from './session.service';
import { IdeaGeneratorService } from './idea-generator.service';
import { ReviewEngineService } from './review-engine.service';
import { TournamentManagerService } from './tournament-manager.service';
import { DecisionMakerService } from './decision-maker.service';
import { logger } from '@/utils/logger';
import { ServiceError } from '@/utils/errors';
import { EventEmitter } from 'events';

interface OrchestratorConfig {
  sessionId: string;
  userId: string;
  apiKey: string;
}

export class OrchestratorService extends EventEmitter {
  private prisma: PrismaClient;
  private config: OrchestratorConfig;
  private agentManager: AgentManagerService;
  private sessionService: SessionService;
  private ideaGenerator: IdeaGeneratorService;
  private reviewEngine: ReviewEngineService;
  private tournamentManager: TournamentManagerService;
  private decisionMaker: DecisionMakerService;

  constructor(prisma: PrismaClient, config: OrchestratorConfig) {
    super();
    this.prisma = prisma;
    this.config = config;

    // Initialize services
    this.agentManager = new AgentManagerService(prisma);
    this.sessionService = new SessionService(prisma);
    this.ideaGenerator = new IdeaGeneratorService(prisma, this.agentManager);
    this.reviewEngine = new ReviewEngineService(prisma, this.agentManager);
    this.tournamentManager = new TournamentManagerService(prisma, this.agentManager);
    this.decisionMaker = new DecisionMakerService(prisma, this.agentManager);

    logger.info('Orchestrator initialized', { sessionId: config.sessionId });
  }

  /**
   * Start the complete narrative development process
   */
  async startProcess(): Promise<void> {
    try {
      logger.info('Starting narrative development process', {
        sessionId: this.config.sessionId,
      });

      // Phase 1: Initialize agents
      await this.executePhase(SessionPhase.BRIEF, async () => {
        await this.initializeAgentsPhase();
      });

      // Phase 2: Generate ideas
      await this.executePhase(SessionPhase.IDEA_GENERATION, async () => {
        await this.generateIdeasPhase();
      });

      // Phase 3: Independent reviews
      await this.executePhase(SessionPhase.INDEPENDENT_REVIEW, async () => {
        await this.conductReviewsPhase();
      });

      // Phase 4: Tournament
      await this.executePhase(SessionPhase.TOURNAMENT, async () => {
        await this.conductTournamentPhase();
      });

      // Phase 5: Final decision
      await this.executePhase(SessionPhase.FINAL_DECISION, async () => {
        await this.makeFinalDecisionPhase();
      });

      // Mark session as completed
      await this.sessionService.updateSessionStatus(
        this.config.sessionId,
        SessionStatus.COMPLETED
      );

      logger.info('Narrative development process completed successfully', {
        sessionId: this.config.sessionId,
      });

      this.emit('process:completed', { sessionId: this.config.sessionId });
    } catch (error) {
      logger.error('Narrative development process failed', {
        sessionId: this.config.sessionId,
        error: error instanceof Error ? error.message : String(error),
      });

      await this.sessionService.updateSessionStatus(
        this.config.sessionId,
        SessionStatus.FAILED
      );

      this.emit('process:failed', {
        sessionId: this.config.sessionId,
        error: error instanceof Error ? error.message : String(error),
      });

      throw error;
    }
  }

  /**
   * Execute a phase with error handling and progress tracking
   */
  private async executePhase(
    phase: SessionPhase,
    executor: () => Promise<void>
  ): Promise<void> {
    const startTime = Date.now();

    try {
      logger.info(`Starting phase: ${phase}`, { sessionId: this.config.sessionId });

      // Update session phase
      await this.sessionService.updateSessionPhase(this.config.sessionId, phase);

      this.emit('phase:started', {
        sessionId: this.config.sessionId,
        phase,
      });

      // Execute phase logic
      await executor();

      const duration = Date.now() - startTime;

      logger.info(`Phase completed: ${phase}`, {
        sessionId: this.config.sessionId,
        duration,
      });

      this.emit('phase:completed', {
        sessionId: this.config.sessionId,
        phase,
        duration,
      });
    } catch (error) {
      logger.error(`Phase failed: ${phase}`, {
        sessionId: this.config.sessionId,
        error: error instanceof Error ? error.message : String(error),
      });

      this.emit('phase:failed', {
        sessionId: this.config.sessionId,
        phase,
        error: error instanceof Error ? error.message : String(error),
      });

      throw error;
    }
  }

  /**
   * Phase 1: Initialize all agents
   */
  private async initializeAgentsPhase(): Promise<void> {
    logger.info('Initializing agents', { sessionId: this.config.sessionId });

    const agents = await this.agentManager.initializeAgents(
      this.config.sessionId,
      this.config.apiKey
    );

    this.emit('agents:initialized', {
      sessionId: this.config.sessionId,
      agentCount: agents.length,
    });

    logger.info('Agents initialized successfully', {
      sessionId: this.config.sessionId,
      agentCount: agents.length,
    });
  }

  /**
   * Phase 2: Generate two competing ideas
   */
  private async generateIdeasPhase(): Promise<void> {
    logger.info('Generating ideas', { sessionId: this.config.sessionId });

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.IDEAS_GENERATING
    );

    // Generate both ideas in parallel
    const [idea1, idea2] = await Promise.all([
      this.ideaGenerator.generateIdea(this.config.sessionId, this.config.apiKey, 1),
      this.ideaGenerator.generateIdea(this.config.sessionId, this.config.apiKey, 2),
    ]);

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.IDEAS_GENERATED
    );

    this.emit('ideas:generated', {
      sessionId: this.config.sessionId,
      ideas: [idea1, idea2],
    });

    logger.info('Ideas generated successfully', {
      sessionId: this.config.sessionId,
    });
  }

  /**
   * Phase 3: Conduct independent reviews by all agents
   */
  private async conductReviewsPhase(): Promise<void> {
    logger.info('Conducting reviews', { sessionId: this.config.sessionId });

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.REVIEWING
    );

    const reviews = await this.reviewEngine.conductAllReviews(
      this.config.sessionId,
      this.config.apiKey
    );

    this.emit('reviews:completed', {
      sessionId: this.config.sessionId,
      reviewCount: reviews.length,
    });

    logger.info('Reviews completed successfully', {
      sessionId: this.config.sessionId,
      reviewCount: reviews.length,
    });
  }

  /**
   * Phase 4: Conduct tournament discussion
   */
  private async conductTournamentPhase(): Promise<void> {
    logger.info('Starting tournament', { sessionId: this.config.sessionId });

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.TOURNAMENT_ACTIVE
    );

    const tournament = await this.tournamentManager.conductTournament(
      this.config.sessionId,
      this.config.apiKey
    );

    this.emit('tournament:completed', {
      sessionId: this.config.sessionId,
      tournamentId: tournament.id,
      turnsCompleted: tournament.currentTurn,
    });

    logger.info('Tournament completed successfully', {
      sessionId: this.config.sessionId,
      turnsCompleted: tournament.currentTurn,
    });
  }

  /**
   * Phase 5: Make final decision
   */
  private async makeFinalDecisionPhase(): Promise<void> {
    logger.info('Making final decision', { sessionId: this.config.sessionId });

    const decision = await this.decisionMaker.makeFinalDecision(
      this.config.sessionId,
      this.config.apiKey
    );

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.DECISION_MADE
    );

    this.emit('decision:made', {
      sessionId: this.config.sessionId,
      decisionId: decision.id,
      winningIdeaId: decision.winningIdeaId,
    });

    logger.info('Final decision made successfully', {
      sessionId: this.config.sessionId,
      winningIdeaId: decision.winningIdeaId,
    });
  }

  /**
   * Get current session progress
   */
  async getProgress(): Promise<SessionProgress> {
    const session = await this.sessionService.getSessionById(this.config.sessionId);

    if (!session) {
      throw new ServiceError('Session not found', 404);
    }

    const phases = Object.values(SessionPhase);
    const currentPhaseIndex = phases.indexOf(session.currentPhase);

    return {
      sessionId: session.id,
      status: session.status,
      currentPhase: session.currentPhase,
      progress: {
        completed: phases.slice(0, currentPhaseIndex),
        current: session.currentPhase,
        remaining: phases.slice(currentPhaseIndex + 1),
        percentage: Math.round((currentPhaseIndex / phases.length) * 100),
      },
    };
  }

  /**
   * Cancel the process
   */
  async cancel(): Promise<void> {
    logger.info('Cancelling process', { sessionId: this.config.sessionId });

    await this.sessionService.updateSessionStatus(
      this.config.sessionId,
      SessionStatus.FAILED
    );

    this.emit('process:cancelled', { sessionId: this.config.sessionId });
  }
}
```

---

### `src/services/session.service.ts`

```typescript
// src/services/session.service.ts

import { PrismaClient, Session } from '@prisma/client';
import { SessionStatus, SessionPhase, CreativeBrief } from '@/types/session.types';
import { logger } from '@/utils/logger';
import { ServiceError } from '@/utils/errors';

export class SessionService {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  /**
   * Create a new session
   */
  async createSession(userId: string, apiKeyId: string): Promise<Session> {
    try {
      const session = await this.prisma.session.create({
        data: {
          userId,
          apiKeyId,
          status: SessionStatus.INITIALIZED,
          currentPhase: SessionPhase.BRIEF,
          sessionData: {},
          metadata: {},
        },
      });

      logger.info('Session created', {
        sessionId: session.id,
        userId,
      });

      return session;
    } catch (error) {
      logger.error('Failed to create session', {
        userId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to create session', 500);
    }
  }

  /**
   * Get session by ID
   */
  async getSessionById(sessionId: string): Promise<Session | null> {
    try {
      return await this.prisma.session.findUnique({
        where: { id: sessionId },
        include: {
          user: {
            select: {
              id: true,
              email: true,
              fullName: true,
            },
          },
          creativeBrief: true,
          ideas: true,
          reviews: true,
          tournament: true,
          finalDecision: true,
        },
      });
    } catch (error) {
      logger.error('Failed to get session', {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to get session', 500);
    }
  }

  /**
   * Get user sessions
   */
  async getUserSessions(
    userId: string,
    limit: number = 20,
    offset: number = 0
  ): Promise<{ sessions: Session[]; total: number }> {
    try {
      const [sessions, total] = await Promise.all([
        this.prisma.session.findMany({
          where: { userId },
          orderBy: { createdAt: 'desc' },
          take: limit,
          skip: offset,
          include: {
            creativeBrief: true,
            finalDecision: {
              include: {
                winningIdea: true,
              },
            },
          },
        }),
        this.prisma.session.count({
          where: { userId },
        }),
      ]);

      return { sessions, total };
    } catch (error) {
      logger.error('Failed to get user sessions', {
        userId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to get user sessions', 500);
    }
  }

  /**
   * Submit creative brief
   */
  async submitCreativeBrief(
    sessionId: string,
    brief: CreativeBrief
  ): Promise<void> {
    try {
      await this.prisma.$transaction([
        this.prisma.creativeBrief.create({
          data: {
            sessionId,
            coreIdea: brief.coreIdea,
            genre: brief.genre,
            targetAudience: brief.targetAudience,
            mainCharacters: brief.mainCharacters,
            themes: brief.themes,
            constraints: brief.constraints || {},
            preferences: brief.preferences || {},
          },
        }),
        this.prisma.session.update({
          where: { id: sessionId },
          data: {
            status: SessionStatus.BRIEF_SUBMITTED,
            sessionData: {
              brief,
            },
          },
        }),
      ]);

      logger.info('Creative brief submitted', { sessionId });
    } catch (error) {
      logger.error('Failed to submit creative brief', {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to submit creative brief', 500);
    }
  }

  /**
   * Update session status
   */
  async updateSessionStatus(
    sessionId: string,
    status: SessionStatus
  ): Promise<void> {
    try {
      await this.prisma.session.update({
        where: { id: sessionId },
        data: {
          status,
          ...(status === SessionStatus.COMPLETED && {
            completedAt: new Date(),
          }),
        },
      });

      logger.info('Session status updated', {
        sessionId,
        status,
      });
    } catch (error) {
      logger.error('Failed to update session status', {
        sessionId,
        status,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to update session status', 500);
    }
  }

  /**
   * Update session phase
   */
  async updateSessionPhase(
    sessionId: string,
    phase: SessionPhase
  ): Promise<void> {
    try {
      await this.prisma.session.update({
        where: { id: sessionId },
        data: { currentPhase: phase },
      });

      logger.info('Session phase updated', {
        sessionId,
        phase,
      });
    } catch (error) {
      logger.error('Failed to update session phase', {
        sessionId,
        phase,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to update session phase', 500);
    }
  }

  /**
   * Delete session
   */
  async deleteSession(sessionId: string, userId: string): Promise<void> {
    try {
      // Verify ownership
      const session = await this.prisma.session.findUnique({
        where: { id: sessionId },
        select: { userId: true },
      });

      if (!session) {
        throw new ServiceError('Session not found', 404);
      }

      if (session.userId !== userId) {
        throw new ServiceError('Unauthorized', 403);
      }

      await this.prisma.session.delete({
        where: { id: sessionId },
      });

      logger.info('Session deleted', {
        sessionId,
        userId,
      });
    } catch (error) {
      if (error instanceof ServiceError) {
        throw error;
      }

      logger.error('Failed to delete session', {
        sessionId,
        userId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to delete session', 500);
    }
  }

  /**
   * Log activity
   */
  async logActivity(
    sessionId: string,
    userId: string,
    activityType: string,
    activityData: any
  ): Promise<void> {
    try {
      await this.prisma.activityLog.create({
        data: {
          sessionId,
          userId,
          activityType,
          activityData,
        },
      });
    } catch (error) {
      // Don't throw error for activity logging failures
      logger.warn('Failed to log activity', {
        sessionId,
        activityType,
        error: error instanceof Error ? error.message : String(error),
      });
    }
  }
}
```

---

### `src/services/idea-generator.service.ts`

```typescript
// src/services/idea-generator.service.ts

import { PrismaClient } from '@prisma/client';
import { Idea, ThreeActStructure, Character, KeyScene } from '@/types/idea.types';
import { AgentType } from '@/types/agent.types';
import { AgentManagerService } from './agent-manager.service';
import { logger } from '@/utils/logger';
import { ServiceError } from '@/utils/errors';

export class IdeaGeneratorService {
  private prisma: PrismaClient;
  private agentManager: AgentManagerService;

  constructor(prisma: PrismaClient, agentManager: AgentManagerService) {
    this.prisma = prisma;
    this.agentManager = agentManager;
  }

  /**
   * Generate a complete idea
   */
  async generateIdea(
    sessionId: string,
    apiKey: string,
    ideaNumber: 1 | 2
  ): Promise<Idea> {
    const startTime = Date.now();

    try {
      logger.info(`Generating idea ${ideaNumber}`, { sessionId });

      // Get creative brief
      const brief = await this.prisma.creativeBrief.findUnique({
        where: { sessionId },
      });

      if (!brief) {
        throw new ServiceError('Creative brief not found', 404);
      }

      // Get Story Architect and Character Development agents
      const storyArchitect = await this.agentManager.getAgentByType(
        sessionId,
        AgentType.STORY_ARCHITECT
      );

      const characterDev = await this.agentManager.getAgentByType(
        sessionId,
        AgentType.CHARACTER_DEVELOPMENT
      );

      if (!storyArchitect || !characterDev) {
        throw new ServiceError('Required agents not found', 404);
      }

      // Build collaborative prompt
      const prompt = this.buildIdeaPrompt(brief, ideaNumber);

      // Execute Story Architect
      logger.info('Executing Story Architect', { sessionId, ideaNumber });
      const storyResponse = await this.agentManager.executeAgent(
        storyArchitect.id,
        prompt,
        apiKey
      );

      // Parse story structure
      const storyStructure = this.parseStoryStructure(storyResponse.content);

      // Execute Character Development with story context
      logger.info('Executing Character Development', { sessionId, ideaNumber });
      const characterPrompt = this.buildCharacterPrompt(brief, storyStructure);
      const characterResponse = await this.agentManager.executeAgent(
        characterDev.id,
        characterPrompt,
        apiKey
      );

      // Parse character details
      const characters = this.parseCharacters(characterResponse.content);

      // Combine into complete idea
      const idea: Omit<Idea, 'id'> = {
        sessionId,
        ideaNumber,
        title: storyStructure.title,
        logline: storyStructure.logline,
        synopsis: storyStructure.synopsis,
        threeActStructure: storyStructure.threeActStructure,
        mainCharacters: characters,
        keyScenes: storyStructure.keyScenes,
        thematicElements: storyStructure.thematicElements,
        uniqueSellingPoints: storyStructure.uniqueSellingPoints,
        generatedBy: {
          storyArchitect: storyArchitect.id,
          characterDevelopment: characterDev.id,
        },
        metadata: {
          generatedAt: new Date(),
          tokensUsed:
            storyResponse.metadata.tokensUsed + characterResponse.metadata.tokensUsed,
          generationTime: Date.now() - startTime,
        },
      };

      // Save to database
      const savedIdea = await this.prisma.idea.create({
        data: {
          sessionId: idea.sessionId,
          ideaNumber: idea.ideaNumber,
          title: idea.title,
          logline: idea.logline,
          synopsis: idea.synopsis,
          threeActStructure: idea.threeActStructure as any,
          mainCharacters: idea.mainCharacters as any,
          keyScenes: idea.keyScenes as any,
          thematicElements: idea.thematicElements,
          uniqueSellingPoints: idea.uniqueSellingPoints,
          generatedByAgents: idea.generatedBy as any,
          generationMetadata: idea.metadata as any,
        },
      });

      logger.info(`Idea ${ideaNumber} generated successfully`, {
        sessionId,
        ideaId: savedIdea.id,
        generationTime: Date.now() - startTime,
      });

      return {
        id: savedIdea.id,
        ...idea,
      };
    } catch (error) {
      logger.error(`Failed to generate idea ${ideaNumber}`, {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw error;
    }
  }

  /**
   * Build prompt for story architect
   */
  private buildIdeaPrompt(brief: any, ideaNumber: number): string {
    return `
# مهمة: توليد الفكرة القصصية رقم ${ideaNumber}

## الموجز الإبداعي:
**الفكرة الأساسية:** ${brief.coreIdea}
**النوع الأدبي:** ${brief.genre}
**الجمهور المستهدف:** ${brief.targetAudience || 'غير محدد'}

**الشخصيات الرئيسية:**
${JSON.stringify(brief.mainCharacters, null, 2)}

**المواضيع:**
${brief.themes.join(', ')}

## المطلوب:
قم بإنشاء فكرة قصصية متكاملة وتفصيلية تتضمن:

1. **العنوان:** عنوان جذاب ومعبر
2. **اللوجلاين:** جملة واحدة تلخص القصة (25-35 كلمة)
3. **الملخص:** ملخص شامل للقصة (200-300 كلمة)
4. **البنية الثلاثية:**
   - الفصل الأول: الإعداد، الحادثة المحفزة، نقطة التحول 1
   - الفصل الثاني: الصراع المتصاعد، نقطة المنتصف، نقطة التحول 2
   - الفصل الثالث: الذروة، الحل، التوازن الجديد
5. **المشاهد الرئيسية:** 5-7 مشاهد محورية
6. **العناصر الموضوعية:** المواضيع الفلسفية والإنسانية
7. **نقاط البيع الفريدة:** ما يميز هذه القصة

**تنسيق الاستجابة:**
استخدم JSON بالهيكل التالي:
\`\`\`json
{
  "title": "...",
  "logline": "...",
  "synopsis": "...",
  "threeActStructure": {
    "actOne": {
      "setup": "...",
      "incitingIncident": "...",
      "plotPoint1": "..."
    },
    "actTwo": {
      "risingAction": "...",
      "midpoint": "...",
      "complications": "...",
      "plotPoint2": "..."
    },
    "actThree": {
      "climax": "...",
      "resolution": "...",
      "newEquilibrium": "..."
    }
  },
  "keyScenes": [
    {
      "sceneNumber": 1,
      "title": "...",
      "description": "...",
      "purpose": "...",
      "emotionalBeat": "..."
    }
  ],
  "thematicElements": ["..."],
  "uniqueSellingPoints": ["..."]
}
\`\`\`

**ملاحظات مهمة:**
- يجب أن تكون الفكرة أصلية ومبتكرة
- احترم النوع الأدبي والجمهور المستهدف
- تأكد من وجود صراع واضح ومقنع
- اجعل البنية الدرامية قوية ومحكمة
`;
  }

  /**
   * Build prompt for character development
   */
  private buildCharacterPrompt(brief: any, storyStructure: any): string {
    return `
# مهمة: تطوير الشخصيات بناءً على البنية القصصية

## البنية القصصية:
**العنوان:** ${storyStructure.title}
**الملخص:** ${storyStructure.synopsis}

## الشخصيات من الموجز:
${JSON.stringify(brief.mainCharacters, null, 2)}

## المطلوب:
قم بتطوير كل شخصية بشكل عميق ومفصل، متضمناً:

1. **الاسم والدور**
2. **الوصف المفصل:** المظهر، الشخصية، الخلفية
3. **القوس الدرامي:** كيف تتغير الشخصية خلال القصة
4. **الدافع:** ما الذي يحرك الشخصية
5. **الصراع:** الصراع الداخلي والخارجي

**تنسيق الاستجابة:**
استخدم JSON بالهيكل التالي:
\`\`\`json
[
  {
    "name": "...",
    "role": "...",
    "description": "...",
    "arc": "...",
    "motivation": "...",
    "conflict": "..."
  }
]
\`\`\`

**ملاحظات:**
- يجب أن تكون كل شخصية معقدة وواقعية
- تأكد من أن الشخصيات تخدم القصة
- اجعل دوافع الشخصيات واضحة ومقنعة
`;
  }

  /**
   * Parse story structure from AI response
   */
  private parseStoryStructure(content: string): any {
    try {
      // Extract JSON from markdown code blocks if present
      const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
      const jsonContent = jsonMatch ? jsonMatch[1] : content;

      const parsed = JSON.parse(jsonContent);

      return {
        title: parsed.title || 'قصة بدون عنوان',
        logline: parsed.logline || '',
        synopsis: parsed.synopsis || '',
        threeActStructure: parsed.threeActStructure || {},
        keyScenes: parsed.keyScenes || [],
        thematicElements: parsed.thematicElements || [],
        uniqueSellingPoints: parsed.uniqueSellingPoints || [],
      };
    } catch (error) {
      logger.error('Failed to parse story structure', {
        error: error instanceof Error ? error.message : String(error),
        content: content.substring(0, 500),
      });
      throw new ServiceError('Failed to parse story structure', 500);
    }
  }

  /**
   * Parse characters from AI response
   */
  private parseCharacters(content: string): Character[] {
    try {
      // Extract JSON from markdown code blocks if present
      const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
      const jsonContent = jsonMatch ? jsonMatch[1] : content;

      const parsed = JSON.parse(jsonContent);

      if (!Array.isArray(parsed)) {
        throw new Error('Expected array of characters');
      }

      return parsed.map((char) => ({
        name: char.name || 'شخصية بدون اسم',
        role: char.role || '',
        description: char.description || '',
        arc: char.arc,
        motivation: char.motivation,
        conflict: char.conflict,
      }));
    } catch (error) {
      logger.error('Failed to parse characters', {
        error: error instanceof Error ? error.message : String(error),
        content: content.substring(0, 500),
      });
      throw new ServiceError('Failed to parse characters', 500);
    }
  }

  /**
   * Get all ideas for a session
   */
  async getSessionIdeas(sessionId: string): Promise<Idea[]> {
    try {
      const ideas = await this.prisma.idea.findMany({
        where: { sessionId },
        orderBy: { ideaNumber: 'asc' },
      });

      return ideas.map((idea) => ({
        id: idea.id,
        sessionId: idea.sessionId,
        ideaNumber: idea.ideaNumber as 1 | 2,
        title: idea.title,
        logline: idea.logline,
        synopsis: idea.synopsis,
        threeActStructure: idea.threeActStructure as ThreeActStructure,
        mainCharacters: idea.mainCharacters as Character[],
        keyScenes: idea.keyScenes as KeyScene[],
        thematicElements: idea.thematicElements as string[],
        uniqueSellingPoints: idea.uniqueSellingPoints as string[],
        generatedBy: idea.generatedByAgents as any,
        metadata: idea.generationMetadata as any,
      }));
    } catch (error) {
      logger.error('Failed to get session ideas', {
        sessionId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw new ServiceError('Failed to get session ideas', 500);
    }
  }
}
```

---

بسبب طول الكود، سأتابع في رسالة تالية مع باقي الـ Services والـ API Routes.

