// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  // Get the last message from the user
  const lastMessage = messages[messages.length - 1];
  const userMessage = lastMessage?.content || "";

  try {
    // Send to Flask backend
    const response = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Response from Flask backend:", data);

    // Create proper streaming response for useChat hook
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      start(controller) {
        // Send the complete response as a single chunk
        const textChunk = `0:${JSON.stringify(data.response)}\n`;
        controller.enqueue(encoder.encode(textChunk));
        
        // Send the proper finish message
        const finishChunk = `d:${JSON.stringify({
          finishReason: "stop",
          usage: {
            promptTokens: 0,
            completionTokens: 0,
            totalTokens: 0
          }
        })}\n`;
        controller.enqueue(encoder.encode(finishChunk));
        controller.close();
      },
    });

    return new Response(stream, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "X-Vercel-AI-Data-Stream": "v1",
      },
    });
  } catch (error) {
    console.error("Error calling Flask backend:", error);

    // Return error in streaming format
    const encoder = new TextEncoder();
    const errorStream = new ReadableStream({
      start(controller) {
        const errorMessage = "Sorry, I encountered an error connecting to the debt tracking service. Please make sure the Flask server is running on port 8000.";
        const errorChunk = `0:${JSON.stringify(errorMessage)}\n`;
        controller.enqueue(encoder.encode(errorChunk));
        
        // Send proper finish message for error case
        const finishChunk = `d:${JSON.stringify({
          finishReason: "stop",
          usage: {
            promptTokens: 0,
            completionTokens: 0,
            totalTokens: 0
          }
        })}\n`;
        controller.enqueue(encoder.encode(finishChunk));
        controller.close();
      },
    });

    return new Response(errorStream, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "X-Vercel-AI-Data-Stream": "v1",
      },
      status: 500,
    });
  }
}
