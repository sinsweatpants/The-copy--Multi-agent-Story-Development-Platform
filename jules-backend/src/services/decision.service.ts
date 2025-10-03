import { PrismaClient } from "@prisma/client";
import { AgentService } from "./agent.service";
import { logger } from "../utils/logger";

export class DecisionService {
  private prisma: PrismaClient;
  private agentService: AgentService;

  constructor(prisma: PrismaClient, agentService: AgentService) {
    this.prisma = prisma;
    this.agentService = agentService;
  }

  async makeFinalDecision(
    sessionId: string,
    winningIdeaId: string,
    decisionRationale: string,
    keyStrengths: string[],
    recommendations: string[],
    voteBreakdown: Record<string, any>,
  ) {
    try {
      const finalDecision = await this.prisma.finalDecision.create({
        data: {
          sessionId,
          winningIdeaId,
          decisionRationale,
          keyStrengths,
          recommendations,
          voteBreakdown,
        },
      });

      logger.info("Final decision created", { sessionId, winningIdeaId });
      return finalDecision;
    } catch (error) {
      logger.error("Failed to create final decision", { error, sessionId });
      throw error;
    }
  }

  async getFinalDecisionBySession(sessionId: string) {
    try {
      const finalDecision = await this.prisma.finalDecision.findUnique({
        where: { sessionId },
      });

      return finalDecision;
    } catch (error) {
      logger.error("Failed to get final decision", { error, sessionId });
      throw error;
    }
  }
}
