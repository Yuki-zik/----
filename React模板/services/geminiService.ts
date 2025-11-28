import { GoogleGenAI, GenerateContentResponse } from "@google/genai";

const apiKey = process.env.API_KEY || '';
const ai = new GoogleGenAI({ apiKey });

const MODEL_NAME = 'gemini-3-pro-preview';

export const sendMessageToGemini = async (
  message: string,
  history: { role: string; parts: { text: string }[] }[] = []
): Promise<string> => {
  if (!apiKey) {
    return "API_KEY is missing. Please set it in the environment variables.";
  }

  try {
    const chat = ai.chats.create({
      model: MODEL_NAME,
      history: history,
      config: {
        systemInstruction: "You are SYNAPSE, a tactical AI assistant embedded in a high-tech wrist terminal. Your responses should be precise, data-driven, and brief, fitting the persona of a futuristic military interface. Avoid flowery language.",
        thinkingConfig: {
            thinkingBudget: 32768, 
        },
      },
    });

    const result: GenerateContentResponse = await chat.sendMessage({
      message: message,
    });

    return result.text || "No response received.";
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Connection lost. Tactical link unstable.";
  }
};